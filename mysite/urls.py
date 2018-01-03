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

from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from polls.jee import testcreator,getdata,savedata,getquest,createquest,deletequest,savedatamarks,getdata_student,getquest_student,gettime_student
from polls.views import index,home,testjson
from polls.student import testdashboard,saveResponse,submitSuccess,result,finalSubmit
from polls.testgen import startpage,dashboard,dashboard01,submit,submitresponse
urlpatterns = [
    url(r'^testjson$',testjson),
    url(r'^$', index),
    url(r'^dashboard/$',dashboard),
    url(r'^dashboard/(\w+)/$',dashboard),
    url(r'^dashboard/question/(\w+)/(\w+)/(\w+)/(\w+)/$',dashboard01),
    url(r'^sampletest/$',startpage),
    url(r'^login/$',auth_views.LoginView.as_view(template_name='login1.html'),name='login'),
    url(r'^logout/$',auth_views.LogoutView.as_view(template_name='logout1.html'),name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/$',home),
    url(r'^submit/(\w+)/$',submit),
    url(r'^submit/response/$',submitresponse),
    url(r'^test/dashboard/$',testdashboard),
    url(r'^test/creator/(\w+)/$',testcreator),
    url(r'^test/creator/$',testcreator),
    # url(r'^test/getdata/(\w+)/$',getdata),
    url(r'^test/getdata/(\w+)/$',getdata),
    url(r'^test/student/getdata/$',getdata_student),
    url(r'^test/savedata/$',savedata),
    url(r'^test/getquest/$',getquest),
    url(r'^test/getquest/student/$',getquest_student),
    url(r'^test/createquest/$',createquest),
    url(r'^test/deletequest/$',deletequest),
    url(r'^test/savedata/marks/$',savedatamarks),
    url(r'^test/save/response/$',saveResponse),
    url(r'^test/submit/result/$',submitSuccess),
    url(r'^result/(\w+)/(\w+)/$',result),
    url(r'^test/final/submit/$',finalSubmit),
    url(r'^test/time/remain/$',gettime_student),
]