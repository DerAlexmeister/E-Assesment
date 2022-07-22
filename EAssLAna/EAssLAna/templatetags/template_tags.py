from django import template
from django.template.defaulttags import register
from django.contrib.auth import get_user_model

import pytz


from datetime import datetime, timedelta, time, date

from EAss.models import *

register = template.Library()



# internal functions
#############
tz = pytz.timezone('Europe/Berlin')

@register.filter
def get_week():
  
  cur_day = datetime.now()
  weekdayNumber = cur_day.weekday()
  dates = []
  n = 0
  for n in range(7):
    day_offset = n-weekdayNumber
    one_day = datetime.now() + timedelta(days=day_offset)
    n +=1
    dates.append(one_day)
    
  return dates

def calcAnswersCorrectWrong(q_set):
    correct, incorrect = 0, 0
    for i in q_set:
        try:
            if i.Correct:
                correct += 1
            else:
                incorrect += 1
        except AttributeError:
            if i.AllCorrect:
                correct += 1
            else:
                incorrect += 1
    return correct, incorrect

def get_EveryonePercentageAnsweredStatistics(cIncArr):
    cCorrect = 0
    cIncorrect = 0
    for key, value in cIncArr.items():
        cCorrect += value[0]
        cIncorrect += value[1]


    # output values for specific task types
    return [cCorrect, cIncorrect]

##################################
@register.filter
def get__array_valueByIndex(array, index):
    try:
        return array[index]
    except:
        return None

   

# otherwise if key missing does not return none
@register.filter
def get__item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get__item_values(dictionary, key):
    if key == -1:
        return dictionary.values()
    else:
        return dictionary.get(key).values()


@register.filter
def get__item_keys(dictionary, key):
    if key == -1:
        return dictionary.keys()
    else:
        return dictionary.get(key).keys()


@register.filter(name='sort')
def listsort(value):
    if isinstance(value, dict):
        new_dict = SortedDict()
        key_list = sorted(value.keys())
        for key in key_list:
            new_dict[key] = value[key]
        return new_dict
    elif isinstance(value, list):
        return sorted(value)
    else:
        return value
    listsort.is_safe = True



# external filter functions
# template filter only allow ONE parameter!!
# simple_tag allow multiple parameter
# {% multiple_args_tag 'arg1' 'arg2' 'arg3' 'arg4' %}
#############################################
@register.simple_tag
def get_Topics():
    topicsList = []
    topics = TOPICS
    for topic in topics:
        if(topic[0] != "None"):
            topicsList.append(topic[0]) #replace not working?
    return topicsList

@register.simple_tag
def get_Topic_SpecificQuestion_UserData(qawset,user_id):
    print("BRU")
    correct = 0
    incorrect = 0
   
    answers = get_Topic_SpecificQuestion_Answers(qawset.ItemType,user_id)
    correct, incorrect = get_SuccessRate_Specific(answers)

    print(get_Percentage(correct,correct+incorrect),correct,incorrect)
    return [get_Percentage(correct,correct+incorrect),correct,incorrect]


@register.simple_tag
def get_Topic_SpecificQuestion_Answers(answerType,user_id):
    print("!!!!!")
    print(answerType)
    print("!!!")
    answers = None
    
    if(answerType == "SingleChoice"):
        answers = SingleChoiceUserAnswer.objects.filter(UserID=user_id)

    if(answerType == "MultipleChoice"):
        answers = MultipleChoiceUserAnswer.objects.filter(UserID=user_id)

    if(answerType == "ClozeText"):
        answers = ClozeUserAnswer.objects.filter(UserID=user_id)

    if(answerType == "TruthTable"):
        answers = TruthTableUserAnswer.objects.filter(UserID=user_id)

    if(answerType == "Assembler"):
        answers = OpenAssemblerAnswer.objects.filter(UserID=user_id)

    if(answerType == "Gates"):
        answers = GatesAnswer.objects.filter(UserID=user_id)

    return answers  

@register.simple_tag
def get_Percentage(value, whole):
    try:
        intNumber = int(value/whole*100)
        return intNumber
    except:
        return 0
    

