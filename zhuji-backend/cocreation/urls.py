from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CoCreationItemViewSet, recent_news

router = DefaultRouter()
router.register(r'items', CoCreationItemViewSet, basename='cocreation-item')

urlpatterns = [
    path('recent-news/', recent_news),
    path('', include(router.urls)),
]
