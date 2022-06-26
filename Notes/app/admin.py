
from django.contrib import admin

# Register your models here.
from app.models import CustomUser, Note

admin.site.register(Note)
admin.site.register(CustomUser)
