from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET
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
    page = request.GET.get('page')
    return render(request, 'qa/new_questions.html', {
        'questions': Question.objects.new()
    })

@require_GET
def popular_questions(request):
    page = request.GET.get('page')
    return render(request, 'qa/popular_questions.html',{
        'questions': Question.objects.popular()
    })
