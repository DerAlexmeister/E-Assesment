from django.db import models
from django.utils import timezone

TOPICS = (
    ('None','None'),
    ('Computer-Models', 'Computer-Models'),
    ('Gates','Gates'),
    ('Calculus','Calculus'),
    ('Optimization','Optimization'),
    ('Assembler','Assembler'),
    ('Quantencomputing','Quantencomputing'),
)

DIFF = (
    ('None','None'),
    ('Easy', 'Easy'),
    ('Medium','Medium'),
    ('Hard','Hard'),
    ('Insane','Insane'),
)

ITEMTYPES = (
    ('None','None'),
    ('MultipleChoice', 'MultipleChoice'),
    ('SingleChoice','SingleChoice'),
    ('ClozeText','ClozeText'),
    ('TruthTable','TruthTable'),
    ('Calculus','Calculus'),
    ('Assembler','Assembler'),
)

CALCTYPES = (
    ('None','None'),
    ('Bin', 'Bin'),
    ('Octa', 'Octa'),
)

class QAWSet(models.Model):

    title = models.CharField(max_length=16384, blank=False, null=False)
    NameID = models.CharField(max_length=1024, blank=False, null=True, default=None, unique=True)
    Topic = models.CharField(max_length=24, choices=TOPICS, default='None', null=False, blank=False)
    Target = models.CharField(max_length=1024, default='', null=False, blank=False)
    Difficulty = models.CharField(max_length=24, choices=DIFF, default='None', null=False, blank=False)
    ItemType = models.CharField(max_length=24, choices=ITEMTYPES, default='None', null=False, blank=False)

    def __str__(self):
        return "{} - {} - {}".format(self.title, self.NameID, self.Difficulty)

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

class OctaStatement(models.Model):

    MaxValue = models.IntegerField(blank=False, null=False)
    Set = models.ForeignKey(QAWSet, blank=False, null=False, on_delete=models.CASCADE)
    
    def __str__(self):
        return "Random expression: {}".format(self.MaxValue)

class Gap(models.Model):
    preceeding_text = models.TextField(blank=False)
    succeeding_text = models.TextField(blank=False)
    Set = models.ForeignKey(QAWSet, blank=False, null=True, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return "{} [...] {}".format(self.preceeding_text, self.succeeding_text)

class GapSolution(models.Model):
    solution = models.TextField(blank=False, null=False)
    gap = models.ForeignKey(Gap, on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.solution)

class Cloze(models.Model):
    qaw = models.ForeignKey(QAWSet, on_delete=models.CASCADE)
    gap = models.ForeignKey(Gap, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()

    def __str__(self):
        return "{} -> (P:{})".format(self.gap, self.position)

class OpenAssemblerCodeQuestions(models.Model):
    
    Question = models.TextField(blank=False, null=False)
    RegisterAnswer = models.TextField(blank=False, null=False)
    Created = models.DateTimeField(default=timezone.now)
    NeededInstructions = models.CharField(max_length=2048, blank=True)
    CheckNeededInstructions = models.BooleanField(default=False)
    OptimizedSolution = models.TextField(blank=True, null=True)
    CheckOptimizedSolution = models.BooleanField(default=False)
    Set = models.ForeignKey(QAWSet, blank=False, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.Question)

#class AssemblerCloze(models.Model):
#    pass

class CalculusSingleUserAnswer(models.Model):

    Answer = models.IntegerField(blank=False, null=False)
    Question = models.IntegerField(blank=False, null=True)
    Correct = models.BooleanField(blank=False, null=False)
    Solved = models.DateTimeField(default=timezone.now)
    CalcType = models.CharField(max_length=24, choices=CALCTYPES, default='None', null=False, blank=False)

    def __str__(self):
        return "{} - Status: {}".format(self.Solved, self.Correct)

class SingleChoiceUserAnswer(models.Model):
    Answer = models.CharField(max_length=1024, blank=False, null=False)
    Question = models.CharField(max_length=1024, blank=False, null=False)
    Correct = models.BooleanField(blank=False, null=False)
    Solved = models.DateTimeField(default=timezone.now)
    Topic = models.CharField(max_length=24, choices=TOPICS, default='None', null=False, blank=False)

    def __str__(self):
        return "{} - Status: {}".format(self.Solved, self.Correct)

class MultipleChoiceUserAnswer(models.Model):
    Question = models.CharField(max_length=1024, blank=False, null=False)
    AllCorrect = models.BooleanField(blank=False, null=False)
    Solved = models.DateTimeField(default=timezone.now)
    Topic = models.CharField(max_length=24, choices=TOPICS, default='None', null=False, blank=False)

    def __str__(self):
        return "{} - Status: {}".format(self.Solved, self.AllCorrect)

class SingleMultipleChoiceUserAnswer(models.Model):
    Answer = models.CharField(max_length=1024, blank=False, null=False)
    Correct = models.BooleanField(blank=False, null=False)
    AllAnswers = models.ForeignKey(MultipleChoiceUserAnswer, blank=False, null=True, default=None, on_delete=models.CASCADE)
    Solved = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} - Status: {}".format(self.Solved, self.Correct)

class TruthTableUserAnswer(models.Model):
    AllCorrect = models.BooleanField(blank=False, null=False)
    Solved = models.DateTimeField(default=timezone.now)
    Topic = models.CharField(max_length=24, choices=TOPICS, default='None', null=False, blank=False)

    def __str__(self):
        return "{} - Status: {}".format(self.Solved, self.AllCorrect)

class SingleTruthTableUserAnswer(models.Model):
    Question = models.CharField(max_length=1024, blank=False, null=False)
    Answer = models.CharField(max_length=1024, blank=False, null=False)
    Correct = models.BooleanField(blank=False, null=False)
    AllAnswers = models.ForeignKey(TruthTableUserAnswer, blank=False, null=True, default=None, on_delete=models.CASCADE)
    Solved = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} - Status: {}".format(self.Solved, self.Correct)

class ClozeUserAnswer(models.Model):
    AllCorrect = models.BooleanField(blank=False, null=False)
    Solved = models.DateTimeField(default=timezone.now)
    Topic = models.CharField(max_length=24, choices=TOPICS, default='None', null=False, blank=False)

    def __str__(self):
        return "{} - Status: {}".format(self.Solved, self.AllCorrect)

class SingleFieldClozeUserAnswer(models.Model):
    ExpectedAnswer = models.CharField(max_length=1024, blank=False, null=False)
    UserAnswer = models.CharField(max_length=1024, blank=False, null=False)
    Correct = models.BooleanField(blank=False, null=False)
    AllGaps = models.ForeignKey(ClozeUserAnswer, blank=False, null=True, default=None, on_delete=models.CASCADE)
    Solved = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} - Status: {}".format(self.Solved, self.Correct)
        
class OpenAssemblerAnswer(models.Model):

    Question = models.TextField(blank=False, null=False)
    Answer = models.TextField(blank=False, null=False)
    Solved = models.DateTimeField(default=timezone.now)
    Correct = models.BooleanField(blank=False, null=False)
    MissedStatements = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{} - Status: {}".format(self.Solved, self.Correct)

class GatesAnswer(models.Model):

    Question = models.TextField(blank=False, null=False)
    Answer = models.TextField(blank=False, null=False)
    Solved = models.DateTimeField(default=timezone.now)
    Correct = models.BooleanField(blank=False, null=False)

    def __str__(self):
        return "{} - Status: {}".format(self.Solved, self.Correct)