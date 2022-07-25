from django import template
from django.template.defaulttags import register
from django.contrib.auth import get_user_model

import pytz


from datetime import datetime, timedelta, time, date

from EAss.models import *
from EAss.normal_forms.model import NormalFormGuess

register = template.Library()



# internal functions
#############
tz = pytz.timezone('Europe/Berlin')

@register.filter
def get_list_empty(list):
    try:
        for i in list:
            if i != 0 and i != None:
                return False
        return True
    except:
        return False
   


@register.simple_tag
def get_users():
    User = get_user_model()
    return User.objects.all()

@register.filter
def get_user_realname(user_id):
    if user_id == "Teacher":
        return None
    try:
        User = get_user_model()
        user = User.objects.get(id=user_id)
        return user.get_full_name()
    except  User.DoesNotExist:
        return None


@register.filter
def get_user_username(user_id):
    if user_id == "Teacher":
        return None
    try:
        User = get_user_model()
        user = User.objects.get(id=user_id)
        return user.get_username()
    except  User.DoesNotExist:
        return None

@register.simple_tag
def get_user_data(user_id):
    if user_id == "Teacher":
        return None
    try:
        User = get_user_model()
        user = User.objects.get(id=user_id)
        return [user.get_username(), user.get_full_name()]
    except  User.DoesNotExist:
        return None

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
    correct = 0
    incorrect = 0

    if user_id == "Teacher":
        answers = get_Topic_SpecificQuestion_Answers_Admin(qawset.ItemType)
    else:
        answers = get_Topic_SpecificQuestion_Answers(qawset.ItemType,user_id)

    if(answers == None):
        return None
    correct, incorrect = get_SuccessRate_Specific(answers)
    if(correct+incorrect == 0):
        return None
    else:
        duration = get_Duration_Specific(answers)
        return [int(get_Percentage(correct,correct+incorrect)),correct,incorrect,duration]


@register.simple_tag
def get_Topic_SpecificQuestion_Answers_Admin(answerType):
    answers = None
    
    if(answerType == "SingleChoice"):
        answers = SingleChoiceUserAnswer.objects.all()

    if(answerType == "MultipleChoice"):
        answers = MultipleChoiceUserAnswer.objects.all()

    if(answerType == "ClozeText"):
        answers = ClozeUserAnswer.objects.all()

    if(answerType == "TruthTable"):
        answers = TruthTableUserAnswer.objects.all()

    if(answerType == "Assembler"):
        answers = OpenAssemblerAnswer.objects.all()

    if(answerType == "Gates"):
        answers = GatesAnswer.objects.all()

    if(answerType == "Calculus"):
        answers = CalculusSingleUserAnswer.objects.all()

    if(answerType == "NormalForm"):
        answers = NormalFormGuess.objects.all()
        print("ANSWERS")
        print(answers)

    return answers

@register.simple_tag
def get_Topic_SpecificQuestion_Answers(answerType,user_id):
    answers = None
    print(answers)
    
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

    if(answerType == "Calculus"):
        answers = CalculusSingleUserAnswer.objects.filter(UserID=user_id)

    if(answerType == "NormalForm"):
        answers = NormalFormGuess.objects.filter(UserID=user_id)

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
def get_SuccessRate_Today_Admin():
    date_min, date_max = get_TimeRange_Today()
    User = get_user_model()
    users = User.objects.all()
    valuesToday = [0,0,0,0]
    for user in users:
        
        if not user.is_superuser:

            try:
                user_valuesToday = get_SuccessRate_All_DateRange(user.id, date_min, date_max)
           

                valuesToday[0] += user_valuesToday[0]
                valuesToday[1] += user_valuesToday[1]
                valuesToday[2] += user_valuesToday[2]
            except:
                pass

    return [int(get_Percentage(valuesToday[1],valuesToday[0])),valuesToday[0],valuesToday[1],valuesToday[2]]




@register.simple_tag
def get_SuccessRate_Today(user_id):
    if user_id == "Teacher":
        return get_SuccessRate_Today_Admin();
    date_min, date_max = get_TimeRange_Today()
    valuesToday = get_SuccessRate_All_DateRange(user_id, date_min, date_max)
    if valuesToday[0] == 0:
        return [0,0,0,0]
    else:
        return [int(get_Percentage(valuesToday[1],valuesToday[0])),valuesToday[0],valuesToday[1],valuesToday[2]]


