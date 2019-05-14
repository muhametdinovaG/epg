# coding: utf8
from django import forms
from .models import *


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"


class FilialForm(forms.ModelForm):
    class Meta:
        model = Filial
        fields = "__all__"


class ProcessQueueForm(forms.ModelForm):
    class Meta:
        model = ProcessQueue
        fields = "__all__"


class KeywordsForm(forms.ModelForm):
    class Meta:
        model = Keywords
        fields = "__all__"
