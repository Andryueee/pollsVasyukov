from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .models import UserProfile, Poll, Choice
from .forms import UserProfileForm, PollForm, RegistrationForm
from django.utils import timezone

def index(request):
    polls = Poll.objects.filter(is_active=True, end_date__gt=timezone.now())
    return render(request, 'polls/index.html', {'polls': polls})

def poll_detail(request, poll_id):
    def poll_detail(request, poll_id):
        poll = get_object_or_404(Poll, pk=poll_id, is_active=True, end_date__gt=timezone.now())
        choices = poll.choice_set.all()
        total_votes = sum(choice.votes for choice in choices)
        percentage_votes = [
            (choice.choice_text, (choice.votes / total_votes) * 100) if total_votes != 0 else (choice.choice_text, 0)
            for choice in choices]
        return render(request, 'polls/poll_detail.html', {'poll': poll, 'choices': choices, 'total_votes': total_votes,
                                                          'percentage_votes': percentage_votes})

@login_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('polls:edit_profile')
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'polls/edit_profile.html', {'form': form})

@login_required
def delete_profile(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('polls:index')
    return render(request, 'polls/delete_profile.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('polls:index')
    else:
        form = RegistrationForm()
    return render(request, 'polls/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('polls:index')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'polls/login.html')

def logout_view(request):
    logout(request)
    return redirect('polls:index')


@login_required
def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id, is_active=True, end_date__gt=timezone.now())
    if request.method == 'POST':
        selected_choice = get_object_or_404(Choice, pk=request.POST['choice'])
        selected_choice.votes += 1
        selected_choice.save()
        return redirect('polls:poll_detail', poll_id=poll.id)
    else:
        return redirect('polls:index')
