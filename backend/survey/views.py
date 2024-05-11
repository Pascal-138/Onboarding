from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .models import Choice, UserSurvey, Survey
from .forms import AnswerChoiceForm


def index(request):
    surveys = Survey.objects.all()
    is_authenticated = request.user.is_authenticated
    context = {
            'surveys': surveys,
            'is_authenticated': is_authenticated,
        }
    return render(request, 'index.html', context)


@login_required
def survey_list(request):
    surveys = Survey.objects.all()
    message = None
    if not surveys.exists():
        message = "Опросы не найдены"

    return render(request, 'survey_list.html', {'surveys': surveys,
                                                'message': message})


@login_required
def survey_detail(request, survey_id, question_id=None):
    survey = get_object_or_404(Survey, id=survey_id)
    user_survey, created = UserSurvey.objects.get_or_create(
        user=request.user, survey=survey
    )

    if user_survey.last_question:
        current_question = user_survey.last_question
    else:
        current_question = survey.questions.first()

    form = AnswerChoiceForm(data=request.POST or None,
                            question=current_question)

    if request.method == 'POST' and form.is_valid():
        selected_choice_id = form.cleaned_data.get('selected_choice')
        selected_choice = None

        if selected_choice_id:
            selected_choice = Choice.objects.get(id=selected_choice_id)

        if selected_choice:
            next_question = selected_choice.next_question

        else:
            next_question = None

        if next_question:
            user_survey.last_question = next_question
            user_survey.save()
            return redirect('survey:survey_detail_with_question',
                            survey_id=survey.id, question_id=next_question.id)
        else:
            user_survey.last_answer = selected_choice.id
            user_survey.completed = True
            user_survey.save()
            return redirect('survey:survey_list')

    return render(request, 'survey_detail.html',
                  {'survey': survey, 'form': form,
                   "current_question": current_question})
