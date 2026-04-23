from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MemeViewSet, CommentViewSet, VoteViewSet

router = DefaultRouter()
router.register(r'memes', MemeViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'votes', VoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
