from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .models import UserProfile, Poll, Choice, Question
from .forms import UserProfileForm, PollForm, RegistrationForm
from django.utils import timezone
from django.views import generic
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'



class PollsView(generic.ListView):
    template_name = 'polls/polls.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')

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
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    # Проверяем, голосовал ли пользователь ранее в данном опросе
    user_has_voted = question.choice_set.filter(voters=request.user.userprofile).exists()

    if user_has_voted:
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'Вы уже голосовали в этом опросе.'
        })

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'Вы не сделали выбор'
        })
    else:
        selected_choice.voters.add(request.user.userprofile)
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


@login_required
def create_poll(request):
    if request.method == 'POST':
        form = PollForm(request.POST)
        if form.is_valid():
            poll = form.save(commit=False)
            poll.created_by = request.user
            poll.save()
            return redirect('polls:index')  # Изменение на 'polls:index'
    else:
        form = PollForm()
    return render(request, 'polls/create_poll.html', {'form': form})

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'