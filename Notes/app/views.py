# coding=utf-8
# Create your views here.
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView, FormView

from app.forms import CreateCustomUserForm, CustomAuthenticationForm, CreateNoteForm
from app.models import CustomUser, Note


class SignUpView(CreateView):
    template_name = 'signup.html'
    form_class = CreateCustomUserForm
    success_url = reverse_lazy('login')


class LoginView(FormView):
    template_name = "login.html"
    form_class = CustomAuthenticationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(self.request, user)
            messages.info(self.request, 'Успешный вход')
        else:
            messages.info(self.request, 'Ошибка логина или пароля')
        return super(LoginView, self).form_valid(form)


def logout_request(request):
    logout(request)
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


class NoteCreateView(CreateView):
    template_name = 'create_note.html'
    form_class = CreateNoteForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(NoteCreateView, self).form_valid(form)
