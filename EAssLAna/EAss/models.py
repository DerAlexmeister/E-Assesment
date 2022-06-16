from django.db import models


class QAWSet(models.Model):

    title = models.CharField(max_length=16384, blank=False, null=False)
    Categorie = models.CharField(max_length=1024, blank=False, null=True, default=None)

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

    MaxValue = models.IntegerField(blank=False, null=False)
    Set = models.ForeignKey(QAWSet, blank=False, null=False, on_delete=models.CASCADE)
    
    def __str__(self):
        return "Random expression: {}".format(self.MaxValue)


class Gap(models.Model):
    preceeding_text = models.TextField(blank=False)
    succeeding_text = models.TextField(blank=False)


class GapSolution(models.Model):
    solution = models.TextField(blank=False, null=False)
    gap = models.ForeignKey(Gap, on_delete=models.CASCADE)


class Cloze(models.Model):
    qaw = models.ForeignKey(QAWSet, on_delete=models.CASCADE)
    gap = models.ForeignKey(Gap, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()
    

