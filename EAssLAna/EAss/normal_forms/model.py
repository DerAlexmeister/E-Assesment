from django.db import models
from .normal_form import CONJUNCTION, DISJUNCTION


class NormalFormQuestion(models.Model):
    normal_form = models.CharField(max_length=50, choices=[(k, k) for k in [CONJUNCTION, DISJUNCTION]])


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
    question = models.ForeignKey(NormalFormQuestion, on_delete=models.CASCADE)
    answer = models.ForeignKey(NormalFormAnswer, on_delete=models.CASCADE)


class NormalFormCorrection(models.Model):
    guess = models.ForeignKey(NormalFormGuess, on_delete=models.CASCADE)
    points = models.IntegerField()