@register.simple_tag
def get_TimeRange_Today():
    date_min = datetime.combine(timezone.now().date(), datetime.today().time().min, tz)
    date_max = datetime.combine(timezone.now().date(), datetime.today().time().max, tz)
    return date_min, date_max

@register.simple_tag
def get_TimeRange(one_day):
    date_min = datetime.combine(one_day.date(), one_day.time().min,tz)
    date_max = datetime.combine(one_day.date(), one_day.time().max,tz)
    return date_min, date_max


@register.simple_tag
def get_SuccessRate_Today(user_id):
    date_min, date_max = get_TimeRange_Today()
    valuesToday = get_SuccessRate_All_DateRange(user_id, date_min, date_max)
    print(valuesToday)
    if valuesToday[0] == 0:
        return [0,0,0,0]
    else:
        return [get_Percentage(valuesToday[1],valuesToday[0]),valuesToday[0],valuesToday[1],valuesToday[2]]



@register.simple_tag
def get_SuccessRate_Week(user_id):
    week_dates = get_week()
    week_dates_All = []
    week_dates_Correct = []
    week_dates_Incorrect = []
    for day in week_dates:
        date_min, date_max = get_TimeRange(day)
        valuesWeek = get_SuccessRate_All_DateRange(user_id,date_min, date_max)
        week_dates_All.append(valuesWeek[0])
        week_dates_Correct.append(valuesWeek[1])
        week_dates_Incorrect.append(valuesWeek[2])
    
    return [week_dates_All, week_dates_Correct, week_dates_Incorrect]

@register.simple_tag
def get_Answers_ByTimeRange(answers_set,date_min,date_max): 
    if(isinstance(answers_set, SingleChoiceUserAnswer)):
        answers_today = SingleChoiceUserAnswer.objects.filter(Solved__range=(date_min, date_max))

    if(isinstance(answers_set, MultipleChoiceUserAnswer)):
        answers_today = MultipleChoiceUserAnswer.objects.filter(Solved__range=(date_min, date_max))

    if(isinstance(answers_set, ClozeUserAnswer)):
        answers_today = ClozeUserAnswer.objects.filter(Solved__range=(date_min, date_max))

    if(isinstance(answers_set, TruthTableUserAnswer)):
        answers_today = TruthTableUserAnswer.objects.filter(Solved__range=(date_min, date_max))

    if(isinstance(answers_set, OpenAssemblerAnswer)):
        answers_today = OpenAssemblerAnswer.objects.filter(Solved__range=(date_min, date_max))

    if(isinstance(answers_set, GatesAnswer)):
        answers_today = GatesAnswer.objects.filter(Solved__range=(date_min, date_max))

    return answers_today

@register.filter
def get_SuccessRate_Specific_DateRange(answers_set,date_min,date_max):
    #print(date_min.strftime('%Y-%m-%d')) 
    #print(date_max.strftime('%Y-%m-%d'))
    answers_daterange = get_Answers_ByTimeRange(answers_set[0],date_min,date_max)
    return get_SuccessRate_Specific(answers_daterange)

def get_SuccessRate_Specific(answers_set):    
    if answers_set is None:
        return 0,0

    correct = 0
    incorrect = 0
    for singleAnswer in answers_set:
        try:
            if singleAnswer.Correct:
                correct += 1
            else:
                incorrect += 1
        except AttributeError:
            if singleAnswer.AllCorrect:
                correct += 1
            else:
                incorrect += 1

    return correct, incorrect

