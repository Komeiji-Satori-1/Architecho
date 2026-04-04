from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MonumentViewSet, SubmissionViewSet

router = DefaultRouter()
router.register(r'monuments', MonumentViewSet, basename='monument')
router.register(r'submissions', SubmissionViewSet, basename='submission')

urlpatterns = [
    path('', include(router.urls)),
]
