from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator, EmptyPage
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
# Create your views here.

from .models import Question, Answer
from .forms import AskForm, AnswerForm, LoginForm, SignUpForm


def test(request):
    return HttpResponse('OK')


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            _ = form.save()
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect(reverse('qa:new_questions'))
    else:
        form = SignUpForm()
    return render(request, 'qa/sign_up.html', {
        'form': form
    })


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        form.request = request
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect(reverse('qa:new_questions'))
    else:
        form = LoginForm()
    return render(request, 'qa/login.html', {
        'form': form
    })


def question(request, pk):
    q = get_object_or_404(Question, pk=pk)
    user = request.user
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        form._user = user
        if form.is_valid():
            _ = form.save()
            return HttpResponseRedirect(q.get_url())
    else:
        form = AnswerForm(initial={'question': q.pk})
    return render(request, 'qa/question.html', {
        'question': q,
        'form': form
    })


def question_add(request):
    user = request.user
    form = AskForm(request.POST)
    form._user = user
    if request.method == 'POST':
        if form.is_valid():
            q = form.save()
            url = q.get_url()
            return HttpResponseRedirect(url)
    return render(request, 'qa/question_add.html', {
        'form': form
    })


@require_GET
def new_questions(request):
    questions = Question.objects.new()
    limit = 10
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise 404
    paginator = Paginator(questions, limit)
    paginator.base_url = reverse('qa:new_questions') + "?page="
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return render(request, 'qa/new_questions.html', {
        'questions': page.object_list,
        'paginator': paginator,
        'page': page
    })


@require_GET
def popular_questions(request):
    questions = Question.objects.popular()
    limit = 10
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise 404
    paginator = Paginator(questions, limit)
    paginator.base_url = reverse('qa:popular_questions') + "?page="
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return render(request, 'qa/popular_questions.html', {
        'questions': page.object_list,
        'paginator': paginator,
        'page': page
    })
