from django.http import HttpResponse,HttpRequest
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import Test,MCQ,MCQProxy,TestProxy
from google.cloud import datastore
from utility import con,decon,calc
import datetime
import json
client = datastore.Client()
@login_required(login_url='/login/')
def studenthome(request):
    user = User.objects.get(username=request.user)
    if user.is_staff==True:
        return redirect('/login/')
    username = user.username
    acc_key  = client.key('Account',username)
    Account = client.get(acc_key)
    if Account==None:
        Account = datastore.Entity(acc_key)
        try:
            Account['email'] = user.email
        except:
            print "Email of the person unknown"    
        client.put(Account)
    else: 
        pass
    q = client.query(kind='Sess')
    q.add_filter('user','=',user.username)
    iter_query = q.fetch()
    ret = []
    for e in iter_query:
        lst = e.key.__dict__['_path']
        temp = {}
        temp['start'] = e['created']
        temp['submit'] = False
        for li in lst:
            try:
                temp[li['kind']] = li['name']
            except:
                temp[li['kind']] = li['id']
        ret.append(temp)
    return render(request,'home1.html',{'tests':ret}) 
@login_required(login_url='/login/')
def testdashboard(request):
    testcode = ''
    if request.method=='POST':
        testcode = request.POST['testcode']
        testkey = client.key('Test',testcode)
        tt = client.get(testkey)
        if tt==None:
            return redirect('/home/')
    else:
        return redirect('/home/')
    testcode = request.POST['testcode']
    user = User.objects.get(username=request.user)
    username = user.username
    acc_key  = client.key('Account',username)
    Account = client.get(acc_key)
    ##The Account is now created or accessed
    ##Now we needd to check if the test proxy object already exists
    ##or it needs to be created
    sesskey = client.key('Test',request.POST['testcode'],'Account',username,'Sess')
    sess = datastore.Entity(sesskey)
    sess['created'] = datetime.datetime.now()
    sess['user'] = username
    client.put(sess)
    return render(request,'dashboard1.html',{'testID':testcode,'sesskey':sess.key.id})

@login_required(login_url='/login/')
def saveResponse(request):
    print request.POST
    data = request.POST.dict()
    user = User.objects.get(username =request.user)
    username = user.username
    testID = None
    questID = None
    ans = None
    attempt = None
    section = None
    number  = None
    try:
        testID = data['testID']
        questID = int(data['questID'])
        attempt = data['attempt']
        section = data['section']
        number = data['number']
    except:
        print "The test ID is not present"
        pass
    # print testID
    # print questID
    # print ans
    # print int(request.POST['sesskey'])
    sesskey = client.key('Test',testID,'Account',username,'Sess',int(request.POST['sesskey']))
    sess = client.get(sesskey)
    # print sess
    if sess==None: return redirect('/home/')
    questIDbyte = str(questID)
    if sess.get(questIDbyte)==None:
        sess[questIDbyte] = {}
    sess[questIDbyte]['attempt'] = attempt
    sess[questIDbyte]['section'] = section
    sess[questIDbyte]['number'] = number
    client.put(sess)
    print sess
    return HttpResponse("Response Saved")
@login_required(login_url='/login/')
def submitSuccess(request):
    return render(request,'message.html',{'mess':'Your responses were submitted successfully.Return to home page to view results'})

@login_required(login_url='/login/')
def result(request,testcode,sesscode):
    #sess code
    sesscode = int(sesscode)
    ##obtain the user object from the MySQL
    user = User.objects.get(username=request.user)
    username = user.username
    Sess = None
    Test = None
    ##ontain the sesskey,Sess object,testkey,Test Object
    ##if either of the two do not exist 
    ##Redirect to /home/
    try:
        sesskey = client.key('Test',testcode,'Account',username,'Sess',sesscode)
        Sess = client.get(sesskey)
        testkey = client.key('Test',testcode)
        Test = client.get(testkey)
        if Sess==None:
            return redirect('/home/')
        if Test==None:
            return redirect('/home/')
    except:
        return redirect('/home/')
    ##ret is the object to be sent to
    ## Django Template Engine
    ## Initialise it with the sections currently 
    ## defined e.g.: ma1,ma2,ma3,ch1,ch2
    ret = {}
    ret['ma1'] = []
    ret['ma2'] = []
    ret['ma3'] = []
    ret['ph1'] = []
    ret['ph2'] = []
    ret['ph3'] = []
    ret['ch1'] = []
    ret['ch2'] = []
    ret['ch3'] = []
    sections = ['ma1','ma2','ma3','ph1','ph2','ph3','ch1','ch2','ch3']
    mp = {}
    mp['1'] = 'ma'
    mp['2'] = 'ph'
    mp['3'] = 'ch'
    ##iterator cursor for quering (iter_query)
    ## Quest with the Test=testcode(e.g.bothra003)
    qgen = client.query(kind='Quest',ancestor=client.key('Test',testcode))
    # qgen.order = ['created']
    iter_query = qgen.fetch()
    ##iterate through the elements of 
    ##iter_query
    for q in iter_query:
        ##temporary dictionary to
        ##store the objects 
        ##
        haha = {}
        ##convert the numerical quest ID 
        ##to string stored in quest_id
        quest_id = str(q.key.id)
        ##section of the question
        quest_section = q.get('section')
        ##subject of the question
        quest_subject = q.get('subject')
        ##
        complete_section = None
        print mp.get(str(quest_subject)) + str(quest_section)
        try:
            complete_section = mp.get(str(quest_subject)) + str(quest_section)
        except:
            print "The complete_section could not be obtained\
                    using concatenation"
            complete_section = None
        ##check is such is section is define
        if complete_section not in sections: 
            print "The section for the question either does not exist"
            print "It has not been assigned a section "
            continue
        tot = q.get('tmarks')
        neg = q.get('nmarks')
        par = q.get('pmarks')
        haha['tot'] = tot
        haha['neg'] = neg 
        haha['par'] = par
        haha['ob'] = 0
        ##Check is the candidate even saved the question once
        if Sess.get(quest_id)==None: continue
        ##If not the quests reponse key would not have 
        ##created in the session 
        ##
        resp = Sess[quest_id]
        haha['questID'] = quest_id
        haha['response'] = 'Did not attempt'
        try:
            haha['correct'] = con(q.get('ans'),int(quest_section))
        except:
            print "con() method could not convert the ans to list representation"
        if haha.get('correct') ==None: continue
        if str(resp.get('attempt'))!="1":
            #not attempted the question 
            ret[complete_section].append(haha) 
        else:
            try:
                haha['response'] = decon(int(resp.get('number')),int(quest_section))
            except:
                haha['response'] = None
            haha['ob'] = calc(haha['response'],haha['correct'],tot,neg,par,int(quest_section))
            ret[complete_section].append(haha)
    return render(request,'result.html',ret)