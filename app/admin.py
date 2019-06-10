from django.contrib import admin
from app.models import *
from django import forms
admin.site.register(AlummniDatabase)
class UserProfileAdmin(admin.ModelAdmin):
	search_fields=['user__username','user_category']
	prepopulated_fields={'slug':('user',)}
	list_display=['user','user_category']
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(County)
class PdtpYearAdmin(admin.ModelAdmin):
	prepopulated_fields={'slug':('year',)}
admin.site.register(PdtpYear,PdtpYearAdmin)
admin.site.register(BankDetail)
admin.site.register(JobContact)
class MentorMenteeAdmin(admin.ModelAdmin):
	search_fields=['mentee__username']
admin.site.register(MentorMenteeMapping,MentorMenteeAdmin)
admin.site.register(PDTPExitRequest)
admin.site.register(AcademicDetail)
admin.site.register(PDTPCV)
admin.site.register(UpdateRequest)
admin.site.register(Event)

admin.site.register(Issue)
admin.site.register(IssueStatus)
admin.site.register(SkillType)
admin.site.register(SkillLevel)

admin.site.register(Project)
admin.site.register(Skill)
admin.site.register(InnovationTeam)

class RefereeAdmin(admin.ModelAdmin):
	search_fields=['user__username']
admin.site.register(Referee,RefereeAdmin)

#Trainings and certifications
admin.site.register(TrainingInstitution)
admin.site.register(TrainingCourseStatus)
admin.site.register(TrainingCourse)
admin.site.register(TrainingStatus)
admin.site.register(TrainingCert)
class TrainingApplicationAdmin(admin.ModelAdmin):
	search_fields=['pdtp__username']
admin.site.register(TrainingApplication, TrainingApplicationAdmin)




admin.site.register(TrainingMode)
admin.site.register(TrainingCategory)
admin.site.register(MustChangePassword)
class SpecializationAdmin(admin.ModelAdmin):
	prepopulated_fields={'slug':('speciality',)}
admin.site.register(Specialization, SpecializationAdmin)

admin.site.register(PDTPMentorshipReport)
admin.site.register(InnovationSubmission)
admin.site.register(ReportComment)
admin.site.register(Meeting)

admin.site.register(ExitParameter)
admin.site.register(ExitRateParameter)

admin.site.register(ExitSingleQuestionParameter)


admin.site.register(ExitSubmitted)
admin.site.register(ExitRateSubmited)
admin.site.register(ExitSingleSubmitted)
admin.site.register(ExitR)
admin.site.register(LeaveType)
admin.site.register(Leave)

#Messaging
admin.site.register(Message)
admin.site.register(Broadcast)
admin.site.register(InnovationEvaluationParameter)

admin.site.register(InnovationEvaluationData)

#partner application form
admin.site.register(PartnerApplication)
admin.site.register(MentorshipApplication)

admin.site.register(JobApps)
admin.site.register(ApplicationCategory)

admin.site.register(Laptop)
admin.site.register(LaptopOrder)
admin.site.register(PaymentHistory)
admin.site.register(InnovationEvaluationPerParam)

admin.site.register(PartnerCohort)
admin.site.register(Partner)

class SuccessStoryAdmin(admin.ModelAdmin):
	prepopulated_fields={'slug':('name',)}
admin.site.register(SuccessStory, SuccessStoryAdmin)
admin.site.register(PartnerApply)
admin.site.register(InterRequest)