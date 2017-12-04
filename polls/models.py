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

from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class MCQ(models.Model):
    MATHS = 'MA'
    CHEMISTRY = 'CH'
    PHYSICS = 'PH'
    GENERAL = 'GE'
    SUBJECT_CHOICES = (
        (MATHS, 'Mathematics'),
        (CHEMISTRY, 'Chemistry'),
        (PHYSICS, 'Physics'),
        (GENERAL, 'General Studies'),
    )
    subject = models.CharField(max_length=2,choices=SUBJECT_CHOICES,default=MATHS,)
    question_code = models.CharField(max_length=16,blank=True)
    question_text = models.CharField(max_length=10000,blank=True)
    optionA = models.CharField(max_length=500,blank=True)
    optionB = models.CharField(max_length=500,blank=True)
    optionC = models.CharField(max_length=500,blank=True)
    optionD = models.CharField(max_length=500,blank=True)
    optionE = models.CharField(max_length=500,blank=True)
    correctAns = models.CharField(max_length=500,blank=True)
    Marks = models.IntegerField()
    NegativeMarks = models.IntegerField()
    PartialMarking  = models.IntegerField()
    MarkingSchemeExplanation = models.CharField(max_length=1000,default='No specifc instruction')
    question_text_image = models.ImageField(upload_to="photos",blank=True,default='no image')
    question_diagram = models.ImageField(upload_to="photos",blank=True,default='no image')
    optionA_image = models.ImageField(upload_to="photos",blank=True,default='no image')
    optionB_image = models.ImageField(upload_to="photos",blank=True,default='no image')
    optionC_image = models.ImageField(upload_to="photos",blank=True,default='no image')
    optionD_image = models.ImageField(upload_to="photos",blank=True,default='no image')
    optionE_image = models.ImageField(upload_to="photos",blank=True,default='no image')
    # test_parent = models.ForeignKey(Test)

class Test(models.Model):
    test_code = models.CharField(max_length=32,blank=True)
    standard = models.IntegerField(default=12)
    batch = models.CharField(max_length=16,default="general")
    updated_at = models.DateField(auto_now=True,null=True)
    description = models.CharField(max_length=100,blank=True)
    teacher_name = models.CharField(max_length=50,blank=True)
    MCQs = models.ManyToManyField(MCQ,null=True)

class MCQProxy(models.Model):
    MCQparent = models.ForeignKey(MCQ)
    MATHS = 'MA'
    CHEMISTRY = 'CH'
    PHYSICS = 'PH'
    GENERAL = 'GE'
    SUBJECT_CHOICES = (
        (MATHS, 'Mathematics'),
        (CHEMISTRY, 'Chemistry'),
        (PHYSICS, 'Physics'),
        (GENERAL, 'General Studies'),
    )
    question_num = models.IntegerField(default=1)
    subject = models.CharField(max_length=2,choices=SUBJECT_CHOICES,default=MATHS,)
    attempted = models.BooleanField(default=False)
    OPTION_CHOICES = (
        ('A','A'),
        ('B','B'),
        ('C','C'),
        ('D','D'),
        ('E','E'),
    )
    answer = models.CharField(max_length=1,choices=OPTION_CHOICES,default='N')
    mark_obtained = models.IntegerField(default=0)

class TestProxy(models.Model):
    user=models.ForeignKey(User)
    test=models.ForeignKey(Test)
    MCQProxy = models.ManyToManyField(MCQProxy)
    start_at = models.TimeField(null=True)
    updated_at = models.TimeField(auto_now = True)
