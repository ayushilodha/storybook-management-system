from django.forms import ModelForm,Textarea
from django import forms
from .models import *

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

