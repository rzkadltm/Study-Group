from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# A topic can have multiple room whereas Room can only have 1 topic
class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    # null = True : set description can be blank in database
    # blank=True = set description can be blank when user submitted the form
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank = True)
    # auto_now=True : automatically set the value of the updated field to the current time every time the object is saved
    updated = models.DateTimeField(auto_now=True)
    # auto_now_add=True : automatically initial timestamp for the first time and will never change
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # ordering = ['updated,' 'created'] the newest one will be last
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # on_delete=models.CASCADE : if the room is deleted, all the messages will be deleted as well
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # ordering = ['updated,' 'created'] the newest one will be last
        ordering = ['-updated', '-created']

    def __str__(self):
        # self.body[0:50] : just showing first 50 message
        return self.body[0:50]
