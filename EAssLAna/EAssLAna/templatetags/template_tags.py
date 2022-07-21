from django import template
from django.template.defaulttags import register
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
    one_day = datetime.now() - timedelta(days=day_offset)
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
    return array[index]


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
def get_SuccessRate_All_Today_CorrectOnly(user_id):
    correct, incorrect = get_SuccessRate_All_Today(user_id)
    return correct/correct+incorrect

@register.simple_tag
def get_SuccessRate_All_Today(user_id):
    date_min, date_max = get_TimeRange_Today()
    return get_SuccessRate_All_DateRange(user_id, date_min, date_max)


@register.simple_tag
def get_SuccessRate_Week(user_id):
    week_dates = get_week()
    week_dates_All = []
    week_dates_Correct = []
    for day in week_dates:
        date_min, date_max = get_TimeRange(day)
        day_All, day_correct = get_SuccessRate_All_DateRange(user_id,date_min, date_max)
        week_dates_All.append(day_All)
        week_dates_Correct.append(day_correct)
    
    return [week_dates_All, week_dates_Correct]

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
        tmpcorrect, tmpincorrect = get_SuccessRate_Specific_DateRange(scAnswers,date_min,date_max)
        correct += tmpcorrect
        incorrect += tmpincorrect
    except:
        pass

    try:
        mcAnswers = MultipleChoiceUserAnswer.objects.filter(UserID=user_id)
        tmpcorrect, tmpincorrect =  get_SuccessRate_Specific_DateRange(mcAnswers,date_min,date_max)
        correct += tmpcorrect
        incorrect += tmpincorrect
    except:
        pass

    try:
        clozeAnswers = ClozeUserAnswer.objects.filter(UserID=user_id)
        tmpcorrect, tmpincorrect =  get_SuccessRate_Specific_DateRange(clozeAnswers,date_min,date_max)
        correct += tmpcorrect
        incorrect += tmpincorrect
    except:
        pass

    try:
        truthTableAnswers = TruthTableUserAnswer.objects.filter(UserID=user_id)
        tmpcorrect, tmpincorrect =  get_SuccessRate_Specific_DateRange(truthTableAnswers,date_min,date_max)
        correct += tmpcorrect
        incorrect += tmpincorrect
    except:
        pass

    try:
        openAssemblerAnswers = OpenAssemblerAnswer.objects.filter(UserID=user_id)
        tmpcorrect, tmpincorrect =  get_SuccessRate_Specific_DateRange(openAssemblerAnswers,date_min,date_max)
        correct += tmpcorrect
        incorrect += tmpincorrect
    except:
        pass

    try:
        gatesAnswers = GatesAnswer.objects.filter(UserID=user_id)
        tmpcorrect, tmpincorrect =  get_SuccessRate_Specific_DateRange(gatesAnswers,date_min,date_max)
        correct += tmpcorrect
        incorrect += tmpincorrect
    except:
        pass

    if correct+incorrect == 0:
        return 0,0
    else:
        # correctPercentage =correct/correct+incorrect
        # incorrectPercentage =incorrect/correct+incorrect
        # print(correctPercentage)
        # print(incorrectPercentage)
        return correct+incorrect, correct




