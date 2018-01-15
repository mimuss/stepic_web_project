from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator, EmptyPage
from django.urls import reverse
# Create your views here.

from .models import Question, Answer

def test(request):
    return HttpResponse('OK')

def question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    return render(request, 'qa/question.html', {
        'question' : question
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
