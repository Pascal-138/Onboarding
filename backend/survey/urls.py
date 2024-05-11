from django.urls import path
from survey import views

app_name = 'survey'

urlpatterns = [
    path('', views.index, name='index'),
    path('surveys/', views.survey_list, name='survey_list'),
    path('surveys/<int:survey_id>/', views.survey_detail,
         name='survey_detail'),
    path('surveys/<int:survey_id>/<int:question_id>/', views.survey_detail,
         name='survey_detail_with_question'),
]
