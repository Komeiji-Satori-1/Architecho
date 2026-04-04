from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DashboardStatsView,
    SensitiveWordViewSet,
    AIConfigViewSet,
    NodeStatusViewSet,
)

router = DefaultRouter()
router.register(r'sensitive-words', SensitiveWordViewSet, basename='sensitive-word')
router.register(r'ai-config', AIConfigViewSet, basename='ai-config')
router.register(r'node-status', NodeStatusViewSet, basename='node-status')

urlpatterns = [
    path('dashboard/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('', include(router.urls)),
]
