from django.urls import path
from .views import (
    HomePageView, QuizCreateView, 
    QuizzesView, QuizDetailView, 
    DashboardView, QuizList,
    QuizDetail, QuestionDetail,
    SubmitQuiz
    )
app_name="main"
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('create/', QuizCreateView.as_view(), name="create_quiz"),
    path('quizzes/', QuizzesView.as_view(), name="quizzes_list"),
    path('quizzes/<int:pk>',QuizDetailView.as_view(), name="quiz"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("dashboard/<int:quiz_id>", DashboardView.as_view(), name="best_attempt"),
    path("api/quizzes/", QuizList.as_view()),
    path("api/quizzes/<int:pk>", QuizDetail.as_view()),
    path("api/quizzes/questions/<int:pk>", QuestionDetail.as_view()),
    path("api/quizzes/submit", SubmitQuiz.as_view()),
]