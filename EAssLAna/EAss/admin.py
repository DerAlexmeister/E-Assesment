from django.contrib import admin

from .models import QAWSet
from .models import WrongStatements
from .models import Question
from .models import Answer
from .models import BinaryStatement
from .models import OctaStatement
from .models import Cloze
from .models import Gap
from .models import GapSolution
from .models import OpenAssemblerCodeQuestions
from .normal_forms.model import *

from .models import CalculusSingleUserAnswer
from .models import SingleChoiceUserAnswer
from .models import MultipleChoiceUserAnswer
from .models import SingleMultipleChoiceUserAnswer
from .models import TruthTableUserAnswer
from .models import SingleTruthTableUserAnswer
from .models import ClozeUserAnswer
from .models import SingleFieldClozeUserAnswer
from .models import OpenAssemblerAnswer
from .models import GatesAnswer

# Questiontypes
admin.site.register(QAWSet)
admin.site.register(Question)
admin.site.register(WrongStatements)
admin.site.register(Answer)
admin.site.register(BinaryStatement)
admin.site.register(OctaStatement)
admin.site.register(Cloze)
admin.site.register(Gap)
admin.site.register(GapSolution)
admin.site.register(OpenAssemblerCodeQuestions)

# Answertypes for Users
admin.site.register(CalculusSingleUserAnswer)
admin.site.register(SingleChoiceUserAnswer)
admin.site.register(MultipleChoiceUserAnswer)
admin.site.register(SingleMultipleChoiceUserAnswer)
admin.site.register(TruthTableUserAnswer)
admin.site.register(SingleTruthTableUserAnswer)
admin.site.register(ClozeUserAnswer)
admin.site.register(SingleFieldClozeUserAnswer)
admin.site.register(OpenAssemblerAnswer)
admin.site.register(GatesAnswer)

admin.site.register(NormalForm)
admin.site.register(NormalFormDifficulty)
admin.site.register(NormalFormGuess)
admin.site.register(NormalFormLiteral)
admin.site.register(NormalFormAnswer)
admin.site.register(NormalFormCorrection)
admin.site.register(NormalFormTerm)
admin.site.register(NormalFormQuestion)
