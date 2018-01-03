from django.http import HttpResponse,HttpRequest
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import Test,MCQ,MCQProxy,TestProxy
from google.cloud import datastore
import datetime
# from datetime import timezone
import json
client = datastore.Client()
@login_required(login_url='/login/')
def testcreator(request):
    user = User.objects.get(username=request.user)
    if user.is_staff==False:
        return redirect('/login/')
    if request.method=='POST':
        testcode = request.POST['testcode']            
        key = client.key('Test',testcode)
        test = client.get(key)
        if test==None:
            test = datastore.Entity(key=key)
        return render(request,'testgen.html',{"testcode":testcode})
    return redirect('/login/')
@login_required(login_url='/login')
def getdata(request,testcode='bothra001'):
    print testcode
    testkey = client.key('Test',testcode)
    test = client.get(testkey)

    quests = {}
    quests['keylst'] = []
    print 'test'
    print test
    if test==None:
        test = datastore.Entity(key=testkey)
        client.put(test)
        return HttpResponse(json.dumps(quests),content_type='application/json')
    questquery = client.query(kind='Quest',ancestor=testkey)
    iter_lst = questquery.fetch()
    ##lst is an iterable 
    # try:
    quests['keylst'] = [e.key.id for e in iter_lst]
    # except:
    #     pass
    print quests
    return HttpResponse(json.dumps(quests),content_type="application/json")
@login_required(login_url='/login')
def getdata_student(request):
    ##Phase One
    ## The method obtains the data
    ## for the particular testcode
    ## for the student dashboard
    ##Phase Two
    ## From the sessId determine whether it exists
    ## From it find the questions that have been attempted
    ## The student response, attempt,marked or not is returned
    ## the request method should be POST
    # print request
    if request.method!='POST':
        print 'getdata student data not post'
        return HttpResponse("Get Data Student method is not POST")
    testcode = request.POST['testID']
    sessID = request.POST['sessID']
    testkey = client.key('Test',testcode)
    test = client.get(testkey)
    quests = {}
    if test==None:
        return HttpResponse("Not OK")
        # test = datastore.Entity(key=testkey)
        # client.put(test)
        # return HttpResponse(json.dumps(quests),content_type='application/json')
    questquery = client.query(kind='Quest',ancestor=testkey)
    # questquery.keys_only()
    iter_lst = questquery.fetch()
    ##lst is an iterable 
    ##initialising th mp dictionary with subject code
    ## 1--> maths
    ## 2-->physics
    ## 3-->chemistry
    ###
    # print testcode
    # print sessID

    subjects = ['1','2','3']
    sections = ['1','2','3']
    ##inititalise the lsts
    mp = {}
    mp['1'] = 'ma'
    mp['2'] = 'ph'
    mp['3'] = 'ch'
    for sub in subjects:
        for sect in sections:
            quests[mp[sub]+sect] = []
    ###
    ##Initialise the Sess object with the session
    ##Now obtain necessary information from the session
    Sess = {}
    user = User.objects.get(username = request.user)
    username = user.username
    try:
        sesskey = client.key('Test',testcode,'Account',username,'Sess',int(sessID))
        Sess = client.get(sesskey)
    except:
        pass
    # if Sess!=None: print"Sess present" ##Debug days
    # print Sess.key.id
    for e in iter_lst:
        # print e.key.id
        try:
            if str(e['subject']) in subjects and str(e['section']) in sections: 
                tmp = {}
                tmp['key'] = e.key.id
                tmp['attempt'] = 0
                tmp['num'] = 0
                tmp['marked'] = 0
                tmp['visited'] = 0
                # print quests[mp[str(e['subject'])]+str(e['section'])] 
                # print e.key.id
                try:
                    # print "find the question in Sess"
                    if Sess.get(str(e.key.id))!=None:
                        res = Sess.get(str(e.key.id))
                        tmp['attempt'] = res.get('attempt',0)
                        tmp['marked'] = res.get('marked',0)
                        tmp['num'] = res.get('number',0)
                        tmp['visited'] = res.get('visited',0)
                except: pass
                quests[mp[str(e['subject'])]+str(e['section'])].append(tmp)
        except: pass
    # print quests
    ##PHASE 4 addtions
    ########===>
    quests["submit"] = Sess.get("submit",False)
    ############
    ##PHASE 5 additions
    ##
    quests["created"] = Sess.get("created",datetime.datetime.now()).isoformat()
    quests["timeLim"] = int(test.get("timeLim",180))
    atm = Sess.get("created").replace(tzinfo=None)
    btm = datetime.datetime.now()
    c = btm-atm
    M = 60*1000
    quests["remains"] = quests["timeLim"]*(M)-(c.total_seconds()*1000)
    return HttpResponse(json.dumps(quests),content_type="application/json")