@register.simple_tag
def get_SuccessRate_All_DateRange(user_id, date_min,date_max):
    correct = 0
    incorrect = 0

    try:
        scAnswers = SingleChoiceUserAnswer.objects.filter(UserID=user_id)
        scCorrect, scIncorrect = get_SuccessRate_Specific_DateRange(scAnswers,date_min,date_max)
        correct += scCorrect
        incorrect += scIncorrect
    except:
        scCorrect = 0
        scIncorrect = 0
        

    try:
        mcAnswers = MultipleChoiceUserAnswer.objects.filter(UserID=user_id)
        mcCorrect, mcIncorrect = get_SuccessRate_Specific_DateRange(mcAnswers,date_min,date_max)
        correct += mcCorrect
        incorrect += mcIncorrect
    except:
        mcCorrect = 0
        mcIncorrect = 0
        

    try:
        clozeAnswers = ClozeUserAnswer.objects.filter(UserID=user_id)
        clozeCorrect, clozeIncorrect = get_SuccessRate_Specific_DateRange(clozeAnswers,date_min,date_max)
        correct += clozeCorrect
        incorrect += clozeIncorrect
    except:
        clozeCorrect = 0
        clozeIncorrect = 0
        

    try:
        truthTableAnswers = TruthTableUserAnswer.objects.filter(UserID=user_id)
        truthTableCorrect, truthTableIncorrect =  get_SuccessRate_Specific_DateRange(truthTableAnswers,date_min,date_max)
        correct += truthTableCorrect
        incorrect += truthTableIncorrect
    except:
        truthTableCorrect = 0
        truthTableIncorrect = 0
        

    try:
        openAssemblerAnswers = OpenAssemblerAnswer.objects.filter(UserID=user_id)
        openAssemblerCorrect, openAssemblerIncorrect =  get_SuccessRate_Specific_DateRange(openAssemblerAnswers,date_min,date_max)
        correct += openAssemblerCorrect
        incorrect += openAssemblerIncorrect
    except:
        openAssemblerCorrect = 0
        openAssemblerIncorrect = 0
        

    try:
        gatesAnswers = GatesAnswer.objects.filter(UserID=user_id)
        gatesCorrect, gatesIncorrect =  get_SuccessRate_Specific_DateRange(gatesAnswers,date_min,date_max)
        correct += gatesCorrect
        incorrect += gatesIncorrect
    except:
        gatesCorrect = 0
        gatesIncorrect = 0
        

    return [correct+incorrect, correct, incorrect, [scCorrect,scIncorrect], [mcCorrect,mcIncorrect], [clozeCorrect,clozeIncorrect], [truthTableCorrect,truthTableIncorrect], [openAssemblerCorrect,openAssemblerIncorrect], [gatesCorrect, gatesIncorrect]]





@register.simple_tag
def get_SuccessRate_All(user_id):
    correct = 0
    incorrect = 0

    try:
        scAnswers = SingleChoiceUserAnswer.objects.filter(UserID=user_id)
        scCorrect, scIncorrect = get_SuccessRate_Specific(scAnswers)
        correct += scCorrect
        incorrect += scIncorrect
    except:
        scCorrect = 0
        scIncorrect = 0
        

    try:
        mcAnswers = MultipleChoiceUserAnswer.objects.filter(UserID=user_id)
        mcCorrect, mcIncorrect = get_SuccessRate_Specific(mcAnswers)
        correct += mcCorrect
        incorrect += mcIncorrect
    except:
        mcCorrect = 0
        mcIncorrect = 0
        

    try:
        clozeAnswers = ClozeUserAnswer.objects.filter(UserID=user_id)
        clozeCorrect, clozeIncorrect = get_SuccessRate_Specific(clozeAnswers)
        correct += clozeCorrect
        incorrect += clozeIncorrect
    except:
        clozeCorrect = 0
        clozeIncorrect = 0
        

    try:
        truthTableAnswers = TruthTableUserAnswer.objects.filter(UserID=user_id)
        truthTableCorrect, truthTableIncorrect =  get_SuccessRate_Specific(truthTableAnswers)
        correct += truthTableCorrect
        incorrect += truthTableIncorrect
    except:
        truthTableCorrect = 0
        truthTableIncorrect = 0
        

    try:
        openAssemblerAnswers = OpenAssemblerAnswer.objects.filter(UserID=user_id)
        openAssemblerCorrect, openAssemblerIncorrect =  get_SuccessRate_Specific(openAssemblerAnswers)
        correct += openAssemblerCorrect
        incorrect += openAssemblerIncorrect
    except:
        openAssemblerCorrect = 0
        openAssemblerIncorrect = 0
        

    try:
        gatesAnswers = GatesAnswer.objects.filter(UserID=user_id)
        gatesCorrect, gatesIncorrect = get_SuccessRate_Specific(gatesAnswers)
        correct += gatesCorrect
        incorrect += gatesIncorrect
    except:
        gatesCorrect = 0
        gatesIncorrect = 0
        


    output = [correct+incorrect, correct, incorrect, [scCorrect,scIncorrect], [mcCorrect,mcIncorrect], [clozeCorrect,clozeIncorrect], [truthTableCorrect,truthTableIncorrect], [openAssemblerCorrect,openAssemblerIncorrect], [gatesCorrect, gatesIncorrect]]
    #print(output)
    return output