@register.simple_tag
def get_SuccessRate_Week_Admin():
    User = get_user_model()
    users = User.objects.all()

    week_dates_All = [0,0,0,0,0,0,0]
    week_dates_Correct = [0,0,0,0,0,0,0]
    week_dates_Incorrect = [0,0,0,0,0,0,0]

    for user in users:
        if not user.is_superuser:
            user_valuesToday = get_SuccessRate_Week(user.id)
            for i in range(7):
                week_dates_All[i] += user_valuesToday[0][i]
                week_dates_Correct[i] += user_valuesToday[1][i]
                week_dates_Incorrect[i] += user_valuesToday[2][i]
    return [week_dates_All, week_dates_Correct, week_dates_Incorrect]


@register.simple_tag
def get_SuccessRate_Week(user_id):
    if user_id == "Teacher":
        return get_SuccessRate_Week_Admin();
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
    answers_today = answers_set.filter(Solved__range=(date_min, date_max))


    return answers_today

@register.filter
def get_SuccessRate_Specific_DateRange(answers_set,date_min,date_max):
    #print(date_min.strftime('%Y-%m-%d')) 
    #print(date_max.strftime('%Y-%m-%d'))
    answers_daterange = get_Answers_ByTimeRange(answers_set,date_min,date_max)
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

def get_Duration_Specific(answers_set):
    if answers_set is None:
        return 0
    Duration = 0
    count = 0


    for singleAnswer in answers_set:
        try:
            Duration += singleAnswer.Duration
            count += 1
        except:
            pass

    if count == 0:
        return 0
    else:
        td_str = str(timedelta(seconds=int(Duration/count)))
        td_split = td_str.split(':')
        td_str = td_split[0]+ ' H '+ td_split[1]+ ' M '+ td_split[2]+ ' S'
        return td_str

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

    try:
        calculusAnswers = CalculusSingleUserAnswer.objects.filter(UserID=user_id)
        calculusCorrect, calculusIncorrect = get_SuccessRate_Specific_DateRange(calculusAnswers,date_min,date_max)
        correct += calculusCorrect
        incorrect += calculusIncorrect
    except:
        calculusCorrect = 0
        calculusIncorrect = 0

    try:
        normalFormGuess = NormalFormGuess.objects.filter(UserID=user_id)
        normalFormGuessALL = NormalFormGuess.objects.all()
        print(normalFormGuessALL)
        print(normalFormGuess)
        normalformCorrect, normalformIncorrect = get_SuccessRate_Specific_DateRange(normalFormGuess,date_min,date_max)
        correct += normalformCorrect
        incorrect += normalformIncorrect
    except:
        normalformCorrect = 0
        normalformIncorrect = 0

    print([correct+incorrect, correct, incorrect, [scCorrect,scIncorrect], [mcCorrect,mcIncorrect], [clozeCorrect,clozeIncorrect], [truthTableCorrect,truthTableIncorrect], [openAssemblerCorrect,openAssemblerIncorrect], [gatesCorrect, gatesIncorrect], [calculusCorrect,calculusIncorrect],[normalformCorrect,normalformIncorrect]]
)
        
    return [correct+incorrect, correct, incorrect, [scCorrect,scIncorrect], [mcCorrect,mcIncorrect], [clozeCorrect,clozeIncorrect], [truthTableCorrect,truthTableIncorrect], [openAssemblerCorrect,openAssemblerIncorrect], [gatesCorrect, gatesIncorrect], [calculusCorrect,calculusIncorrect],[normalformCorrect,normalformIncorrect]]


