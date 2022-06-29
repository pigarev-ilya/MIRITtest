from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.extras.widgets import SelectDateWidget

from app.models import CustomUser, Note


# Create your forms here.


class CreateCustomUserForm(UserCreationForm):
    this_year = date.today().year - 4
    year_range = [x for x in range(this_year - 100, this_year + 1)]
    date_of_birth = forms.DateField(widget=SelectDateWidget(years=year_range), required=False)
    status = forms.CharField(max_length=140, required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = CustomUser
        fields = ("username", 'date_of_birth', 'bio', 'status', "password1", "password2")


class CreateNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ("title", 'text')


class CustomAuthenticationForm(forms.Form):
    username = forms.CharField(label="Username", max_length=15)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
