from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from datetime import date
from django.contrib.auth.models import User
from app.models import *
from datetimewidget.widgets import DateTimeWidget
from django.forms import BaseModelFormSet
from tinymce.widgets import TinyMCE
from deployments.models import *
from bootstrap_datepicker.widgets import DatePicker
from bootstrap3_datetime.widgets import DateTimePicker
#DateInput = partial(forms.DateInput, {'class': 'datepicker'})
from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class JobContactForm(forms.ModelForm):
    class Meta:
        model = JobContact
        exclude = ('date', 'pdtp_contacted')
class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
            super(UserForm, self).__init__(*args, **kwargs)
            self.fields['email'].required = True
            self.fields['first_name'].required = True
            self.fields['last_name'].required = True
            self.fields['email'].unique=True
            self.fields['first_name'].label="Other Names"
            self.fields['last_name'].label = "Surname"
    class Meta:
        model=User
        fields=['last_name','first_name','email']

class UForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
            super(UForm, self).__init__(*args, **kwargs)
            self.fields['first_name'].required = True
            self.fields['last_name'].required = True
            self.fields['first_name'].label = "Other Names"
            self.fields['last_name'].label = "Surname"
    class Meta:
        model=User
        fields=['last_name','first_name']

#form for adding a pdtp year by the management or secretariat
class ManagementAddPdtpForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['year']


class AlummniDatabaseForm(forms.ModelForm):
    class Meta:
        model=AlummniDatabase
        fields='__all__'

#Form for updating PDPTP profile
class PDTPProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
            super(PDTPProfileForm, self).__init__(*args, **kwargs)
            self.fields['gender'].required = True
            self.fields['id_no'].required = True
            self.fields['phone_number'].required = True
            self.fields['county_of_birth'].required=True

            
            
    class Meta:
        model=UserProfile
        
        exclude=('user','bio','user_category','year','date_added','date_deactivated',
            'deactivated_by','picture','area_of_specialization',
            'assignedmentor','slug',)
        
        
#Form for Adding and updating PDTP bank Details     
class BankDetailForm(forms.ModelForm):
    class Meta:
        model=BankDetail
        exclude=('user','year',)
class PicForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['picture',]
        
#Form for adding and Updating Mentors Details
class MentorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
            super(MentorForm, self).__init__(*args, **kwargs)
            self.fields['phone_number'].required = True
    class Meta:
        model=UserProfile
        fields=['phone_number',]
        
        
class UserActivateForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['is_active']

class ManProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
            super(ManProfileForm, self).__init__(*args, **kwargs)
            self.fields['gender'].required = True
            self.fields['id_no'].required = True
            self.fields['phone_number'].required = True
    class Meta:
        model=UserProfile
        fields=('gender','id_no','phone_number',)


class MentorshipApplicationForm(forms.ModelForm):
    class Meta:
        model = MentorshipApplication
        fields = '__all__'
class PDTPAssignmentForm(forms.ModelForm):
 
    pdtp =forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=UserProfile.objects.filter(user_category="PDTP"))
    
    class Meta:
        model=Assignment
        fields=('pdtp',)
        
        

class ExitRequestForm(forms.ModelForm):
    class Meta:
        model=PDTPExitRequest
        fields=['exit_request',]
        
class PDTPClearanceForm(forms.ModelForm):
    class Meta:
        model=ExitR
        fields=['reason_for_leaving',]
        
class PClearanceForm(forms.ModelForm):
    class Meta:
        model=PDTPExitRequest
        fields=['supervisor_comment',]
        
class DebriefForm(forms.ModelForm):
    class Meta:
        model=PDTPExitRequest
        fields=['debrief_question',]
        

class BioForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['bio',]
    class Media:
        js = ('/media/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '',)
class AcademicForm(forms.ModelForm):
    class Meta:
        model=AcademicDetail
        fields=['academic_level','course_name','higher_institution_attended','year','grade',]

class UpdateRequestForm(forms.ModelForm):
    class Meta:
        model=UpdateRequest
        fields=['message',]

class EventForm(forms.ModelForm):
    dateTimeOptions = {
        'format': 'dd/mm/yyyy HH:ii P',
        'autoclose': True,
        'showMeridian' : True
     }
    class Meta:
        model =Event 
        fields=['attendees','event','start_date','end_date','venue','details',]
        widgets = {
            'start_date': DateTimeWidget(attrs = {'id':'id_start_date'}, bootstrap_version=3, usel10n=True),
            'end_date': DateTimeWidget(attrs = {'id':'id_end_date'}, bootstrap_version=3, usel10n=True)
}

class EventCancelForm(forms.ModelForm):
    class Meta:
        model =Event 
        fields=['reason',]
class IssueForm(forms.ModelForm):
    class Meta:
        model =Issue
        exclude=('pdtp','date','solved',)

class IssueStatusForm(forms.ModelForm):
    class Meta:
        model =IssueStatus
        fields=['status','comment',]
        

        

class WorkPlanForm(forms.ModelForm):
    #assignement = forms.CharField(widget=TinyMCE(attrs={'cols': 2, 'rows': 1}))
    #project_name = forms.CharField(widget=TinyMCE(attrs={'cols': 2, 'rows': 1}))
    #expected_impact = forms.CharField(widget=TinyMCE(attrs={'cols': 2, 'rows': 1}))
    #task = forms.CharField(widget=TinyMCE(attrs={'cols': 2, 'rows': 1}))
    #resources = forms.CharField(widget=TinyMCE(attrs={'cols': 2, 'rows': 1}))
    #status = forms.CharField(widget=TinyMCE(attrs={'cols': 2, 'rows': 1}))
    start_date = forms.DateField(widget=DateInput(),help_text="MM/DD/YYYY")
    end_date = forms.DateField(widget=DateInput(),help_text="MM/DD/YYYY")
    #start_date = forms.DateField(widget=DatePicker(options={"format": "YYYY-MM-DD"}))
    #end_date = forms.DateField(widget=DatePicker(options={"format": "YYYY-MM-DD"}))
    #start_date = forms.DateField(
          #widget=DateTimePicker(options={"format": "YYYY-MM-DD"}))
    #end_date = forms.DateField(
          #widget=DateTimePicker(options={"format": "YYYY-MM-DD"}))

    def __init__(self, *args, **kwargs):
        super(WorkPlanForm, self).__init__(*args, **kwargs)
        self.fields['project_name'].required = True
        self.fields['task'].required = True
        self.fields['resources'].required = True
        self.fields['outputs'].required = True
        self.fields['expected_impact'].required = True
        self.fields['start_date'].required = True
        self.fields['end_date'].required = True
        self.fields['status'].required = True
        self.empty_permitted = False

    class Meta:
        model=WorkPlan
        fields=['project_name','task','resources',
        'outputs','expected_impact','start_date','end_date','status',]
        
class PlanForm(forms.ModelForm):
    supervisor_comment = forms.CharField(widget=TinyMCE(attrs={'cols': 4, 'rows': 2}))

    class Meta:
        model=WorkPlan
        fields=['approved_by_supervisor','supervisor_comment',]
        
class ProjectForm(forms.ModelForm):
    class Meta:
        model= Project
        fields=['project_name','project_date','project_Edate','project_description','link',]


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields=['skill_type','skill_level','skill','detail',]

class RefereeForm(forms.ModelForm):
    class Meta:
        model = Referee
        fields = ['name','company','position','phone_number','email','country','town',]

#Training
class TrainingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TrainingForm, self).__init__(*args, **kwargs)
        self.empty_permitted = False

    class Meta:
        model = TrainingCourse
        exclude = ('secretariat',)


class TrainingApplicationUpdateForm(forms.ModelForm):
        
    class Meta:
        model=TrainingApplication
        exclude = ('secretariat',)
       

class ApplicationUpdateForm(forms.ModelForm):
    class Meta:
        model = TrainingApplication
        fields = ['status','cert_no','attended_training',]
        
class InternTrainingApplicationForm(forms.ModelForm):
    class Meta:
        model = TrainingApplication
        exclude = ('pdtp','course','cert_no','year','category','institution','status','attended_training',)
        
class TrainFeedbackForm(forms.ModelForm):
    class Meta:
        model= TrainingFeedback
        fields = ['feedback',]

class SignupForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = False
        

    def signup(self, request, user):
        user.email =self.cleaned_data['email']
        user.username=self.cleaned_data['email']

        year = PdtpYear.objects.get(year=2018)
        user.save()
        userprofile = UserProfile(user=user,
                                user_category="PDTP",year=year)
        userprofile.save()
        try:
            user=UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            user.delete()
        #photo.save()
        #CV.save()
