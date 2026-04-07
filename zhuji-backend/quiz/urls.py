from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuizQuestionViewSet, QuizOptionViewSet, submit_answer

router = DefaultRouter()
router.register(r'questions', QuizQuestionViewSet, basename='quiz-question')
router.register(r'options', QuizOptionViewSet, basename='quiz-option')

urlpatterns = [
    path('submit-answer/', submit_answer),
    path('', include(router.urls)),
]
