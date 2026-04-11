from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CoCreationItemViewSet, recent_news, my_progress

router = DefaultRouter()
router.register(r'items', CoCreationItemViewSet, basename='cocreation-item')

urlpatterns = [
    path('recent-news/', recent_news),
    path('my-progress/', my_progress),
    path('', include(router.urls)),
]
