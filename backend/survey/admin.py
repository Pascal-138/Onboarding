from django.contrib import admin
from .models import Choice, Question, Survey, UserSurvey


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title', 'description')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('survey', 'text')
    list_filter = ('survey',)


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'text')
    list_filter = ('question',)


@admin.register(UserSurvey)
class UserSurveyAdmin(admin.ModelAdmin):
    list_display = ('user', 'survey', 'last_question', 'completed')
    list_filter = ('survey', 'completed')
