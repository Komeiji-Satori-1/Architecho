from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import my_progress, my_stamp_for_monument, StampViewSet, StampColorLayerViewSet

router = DefaultRouter()
router.register(r'stamps', StampViewSet, basename='stamp')
router.register(r'layers', StampColorLayerViewSet, basename='stamp-layer')

urlpatterns = [
    path('my-progress/', my_progress),
    path('my-progress/monument/<int:monument_id>/', my_stamp_for_monument),
    path('', include(router.urls)),
]
