from rest_framework import serializers
from .models import Category, Quiz, Question, Choice, QuizAttempt
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'created_at', 'updated_at']

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'question', 'choice_text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    choice_set = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'quiz', 'question_text', 'created_at', 'updated_at', 'score', 'choice_set']

class QuizSerializer(serializers.ModelSerializer):
    question_set = QuestionSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'category', 'created_by', 'created_at', 'updated_at', 'meta_tag', 'question_set']

class QuizAttemptSerializer(serializers.ModelSerializer):
    quiz = QuizSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = QuizAttempt
        fields = ['id', 'quiz', 'user', 'score', 'attempted_at']

