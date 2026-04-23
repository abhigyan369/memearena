from django.urls import path
from . import views

urlpatterns = [
    path('', views.LatestMemeListView.as_view(), name='latest_memes'),
    path('trending/', views.TrendingMemeListView.as_view(), name='trending_memes'),
    path('upload/', views.MemeCreateView.as_view(), name='meme_upload'),
    path('meme/<slug:slug>/', views.MemeDetailView.as_view(), name='meme_detail'),
    path('top/day/', views.TopTodayListView.as_view(), name='top_today'),
    path('top/week/', views.TopWeekListView.as_view(), name='top_week'),
    path('top/all/', views.AllTimeTopListView.as_view(), name='top_all'),
    path('tag/<slug:slug>/', views.TagMemeListView.as_view(), name='tag_memes'),
    path('random/', views.RandomMemeView.as_view(), name='random_meme'),
]
