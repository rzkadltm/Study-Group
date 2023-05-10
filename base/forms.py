from django.forms import ModelForm
from .models import Room

# ModelForm is a package for creating form from model


class RoomForm(ModelForm):
    class Meta:
        model = Room
        # # '__all__ is gonna import all the field in Room's Model'
        fields = '__all__'
