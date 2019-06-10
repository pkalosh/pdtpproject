from django.db import models
from django.contrib.auth.models import User
from pdtpproject.constants import *
BOOL_CHOICES = ((True, 'Public'), (False, 'Private'))
from app.models import *
from tinymce.models import HTMLField
from auditlog.registry import auditlog
from django.template.defaultfilters import slugify
from django.db.models import Q

# Create your models here.
class Title(models.Model):
	title=models.CharField(max_length=200,verbose_name=" Title")
	def __str__(self):
		return self.title

class Organization(models.Model):
	category=models.BooleanField(default=False,choices=BOOL_CHOICES)
	organization=models.CharField(max_length=255,unique=True, verbose_name="Organization Name")
	location=models.CharField(max_length=200,null=True,blank=True, verbose_name="Physical Location")
	county=models.ForeignKey(County, null=True,blank=True, verbose_name="County Located")
	town=models.CharField(max_length=200, null=True,blank=True,verbose_name="Town Located")
	logo=models.ImageField(upload_to="Companie Logos",null=True,blank=True)
	slug=models.SlugField(unique=False,blank=True,null=True)
	def save(self,*args,**kwargs):
		self.slug=slugify(self.organization)
		super(Organization, self).save(*args,**kwargs)
	def __str__(self):
		return self.organization
	class Meta:
		verbose_name_plural='Partner Organizations and MDAs'
auditlog.register(Organization)
		
class Supervisor(models.Model):
	organization=models.ForeignKey(Organization)
	supervisor=models.ForeignKey(User)
	position=models.CharField(max_length=200, verbose_name="Business Title", null=True, blank=True)
	title=models.ForeignKey(Title, verbose_name="Title", null=True, blank=True)
	is_contact_person=models.BooleanField(default=False)
	honors=models.CharField(max_length=200,blank=True,null=True, verbose_name="Honors")
	mentor_availability=models.BooleanField(default=True,verbose_name="Availability")
	is_mentor=models.BooleanField(default=False, verbose_name="Is a Mentor")
	is_supervisor=models.BooleanField(default=False, verbose_name="Is a Supervisor")
	is_buddy=models.BooleanField(default=False, verbose_name="Is a Buddy")
	
	
	@staticmethod
	def get_mentors():
		mentors=Supervisor.objects.filter(is_mentor=True)
		return mentors

	@staticmethod
	def get_supervisors():
		supervisors=Supervisor.objects.filter(Q(is_supervisor=True) | Q(is_contact_person=True))
		return supervisors
	def __str__(self):
		return self.supervisor.username
	class Meta:
		verbose_name_plural='Mentors and Supervisors'
auditlog.register(Supervisor)
		
class Deployment(models.Model):
	pdtp=models.ForeignKey(User)
	organization=models.ForeignKey(Organization)
	year=models.ForeignKey(PdtpYear)
	sector=models.CharField(max_length=200)

	
	#Confirm Interns
	confirmed=models.BooleanField(default=True)
	date_confirmed=models.DateField(auto_now_add=True)
	reporting_date=models.DateField(null=True,blank=True)
	completion_date=models.DateField(null=True,blank=True)
	reporting_details=HTMLField(null=True,blank=True,verbose_name="Attachment Reporting Instructions:")

	#Invite for interview
	interview=models.BooleanField(default=False)
	date_invited=models.DateField(null=True,blank=True)
	interview_date=models.DateField(null=True,blank=True)
	interview_instructions=HTMLField(null=True,blank=True,verbose_name="Interview Instructions:")
	def __str__(self):
		return self.pdtp.username
auditlog.register(Deployment)
class InternSupervisor(models.Model):
	pdtp = models.ForeignKey(User)
	supervisor = models.ForeignKey(User,related_name="sup_assigned")
	company=models.ForeignKey(Organization,null=True,blank=True)
	#year=models.CharField(max_length=200,null=True)
	
	def __str__(self):
		return self.pdtp.username
auditlog.register(InternSupervisor)



class Parametor(models.Model):
	name=models.CharField(max_length=200)
	def __str__(self):
		return self.name
