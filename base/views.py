from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm  # Create User Form
from django.contrib import messages
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Room, Topic, Message
from .forms import RoomForm


def loginPage(request):
    page = 'login'
    # If user has logged in then redirect to homef
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        # Get the username and password from form
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        # Check if the username exists
        try:
            username = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        # If exist check the username and the password and mathes with database
        # Make sure credentials are correct and get the username and password object
        user = authenticate(request, username=username, password=password)

        # Create a session in the database and the browser
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password Does not exist")

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    # Delete session's token
    logout(request)
    return redirect('home')


def registerPage(request):
    form = UserCreationForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            # commit = false is freezing the object to save (intend to customize the user's object)
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An Error Occured during registration')
    context = {'form': form}
    return render(request, 'base/login_register.html', context)


@receiver(pre_delete, sender=User)
def on_user_delete(sender, instance, **kwargs):
    rooms = Room.objects.filter(host=instance)
    for room in rooms:
        room.host = None
        room.save()


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # if q == null ?
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    # count how many are rooms in database
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    # messages = room.message_set.all() is getting all the children from the room
    room_messages = room.message_set.all()
    participants = room.participants.all()
    # Here, Message.objects.create() creates a new message object in the database and saves it. Then, the function redirects the user back to the same room page by using the redirect() function with the pk parameter set to the current room's id.
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        # adding new user to participant when requested
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        # passing all the data as an argument into the RoomForm
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    # print(room)
    # instance is initializing field's value to the form
    form = RoomForm(instance=room)

    # if user is not who created the room then user is not allowed
    if request.user != room.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    # if user is not who created the room then user is not allowed
    if request.user != room.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    # if user is not who created the room then user is not allowed
    if request.user != message.user:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        message.delete()
        return redirect('homwe')
    return render(request, 'base/delete.html', {'obj': message})
