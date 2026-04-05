from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ForumCategoryViewSet, ForumPostViewSet, CommentViewSet, hot_topics

router = DefaultRouter()
router.register(r'categories', ForumCategoryViewSet, basename='forum-category')
router.register(r'posts', ForumPostViewSet, basename='forum-post')
router.register(r'comments', CommentViewSet, basename='forum-comment')

urlpatterns = [
    path('hot-topics/', hot_topics),
    path('', include(router.urls)),
]
