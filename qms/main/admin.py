from django.contrib import admin
from .models import *

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(QuizAttempt)
admin.site.register(Category)
admin.site.register(Choice)

