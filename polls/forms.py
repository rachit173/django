from django import forms
from django.contrib import admin
from .models import Test,MCQ
# admin.site.register(Question)
class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields =['test_code','standard','question_pool']
    question_pool = forms.ModelMultipleChoiceField(
        MCQ.objects.all(),
        required=False,
    )
    def __init__(self, *args, **kwargs):                         
        super(TestForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            print "here in existing test"
            self.initial['question_pool'] = self.instance.MCQs.all()
    def save(self, *args, **kwargs):                             
        instance = super(TestForm, self).save(*args, **kwargs)   
        if instance.pk:
            for mcq in instance.MCQs.all():
                if mcq not in self.cleaned_data['question_pool']:            
                # we remove books which have been unselected 
                    instance.MCQs.remove(mcq)
            for mcq in self.cleaned_data['question_pool']:                  
                if mcq not in instance.MCQs.all():                   
                # we add newly selected books
                    instance.MCQs.add(mcq)      
        return instance