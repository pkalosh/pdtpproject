from django.db import models
from django.contrib.auth.models import User
from pdtpproject .validators import *
from django.db.models import Sum
from django.core.validators import MaxValueValidator, MinValueValidator


class MentorshipInternReport(models.Model):
	pdtp = models.OneToOneField(User)
	mentor = models.ForeignKey(User, related_name="my_mentor")
	awareness_description = models.CharField(max_length=300)
	awareness_impact = models.CharField(max_length=300)

	goal_description = models.CharField(max_length=300)
	goal_impact = models.CharField(max_length=300)

	adaptability_description = models.CharField(max_length=300)
	adaptability_impact = models.CharField(max_length=300)

	confidence_description = models.CharField(max_length=300)
	confidence_impact = models.CharField(max_length=300)

	presentation_description = models.CharField(max_length=300)
	presentation_impact = models.CharField(max_length=300)

	def __str__(self):
		return self.pdtp.username

class AttendanceGroup(models.Model):
	group = models.CharField(max_length=200)
	score = models.IntegerField(default=0)

	def __str__(self):
		return self.group

class MeetingGroup(models.Model):
	group = models.CharField(max_length=200)
	score = models.DecimalField(max_digits=5, decimal_places=2)

	def __str__(self):
		return self.group


class QuarterlyReportGroup(models.Model):
	group = models.CharField(max_length=200)
	score = models.IntegerField(default=0)

	def __str__(self):
		return self.group
class DailyRoutineGroup(models.Model):
	group = models.CharField(max_length=200)
	score = models.IntegerField(default=0)

	def __str__(self):
		return self.group

class MinistryReport(models.Model):
	pdtp 		= 	models.OneToOneField(User)
	attendance 	= 	models.ForeignKey(AttendanceGroup)
	meeting 	=	models.ForeignKey(MeetingGroup)
	report 		=	models.ForeignKey(QuarterlyReportGroup, null=True,blank=True)
	supervisor_approved =models.BooleanField(default=False)
	supervisor = models.ForeignKey(User,related_name="report_approved_by_supervisor",null=True,blank=True)
	date_approved =models.DateTimeField(null= True,blank=True)
	def __str__(self):
		return self.pdtp.username

	#reports_attachment model.

class WorkAssignment(models.Model):
	pdtp = models.OneToOneField(User)
	daily_activity =models.ForeignKey(DailyRoutineGroup)
	supervisor_approved =models.BooleanField(default=False)
	supervisor = models.ForeignKey(User,related_name="approved_by_supervisor",null=True,blank=True)
	date_approved =models.DateTimeField(null= True,blank=True)
	def __str__(self):
		return self.pdtp.username



class WorkAssignmentEvidence(models.Model):
	pdtp = models.ForeignKey(User)
	project_name =models.CharField(max_length=200)
	description = models.CharField(max_length=400)
	link = models.CharField(max_length=400,null=True, blank=True)
	supervisor_approved =models.BooleanField(default=False)
	supervisor = models.ForeignKey(User,related_name="assignment_approved_by_supervisor",null=True,blank=True)
	date_approved =models.DateTimeField(null= True,blank=True)
	def __str__(self):
		return self.pdtp.username

class AdditionalActivity(models.Model):
	pdtp = models.ForeignKey(User)
	project_name =models.CharField(max_length=200)
	task=models.CharField(max_length=200, null=True)
	description = models.CharField(max_length=400)
	link = models.CharField(max_length=400,null=True, blank=True)
	supervisor_approved =models.BooleanField(default=False)
	supervisor = models.ForeignKey(User,related_name="activity_approved_by_supervisor",null=True,blank=True)
	date_approved =models.DateTimeField(null= True,blank=True)
	def __str__(self):
		return self.pdtp.username

