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
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from student import studenthome
import json
import datetime
from polls.ndbmodels import *
def index(request):
    return redirect('/login/')
@login_required()
def home(request):
        user = User.objects.get(username=request.user)
        if user.is_staff:
            return render(request,'staffhome.html')
        else:
            return studenthome(request)
def login_redirect(request):
    return redirect('/login/')
def testjson(request):
    json_dic={}
    json_dic['question']='what to do?'
    json_dic['answer'] = 'ask google'
    sandy = Account(username='rachit',userid=123,email='r@t.com')
    sandy_key = sandy.put()
    print sandy_key
    return HttpResponse(json.dumps(json_dic),content_type='application/json')
def instr(request):
    return HttpResponse("OK")