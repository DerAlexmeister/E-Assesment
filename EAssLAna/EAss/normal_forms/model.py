from django.db import models
from django.db.models.deletion import CASCADE

from ..models import QAWSet
from .normal_form import CONJUNCTION, DISJUNCTION, NORMAL_FORMS
from .assessment import ASSESSMENTS


class NormalFormQuestion(models.Model):
    normal_form = models.CharField(max_length=50, choices=[(k, k) for k in NORMAL_FORMS])


class FunctionValue(models.Model):
    question = models.ForeignKey(NormalFormQuestion, on_delete=models.CASCADE)
    one = models.SmallIntegerField()


class NormalFormAnswer(models.Model):
    pass


class NormalFormTerm(models.Model):
    answer = models.ForeignKey(NormalFormAnswer, on_delete=models.CASCADE)


class NormalFormLiteral(models.Model):
    term = models.ForeignKey(NormalFormTerm, on_delete=models.CASCADE)
    variable = models.CharField(max_length=20)
    sign = models.BooleanField()


class NormalFormGuess(models.Model):
    qaw = models.ForeignKey(QAWSet, on_delete=CASCADE)
    question = models.ForeignKey(NormalFormQuestion, on_delete=models.CASCADE)
    answer = models.ForeignKey(NormalFormAnswer, on_delete=models.CASCADE)


class NormalFormCorrection(models.Model):
    guess = models.ForeignKey(NormalFormGuess, on_delete=models.CASCADE)
    points = models.IntegerField()
    total_points = models.IntegerField()


class NormalFormDifficulty(models.Model):
    num_variables = models.IntegerField()
    num_terms = models.IntegerField()
    normal_form = models.CharField(max_length=20, choices=[(k, k) for k in NORMAL_FORMS])

    def __str__(self):
        return f"{self.normal_form}-{self.num_variables}-{self.num_terms}"


class NormalForm(models.Model):
    normal_form = models.ForeignKey(NormalFormDifficulty, on_delete=models.CASCADE)
    assessment = models.CharField(max_length=50, choices=[(k, k) for k in ASSESSMENTS.keys()])
    Set = models.ForeignKey(QAWSet, blank=False, null=True, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.normal_form}, {self.assessment}"