class Transformation(models.Model):
	pdtp = models.ForeignKey(User)
	ministry =models.CharField(max_length=200)
	project_name =models.CharField(max_length=200)
	task =models.CharField(max_length=200, null=True)
	description = models.CharField(max_length=400)
	link = models.CharField(max_length=400,null=True, blank=True)
	supervisor_approved =models.BooleanField(default=False)
	supervisor = models.ForeignKey(User,related_name="trans_approved_by_supervisor",null=True,blank=True)
	date_approved =models.DateTimeField(null= True,blank=True)

	def __str__(self):
		return self.pdtp.username

class ReportAttachment(models.Model):
	pdtp = models.ForeignKey(User, null=True,blank=True)
	file = models.FileField(upload_to='attachments', null=True,blank=True,verbose_name="Attach Reports(max 4 Files)",validators=[validate_file_extension],help_text="only pdf files allowed")
	def __str__(self):
		return self.pdtp.username

#Private Sector atandance Groups
class PrivateSectorAttendaceGroup(models.Model):
	group = models.CharField(max_length=200)
	score = models.IntegerField(default=0)

	def __str__(self):
		return self.group

#Private Sector attendance
class PrivateSectorAttendance(models.Model):
	pdtp = models.OneToOneField(User)
	attendance = models.ForeignKey(PrivateSectorAttendaceGroup)
	attachment = models.FileField(upload_to="Private Exit Notes", null=True,blank=True)
	supervisor_approved =models.BooleanField(default=False)
	supervisor = models.ForeignKey(User,related_name="attendance_approved_by_supervisor",null=True,blank=True)
	date_approved =models.DateTimeField(null= True,blank=True)
	def __str__(self):
		return self.pdtp.username

#On Job Training, Soft Skills
class PrivateOnJobTraining(models.Model):
	pdtp = models.ForeignKey(User)
	subject = models.CharField(max_length=200)
	description = models.CharField(max_length=400)
	supervisor_approved =models.BooleanField(default=False)
	supervisor = models.ForeignKey(User,related_name="train_approved_by_supervisor",null=True,blank=True)
	date_approved =models.DateTimeField(null= True,blank=True)
	def __str__(self):
		return self.pdtp.username

#Private Sector Trainings on Skill area
class PrivateTraining(models.Model):
	pdtp = models.ForeignKey(User)
	subject = models.CharField(max_length=200)
	description = models.CharField(max_length=400)
	attachment = models.FileField(upload_to="Certificate", null=True,blank=True)
	supervisor_approved =models.BooleanField(default=False)
	supervisor = models.ForeignKey(User,related_name="training_approved_by_supervisor",null=True,blank=True)
	date_approved =models.DateTimeField(null= True,blank=True)
	def __str__(self):
		return self.pdtp.username

class Parameter(models.Model):
	parameter = models.CharField(max_length=200)
	def __str__(self):
		return self.parameter

class MentorParameter(models.Model):
	parameter = models.CharField(max_length=200, unique=True)
	def __str__(self):
		return self.parameter

class PrivateSupervisorEvaluation(models.Model):
	pdtp =models.ForeignKey(User)
	parameter =models.ForeignKey(Parameter,null=True)
	score =models.IntegerField(default=0,null=True)
	supervisor = models.ForeignKey(User,related_name="intern_evaluated_by_supervisor",null=True,blank=True)

	def __str__(self):
		return self.pdtp.username
class PublicSupervisorEvaluation(models.Model):
	pdtp =models.ForeignKey(User)
	parameter =models.ForeignKey(Parameter,null=True)
	score =models.IntegerField(default=0,null=True)
	supervisor = models.ForeignKey(User,related_name="intern_evaluated_by_psupervisor",null=True,blank=True)

	def __str__(self):
		return self.pdtp.username

class MentorMeetingGroup(models.Model):
	group = models.CharField(max_length=200)
	score = models.IntegerField(default=0)

	def __str__(self):
	
		return self.group

class MentorMeeting(models.Model):
	pdtp =models.ForeignKey(User)
	meeting=models.ForeignKey(MentorMeetingGroup)
	def __str__(self):
		return self.pdtp.username

