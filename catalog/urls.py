from django.views.decorators.csrf import csrf_exempt

from . import views
from django.urls import path
app_name = 'catalog'
urlpatterns = [
    path('', csrf_exempt(views.ProjectListView.as_view()), name='project'),
]