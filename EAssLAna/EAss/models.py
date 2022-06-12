from dataclasses import dataclass

from typing import List, Set

from django.db import models


class QAWSet(models.Model):

    title = models.CharField(max_length=16384, blank=False, null=False)

    def __str__(self):
        return self.title

class Question(models.Model):
    
    Question = models.TextField(blank=False, null=False)
    Set = models.ForeignKey(QAWSet, blank=False, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.Question

class Answer(models.Model):
    
    Answer = models.TextField(blank=False, null=False)
    Set = models.ForeignKey(QAWSet, blank=False, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.Answer

class WrongStatements(models.Model):
    
    Statement = models.TextField(blank=False, null=False)
    Set = models.ForeignKey(QAWSet, blank=False, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.Statement

class BinaryStatement(models.Model):

    Length = models.IntegerField(blank=False, null=False)
    Set = models.ForeignKey(QAWSet, blank=False, null=False, on_delete=models.CASCADE)
    
    def __str__(self):
        return "Random expression: {}".format(self.Length)


class GapModel(models.Model):
    preceeding_text = models.TextField(blank=False)
    suceeding_text = models.TextField(blank=False)


class GapSolution(models.Model):
    solution = models.TextField(blank=False, null=False)
    gap = models.ForeignKey(GapModel, on_delete=models.CASCADE)


class ClozeModel(models.Model):
    position = models.PositiveIntegerField()
    gap = models.ForeignKey(GapSolution, on_delete=models.CASCADE)


@dataclass
class Gap:
    preceeding_text: str
    succeeding_text: str
    solutions: Set[str]


@dataclass
class Cloze:
    gaps: List[Gap]


def create_cloze_model(cloze: Cloze):
    for i, gap in enumerate(cloze.gaps):
        gap_model = GapModel(
            preceeding_text=gap.preceeding_text,
            succeeding_text=gap.succeeding_text,
        )
        gap_model.save()

        ClozeModel(position=i, gap=gap).save()

        for solution in gap.solutions:
            solution_model = GapSolution(
                solution=solution,
                gap=gap_model,
            )
            solution_model.save()