@login_required(login_url='/login')
def gettime_student(request):
    ##Phase One
    ## The method obtains the data
    ## for the particular testcode
    ## for the student dashboard
    ##Phase Two
    ## From the sessId determine whether it exists
    ## From it find the questions that have been attempted
    ## The student response, attempt,marked or not is returned
    ## the request method should be POST
    # print request
    if request.method!='POST':
        # print 'getdata student data not post'
        return HttpResponse("Get Data Student method is not POST")
    testcode = request.POST['testID']
    sessID = request.POST['sessID']
    testkey = client.key('Test',testcode)
    test = client.get(testkey)
    Sess = {}
    user = User.objects.get(username = request.user)
    username = user.username
    try:
        sesskey = client.key('Test',testcode,'Account',username,'Sess',int(sessID))
        Sess = client.get(sesskey)
    except:
        pass
    submit = Sess.get("submit",False)
    ############
    ##PHASE 5 additions
    ##
    # quests["created"] = Sess.get("created",datetime.datetime.now()).isoformat()
    # quests["timeLim"] = int(test.get("timeLim",180))
    ret = {}
    atm = Sess["created"].replace(tzinfo=None)
    btm = datetime.datetime.now()
    c = btm-atm
    M = 60*1000
    delta = 3*1000
    timeLim = test["timeLim"]
    # remains = quests["timeLim"]*(M)-(c.total_seconds()*1000)
    if timeLim+delta<c.total_seconds():
        Sess["submit"]=True
        client.put(Sess)
        ret["submit"] = True        
    return HttpResponse(json.dumps(ret),content_type="application/json")
@login_required(login_url='/login')
def savedata(request):
    print 'savedata'
    # print request
    if request.method=='POST':
        print request.POST
        data = request.POST['partial']
        doc = request.POST['doc']
        isquest = request.POST['isquest']
        testcode = request.POST['testID']
        questcode = request.POST['questID']
        # testkey = client.key('Test',testcode)
        # test = client.get(testkey)
        questkey = client.key('Test',testcode,'Quest',int(questcode))
        try:
            quest = client.get(questkey)
            print "questsave"
            data = json.loads(data.encode('utf-8'))
            doc = json.loads(doc.encode('utf-8'))
            # print isquest
            # print 'doc',
            # print type(doc)
            # print doc
            if int(isquest)==-1:
                try:
                    quest[str(isquest)] = doc['answer']
                    client.put(quest)
                    return HttpResponse("CS") ##CS stands for correct structure
                except:
                    return HttpResponse("Answer Data Save Failed")
            try:
                # print "try saving quest"
                # print quest[str(isquest)]
                if doc!=None:
                    quest[str(isquest)] = doc['ops']
                else:
                    quest[str(isquest)].extend(data['ops'])
            except:
                # print "exception thrown"
                if doc!=None:
                    quest[str(isquest)] = doc['ops']
                else:
                    quest[str(isquest)] = data['ops']
        except:
            # print "err"
            return HttpResponse("Not OK")
        client.put(quest)
        return HttpResponse("OK")
@login_required(login_url='/login/')
def savedatamarks(request):
    # print request
    if request.method=='POST':
        print request.POST
        testcode = request.POST['testID']
        questcode = request.POST['questID']
        questkey = client.key('Test',testcode,'Quest',int(questcode))

        try:
            quest = client.get(questkey)
            checklst = ["tmarks","nmarks","pmarks","section","subject"]
            for e in checklst:
                try:
                    if request.POST[e]!=None and request.POST[e].isdigit()==True:
                        quest[e] = int(request.POST[e])
                except: pass
            if request.POST["ans"] !=None:
                quest["ans"] = request.POST["ans"]
            if request.POST.get("imgCheck")=='true':
                quest["imgCheck"] = True
            else:
                quest["imgCheck"] = False
            if request.POST.get("imgURL",None)!=None:
                quest["imgURL"] = request.POST["imgURL"]
        except:
            return HttpResponse("Error from the cloud datastore")
        client.put(quest)
        return HttpResponse("OK")
