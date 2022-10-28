from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import User

User = get_user_model()

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class':'form-control','type':'password', 'name':'password1',
        'placeholder':'Password'}
    ))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(
        attrs={'class':'form-control','type':'password', 'name':'password2', 'placeholder':'Password again'}
    ))

    class Meta:
        model = User
        fields = ['email']
        # field_order = ['username', 'email','password1','password2']

    # style a field define in a model
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['username'].widget.attrs.update(
        #         {'class':'form-control','placeholder':"Username"})
        self.fields['email'].widget.attrs.update(
                {'class':'form-control',
                'placeholder':"Email"})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            user = User.objects.get(email = email)
            if user:
                raise ValidationError(_("Something went wrong. Try again"), code='invalid')
        except User.DoesNotExist:
            return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match. Please try again!")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
        """The save(commit=False) tells Django to save the new record, but dont commit it to the
        database yet"""


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = User
        fields = ('email', 'password','is_active', 'is_admin')


class AuthenticationForm(forms.Form): # Note: forms.Form NOT forms.ModelForm
    """A form for authenticate users, base on email field an password."""

    email = forms.EmailField(widget=forms.TextInput(
    attrs={'class': 'form-control','type':'email','name': 'email','placeholder':'Email',}),
    label='Email')
    password = forms.CharField(widget=forms.PasswordInput(
    attrs={'class':'form-control','type':'password', 'name':
    'password','placeholder':'Password'}),
    label='Password')
    class Meta:
        fields = ['email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        try:
            user = User.objects.get(email = cleaned_data.get('email'))
        except:
            raise ValidationError(
                _("Email or Password are wrong. Try again! "),
                code='invalid',
                )
            # msg = "Email or Password are wrong. Try again!"
            # self.add_error('email', msg)