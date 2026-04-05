from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import my_progress

router = DefaultRouter()

urlpatterns = [
    path('my-progress/', my_progress),
    path('', include(router.urls)),
]