@login_required(login_url='/login/')
def getquest(request):
    print request
    if request.method=='POST':
        # print request.POST['partial']
        testcode = request.POST['testID']
        questcode = request.POST['questID']
        # testkey = client.key('Test',testcode)
        # test = client.get(testkey)
        questkey = client.key('Test',testcode,'Quest',int(questcode))
        ret = {}
        print questkey
        try:
            quest = client.get(questkey)
            print quest
            for i in range(5):
                try:
                    ret['opt'+str(i)] = quest[str(i)]
                except:
                    ret['opt'+str(i)] = []
            try:
                ret['ans'] = quest['ans']
            except:
                ret['ans'] = None
            try:
                ret["nmarks"] = quest["nmarks"]
            except:
                ret["nmarks"] = None
            try:
                ret["tmarks"] = quest["tmarks"]
            except:
                ret["tmarks"] = None
            try:
                ret["pmarks"] = quest["pmarks"]
            except:
                ret["pmarks"] = None
            try:
                ret["subject"] = quest["subject"]
            except:
                ret["subject"] = None
            try:
                ret["section"] = quest["section"]
            except:
                ret["section"] = None 
            try:
                ret["imgCheck"] = quest["imgCheck"]
            except:
                ret["imgCheck"] = False
            try:
                ret["imgURL"] = quest["imgURL"]
            except:
                ret["imgURL"] = None
        except:
            return HttpResponse("err")
        return HttpResponse(json.dumps(ret),content_type='application/json')
@login_required(login_url='/login/')
def getquest_student(request):
    print request
    if request.method=='POST':
        # print request.POST['partial']
        testcode = request.POST['testID']
        questcode = request.POST['questID']
        # testkey = client.key('Test',testcode)
        # test = client.get(testkey)
        questkey = client.key('Test',testcode,'Quest',int(questcode))
        ret = {}
        print questkey
        try:
            quest = client.get(questkey)
            print quest
            for i in range(5):
                try:
                    ret['opt'+str(i)] = quest[str(i)]
                except:
                    ret['opt'+str(i)] = []
            try:
                ret["nmarks"] = quest["nmarks"]
            except:
                ret["nmarks"] = None
            try:
                ret["tmarks"] = quest["tmarks"]
            except:
                ret["tmarks"] = None
            try:
                ret["pmarks"] = quest["pmarks"]
            except:
                ret["pmarks"] = None
            try:
                ret["subject"] = quest["subject"]
            except:
                ret["subject"] = None
            try:
                ret["section"] = quest["section"]
            except:
                ret["section"] = None
            try:
                ret["imgCheck"] = quest["imgCheck"]
            except:
                ret["imgCheck"] = False
            try:
                ret["imgURL"] = quest["imgURL"]
            except:
                ret["imgURL"] = None 
        except:
            return HttpResponse("err")
        return HttpResponse(json.dumps(ret),content_type='application/json')
@login_required(login_url='/login/')
def deletequest(request):
    # print request
    if request.method=='POST':
        testcode = request.POST['testID']
        questcode = request.POST['questID']
        questkey = client.key('Test',testcode,'Quest',int(questcode))
        try:
            client.delete(questkey)
            return HttpResponse("Delete OK")
        except:
            return HttpResponse("Delete fail")
@login_required(login_url='/login/')
def createquest(request):
    # print request
    if request.method=='POST':
        testcode = request.POST['testID']
        incomplete_key = client.key('Test',testcode,'Quest')
        e = datastore.Entity(
            incomplete_key,
            # exclude_from_indexes=['0','1','2','3','4']
            )
        e.update({
            '-1':[],
            '0':[],
            '1':[],
            '2':[],
            '3':[],
            '4':[],
            "nmarks":None,
            "pmarks":None,
            "tmarks":None,
            "ans":None,
            "subject":None,
            "section":None,
            "imgCheck":False,
            "imgURL":None,
            'created': datetime.datetime.now()
        })
        client.put(e)
        complete_id = e.key.id 
        ret = {}
        ret['questID'] = complete_id
        return HttpResponse(json.dumps(ret),content_type='application/json')
