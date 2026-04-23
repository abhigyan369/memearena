from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:meme_id>/', views.add_comment, name='add_comment'),
    path('add/<int:meme_id>/<int:parent_id>/', views.add_comment, name='add_reply'),
]