auditlog.register(Parametor)
	
class Evaluation(models.Model):
	supervisor=models.ForeignKey(User)
	pdtp=models.ForeignKey(User,related_name="pdtp")
	parameter=models.ForeignKey(Parametor)
	rating=models.CharField(max_length=200)
	
	def __str__(self):
		return self.pdtp
auditlog.register(Evaluation)

class WorkPlan(models.Model):
	pdtp=models.ForeignKey(User)
	project_name=models.CharField(verbose_name="Assignment/Project Name", help_text="e.g. PDTP Helpdesk system(Indicate whether new or existing)max 100 words",max_length=100)
	task=models.CharField(verbose_name="Activity/Task", help_text="e.g.Collection and compiling of user requirements, Design, Testing, Implementation (max 300 words)",max_length=300)
	resources=models.CharField(max_length=300,verbose_name="Input/Resources required", help_text="e.g. Laptops, finances (max 300 words)")
	outputs=models.CharField(max_length=300, verbose_name="Outputs/Deliverables(Measurable)",help_text="e.g. PDTP Helpdesk system(Max 300 Words ")
	expected_impact=models.CharField(max_length=300,help_text="Max 300 words")
	start_date=models.DateField(null=True)
	end_date=models.DateField(null=True)
	status=models.CharField(max_length=300,help_text="Max 300 words")
	approved_by_supervisor=models.BooleanField(default=False,verbose_name="Approve?")
	supervisor_comment=models.CharField(max_length=300,null=True,blank=True,verbose_name="Comment")
	date_approved=models.DateField(null=True,blank=True)
	date_submitted=models.DateField(auto_now_add=True)
	supervisor=models.ForeignKey(User,related_name="intern_supervisor",null=True,blank=True)
	organization=models.ForeignKey(Organization,null=True,blank=True)
	class Meta:
		ordering = ['-date_submitted', 'pdtp']

	def __str__(self):
		return self.pdtp.username
auditlog.register(WorkPlan)

class InternMEParameter(models.Model):
	year = models.ForeignKey(PdtpYear, null=True, blank=True)
	name = models.CharField(verbose_name="Intern M & E parameter", max_length=500)

	def __str__(self):
		return self.name
auditlog.register(InternMEParameter)
class SupervisorMEParameter(models.Model):
	year = models.ForeignKey(PdtpYear,null=True, blank=True)
	name = models.CharField(verbose_name="supervisor M & E parameter", max_length=500)

	def __str__(self):
		return self.name
auditlog.register(SupervisorMEParameter)
class MonitoringStatus(models.Model):
	status = models.CharField(max_length=200)
	class Meta:
		verbose_name_plural = 'MonitoringStatus'
	def __str__(self):
		return self.status
auditlog.register(MonitoringStatus)

class MonitoringAndEvaluationPhase(models.Model):
	secretariat = models.ForeignKey(User, related_name='phase',null=True)
	phase = models.CharField(max_length=200, unique=True)
	status = models.ForeignKey(MonitoringStatus, on_delete=models.CASCADE)
	year = models.ForeignKey(PdtpYear, null=True)


	def __str__(self):
		return self.phase
auditlog.register(MonitoringAndEvaluationPhase)

