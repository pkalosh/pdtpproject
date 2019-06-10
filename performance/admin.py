from django.contrib import admin

from performance.models import *
admin.site.register(AttendanceGroup)
admin.site.register(MeetingGroup)
admin.site.register(QuarterlyReportGroup)

admin.site.register(DailyRoutineGroup)

class MinistryReportAdmin(admin.ModelAdmin):
    search_fields=['pdtp__username']

admin.site.register(MinistryReport,MinistryReportAdmin)

class MentorshipInternReportAdmin(admin.ModelAdmin):
    search_fields=['pdtp__username']

admin.site.register(MentorshipInternReport,MentorshipInternReportAdmin)

class WorkAssignmentAdmin(admin.ModelAdmin):
    search_fields=['pdtp__username']
admin.site.register(WorkAssignment,WorkAssignmentAdmin)

class WorkAssignmentEvidenceAdmin(admin.ModelAdmin):
    search_fields=['pdtp__username']
admin.site.register(WorkAssignmentEvidence,WorkAssignmentEvidenceAdmin)

class AdditionalActivityAdmin(admin.ModelAdmin):
    search_fields=['pdtp__username']
admin.site.register(AdditionalActivity,AdditionalActivityAdmin)


class TransformationAdmin(admin.ModelAdmin):
    search_fields=['pdtp__username']
admin.site.register(Transformation,TransformationAdmin)

class ReportAttachmentAdmin(admin.ModelAdmin):
    search_fields=['pdtp__username']
admin.site.register(ReportAttachment,ReportAttachmentAdmin)

admin.site.register(PrivateSectorAttendaceGroup)

class PrivateSectorAttendanceAdmin(admin.ModelAdmin):
    search_fields=['pdtp__username']
admin.site.register(PrivateSectorAttendance,PrivateSectorAttendanceAdmin)

class PrivateOnJobTrainingAdmin(admin.ModelAdmin):
    search_fields=['pdtp__username']
admin.site.register(PrivateOnJobTraining,PrivateOnJobTrainingAdmin)

class PrivateTrainingAdmin(admin.ModelAdmin):
    search_fields=['pdtp__username']
admin.site.register(PrivateTraining,PrivateTrainingAdmin)

#Private Sector Supervisor Evaluation
admin.site.register(Parameter)
admin.site.register(MentorParameter)

class PrivateSupervisorEvaluationAdmin(admin.ModelAdmin):
    search_fields=['pdtp__username']
admin.site.register(PrivateSupervisorEvaluation,PrivateSupervisorEvaluationAdmin)

class PublicSupervisorEvaluationAdmin(admin.ModelAdmin):
    search_fields=['pdtp__username']
admin.site.register(PublicSupervisorEvaluation,PublicSupervisorEvaluationAdmin)

class MentorEvaluationAdmin(admin.ModelAdmin):
    search_fields=['pdtp__username']
admin.site.register(MentorEvaluation, MentorEvaluationAdmin)


class InnovationEvaluationAdmin(admin.ModelAdmin):
    search_fields=['pdtp__username']
admin.site.register(InnovationEvaluation, InnovationEvaluationAdmin)
admin.site.register(MentorMeetingGroup)

class MentorMeetingAdmin(admin.ModelAdmin):
    search_fields=['pdtp__username']
admin.site.register(MentorMeeting, MentorMeetingAdmin)

class MentorCommentAdmin(admin.ModelAdmin):
    search_fields=['pdtp__username']
admin.site.register(MentorComment, MentorCommentAdmin)

class SupervisorToEvaluateAdmin(admin.ModelAdmin):
    search_fields=['pdtp__username']
admin.site.register(SupervisorToEvaluate, SupervisorToEvaluateAdmin)


class SupervisorCommentAdmin(admin.ModelAdmin):
    search_fields=['pdtp__username']
admin.site.register(SupervisorComment, SupervisorCommentAdmin)

class SupervisorApprovalCommentAdmin(admin.ModelAdmin):
    search_fields=['pdtp__username']
admin.site.register(SupervisorApprovalComment, SupervisorApprovalCommentAdmin)

class BuddyCommentAdmin(admin.ModelAdmin):
    search_fields=['pdtp__username']
admin.site.register(BuddyComment, BuddyCommentAdmin)

class BuddyApprovalCommentAdmin(admin.ModelAdmin):
    search_fields=['pdtp__username']
admin.site.register(BuddyApprovalComment, BuddyApprovalCommentAdmin)
class PrivateProjectAdmin(admin.ModelAdmin):
    search_fields=['pdtp__username']
admin.site.register(PrivateProject,PrivateProjectAdmin)

class MentorshipReportAdmin(admin.ModelAdmin):
    search_fields=['pdtp__username']
admin.site.register(MentorshipReport,MentorshipReportAdmin)


admin.site.register(Cohort)
admin.site.register(Work)
admin.site.register(Level)
admin.site.register(Complete)
admin.site.register(BasicEvaluation)