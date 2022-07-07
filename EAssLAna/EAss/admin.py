import imp
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
from .models import NormalForm, NormalFormDifficulty

admin.site.register(QAWSet)
admin.site.register(Question)
admin.site.register(WrongStatements)
admin.site.register(Answer)
admin.site.register(BinaryStatement)
admin.site.register(OctaStatement)
admin.site.register(Cloze)
admin.site.register(Gap)
admin.site.register(GapSolution)
admin.site.register(NormalForm)
admin.site.register(NormalFormDifficulty)
