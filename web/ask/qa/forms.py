from django import forms
from .models import Question, Answer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
#form for adding a question


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=20)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean__email(self):
        try:
            User.objects.get(email=self.cleaned_data['email'])
            raise forms.ValidationError('User with this email already exists')
        except User.DoesNotExist:
            return self.cleaned_data['email']

    def clean_username(self):
        try:
            User.objects.get(username=self.cleaned_data['username'])
            raise forms.ValidationError('User with this username already exists')
        except User.DoesNotExist:
            return self.cleaned_data['username']

    def save(self):
        return User.objects.create_user(username=self.cleaned_data['username'],
                                        email=self.cleaned_data['email'],
                                        password=self.cleaned_data['password'])


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        self._user = authenticate(self.request, username=self.cleaned_data['username'], password=self.cleaned_data['password'])
        if self._user is None:
            raise forms.ValidationError("Username or password are not correct/does not exist")

    def get_user(self):
        return self._user


class AskForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)

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

