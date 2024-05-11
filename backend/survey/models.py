from django.db import models
from django.contrib.auth.models import User


class Survey(models.Model):
    """Модель опроса."""
    title = models.CharField(
        max_length=255,
        verbose_name="Название")
    description = models.TextField(
        blank=True,
        verbose_name="Описание")

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'
        ordering = ['title']

    def __str__(self):
        return self.title


class Choice(models.Model):
    """Модель для вариантов ответа на вопрос."""
    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE,
        related_name='choice_list',
        verbose_name='Вопрос'
    )
    text = models.CharField(
        max_length=255,
        verbose_name='Вариант ответа'
    )
    next_question = models.ForeignKey(
        'Question',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Следующий вопрос"
    )

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'

    def __str__(self):
        return self.text


class Question(models.Model):
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name="Опрос"
    )
    text = models.CharField(
        max_length=255,
        verbose_name="Текст вопроса"
    )

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return f"{self.survey.title}: {self.text}"


class UserSurvey(models.Model):
    """Модель для результата пройденного опроса."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_surveys',
        verbose_name="Пользователь"
    )
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        related_name='user_surveys',
        verbose_name="Опрос"
    )
    last_question = models.ForeignKey(
        Question,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Последний вопрос"
    )
    last_answer = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='id последнего ответа',
    )
    completed = models.BooleanField(
        default=False,
        verbose_name="Завершен")

    class Meta:
        verbose_name = 'Завершенный опрос'
        verbose_name_plural = 'Завершенные опросы'
        unique_together = ('user', 'survey')

    def __str__(self):
        return f"{self.user.username} - {self.survey.title}"
