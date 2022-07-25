[1mdiff --git a/EAssLAna/EAss/views.py b/EAssLAna/EAss/views.py[m
[1mindex d5a1661..f37134b 100644[m
[1m--- a/EAssLAna/EAss/views.py[m
[1m+++ b/EAssLAna/EAss/views.py[m
[36m@@ -1,5 +1,6 @@[m
 import urllib.parse[m
 import json[m
[32m+[m[32mimport datetime[m
 [m
 from django.http.response import HttpResponse[m
 from django.shortcuts import render[m
[36m@@ -527,31 +528,31 @@[m [mdef generateOpenAssemblerQuestions(request):[m
                     parsed.checkForStatement(n_instructions)[m
                     n_instructions = ','.join(parsed.getMissingInstructions())[m
                     correct = (parsed.equalsState(answerdict) and parsed.hasMissingInstructions())[m
[31m-                else:[m
[32m+[m
                     [m
[31m-                    NameID = ""[m
[31m-                    raw_request = request.body.decode("UTF-8")[m
[31m-                    raw_request_split = raw_request.split("&")[m
[31m-                    answers = [][m
[31m-[m
[31m-                    for element in raw_request_split:[m
[31m-[m
[31m-                        if element.startswith("NameID="):[m
[31m-                            NameID += urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("NameID=", "")))   [m
[31m-                        if element.startswith("BeginTime="):[m
[31m-                            beginTime = urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("BeginTime=", "")))[m
[31m-[m
[31m-                    qaw_set = QAWSet.objects.get(NameID=NameID)[m
[31m-[m
[31m-                    correct = parsed.equalsState(answerdict)[m
[31m-                    useranswer = OpenAssemblerAnswer(Duration=calculateTimeDuration(beginTime,endtime), Solved=endtime,Set=qaw_set,[m
[31m-                    Question=AssemblerQuestion.Question,[m
[31m-                    Answer=usercode,[m
[31m-                    Correct=correct,[m
[31m-                    QuestionID=AssemblerQuestion.id,[m
[31m-                    OptimizedAnswer=AssemblerQuestion.OptimizedSolution[m
[31m-                )[m
[31m-                if len(n_instructions) > 2: useranswer.MissedStatements = n_instructions[m
[32m+[m[32m                NameID = ""[m
[32m+[m[32m                raw_request = request.body.decode("UTF-8")[m
[32m+[m[32m                raw_request_split = raw_request.split("&")[m
[32m+[m
[32m+[m[32m                for element in raw_request_split:[m
[32m+[m
[32m+[m[32m                    if element.startswith("NameID="):[m
[32m+[m[32m                        NameID += urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("NameID=", "")))[m[41m   [m
[32m+[m[32m                    if element.startswith("BeginTime="):[m
[32m+[m[32m                        beginTime = urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("BeginTime=", "")))[m
[32m+[m
[32m+[m[32m                qaw_set = QAWSet.objects.get(NameID=NameID)[m
[32m+[m[32m                endtime = datetime.datetime.now()[m
[32m+[m[32m                correct = parsed.equalsState(answerdict)[m
[32m+[m[32m                useranswer = OpenAssemblerAnswer(Duration=calculateTimeDuration(beginTime,endtime), Solved=endtime,Set=qaw_set,[m
[32m+[m[32m                        Question=AssemblerQuestion.Question,[m
[32m+[m[32m                        Answer=usercode,[m
[32m+[m[32m                        Correct=correct,[m
[32m+[m[32m                        QuestionID=AssemblerQuestion.id,[m
[32m+[m[32m                        OptimizedAnswer=AssemblerQuestion.OptimizedSolution[m
[32m+[m[32m                    )[m
[32m+[m[32m                if len(n_instructions) > 2:[m
[32m+[m[32m                    useranswer.MissedStatements = n_instructions[m
                 useranswer.save()[m
                 [m
                 return redirect("/learninganalytics/assembleranalysis?t={}".format(useranswer.id))[m
