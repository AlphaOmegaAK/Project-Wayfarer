from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import UserProfile, City, Post
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    class Meta:
        model = UserProfile
        fields = ("email", "username", "password")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = UserProfile.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            User.save()
        return User


class ProfileForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password Confirmation", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords Don't Match!")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)

        user.set_password(user.password)
        if commit:
            UserProfile.save(User)
            user.save(User)
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserProfile
        fields = ('email', 'first_name', 'last_name', 'location',
                  'picture')

    def clean_password(self):
        return self.initial["password"]


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['city']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['user', 'title', 'body', 'city']

