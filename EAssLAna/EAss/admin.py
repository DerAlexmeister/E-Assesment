import imp
from django.contrib import admin

from .models import QAWSet
from .models import WrongStatements
from .models import Question
from .models import Answer
from .models import BinaryStatement
from .models import OctaStatement

admin.site.register(QAWSet)
admin.site.register(Question)
admin.site.register(WrongStatements)
admin.site.register(Answer)
admin.site.register(BinaryStatement)
admin.site.register(OctaStatement)