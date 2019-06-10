from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from datetime import date
from django.contrib.auth.models import User
from performance.models import *
from tinymce.widgets import TinyMCE
from multiupload.fields import MultiFileField
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory


        
class MinistryReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MinistryReportForm, self).__init__(*args, **kwargs)
        self.fields['attendance'].label = "Internship attendance"
        self.fields['meeting'].label ="Quarterly Meetings attended"
        # self.fields['report'].label ="Quarterly Reports submitted? if not please attach them"
    class Meta:
        model = MinistryReport
        fields=['attendance','meeting',]
        


class UploadForm(forms.Form):
    attachments = MultiFileField(min_num=1, max_num=3)
    def __init__(self, *args, **kwargs):
        super(UploadForm, self).__init__(*args, **kwargs)
        self.fields['attachments'].label = "Attach Quarterly Reports(max 4 Files)"
        self.fields['attachments'].required = False


class BasicForm(forms.ModelForm):
    class Meta:
        model = BasicEvaluation
        fields = '__all__'
    def __init__ (self, *args, **kwargs):
        super(BasicForm, self).__init__(*args, **kwargs)
        self.fields["work"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["work"].help_text = ""
        self.fields["other"].placeholder = ""
        self.fields["work"].queryset = Work.objects.all()
        self.fields["education"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["education"].help_text = ""
        self.fields["education"].queryset = Level.objects.all()
        
        

class WorkAssignmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WorkAssignmentForm, self).__init__(*args, **kwargs)
        self.fields['daily_activity'].label = "Have you been completing your daily tasks?"
        self.empty_permitted = False
    class Meta:
        model = WorkAssignment
        fields=['daily_activity',]

class EvidenceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EvidenceForm, self).__init__(*args, **kwargs)
        self.fields['project_name'].label = "Task Performed(Max 200 Char)"
        self.fields['description'].label = "Task Description (Max 400 Char)"
        self.fields['link'].label = "Task Link(Optional)"
        self.empty_permitted = False
    class Meta:
        model = WorkAssignmentEvidence
        fields=['project_name','description','link',] 
        widgets = {
          'description': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }
        
class AdditionalActivityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AdditionalActivityForm, self).__init__(*args, **kwargs)
        self.fields['project_name'].label = "Project Name(Max 200 Char)"
        self.fields['task'].label = "Role(Max 200 Char)"
        self.fields['description'].label = "Task Description (Max 400 Char)"
        self.fields['link'].label = "Task Link(Optional)"
        self.empty_permitted = False
    class Meta:
        model = AdditionalActivity
        fields=['project_name','task','description','link',] 
        widgets = {
          'description': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }
        
class TransformationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TransformationForm, self).__init__(*args, **kwargs)
        self.fields['ministry'].label = "Ministry(Max 200 Char)"
        self.fields['project_name'].label = "Project Name(Max 200 Char)"
        self.fields['task'].label = "Role/Task(Max 200 Char)"
        self.fields['description'].label = "Task Description (Max 400 Char)"
        self.fields['link'].label = "Task Link(Optional)"
        self.empty_permitted = False
    class Meta:
        model = Transformation
        fields=['ministry','project_name','task','description','link',] 
        widgets = {
          'description': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }
        
class PrivateSectorAttendanceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PrivateSectorAttendanceForm, self).__init__(*args, **kwargs)
        self.fields['attendance'].label = "Did you complete the 2 months private sector attachment"
        self.fields['attachment'].label = "Attach Private Sector Exit Note(Optional)"
        
    class Meta:
        model = PrivateSectorAttendance
        fields=['attendance','attachment',] 
        
class PrivateOnJobTrainingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PrivateOnJobTrainingForm, self).__init__(*args, **kwargs)
        self.fields['subject'].label = "Course Title"
        self.fields['description'].label = "Give brief details(max 400chr)"
        self.empty_permitted = False
        
    class Meta:
        model = PrivateOnJobTraining
        fields=['subject','description',]
        widgets = {
          'description': forms.Textarea(attrs={'rows':4, 'cols':15}),
        } 
        
class PrivateTrainingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PrivateTrainingForm, self).__init__(*args, **kwargs)
        self.fields['subject'].label = "Course Title"
        self.fields['description'].label = "Give brief details(max 400chr)"
        self.fields['attachment'].label = "Attach certificate (Optional)"
        self.empty_permitted = False
        
    class Meta:
        model = PrivateTraining
        fields=['subject','description', 'attachment',]
        widgets = {
          'description': forms.Textarea(attrs={'rows':4, 'cols':15}),
        } 

class InnovationsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InnovationsForm, self).__init__(*args, **kwargs)
        self.fields['initiative'].label = "Initiative(2 marks)"
        self.fields['presentation'].label = "Presentation (3 marks)"
        self.fields['evaluation'].label = "First Evaluation (5 marks)"
        self.fields['final'].label = "Final Evaluation (5 marks)"
        self.empty_permitted = False
        
    class Meta:
        model = InnovationEvaluation
        fields=['initiative','presentation', 'evaluation','final']
        
class MentorMeetingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MentorMeetingForm, self).__init__(*args, **kwargs)
        self.fields['meeting'].label = "How many times did your meet?"
        self.empty_permitted = False
        
    class Meta:
        model = MentorMeeting
        fields=['meeting',]
        

class SupervisorCommentForm(forms.ModelForm):
    class Meta:
        model = SupervisorComment
        fields=['comment',]
        widgets = {
          'comment': forms.Textarea(attrs={'rows':4, 'cols':15}),
        } 
class SupervisorApprovalCommentForm(forms.ModelForm):
    class Meta:
        model = SupervisorApprovalComment
        fields=['award_marks','comment',]
        widgets = {
          'comment': forms.Textarea(attrs={'rows':4, 'cols':15}),
        } 
class BuddyCommentForm(forms.ModelForm):
    class Meta:
        model = BuddyComment
        fields=['comment',]
        widgets = {
          'comment': forms.Textarea(attrs={'rows':4, 'cols':15}),
        } 
class BuddyApprovalCommentForm(forms.ModelForm):
    class Meta:
        model = BuddyApprovalComment
        fields=['award_marks','comment',]
        widgets = {
          'comment': forms.Textarea(attrs={'rows':4, 'cols':15}),
        } 

class MentorCommentForm(forms.ModelForm):
    class Meta:
        model = MentorComment
        fields=['comment',]
        widgets = {
          'comment': forms.Textarea(attrs={'rows':4, 'cols':15}),
        } 


class MentorshipInternReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MentorshipInternReportForm, self).__init__(*args, **kwargs)
        self.fields['awareness_description'].label = False
        self.fields['awareness_impact'].label = False
        self.fields['goal_description'].label = False
        self.fields['goal_impact'].label = False
        self.fields['adaptability_description'].label = False
        self.fields['adaptability_impact'].label = False
        self.fields['confidence_impact'].label = False
        self.fields['confidence_description'].label = False
        self.fields['presentation_description'].label = False
        self.fields['presentation_impact'].label = False
        
    class Meta:
        model = MentorshipInternReport
        fields=['awareness_description','awareness_impact','goal_description','goal_impact',
        'adaptability_description','adaptability_impact','confidence_description',
        'confidence_impact','presentation_description','presentation_impact',]
        widgets = {
          'awareness_description': forms.Textarea(attrs={'rows':3, 'cols':10}),
          'awareness_impact': forms.Textarea(attrs={'rows':3, 'cols':10}),
          'goal_description': forms.Textarea(attrs={'rows':3, 'cols':10}),
          'goal_impact': forms.Textarea(attrs={'rows':3, 'cols':10}),
          'adaptability_description': forms.Textarea(attrs={'rows':3, 'cols':10}),
          'adaptability_impact': forms.Textarea(attrs={'rows':3, 'cols':10}),
          'confidence_description': forms.Textarea(attrs={'rows':3, 'cols':10}),
          'confidence_impact': forms.Textarea(attrs={'rows':3, 'cols':10}),
          'presentation_description': forms.Textarea(attrs={'rows':3, 'cols':10}),
          'presentation_impact': forms.Textarea(attrs={'rows':3, 'cols':10}),

        } 

class MentorshipReportForm(forms.ModelForm):
    class Meta:
        model = MentorshipReport
        exclude=['approved', 'approved_by','pdtp']
     


class PrivateProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PrivateProjectForm, self).__init__(*args, **kwargs)
        self.fields['project_name'].label = "Task Performed(Max 200 Char)"
        self.fields['description'].label = "Task Description (Max 400 Char)"
        self.fields['link'].label = "Task Link(Optional)"
        self.empty_permitted = False
    class Meta:
        model =PrivateProject
        fields=['project_name','description','link',] 
        widgets = {
          'description': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }