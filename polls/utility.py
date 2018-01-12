from google.cloud import datastore
from django.contrib.auth.models import User
def con(ans,section):
    # if section not in [1,2,3]: return None
    num=[]
    ans = ans.lower()
    if section==1:
        num = []
        if 'a' in ans: num.append('a')
        elif 'b' in ans: num.append('b')
        elif 'c' in ans: num.append('c')
        elif 'd' in ans: num.append('d')
        return sorted(num)
    elif section==2:
        print "#ans",ans
        num = []
        if 'a' in ans: num.append('a')
        if 'b' in ans: num.append('b')
        if 'c' in ans: num.append('c')
        if 'd' in ans: num.append('d')
        return sorted(num)
    elif section==3:
        num = []
        try:
            num.append(int(ans))
        except:
            pass    
        return sorted(num)
    else:
        return None    

def decon(num,section):
    if section==1:
        ret = []
        for i in range(4):
            if num%2==1:
                ret.append(chr(ord('a')+i))
                return ret
            num/=2
    elif section==2:
        ret = []
        for i in range(4):
            if num%2==1:
                ret.append(chr(ord('a')+i))
            num/=2
        return sorted(ret)
    elif section==3:
        ret = [num]
        return sorted(ret)
    else:
        return None

def calc(res,ans,tot,neg,par,section):
    if res==None: return 0
    if section==2: print res,ans
    if ans==None: 
        print "Bonus"
        return tot
    try:
        tot = int(tot)
    except:
        tot = 0
    try:
        neg = -1*abs(int(neg))
    except:
        neg = 0
    try:
        par = int(par)
    except:
        par = 0
    if section==1:
        if res[0]==ans[0]: return tot
        else: return neg
    elif section==2:
        ret=0
        if res==ans: return tot
        else:
            for e in res:
                if e not in ans: return neg
                else: ret+=par
            return ret
    elif section==3:
        if res[0]==ans[0]: return tot
        else: return neg
    print "Reached the end of conditional execution in\
            calc() method,hence return 0"
    return 0

def resultRowDict(Sess,lst_query):
    ###
    #   user is the object which contains username and maybe the batch number 
    #   Sess is the session of the user which contains the answers given by the user 
    #   lst_query contains the lst of questions in the test
    ###
    user = None
    username = Sess['user']
    try:
        user = User.objects.get(username = username)
    except:
        print "This sucks"
        return None
    if user==None: return None
    try:
        username = user.username
    except:
        username = None
    batch = None
    try:
        batch = user.batch
    except:
        batch = None
    ret = {}
    ret['name'] = None
    try:
        ret['name'] = user.first_name+" "+user.last_name
    except:
        ret['none'] = None
    ret['roll_number'] = username
    ret['batch'] = batch
    ret['ma'] = 0
    ret['ph'] = 0
    ret['ch'] = 0
    sections = ['ma1','ma2','ma3','ph1','ph2','ph3','ch1','ch2','ch3']
    mp = {}
    mp['1'] = 'ma'
    mp['2'] = 'ph'
    mp['3'] = 'ch'
    ##iterate through the elements of 
    ##lst_query
    for q in lst_query:
        ##temporary dictionary to
        ##store the objects 
        ##
        ##convert the numerical quest ID 
        ##to string stored in quest_id
        quest_id = str(q.key.id)
        ##section of the question
        quest_section = q.get('section')
        ##subject of the question
        quest_subject = q.get('subject')
        ##
        complete_section = None
        # print mp.get(str(quest_subject)) + str(quest_section)
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
        ##Check is the candidate even saved the question once
        if Sess.get(quest_id)==None:
            ##The question has not been attempted
            ##
            continue
        correctAns = None
        responseAns = None
        resp = Sess[quest_id]
        try:
            correctAns = con(q.get('ans'),int(quest_section))
        except:
            print "con() method could not convert the ans to list representation"
        if correctAns ==None: continue
        if str(resp.get('attempt'))!="1":
            #not attempted the question 
            continue
        else:
            try:
                responseAns = decon(int(resp.get('number')),int(quest_section))
            except:
                responseAns = None
            ob = calc(responseAns,correctAns,tot,neg,par,int(quest_section))
            try:
                ret[mp[str(quest_subject)]] += ob
            except:
                pass  
    return convertToRow(ret)
def convertToRow(haha):
    if haha==None:
        return None
    return [haha.get('name',None),haha.get('roll_number',None),haha.get('batch',None),haha.get('ma',None),haha.get('ph',None),haha.get('ch',None)]