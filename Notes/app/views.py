# coding=utf-8
# Create your views here.
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import TemplateView

from app.forms import CreateCustomUserForm, CustomAuthenticationForm, CreateNoteForm
from app.models import CustomUser, Note
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages


class SignUpView(TemplateView):
    template_name = "signup.html"

    def post(self, request, *args, **kwargs):
        form = CreateCustomUserForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Регистрация прошла успешно.")
            return redirect(reverse('sign-up'))
        else:
            messages.info(request, "Ошибка регистрации!")
            return redirect(reverse('sign-up'))

    def get_context_data(self, **kwargs):
        context = {'create_user_form': CreateCustomUserForm}
        return context


class LoginView(TemplateView):
    template_name = "login.html"

    def post(self, request, *args, **kwargs):
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, "Успешная авторизация")
                return redirect(reverse('login'))
            else:
                messages.info(request, "Неправильные данные.")
        else:
            messages.info(request, "Неправильные данные.")
        return redirect(reverse('login'))

    def get_context_data(self, **kwargs):
        context = {'login_form': CustomAuthenticationForm}
        return context


def logout_request(request):
    logout(request)
    messages.info(request, "Вы покинули аккаунт.")
    return redirect(reverse('login'))


class NotePageView(TemplateView):
    template_name = "note.html"

    def get_context_data(self, note_id, **kwargs):
        note = Note.objects.filter(id=note_id)[0]
        context = {'note': note}
        return context


class HomePageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        users = CustomUser.objects.all()
        context = {'users': users}
        return context


class CreateNoteView(TemplateView):
    template_name = "create_note.html"

    def post(self, request, *args, **kwargs):
        form = CreateNoteForm(data=request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            text = form.cleaned_data.get('text')
            Note.objects.create(title=title, text=text, author=request.user)
            messages.info(request, "Заявка добавлена.")
            return redirect(reverse('create-note'))
        else:
            messages.info(request, "Ошибка.")
        return redirect(reverse('create-note'))

    def get_context_data(self, **kwargs):
        context = {'create_note_form': CreateNoteForm}
        return context