class MentorEvaluation(models.Model):
	pdtp =models.ForeignKey(User)
	parameter =models.ForeignKey(MentorParameter,null=True)
	score =models.IntegerField(default=0,null=True)
	mentor = models.ForeignKey(User,related_name="mentee_evaluated_by_mentor",null=True,blank=True)
	
	@staticmethod
	def get_mentor_evaluation(user):
		data=MentorEvaluation.objects.filter(pdtp=user)
		meet = MentorMeeting.objects.get(pdtp=user)
		score=0
		total=0
		for m in data:
			score += m.score
			total= score + meet.meeting.score
		return total
	def __str__(self):
		return self.pdtp.username

class InnovationEvaluation(models.Model):
	pdtp =models.OneToOneField(User)
	initiative =models.DecimalField(max_digits=5, decimal_places=2,default=0.00, verbose_name="Submission/Initiative",validators=[
            MaxValueValidator(2),
            MinValueValidator(0)
        ])
	presentation = models.DecimalField(max_digits=5, decimal_places=2,default=0.00, verbose_name="Shortlisted",validators=[
            MaxValueValidator(3),
            MinValueValidator(0)
        ])
	evaluation = models.DecimalField(max_digits=5, decimal_places=2,default=0.00, verbose_name="First Evaluation",validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ])
	final = models.DecimalField(max_digits=5, decimal_places=2,default=0.00, verbose_name="Final Evaluation")
	total =models.DecimalField(max_digits=5, decimal_places=2)

	def save(self, *args, **kwargs):

		score= (((float(self.initiative) + float(self.presentation) + float(self.evaluation)+float(self.final))*20)/15)
		#self.total = ((20/100)*int(score))

		self.total = round(score,2)
		super(InnovationEvaluation, self).save(*args, **kwargs)

	


# class QuarterlyPresentationEvaluation(models.Model):
# 	pdtp =models.OneToOneField(User)
# 	initiative =models.DecimalField(max_digits=5, decimal_places=2,default=0.00, verbose_name="Submission/Initiative",validators=[
#             MaxValueValidator(2),
#             MinValueValidator(0)
#         ])
# 	presentation = models.DecimalField(max_digits=5, decimal_places=2,default=0.00, verbose_name="Shortlisted",validators=[
#             MaxValueValidator(3),
#             MinValueValidator(0)
#         ])
# 	evaluation = models.DecimalField(max_digits=5, decimal_places=2,default=0.00, verbose_name="First Evaluation",validators=[
#             MaxValueValidator(5),
#             MinValueValidator(0)
#         ])
# 	final = models.DecimalField(max_digits=5, decimal_places=2,default=0.00, verbose_name="Final Evaluation")
# 	total =models.DecimalField(max_digits=5, decimal_places=2)

# 	def save(self, *args, **kwargs):

# 		score= (((float(self.initiative) + float(self.presentation) + float(self.evaluation)+float(self.final))*20)/15)
# 		#self.total = ((20/100)*int(score))

# 		self.total = round(score,2)
# 		super(InnovationEvaluation, self).save(*args, **kwargs)


# 	def __str__(self):
# 		return self.pdtp.username

class MentorComment(models.Model):
	pdtp =models.OneToOneField(User)
	comment =models.CharField(max_length=500,verbose_name="Kindly share your overall assesment of the intern (a paragraph not a single word(500 Char))")
	mentor = models.ForeignKey(User,related_name="comment_by_mentor",null=True,blank=True)
	def __str__(self):
		return self.pdtp.username


class SupervisorComment(models.Model):
	pdtp =models.OneToOneField(User)
	comment =models.CharField(max_length=500,verbose_name="Kindly share your overall assesment of the intern (a paragraph not a single word(500 Char))")
	supervisor = models.ForeignKey(User,related_name="comment_by_supervisor",null=True,blank=True)
	def __str__(self):
		return self.pdtp.username

class SupervisorApprovalComment(models.Model):
	pdtp =models.OneToOneField(User)
	award_marks = models.IntegerField(default=0,validators=[
            MaxValueValidator(12),
            MinValueValidator(0)
        ], verbose_name="Award the intern marks as per his/her performance in your ourgnization and based on the report above(max 12)")
	comment =models.CharField(max_length=500,verbose_name="Kindly share your overall assesment of the intern (a paragraph not a single word(500 Char))")
	supervisor = models.ForeignKey(User,related_name="approvalc_by_supervisor",null=True,blank=True)
	def __str__(self):
		return self.pdtp.username