class MonitoringAndEvaluation(models.Model):
	pdtp = models.ForeignKey(User)
	year = models.CharField(max_length=100,verbose_name="Cohort Year",null=True,blank=True)
	phase = models.ForeignKey(MonitoringAndEvaluationPhase,null=True,blank=True, on_delete=models.CASCADE,verbose_name="Monitoring and Evaluation Phase")
	projects = HTMLField(null=True,blank=True, verbose_name="Projects involved in at the Ministry/State Corporation/County")
	my_contribution = HTMLField(null=True,blank=True,verbose_name="My Contribution to those projects")
	lessons_learned_during_internship = HTMLField(null=True,verbose_name="Briefly describe what you consider to be your most significant lessons learned so far during this internship?Please provide specific examples.")
	specific_projects_or_assignments_you_are_given = HTMLField(null=True,verbose_name="What specific projects or assignments are you givenduring the internship?")
	projects_given_are_they_challenging_or_stimulating = HTMLField(null=True,verbose_name="specific projects or assignments given ,Are they challenging and stimulating?")
	evaluate_your_experience = HTMLField(null=True,verbose_name="Please evaluate your experience with each one of the projects and assigements you listed above")
	instruction_and_Directions_given_by_supervisor = HTMLField(null=True, verbose_name="Are you given adequate instruction anddirection/support from staff/supervisor in order to complete your assignments?")
	supervisor_availability = models.CharField(max_length=100,null=True, verbose_name="Has your supervisor been available and accessible tosupport you whenever you needed?")
	field_of_specialization = HTMLField(null=True, verbose_name="Has this internship stimulated your interest in your fieldof Specialization (Application, Networking, Security orProject Management)? Why or why not?")
	opportunities_for_learning = models.CharField(max_length=1000, null=True, verbose_name="Are there ample opportunities for learning?")
	preparedness_to_enter_world_of_work = models.CharField(max_length=500,null=True,verbose_name="Do you feel that you are better prepared to enter theworld of work/innovation after the internship?")
	Your_relationship_with_other_workers = models.CharField(max_length=1000, null=True, verbose_name="How’s your working relationship with the other workersin the organization?")
	How_have_you_been_treated_by_the_organization= models.CharField(max_length=1000, null=True)
	Has_the_attachment_met_your_expectations = models.CharField(max_length=1000, null=True, verbose_name="Has the attachment met your expectations as per thePDTP curriculum (time, office environment, type of work)? Please explain.")
	suggestions_to_improve_the_internship_programme = HTMLField(null=True, verbose_name="Based on your experience, what suggestions can youprovide which can improve the program in regards to internships/attachments in private/public sector in thefuture?")
	recommend_this_organisation= HTMLField(null=True,verbose_name="Would you recommend this organisation for internship to others? Why/why not?")
	best_practices = HTMLField(null=True,verbose_name="What best practices can we apply to the government from the private sector? (For Private sector internships ONLY)")
	innovation = HTMLField(null=True,blank=True, verbose_name="Have you identified any innovation opportunities at your place of attachment? if yes list them")
	innovation_reason = HTMLField(null=True, verbose_name="Have you identified any innovation opportunities at your place of attachment? if No Give reasons")
	mentorship_sessions = models.CharField(max_length=100, null=True,verbose_name="How many times have u met your mentor?")
	mentorship_lesson_learned = HTMLField(null=True,blank=True, verbose_name="State lessons (if any) learnt from your mentor:")
	mentorship_problem_faced = HTMLField(null=True,blank=True, verbose_name="State any problem relating to mentorship")
	training_attended = HTMLField(null=True, verbose_name="How many Trainings have you attended? List them")
	Certifications_attained = HTMLField(null=True, verbose_name="How many Certifications have you successfully done? List them")
	suggestion_on_job_training = HTMLField(null=True,blank=True, verbose_name="Your Suggestions On-job training at attachment station")
	suggestion_innovation = HTMLField(null=True,blank=True, verbose_name="Your Suggestions on Innovations")
	suggestion_mentorship = HTMLField(null=True,blank=True, verbose_name="Your Suggestions on Mentorship")
	suggestion_training =  HTMLField(null=True,blank=True, verbose_name="Your Suggestions on Training and Certifications")
	comment_icta_secretariat_support =  HTMLField(null=True,blank=True, verbose_name="Your Comment on the support given to you by the ICT Authority/PDTP Secretariat")
	challenges_faced = models.CharField(max_length=1000, null=True,blank=True, verbose_name="List any challenges you have faced during your time in the programme:")
	supervisor = models.ForeignKey(User, related_name="Intern_report", null=True, blank=True)
	date_supervisor_submitted=models.DateField(null=True,blank=True)
	date_submitted_by_intern=models.DateField(auto_now_add=True)
	intern_strength = HTMLField(null=True,blank=True,verbose_name="What are the interns outstanding STRENGTHS")
	areas_improvement = HTMLField(null=True,blank=True, verbose_name="In what areas does the intern need IMPROVEMENT?")
	
	def __str__(self):
		return self.pdtp.username
