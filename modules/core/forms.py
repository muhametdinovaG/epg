# coding: utf8
from django import forms
from modules.core.widgets import MultiImageInput
from .models import *


class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = "__all__"
        widgets = {
            'icon': MultiImageInput(),
        }


class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = "__all__"


class DvbGenreForm(forms.ModelForm):
    class Meta:
        model = DvbGenre
        fields = "__all__"


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = "__all__"


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = "__all__"