class BuddyComment(models.Model):
	pdtp =models.OneToOneField(User)
	comment =models.CharField(max_length=500,verbose_name="Kindly share your overall assesment of the intern (a paragraph not a single word(500 Char))")
	supervisor = models.ForeignKey(User,related_name="comment_by_buddy",null=True,blank=True)
	def __str__(self):
		return self.pdtp.username

class BuddyApprovalComment(models.Model):
	pdtp =models.OneToOneField(User)
	award_marks = models.IntegerField(default=0,validators=[
            MaxValueValidator(20),
            MinValueValidator(0)
        ], verbose_name="Award the intern marks as per his/her performance in your ourgnization and based on the report above(max 20)")
	comment =models.CharField(max_length=500,verbose_name="Kindly share your overall assesment of the intern (a paragraph not a single word(500 Char))")
	supervisor = models.ForeignKey(User,related_name="approvalc_by_buddy",null=True,blank=True)
	def __str__(self):
		return self.pdtp.username


class PrivateProject(models.Model):
	pdtp = models.ForeignKey(User)
	project_name =models.CharField(max_length=200)
	description = models.CharField(max_length=400)
	link = models.CharField(max_length=400,null=True, blank=True)
	supervisor_approved =models.BooleanField(default=False)
	supervisor = models.ForeignKey(User,related_name="pproject_approved_by_supervisor",null=True,blank=True)
	date_approved =models.DateTimeField(null= True,blank=True)

	def __str__(self):
		return self.pdtp.username




class MentorshipReport(models.Model):
	pdtp = models.OneToOneField(User)
	approved = models.BooleanField(default=False)
	report = models.FileField(upload_to='mentorship reports', null=True,blank=True,verbose_name="Attach Reports(max 4 Files)",validators=[validate_file_extension],help_text="only pdf files allowed")
	approved_by = models.ForeignKey(User, related_name="report_approved_by_mentor", null=True,blank=True)
	def __str__(self):
		return self.pdtp.username


class SupervisorToEvaluate(models.Model):
	pdtp = models.ForeignKey(User)
	supervisor =models.ForeignKey(User, related_name="sup")
	sector = models.CharField(max_length=200)

	def __str__(self):
		return self.pdtp.username



class Cohort(models.Model):
	cohort = models.CharField(max_length=200)
	def __str__(self):
		return self.cohort

class Work(models.Model):
	work = models.CharField(max_length=200)
	def __str__(self):
		return self.work

class Level(models.Model):
	level = models.CharField(max_length=200)
	def __str__(self):
		return self.level
class Complete(models.Model):
	complete = models.CharField(max_length=200)
	def __str__(self):
		return self.complete
class BasicEvaluation(models.Model):
	cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE, verbose_name="Which of the following represents your cohort?")
	motivation = models.CharField(max_length=200, verbose_name="What motivated you to join the PDTP Programme? *(200 characters")
	work = models.ManyToManyField(Work, verbose_name="What are you currently doing? *")
	education = models.ManyToManyField(Level, verbose_name="If in school, which level of education?")
	other = models.CharField(max_length=500, null=True, blank=True)
	completion = models.ForeignKey(Complete, on_delete=models.CASCADE, verbose_name="Did you complete the 12-months internship period? After how long did you exit?")
	reason =models.CharField(max_length=200, null=True,blank=True,verbose_name="If you didn't stay for 12 Months period, what was your reason(s)")
	training = models.CharField(max_length=500, verbose_name="List the Trainings you attended during the PDTP programme?")
	training_expectection = models.CharField(max_length=200, verbose_name="List professional Certifications you successfully undertook during your PDTP progamme period. ")
	other_expectation = models.CharField(max_length=500, null=True, blank=True)
	def __str__(self):
		return self.cohort.cohort