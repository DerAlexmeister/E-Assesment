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
    ('Gates','Gates'),
    ('NormalForm','NormalForm'),
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
    Hint = models.TextField(blank=False, null=False, default='no hint')
    Set = models.ForeignKey(QAWSet, blank=False, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.Answer

class WrongStatements(models.Model):
    
    Statement = models.TextField(blank=False, null=False)
    Hint = models.TextField(blank=False, null=False, default='no hint')
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
    preceeding_text = models.TextField(blank=True)
    succeeding_text = models.TextField(blank=True)

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
        return "{}: {}".format(self.id, self.Question)

class CalculusSingleUserAnswer(models.Model):
    UserID = models.CharField(max_length=1024, default='None',blank=False, null=False)
    Duration = models.IntegerField(default=0,blank=False, null=False)
    Set = models.ForeignKey(QAWSet, blank=False, null=True, on_delete=models.CASCADE)
    Answer = models.IntegerField(blank=False, null=False)
    Question = models.IntegerField(blank=False, null=True)
    Correct = models.BooleanField(blank=False, null=False)
    Solved = models.DateTimeField(default=timezone.now)
    CalcType = models.CharField(max_length=24, choices=CALCTYPES, default='None', null=False, blank=False)

    def __str__(self):
        return "{} - Status: {}".format(self.Solved, self.Correct)

class SingleChoiceUserAnswer(models.Model):
    UserID = models.CharField(max_length=1024, default='None',blank=False, null=False)
    Duration = models.IntegerField(default=0,blank=False, null=False)
    Set = models.ForeignKey(QAWSet, blank=False, null=True, on_delete=models.CASCADE)
    Answer = models.CharField(max_length=1024, blank=False, null=False)
    Question = models.CharField(max_length=1024, blank=False, null=False)
    Correct = models.BooleanField(blank=False, null=False)
    Solved = models.DateTimeField(default=timezone.now)
    Topic = models.CharField(max_length=24, choices=TOPICS, default='None', null=False, blank=False)


    def __str__(self):
        return "{} - Status: {}".format(self.Solved, self.Correct)

class MultipleChoiceUserAnswer(models.Model):
    UserID = models.CharField(max_length=1024, default='None',blank=False, null=False)
    Duration = models.IntegerField(default=0,blank=False, null=False)
    Set = models.ForeignKey(QAWSet, blank=False, null=True, on_delete=models.CASCADE)
    Question = models.CharField(max_length=1024, blank=False, null=False)
    AllCorrect = models.BooleanField(blank=False, null=False)
    Solved = models.DateTimeField(default=timezone.now)
    Topic = models.CharField(max_length=24, choices=TOPICS, default='None', null=False, blank=False)

    def __str__(self):
        return "{} - Status: {}".format(self.Solved, self.AllCorrect)

class SingleMultipleChoiceUserAnswer(models.Model):
    UserID = models.CharField(max_length=1024, default='None',blank=False, null=False)
    Duration = models.IntegerField(default=0,blank=False, null=False)
    Set = models.ForeignKey(QAWSet, blank=False, null=True, on_delete=models.CASCADE)
    Answer = models.CharField(max_length=1024, blank=False, null=False)
    Correct = models.BooleanField(blank=False, null=False)
    AllAnswers = models.ForeignKey(MultipleChoiceUserAnswer, blank=False, null=True, default=None, on_delete=models.CASCADE)
    Solved = models.DateTimeField(default=timezone.now)
    Topic = models.CharField(max_length=24, choices=TOPICS, default='None', null=False, blank=False)

    def __str__(self):
        return "{} - Status: {}".format(self.Solved, self.Correct)
    

class TruthTableUserAnswer(models.Model):
    UserID = models.CharField(max_length=1024, default='None',blank=False, null=False)
    Duration = models.IntegerField(default=0,blank=False, null=False)
    Set = models.ForeignKey(QAWSet, blank=False, null=True, on_delete=models.CASCADE)
    AllCorrect = models.BooleanField(blank=False, null=False)
    Question = models.CharField(max_length=1024, blank=False, null=False)
    Solved = models.DateTimeField(default=timezone.now)
    Topic = models.CharField(max_length=24, choices=TOPICS, default='None', null=False, blank=False)

    def __str__(self):
        return "{} - Status: {}".format(self.Solved, self.AllCorrect)

class SingleTruthTableUserAnswer(models.Model):
    UserID = models.CharField(max_length=1024, default='None',blank=False, null=False)
    Duration = models.IntegerField(default=0,blank=False, null=False)
    Set = models.ForeignKey(QAWSet, blank=False, null=True, on_delete=models.CASCADE)
    Statement = models.CharField(max_length=1024, blank=False, null=False)
    Answer = models.CharField(max_length=1024, blank=False, null=False)
    Expectedanswer = models.CharField(max_length=1024, blank=False, null=False)
    Correct = models.BooleanField(blank=False, null=False)
    AllAnswers = models.ForeignKey(TruthTableUserAnswer, blank=False, null=True, default=None, on_delete=models.CASCADE)
    Solved = models.DateTimeField(default=timezone.now)
    Topic = models.CharField(max_length=24, choices=TOPICS, default='None', null=False, blank=False)

    def __str__(self):
        return "{} - Status: {}".format(self.Solved, self.Correct)
    

class ClozeUserAnswer(models.Model):
    UserID = models.CharField(max_length=1024, default='None',blank=False, null=False)
    Duration = models.IntegerField(default=0,blank=False, null=False)
    Set = models.ForeignKey(QAWSet, blank=False, null=True, on_delete=models.CASCADE)
    AllCorrect = models.BooleanField(blank=False, null=False)
    Solved = models.DateTimeField(default=timezone.now)
    Topic = models.CharField(max_length=24, choices=TOPICS, default='None', null=False, blank=False)

    def __str__(self):
        return "{} - Status: {}".format(self.Solved, self.AllCorrect)

class SingleFieldClozeUserAnswer(models.Model):
    UserID = models.CharField(max_length=1024, default='None',blank=False, null=False)
    Duration = models.IntegerField(default=0,blank=False, null=False)
    Set = models.ForeignKey(QAWSet, blank=False, null=True, on_delete=models.CASCADE)
    ExpectedAnswer = models.CharField(max_length=1024, blank=False, null=False)
    UserAnswer = models.CharField(max_length=1024, blank=False, null=False)
    Correct = models.BooleanField(blank=False, null=False)
    AllGaps = models.ForeignKey(ClozeUserAnswer, blank=False, null=True, default=None, on_delete=models.CASCADE)
    Solved = models.DateTimeField(default=timezone.now)
    Topic = models.CharField(max_length=24, choices=TOPICS, default='None', null=False, blank=False)

    def __str__(self):
        return "{} - Status: {}".format(self.Solved, self.Correct)
        
class OpenAssemblerAnswer(models.Model):
    UserID = models.CharField(max_length=1024, default='None',blank=False, null=False)
    Duration = models.IntegerField(default=0,blank=False, null=False)
    Set = models.ForeignKey(QAWSet, blank=False, null=True, on_delete=models.CASCADE)
    Question = models.TextField(blank=False, null=False)
    QuestionID = models.IntegerField(blank=True, null=True)
    Answer = models.TextField(blank=False, null=False)
    Solved = models.DateTimeField(default=timezone.now)
    Correct = models.BooleanField(blank=False, null=False)
    MissedStatements = models.TextField(blank=True, null=True)
    Topic = models.CharField(max_length=24, choices=TOPICS, default='Assembler', null=False, blank=False)
    OptimizedAnswer = models.TextField(blank=False, null=True)

    def __str__(self):
        return "{}: {} - Status: {}".format(self.id, self.Solved, self.Correct)

    def pdate(self):
        return self.Solved.strftime("%m/%d/%Y, %H:%M:%S")

class GatesAnswer(models.Model):
    UserID = models.CharField(max_length=1024, default='None',blank=False, null=False)
    Duration = models.IntegerField(default=0,blank=False, null=False)
    Set = models.ForeignKey(QAWSet, blank=False, null=True, on_delete=models.CASCADE)
    Question = models.TextField(blank=False, null=False)
    Expectedanswer = models.TextField(blank=False, null=False)
    Answer = models.PositiveIntegerField(blank=False, null=False)
    Solved = models.DateTimeField(default=timezone.now)
    Correct = models.BooleanField(blank=False, null=False)
    Topic = models.CharField(max_length=24, choices=TOPICS, default='Gates', null=False, blank=False)
    Imgpath = models.CharField(max_length=1024, null=False, blank=False)
    Expectedcircuitfunction = models.CharField(max_length=1024, null=False, blank=False)
    Answerircuitfunction = models.CharField(max_length=1024, null=False, blank=False)
    Input = models.CharField(max_length=1024, null=False, blank=False)

    def __str__(self):
        return "{} - Status: {}".format(self.Solved, self.Correct)
