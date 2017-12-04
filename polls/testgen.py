# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.http import HttpResponse,HttpRequest
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import Test,MCQ,MCQProxy,TestProxy
subjects = ['MA','PH','CH']
def startpage(request):
    return render(request,'startpage.html',{'testInstructions':'This is a 3 hour test with 90 questions.Keep calm and give your best.'})
@login_required(login_url='/login/')
def dashboard(request,testcode=None):
    if testcode==None:  testcode = int(request.POST['testcode'])
    user=User.objects.get(username=request.user)
    testcode = int(testcode)
    try:
        testparent = Test.objects.get(pk=testcode)
    except:
        return render(request,'home.html',{'error':'Test Code does not exist'})
    try:
        testproxy = user.testproxy_set.get(test=testparent)
        math_mcqlist = testparent.MCQs.filter(subject='MA')
        phy_mcqlist = testparent.MCQs.filter(subject='PH')
        chem_mcqlist = testparent.MCQs.filter(subject='CH')
    except:
        testproxy = user.testproxy_set.create(test=testparent)
        math_mcqlist = testparent.MCQs.filter(subject='MA')
        phy_mcqlist = testparent.MCQs.filter(subject='PH')
        chem_mcqlist = testparent.MCQs.filter(subject='CH')
    i=1
    for mcq in math_mcqlist:
        try:
            mcqanswer = testproxy.MCQProxy.get(MCQparent=mcq,subject = mcq.subject,question_num=i)
        except:
            mcqanswer = testproxy.MCQProxy.create(MCQparent=mcq,subject = mcq.subject,question_num=i)
        i+=1
    i=1
    for mcq in chem_mcqlist:
        try:
            mcqanswer = testproxy.MCQProxy.get(MCQparent=mcq,subject = mcq.subject,question_num=i)
        except:
            mcqanswer = testproxy.MCQProxy.create(MCQparent=mcq,subject = mcq.subject,question_num=i)
        i+=1
    i=1
    for mcq in math_mcqlist:
        try:
            mcqanswer = testproxy.MCQProxy.get(MCQparent=mcq,subject = mcq.subject,question_num=i)
        except:
            mcqanswer = testproxy.MCQProxy.create(MCQparent=mcq,subject = mcq.subject,question_num=i)
        i+=1
    haha = {}
    haha['testcode'] = testparent.pk
    haha['ma'] = []
    i=1
    for mcq in math_mcqlist:
        haha['ma'].append(mcq)
    haha['ch']=[]
    i=1
    for mcq in chem_mcqlist:
        haha['ch'].append(mcq)
    haha['ph']=[]
    i=1
    for mcq in phy_mcqlist:
        haha['ph'].append(mcq) 
    haha['questionSelected']=False
    return render(request,'dashboard.html',haha)
@login_required(login_url='/login/')
def dashboard01(request,sub,testcode,question_number,question_id):
    testcode = int(testcode)
    user = User.objects.get(username=request.user)
    try:
        testparent = Test.objects.get(pk=testcode)
    except:
        return render(request,'home.html',{'error':'Test Code does not exist'})
    haha={}
    # try:
    testproxy = user.testproxy_set.get(test=testparent)
    haha['ma'] = testparent.MCQs.filter(subject='MA')
    haha['ph'] = testparent.MCQs.filter(subject='PH')
    haha['ch'] = testparent.MCQs.filter(subject='CH')
    # except:
    #     return redirect('/dashboard/'+str(testcode)+'/')

    ##The user has testproxy linked with a test and the user
    # print testproxy.MCQProxy.count()
    haha['questionSelected']=True
    haha['testcode']=testcode
    # try:
    haha['question_number']=question_number
    # haha['answer'] = testproxy.MCQProxy.get(subject=sub,question_num=qnum)
    # haha['mcq'] = haha['answer'].MCQparent
    haha['mcq'] = testparent.MCQs.get(pk=question_id)
    haha['answer'] = haha['mcq'].mcqproxy_set.get(testproxy=testproxy)
    # except:
    #     return redirect('/dashboard/'+str(testcode)+'/')
    return render(request,'dashboard.html',haha)
@login_required(login_url='/login/')
def submit(request,testcode):
    testcode = int(testcode)
    user = User.objects.get(username=request.user)
    try:
        testparent = Test.objects.get(pk=testcode)
    except:
        return render(request,'home.html',{'error':'Test Code does not exist'})
    haha={}
    haha['testcode'] = testcode
    # try:
    testproxy = user.testproxy_set.get(test=testparent)
    haha['ma'] = testparent.MCQs.filter(subject='MA')
    haha['ph'] = testparent.MCQs.filter(subject='PH')
    haha['ch'] = testparent.MCQs.filter(subject='CH')
    haha['ma_score']=[]
    haha['ph_score']=[]
    haha['ch_score']=[]
    haha['total_ma_score'] = 0
    haha['total_ph_score'] = 0
    haha['total_ch_score'] = 0
    i=1
    for mcq in haha['ma']:
        stud_ans = mcq.mcqproxy_set.get(testproxy=testproxy)
        if stud_ans.answer=='N':
            # the student has not attempted the question
            stud_ans.marks_obtained = 0
        else:
            if stud_ans.answer==mcq.correctAns.strip().upper():
                stud_ans.marks_obtained = mcq.Marks
            else:
                stud_ans.marks_obtained = mcq.NegativeMarks
        haha['ma_score'].append({'qnum':i,'cans':mcq.correctAns.strip().upper(),'sans':stud_ans.answer,'marks':mcq.Marks,'nmarks':mcq.NegativeMarks,'smarks':stud_ans.NegativeMarks})
        haha['total_ma_score']+=stud_ans.marks_obtained
    i=1
    for mcq in haha['ph']:
        stud_ans = mcq.mcqproxy_set.get(testproxy=testproxy)
        if stud_ans.answer=='N':
            # the student has not attempted the question
            stud_ans.marks_obtained = 0
        else:
            if stud_ans.answer==mcq.correctAns.strip().upper():
                stud_ans.marks_obtained = mcq.Marks
            else:
                stud_ans.marks_obtained = mcq.NegativeMarks
        haha['ph_score'].append({'qnum':i,'cans':mcq.correctAns.strip().upper(),'sans':stud_ans.answer,'marks':mcq.Marks,'nmarks':mcq.NegativeMarks,'smarks':stud_ans.NegativeMarks})
        haha['total_ph_score']+=stud_ans.marks_obtained
    i=1
    for mcq in haha['ch']:
        stud_ans = mcq.mcqproxy_set.get(testproxy=testproxy)
        if stud_ans.answer=='N':
            # the student has not attempted the question
            stud_ans.marks_obtained = 0
        else:
            if stud_ans.answer==mcq.correctAns.strip().upper():
                stud_ans.marks_obtained = mcq.Marks
            else:
                stud_ans.marks_obtained = mcq.NegativeMarks
        haha['ch_score'].append({'qnum':i,'cans':mcq.correctAns.strip().upper(),'sans':stud_ans.answer,'marks':mcq.Marks,'nmarks':mcq.NegativeMarks,'smarks':stud_ans.NegativeMarks})    
        haha['total_ch_score']+=stud_ans.marks_obtained
    haha['total_test_score'] = haha['total_ma_score']+haha['total_ch_score']+haha['total_ph_score']
    return render(request,'scorepage.html',haha)