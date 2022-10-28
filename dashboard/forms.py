from django import forms
# from django.contrib.auth import get_user_model
# from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import Profile

class UpdateProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = ['id', 'user',]