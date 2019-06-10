from django.contrib import admin

# Register your models here.
from deployments.models import *
from django.forms import ModelForm
from django import forms

admin.site.register(Deployment)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields=['category','organization','location','logo','county','town','slug']
        widgets = {
          'category':forms.RadioSelect
        }

class OrganizationAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('organization',)}
    search_fields=['organization']
    form = CategoryForm
admin.site.register(Organization, OrganizationAdmin)

class SupervisorAdmin(admin.ModelAdmin):

#class NewAdmin(admin.ModelAdmin):

    list_display=['supervisor','organization']
    list_filter=['organization']
    
    search_fields=['supervisor__username']
    

class WorkPlanAdmin(admin.ModelAdmin):

#class NewAdmin(admin.ModelAdmin):
    #prepopulated_fields={'slug':('title',)}
    list_display=['pdtp','project_name','date_submitted','start_date','end_date']
    list_filter=['date_submitted']
    
    search_fields=['pdtp','date_submitted']
   
    #fields=(('category','channel'),'image','title','content',)
 

admin.site.register(Supervisor,SupervisorAdmin)

class InternSupervisorAdmin(admin.ModelAdmin):
    search_fields=['pdtp__username']
admin.site.register(InternSupervisor, InternSupervisorAdmin)
admin.site.register(Parametor)
admin.site.register(Evaluation)
admin.site.register(Title)
admin.site.register(WorkPlan, WorkPlanAdmin)
admin.site.register(SupervisorMEParameter)
admin.site.register(InternMEParameter)
admin.site.register(MonitoringAndEvaluation)
admin.site.register(InternMERate)
admin.site.register(SupervisorMERate)
admin.site.register(QuarterlyReport)
admin.site.register(Attendance)
admin.site.register(ReportStatus)
# admin.site.register(Quarter)
admin.site.register(ProjectSection)
admin.site.register(PhaseOrQuarter)
admin.site.register(MonitoringAndEvaluationPhase)
admin.site.register(MonitoringStatus)



