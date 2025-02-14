from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = _('Categories')


class Quiz(models.Model):
    title = models.CharField(max_length=255, default=_('New Quiz'))
    category = models.ForeignKey(Category, default=1, on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name_plural = _('Quizzes')


class Question(models.Model):
    SCALE = (
        (0, _('Fundamental')),
        (1, _('Beginner')),
        (2, _('Intermediate')),
        (3, _('Advanced')),
        (4, _('Expert')),
    )
    
    TYPE = (
        (0, _('Multiple Choice')),
    )
    
    quiz = models.ForeignKey(Quiz, related_name='question', on_delete=models.CASCADE)
    technique = models.IntegerField(choices=TYPE, default=0, verbose_name=_('Type of Question'))
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    difficulty = models.IntegerField(choices=SCALE, default=0, verbose_name=_('Difficulty'))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Date Created'))
    is_active = models.BooleanField(default=False, verbose_name=_('Active Status'))
    
    def __str__(self) -> str:
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answer', on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=255, verbose_name=_('Answer Text'))
    is_right = models.BooleanField(default=False)
    