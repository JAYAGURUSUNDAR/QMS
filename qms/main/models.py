from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    class Meta:
        db_table="categories"
        verbose_name_plural="Categories"
        ordering=["-created_at"]
    name = models.CharField(max_length=50, null=False, help_text="Enter the category's name")
    slug = models.SlugField(max_length=50, null=False, help_text="Enter the slug name for easy identification.")
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

class Quiz(models.Model):
    class Meta:
        db_table="quizzes"
        verbose_name_plural="Quizzes"
        ordering=['-created_at']
    title = models.CharField(max_length=512, null=False, help_text="Enter the title of the Quiz, be short, about 500 letter.")
    description = models.TextField(null=False, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_by=models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    meta_tag = models.CharField(max_length=50, null=False)

    def __str__(self) -> str:
        return self.title + "|" + self.category.name

class Question(models.Model):
    class Meta:
        db_table="questions"
        ordering=['-created_at']

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.TextField(null=False, blank=False, help_text="Enter the text of the question")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    score = models.PositiveSmallIntegerField(null=False, default=1)

    @staticmethod
    def total_score():
        # Returns the sum of all scores in this table
        qs = Question.objects.all()
        return sum([q.score for q in qs])

    def __str__(self) -> str:
        return self.question_text
    

class Choice(models.Model):
    class Meta:
        db_table="choices"
        verbose_name_plural="Choices"
    
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=512, null=False, help_text="Enter the text for choice, be short, about 500 words")
    is_correct = models.BooleanField(default=False, help_text="Choose if the choice is correct.")

    @staticmethod
    def get_correct_choice(question:int):
        try:choice =  Choice.objects.get(question=question, is_correct=True)
        except Exception as e:print(e)
        finally: return choice.choice_text
        
    def __str__(self) -> str:
        return self.choice_text

class QuizAttempt(models.Model):
    class Meta:
        db_table="quiz_attempts"
        ordering = ['attempted_at']

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    attempted_at = models.DateTimeField(auto_now_add=True)









