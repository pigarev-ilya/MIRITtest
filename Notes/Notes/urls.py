from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

import app.views
from app.views import HomePageView, NotePageView, SignUpView, LoginView, NoteCreateView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^note/(?P<note_id>\d+)/$', NotePageView.as_view()),
    url(r'^sign-up/', SignUpView.as_view(), name='sign-up'),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', app.views.logout_request, name='logout'),
    url(r'^create-note/', NoteCreateView.as_view(), name='create-note'),
    url('', HomePageView.as_view(), name='home')

)
