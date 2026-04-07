from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MonumentViewSet, SubmissionViewSet, featured_monument,
    discovery_monuments, MonumentArticleViewSet, MonumentArticlePageViewSet,
)

router = DefaultRouter()
router.register(r'monuments', MonumentViewSet, basename='monument')
router.register(r'submissions', SubmissionViewSet, basename='submission')
router.register(r'articles', MonumentArticleViewSet, basename='monument-article')
router.register(r'article-pages', MonumentArticlePageViewSet, basename='monument-article-page')

urlpatterns = [
    path('featured/', featured_monument),
    path('discovery/', discovery_monuments),
    path('', include(router.urls)),
]
