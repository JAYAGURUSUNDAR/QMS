from typing import Any
from django.shortcuts import render, get_object_or_404
from django.views import View, generic
from django.http import HttpRequest, JsonResponse
from .models import Quiz, Question, Choice, QuizAttempt
from .forms import QuizForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from datetime import datetime
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import generics, views, status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from .serializers import QuizSerializer, QuestionSerializer

class SubmitQuiz(views.APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request:HttpRequest):
        data:dict = JSONParser().parse(request)
        questions:dict = data["questions"]
        quiz_atmpt =  QuizAttempt()
        if data:
            score = 0
            correct_answers=0
            try:
                for question, answer in questions.items():
                    if self.validate_answers(int(question), int(answer)):
                        correct_answers+=1
                        score+=Question.objects.get(id=int(question)).score
            except Exception as e:print(e)
            finally:
                quiz_atmpt.user = request.user
                quiz_atmpt.quiz = Quiz.objects.get(id=data['quiz'])
                quiz_atmpt.score = score
                quiz_atmpt.save()
                return views.Response(
                {
                    'message': 'Quiz submitted successfully', 
                    'correct_answers':correct_answers
                }, 
                status=status.HTTP_200_OK, 
                )
        else:
            return views.Response(status=status.HTTP_400_BAD_REQUEST)
    def validate_answers(self, question:int, answer:int):
        return True if Choice.objects.get(question=question, pk=answer).is_correct else False

class GetUserDetails(views.APIView):
    def get(self, request:HttpRequest, pk:int):
        try:
            data = {}
            data["username"] = User.objects.get(pk=pk).username
            data["email"] = User.objects.get(pk=pk).email
            data["quizzes_attended"] = Quiz.objects.filter(id__in=QuizAttempt.objects.filter(user=User.objects.get(pk=pk)).values("quiz_id")).count()
            data["highest_score"] = QuizAttempt.objects.filter(user=User.objects.get(pk=pk)).order_by("-score").first().score
            return views.Response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return views.Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:data=None

    
    
        

class QuizList(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    
class QuizDetail(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class QuestionDetail(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class HomePageView(View):
    def get(self, request:HttpRequest):
        return render(request, 'home.html', {})

class QuizCreateView(LoginRequiredMixin, generic.CreateView):
    model = Quiz
    form_class = QuizForm
    template_name = 'createQuiz.html'
    success_url = '/qms/quizzes'


class QuizzesView(generic.ListView):
    model = Quiz
    template_name = 'quizzes_list.html'
    context_object_name = 'quizzes'

class QuizDetailView(LoginRequiredMixin, generic.DetailView):
    model = Quiz
    template_name = 'quiz_detail.html'
    context_object_name = 'quiz'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        data =  super().get_context_data(**kwargs)
        data['questions'] = Question.objects.filter(quiz=data['quiz'].id)
        return data
    
    def post(self, request:HttpRequest, *args, **kwargs):
        correct_answers=0
        answer_key={}
        score = 0
        try:
            for question, answer in request.POST.items():
                qst = get_object_or_404(Question, pk=int(question))
                if self.validate_answers(int(question), int(answer)):
                    correct_answers+=1
                    score+=qst.score
                answer_key[str(qst.pk)] = self.validate_answers(int(question), int(answer))
            attempt = QuizAttempt()
            attempt.quiz = get_object_or_404(Quiz, pk=kwargs["pk"])
            attempt.user = request.user
            attempt.score = score
            attempt.save()
            html_message = render_to_string('emails/quiz_email_template.html', {
                'username': request.user.username,
                'quiz_title': attempt.quiz.title,
                'current_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'correct_answers': correct_answers
            })
            
            # Strip HTML tags for plain text email
            plain_message = strip_tags(html_message)
            
            # Send email
            send_mail(
                subject=f"Quiz {attempt.quiz.title} attended",
                message=plain_message,
                from_email=None,  # Use default email specified in settings.py
                recipient_list=[request.user.email],
                html_message=html_message,
            )
        except Exception as e:print(e)
        finally:
            plain_message = None
            attempt = None
            return JsonResponse({"action":"quiz_submitted", "correct answers":correct_answers, "answer_key":answer_key})
    
    def validate_answers(self, question:int, answer:int):
        return True if Choice.objects.get(question=question, pk=answer).is_correct else False

class DashboardView(View):
    def get(self, request: HttpRequest, quiz_id: int = None):
        if quiz_id is None:
            quizzes_attempts = QuizAttempt.objects.filter(user=request.user)
            recent_attempt = quizzes_attempts.order_by('-attempted_at').first().attempted_at
            total = sum([sum([question.score for question in Question.objects.filter(quiz=quiz_attempt.quiz)]) for quiz_attempt in quizzes_attempts.order_by('quiz')])
            scores = quizzes_attempts.order_by('-score')
            best = scores.first()
            total_score = sum([a.score for a in scores])
            average_score =f"{total_score / len(scores):.2f}"
            context = {
                "attempts": quizzes_attempts, 
                "recent_attempt": recent_attempt, 
                "best":best, 
                "average_score":average_score, 
                "total":total,
                "total_score":total_score,}
            return render(request, 'dashboard.html', context)
        else:
            best_attempt = QuizAttempt.objects.filter(user=request.user, quiz__pk=quiz_id)\
                                                .order_by('-score')\
                                                .first()
            context = {'best_attempt': best_attempt.score}
            return JsonResponse(context)




    



