from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile, Poll

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['question']

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class VoteForm(forms.Form):
    CHOICES = [(1, 'Option 1'), (2, 'Option 2')]  # Предположим, у вас есть два варианта ответов
    vote_option = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