@register.simple_tag
def get_UserAnsweredTopics_Count():
    User = get_user_model()
    users = User.objects.all()
    topics = get_Topics()
    topics_count_dict = []
    topics_count_dict_correct = []

    n = 0
    for topic in topics:
        topics_count_dict.append(0)
        topics_count_dict_correct.append(0)
        n+=1

    for user in users:
        if not user.is_superuser:
            val = get_UserAnsweredTopics_Count()
            z = 0
            for i in topics:
                topics_count_dict[z] += val[1][z]
                topics_count_dict_correct[z] += val[2][z]
                z += 1
                
    return [topics, topics_count_dict,topics_count_dict_correct]


@register.simple_tag
def get_UserAnsweredTopics_Count(user_id):
    topics = get_Topics()
    topics_count_dict = []
    topics_count_dict_correct = []

    n = 0
    for topic in topics:
        topics_count_dict.append(0)
        topics_count_dict_correct.append(0)
        n+=1

    try:
        scAnswers = SingleChoiceUserAnswer.objects.filter(UserID=user_id)
        for item in scAnswers:
            qawSets = item.Set
            try:
                topics_count_dict[topics.index(item.Set.Topic)] += 1 
            except:
                pass
            try:
                if(item.Correct):
                    topics_count_dict_correct[topics.index(item.Set.Topic)] += 1 
            except:
                pass
           
    except:
        pass

    try:
        mcAnswers = MultipleChoiceUserAnswer.objects.filter(UserID=user_id)
        for item in mcAnswers:
            qawSets = item.Set
            try:
                topics_count_dict[topics.index(item.Set.Topic)] += 1 
            except:
                pass
    except:
        pass

    try:
        clozeAnswers = ClozeUserAnswer.objects.filter(UserID=user_id)
        for item in clozeAnswers:
            qawSets = item.Set
            try:
                topics_count_dict[topics.index(item.Set.Topic)] += 1 
            except:
                pass
    except:
        pass

    try:
        truthTableAnswers = TruthTableUserAnswer.objects.filter(UserID=user_id)
        for item in truthTableAnswers:
            qawSets = item.Set
            try:
                topics_count_dict[topics.index(item.Set.Topic)] += 1 
            except:
                pass
    except:
        pass

    try:
        openAssemblerAnswers = OpenAssemblerAnswer.objects.filter(UserID=user_id)
        for item in openAssemblerAnswers:
            qawSets = item.Set
            try:
                topics_count_dict[topics.index(item.Set.Topic)] += 1 
            except:
                pass
    except:
        pass

    try:
        gatesAnswers = GatesAnswer.objects.filter(UserID=user_id)
        for item in gatesAnswers:
            qawSets = item.Set
            try:
                topics_count_dict[topics.index(item.Set.Topic)] += 1 
            except:
                pass
    except:
        pass

    return [topics, topics_count_dict,topics_count_dict_correct]

@register.filter
def get_AllUserAnsweredTopics_Count():
    userModel = get_user_model()
    allusers = userModel.objects.all()

    topics_dict_peruser = {}
    everyone_topics_dict = {}
    for key, value in TOPICS:
        everyone_topics_dict[key] = 0
    #print(everyone_topics_dict)
    for studentuser in allusers:
        if not studentuser.is_superuser:
            topics_dict_peruser[studentuser.id] = getUserAnsweredTopics_Count(studentuser.id)
            
            for key, value in topics_dict_peruser[studentuser.id].items():
                everyone_topics_dict[key] += value
    #print(everyone_topics_dict)
    #print(topics_dict_peruser)

    return topics_dict_peruser, everyone_topics_dict



