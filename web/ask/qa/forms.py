from django import forms
from .models import Question, Answer
from django.contrib.auth.models import User
#form for adding a question


class AskForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)

    def __init__(self, user, post_request):
        self._user = user
        super(AskForm, self).__init__(post_request)

    def save(self):
        self.cleaned_data['author'] = self._user
        question = Question(**self.cleaned_data)
        question.save()
        return question


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField(widget=forms.HiddenInput)

    def clean_answer(self):
        question_pk = self.cleaned_data['question']
        try:
            _ = Question.objects.get(pk=question_pk)
        except Question.DoesNotExist:
            raise forms.ValidationError("Could not get the question")
        return question_pk

    def save(self):
        self.cleaned_data['author'] = self._user
        return Answer.objects.create(text=self.cleaned_data['text'],
                                     author=self._user,
                                     question=Question.objects.get(pk=self.cleaned_data['question']))