class InternMERate(models.Model):
	pdtp = models.ForeignKey(User)
	phase = models.ForeignKey(MonitoringAndEvaluationPhase, on_delete=models.CASCADE,null=True,blank=True)
	intern_parameter= models.ForeignKey(InternMEParameter,on_delete=models.CASCADE, null=True, blank=True, verbose_name="Intern parameter")
	rate = models.CharField(max_length= 500)



	def __str__(self):
		return self.intern_parameter.name

class SupervisorMERate(models.Model):
	supervisor = models.ForeignKey(User)
	phase = models.ForeignKey(MonitoringAndEvaluationPhase, on_delete=models.CASCADE,null=True,blank=True)
	supervisor_parameter= models.ForeignKey(SupervisorMEParameter,on_delete=models.CASCADE, null=True,blank=True, verbose_name="Supervisor parameter")
	Jibu = models.CharField(max_length=100, null=True,blank=True)
	pdtp = models.ForeignKey(User, related_name="intern_supervisor_rates", on_delete=models.CASCADE,null=True,blank=True)


	def __str__(self):
		return self.supervisor_parameter.name



class ReportStatus(models.Model):
	status = models.CharField(max_length=200)
	class Meta:
		verbose_name_plural = 'ReportStatus'
	def __str__(self):
		return self.status

class ProjectSection(models.Model):
	section = models.CharField(max_length=200)
	def __str__(self):
		return self.section

class PhaseOrQuarter(models.Model):
	secretariat = models.ForeignKey(User, related_name='phase_quaters',null=True)
	quater = models.CharField(max_length=200, unique=True)
	status = models.ForeignKey(ReportStatus, on_delete=models.CASCADE)
	# year = models.ForeignKey(PdtpYear, null=True, blank=True)


	def __str__(self):
		return self.quater


class QuarterlyReport(models.Model):
	approved = models.BooleanField(default=False)
	year = models.ForeignKey(PdtpYear, on_delete=models.CASCADE)
	quater = models.ForeignKey(PhaseOrQuarter, on_delete=models.CASCADE)
	date_approved = models.DateTimeField(auto_now_add=True,null=True)
	pdtp = models.ForeignKey(User,on_delete=models.CASCADE)
	introduction = HTMLField(verbose_name="Summary of Your Experience in place of Deployment", null=True, blank=True)
	projects_involved = HTMLField(verbose_name="Projects Involved in at place of Deployment ", null=True, blank=True, help_text='Name and description of the project')
	project_Category = models.ForeignKey(ProjectSection, on_delete=models.CASCADE, null=True, blank=True)
	innovation_opportunity = HTMLField(verbose_name="Innovations opportunities at Deployment Station", null=True, blank=True)
	mentorship_progress = HTMLField(null=True, blank=True)
	training_certification = HTMLField(null=True, blank=True,verbose_name="Training and certifications done so far/in progress")
	lesson_learnt = HTMLField(verbose_name="Lesson Learnt from Your deployment station", null=True, blank=True)
	challenges_faced = HTMLField(verbose_name="Challenges Experienced while Undertaking your duties", null=True, blank=True)
	recommendation = HTMLField(verbose_name="Recommendations to Improve PDTP programme", null=True, blank=True)
	supervisor = models.ForeignKey(User, related_name="station_supervisor", null=True, blank=True)
	comments = HTMLField(max_length=500,verbose_name="Supervisor Comments",null=True, blank=True)
	

	def __str__(self):
		return self.pdtp.username


class Attendance(models.Model):
	pdtp = models.ForeignKey(User)
	days_attended = models.IntegerField(verbose_name="Days Attended")
	supervisor = models.ForeignKey(User, related_name="monthly_attendance")
	date_submitted  = models.DateTimeField(auto_now_add=True,null=True)

	class Meta:
		verbose_name_plural = "Attendance"

	def __str__(self):
		return self.pdtp.username
	