@register.simple_tag
def get_SuccessRate_All_Admin():
    User = get_user_model()
    users = User.objects.all()

    correct = 0
    incorrect = 0
    scCorrect = 0
    scIncorrect = 0
    mcCorrect = 0
    mcIncorrect = 0
    clozeCorrect = 0
    clozeIncorrect = 0
    truthTableCorrect = 0
    truthTableIncorrect = 0
    openAssemblerCorrect = 0
    openAssemblerIncorrect = 0
    gatesCorrect = 0
    gatesIncorrect = 0
    calculusCorrect = 0
    calculusIncorrect = 0
    normalformsCorrect = 0
    normalformsIncorrect = 0


    for user in users:
        if not user.is_superuser:
            val = get_SuccessRate_All(user.id)

            correct += val[1]
            incorrect += val[2]

            scCorrect += val[3][0]
            scIncorrect += val[3][1]

            mcCorrect += val[4][0]
            mcIncorrect += val[4][1]

            clozeCorrect += val[5][0]
            clozeIncorrect += val[5][1]

            truthTableCorrect += val[6][0]
            truthTableIncorrect += val[6][1]

            openAssemblerCorrect += val[7][0]
            openAssemblerIncorrect += val[7][1]

            gatesCorrect += val[8][0]
            gatesIncorrect += val[8][1]

            calculusCorrect += val[9][0]
            calculusIncorrect += val[9][1]

            normalformsCorrect += val[10][0]
            normalformsIncorrect += val[10][1]
    


    output = [correct+incorrect, correct, incorrect,
    [get_Percentage(scCorrect,(scCorrect+scIncorrect)),get_Percentage(scIncorrect,(scCorrect+scIncorrect))],
    [get_Percentage(mcCorrect,(mcCorrect+mcIncorrect)),get_Percentage(mcIncorrect,(mcCorrect+mcIncorrect))],
    [get_Percentage(clozeCorrect,(clozeCorrect+clozeIncorrect)),get_Percentage(clozeIncorrect,(clozeCorrect+clozeIncorrect))],
    [get_Percentage(truthTableCorrect,(truthTableCorrect+truthTableIncorrect)),get_Percentage(truthTableIncorrect,(truthTableCorrect+truthTableIncorrect))],
    [get_Percentage(openAssemblerCorrect,(openAssemblerCorrect+openAssemblerIncorrect)),get_Percentage(openAssemblerIncorrect,(openAssemblerCorrect+openAssemblerIncorrect))],
    [get_Percentage(gatesCorrect,(gatesCorrect+gatesIncorrect)),get_Percentage(gatesIncorrect,(gatesCorrect+gatesIncorrect))],
    [get_Percentage(calculusCorrect,(calculusCorrect+calculusIncorrect)),get_Percentage(calculusIncorrect,(calculusCorrect+calculusIncorrect))],
    [get_Percentage(normalformsCorrect,(normalformsCorrect+normalformsIncorrect)),get_Percentage(normalformsIncorrect,(normalformsCorrect+normalformsIncorrect))]
    ]

    return output


@register.simple_tag
def get_SuccessRate_All(user_id):
    if user_id == "Teacher":
        return get_SuccessRate_All_Admin();

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

    try:
        calculusAnswers = CalculusSingleUserAnswer.objects.filter(UserID=user_id)
        calculusCorrect, calculusIncorrect = get_SuccessRate_Specific(calculusAnswers)
        correct += calculusCorrect
        incorrect += calculusIncorrect
    except:
        calculusCorrect = 0
        calculusIncorrect = 0

    try:
        normalFormGuess = NormalFormGuess.objects.filter(UserID=user_id)
        normalformCorrect, normalformIncorrect = get_SuccessRate_Specific(normalFormGuess)
        correct += normalformCorrect
        incorrect += normalformIncorrect
    except:
        normalformCorrect = 0
        normalformIncorrect = 0
        

    output = [correct+incorrect, correct, incorrect, [scCorrect,scIncorrect], [mcCorrect,mcIncorrect], [clozeCorrect,clozeIncorrect], [truthTableCorrect,truthTableIncorrect], [openAssemblerCorrect,openAssemblerIncorrect], [gatesCorrect, gatesIncorrect], [calculusCorrect, calculusIncorrect], [normalformCorrect,normalformIncorrect]]
    return output

@register.simple_tag
def get_UserAnsweredTopics_Count_Admin():
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
            val = get_UserAnsweredTopics_Count(user.id)
            z = 0
            for i in topics:
                topics_count_dict[z] += val[1][z]
                topics_count_dict_correct[z] += val[2][z]
                z += 1

    return [topics, topics_count_dict,topics_count_dict_correct]


@register.simple_tag
def get_UserAnsweredTopics_Count(user_id):
    if user_id == "Teacher":
        return get_UserAnsweredTopics_Count_Admin();
    
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
    
    try:
        calculusAnswers = CalculusSingleUserAnswer.objects.filter(UserID=user_id)
        for item in calculusAnswers:
            qawSets = item.Set
            try:
                topics_count_dict[topics.index(item.Set.Topic)] += 1 
            except:
                pass
    except:
        pass

    try:
        normalFormGuess = NormalFormGuess.objects.filter(UserID=user_id)
        for item in normalFormGuess:
            qawSets = item.Set
            try:
                topics_count_dict[topics.index(item.Set.Topic)] += 1 
            except:
                pass
    except:
        pass


    return [topics, topics_count_dict,topics_count_dict_correct]


@register.simple_tag
def get_UserAnsweredTopics_MostConfident(topics_array):
    topic_name = None
    percentage_correct = 0
    n = 0
    for topic in topics_array[0]:
        tmp_perc = topics_array[2][n]/topics_array[1][n]
        if(tmp_perc > percentage_correct):
            percentage_correct = tmp_perc
            topic_name = topics_array[0]
        n+=1

    if topic_name == None: 
        return None
    
    return [topic_name, percentage_correct]






