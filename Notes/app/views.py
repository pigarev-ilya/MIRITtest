# Create your views here.
from django.views.generic import TemplateView

from app.models import CustomUser, Note


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
