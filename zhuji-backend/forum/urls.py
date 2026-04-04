from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# ViewSet 将在后续 views.py 中补充
urlpatterns = [
    path('', include(router.urls)),
]