class PdtpMentorshipReportForm(forms.ModelForm):
    
    def __init__(self, user, *args, **kwargs):
        super(PdtpMentorshipReportForm, self).__init__(*args, **kwargs)
        self.fields['report'].required = True
        if user:
           
           self.fields['parametors'].queryset = Meeting.objects.filter(mentee=user)
    class Meta:
        model=PDTPMentorshipReport
        fields=['parametors', 'report',]

        # parametors =forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
        #  queryset=Meeting.objects.filter(mentee=user)) 

    
# class MentorParameterForm(forms.ModelForm):
#     class Meta:
#         model = MentorParameter
#         fileds = ['parameter',]

class MeetingForm(forms.ModelForm):
    dateTimeOptions = {
        'format': 'dd/mm/yyyy HH:ii P',
        'autoclose': True,
        'showMeridian' : True
     }
    class Meta:
        model = Meeting
        fields = ['agenda','meeting_date','venue','note',]
        widgets = {
            'meeting_date': DateTimeWidget(attrs = {'id':'id_meeting_date'}, bootstrap_version=3, usel10n=True),
            
            }

class MeetingConfirmForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['confirm','confirm_text',]
class MeetingReportForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['report',]
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['feedback',]

class CommentForm(forms.ModelForm):
    def __init__(self, mentee, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['comment'].required= True
        if mentee:
            self.fields['parametor'].queryset = Meeting.objects.filter(mentee=mentee)
            self.fields['mentorship_report'].queryset = PDTPMentorshipReport.objects.filter(pdtp=mentee)
    class Meta:
        model = ReportComment
        fields = ['parametor', 'mentorship_report','comment',]


class InnovationSubmissionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InnovationSubmissionForm, self).__init__(*args, **kwargs)
        self.fields['innovation_name'].required = True
        self.fields['industry'].required = True
        self.fields['innovators_roles'].required = True
        self.fields['need'].required = True
        self.fields['option'].required = True
        self.fields['market_potential'].required = True
        self.fields['business_model'].required = True
        self.fields['feasiblity'].required = True
        self.fields['relevance'].required = True
        self.fields['how_it_works'].required = True
        self.fields['relevant_information'].required = True
        self.fields['bibliography'].required = True
        self.fields['appendices'].required = True
    

    class Meta:
        model=InnovationSubmission
        exclude=('date_submitted', 'pdtp',)


# class LeaveApplicationForm(forms.ModelForm):
#     class Meta:
#         model = Leave
#         fields =('start_date','end_date')

class LeaveApplicationForm(forms.ModelForm):
    start_date = forms.DateField(widget=DateInput(),help_text="MM/DD/YYYY")
    end_date = forms.DateField(widget=DateInput(),help_text="MM/DD/YYYY")

    def __init__(self, *args, **kwargs):
        super(LeaveApplicationForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].required = True
        self.fields['end_date'].required = True
        self.fields['start_date'].label = "Leave Start Date"
        self.fields['end_date'].label = "Leave End Date"
        self.empty_permitted = False

    class Meta:
        model=Leave
        fields=['start_date','end_date','leave_type','leave_details','attachment']

class LeaveApplicationSupervisor(forms.ModelForm):
    class Meta:
        model=Leave
        fields=['supervisor_recommmended_days','duties_delagated_to','supervisor_comment',]


class LeaveApplicationSecretariat(forms.ModelForm):
    class Meta:
        model=Leave
        fields=['recommended','secretariat_comment','internship_contract_date',]

class SendMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('sender','recipient','sent','timestamp',)
        



class BroadcastForm(forms.ModelForm):
    class Meta:
        model = Broadcast
        fields = ('recipient','year','subject','message')
    

class InternalApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApps
        fields = ('application_category',)

class LaptopForm(forms.ModelForm):
    class Meta:
        model = Laptop
        exclude = ('created_by',)

class LaptopApplicantsForm(forms.ModelForm):
    class Meta:
        model = LaptopOrder
        fields = '__all__'



class PartnerApplyForm(forms.ModelForm):
    class Meta:
        model = PartnerApply
        exclude = ('handled','partnership')