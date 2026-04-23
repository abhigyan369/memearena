from django.urls import path
from . import views

urlpatterns = [
    path('<int:meme_id>/<int:value>/', views.vote, name='vote'),
]
