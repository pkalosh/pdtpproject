from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from datetime import date
from django.contrib.auth.models import User
from app.models import *
from deployments.models import *
from tinymce.widgets import TinyMCE


        
class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields=['slug','category','organization','location','logo','county','town',]
        widgets = {
          'category':forms.RadioSelect
        }
class ContactPersonForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields=['phone_number','alternate_email','alternate_cell',]

class InternRequestForm(forms.ModelForm):
    class Meta:
        model = InterRequest
        exclude = ('date_submitted', 'handled')

class OrganizationUpdateForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields=['category','organization','location','logo','county','town',
                ]

        widgets = {
          'category':forms.RadioSelect
        }
        
class ReportStatusForm(forms.ModelForm):
    class Meta:
        model = QuarterlyReport
        fields = '__all__'


class SupervisorForm(forms.ModelForm):
    class Meta:
        model=Supervisor
        fields=['honors','is_mentor','is_supervisor','position', 'title','is_contact_person','mentor_availability']
class OrgSupervisorForm(forms.ModelForm):
    class Meta:
        model=Supervisor
        fields=['honors','position', 'title','is_contact_person',]
        
class SupervisorMentorForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['phone_number',]

        
class DeploymentForm(forms.ModelForm):
    #pdtp = forms.ModelMultipleChoiceField(queryset=UserProfile.get_pdtps(), widget=forms.SelectMultiple)
    def __init__(self, *args, **kwargs):
            super(DeploymentForm, self).__init__(*args, **kwargs)
            self.fields['reporting_details'].required = True
    class Meta:
        model=Deployment
        fields=['reporting_details',]

class InterviewForm(forms.ModelForm):
    #pdtp = forms.ModelMultipleChoiceField(queryset=UserProfile.get_pdtps(), widget=forms.SelectMultiple)
    def __init__(self, *args, **kwargs):
            super(InterviewForm, self).__init__(*args, **kwargs)
            self.fields['interview_instructions'].required = True
    class Meta:
        model=Deployment
        fields=['interview_instructions',]
class PhaseForm(forms.ModelForm):
    class Meta:
        model = MonitoringAndEvaluationPhase
        fields = ['phase','status','year',]
        
class InternMEForm(forms.ModelForm):
    
    class Meta:
        model = MonitoringAndEvaluation
        exclude = ('pdtp','supervisor','year','phase','date_submitted_by_intern','date_supervisor_submitted','intern_strength',
            'areas_improvement',)
        
class SupervisorMEForm(forms.ModelForm):
    class Meta:
        model = MonitoringAndEvaluation
        fields = ['intern_strength','areas_improvement',]

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['days_attended',]

class QuarterlyReportForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #    super(QuarterlyReportForm, self).__init__(*args, **kwargs)
    #    self.fields['year'].readonly = True
    class Meta:
        model = QuarterlyReport
        exclude = ('pdtp','supervisor','approved','comments','secretariat','year','quater')


class PhaseOrQuarterForm(forms.ModelForm):
    class Meta:
        model = PhaseOrQuarter
        fields = ['quater', 'status',]
class SupervisorQuarterlyCommentForm(forms.ModelForm):
    class Meta:
        model = QuarterlyReport
        fields = ['comments',]

