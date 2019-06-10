
from django.db import models
from django.contrib.auth.models import User
from pdtpproject.constants import *
BOOL_CHOICES = ((True, 'Public'), (False, 'Private'))
from tinymce.models import HTMLField
from auditlog.registry import auditlog
from django.template.defaultfilters import slugify
from performance.models import *
from datetime import datetime

class JobContact(models.Model):
	email = models.EmailField()
	pdtp_contacted = models.EmailField()
	message = models.TextField()
	date = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.email

class PartnerCohort(models.Model):
	cohort = models.CharField(max_length=200)
	def __str__(self):
		return self.cohort

class Partner(models.Model):
	cohort = models.ForeignKey(PartnerCohort, null=True,blank=True)
	partner = models.CharField(max_length=500, verbose_name="Name")
	logo = models.ImageField(null=True,blank=True)
	website = models.CharField(max_length=300, null=True,blank=True)

	def __str__(self):
		return self.partner
class PartnerApplication(models.Model):
	organization_name = models.CharField(max_length=200,verbose_name="Organization Name")
	full_name = models.CharField(max_length=200, verbose_name="Full Name")
	position = models.CharField(max_length=200, verbose_name="Position/Title*")
	department = models.CharField(max_length=200, verbose_name="Department *")
	address = models.CharField(max_length=200, verbose_name="Postal Address*")
	office_tel = models.CharField(max_length=200, verbose_name="Office Tel No*")
	mobile = models.CharField(max_length=200, verbose_name="Personal Mobile No. *")
	office_mail = models.EmailField(max_length=200, verbose_name="General Office Email*")
	email = models.EmailField(max_length=200, verbose_name="Official Email*")
	telephone = models.CharField(max_length=200, verbose_name="Telephone (Persons To Contact)")
	partnership_category = models.CharField(max_length=200, verbose_name="Partnership Category*")
	mentor_intern = models.CharField(max_length=100, verbose_name="Mentor an Intern(s)*")
	speaker = models.CharField(max_length=200, verbose_name="Motivate Interns (Speaker)*")
	trainer = models.CharField(max_length=200, verbose_name="Life Skills Coaching​(Train)​*")
	panelist = models.CharField(max_length=200, verbose_name="nnovation Evaluation ​(​Panelist​)​*")
	legal_support = models.CharField(max_length=200, verbose_name="IP legal Support for innovators​(serve)*")

	def __str__(self):
		return self.full_name


class MentorshipApplication(models.Model):
	full_name = models.CharField(max_length=200, verbose_name="Full Name *")
	email = models.EmailField(max_length=200, verbose_name="E-mail address *")
	mobile = models.CharField(max_length=200, verbose_name="Personal Mobile No *")
	company = models.CharField(max_length=200, verbose_name="Company *")
	position = models.CharField(max_length=200, verbose_name="Position/Job Title *")
	academic_profile = models.CharField(max_length=1000, verbose_name="Please list your Academic Qualifications : Degrees and/or diplomas held (Maximum 15 Entries)")
	academic_qualifications = models.CharField(max_length=1000, verbose_name="Do you have academic qualifications in these areas? (Tick all that are applicable) *")
	work_experience = models.IntegerField( verbose_name="How many years have you worked in total? *")
	technical_position = models.BooleanField(default=False, verbose_name="Have you held any management or technical positions? *")
	achievement = models.TextField(verbose_name="What do you consider your greatest achievement? *")
	ethics = models.BooleanField(default=False, verbose_name="Have your ethics ever come into question? *")
	criminally_liable = models.BooleanField(default=False, verbose_name="Have you ever been deemed criminally liable? *")
	availability = models.BooleanField(default=False, verbose_name="Does your position necessitate frequent and long term travel? ")
	shortest_out_of_country = models.IntegerField(verbose_name="What is the shortest length of time you are out of the country? (No of Days) *")
	longest_out_of_country = models.IntegerField(verbose_name="What is the longest length of time you are out of the country? *")
	personal_obligation = models.BooleanField(default=False, verbose_name="Do you have personal obligations that may limit your availability to mentor? *")
	commitment =  models.TextField(verbose_name="How would you handle your mentorship duties during busy periods at your work or personal life? *")
	suggestions = models.TextField(verbose_name="Any other form of partnership or suggestion/s you may have?")
	Application_time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.full_name

class MustChangePassword(models.Model):
    user=models.OneToOneField(User)
    def __str__(self):
        return "%s " % (self.user.username)

class Specialization(models.Model):
    speciality =models.CharField(max_length=400)
    description = models.TextField(null=True,blank=True)
    slug=models.SlugField(unique=False,blank=True,null=True)
    def save(self,*args,**kwargs):
    	self.slug=slugify(self.speciality)
    	super(Specialization, self).save(*args,**kwargs)
    def __str__(self):
    	return  self.speciality
        
class PdtpYear(models.Model):
	year=models.CharField(max_length=200, unique=True)
	slug=models.SlugField(unique=False,blank=True,null=True)
	def save(self,*args,**kwargs):
		self.slug=slugify(self.year)
		super(PdtpYear, self).save(*args,**kwargs)
	def  __str__(self):
		return self.year
	class Meta:
		verbose_name_plural='PDTP Years'
		ordering =('-year',)
auditlog.register(PdtpYear)
	
class County(models.Model):
	county=models.CharField(max_length=200)

	def __str__(self):
		return self.county
	class Meta:
		verbose_name_plural='Counties'
auditlog.register(County)
	
class AlummniDatabase(models.Model):
	name = models.CharField(max_length=200, verbose_name="Full Name")
	email = models.EmailField(verbose_name="Email", unique=True)
	phone = models.CharField(max_length=15, verbose_name="Phone Number", unique=True)
	gender = models.CharField(max_length=200,null=True,blank=True,choices=GENDER)
	cohort = models.ForeignKey(PdtpYear)
	speciality =models.ForeignKey(Specialization)
	employer = models.CharField(max_length=400, verbose_name="Current Employer")
	job = models.CharField(max_length=400, verbose_name="Current Job(Position)")
	country = models.CharField(max_length=400,verbose_name=" In which country do you currently live?")
	date_registered = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		self.name



class UserProfile(models.Model):
	user=models.OneToOneField(User)
	bio=HTMLField(null=True,blank=True)
	user_category=models.CharField(max_length=200)
	title=models.CharField(max_length=200, null=True,blank=True, verbose_name="Professional Title")
	gender=models.CharField(max_length=200,null=True,blank=True,choices=GENDER)
	year=models.ForeignKey(PdtpYear, verbose_name="Year Joined", null=True, blank=True)
	nationality=models.CharField(max_length=200,null=True,blank=True)
	id_no=models.IntegerField(null=True,blank=True,verbose_name="ID/Passport Number")
	ref_no=models.CharField(max_length=200,null=True,blank=True,verbose_name="PDTP Number")
	phone_number = models.CharField(max_length=100,null=True,blank=True,help_text="format 0712345678", verbose_name="Phone Number")
	postal_address=models.CharField(max_length=200,null=True,blank=True,verbose_name="Postal Address", help_text="Enter Address, Code,City")
	date_of_birth=models.DateField(null=True, blank=True)
	county_of_birth=models.ForeignKey(County,null=True,blank=True,verbose_name="County of Birth", related_name="county_of_origin")
	area_of_specialization=models.CharField(max_length=200,null=True,blank=True,verbose_name="Area of Specialization")
	speciality = models.ForeignKey(Specialization, null= True, blank =True)
	marital_status=models.CharField(max_length=200,null=True,blank=True,choices=MARITAL_STATUS)
	date_added=models.DateTimeField(auto_now_add=True)
	#date_deactivated=models.DateTimeField(auto_now=True)
	picture=models.ImageField(upload_to="pdtp pictures", blank=True, null=True)
	alternate_email=models.EmailField(verbose_name="Alternative Email Address", null=True,blank=True)
	alternate_cell=models.CharField(max_length=16,verbose_name="Alternative Phone No.", null=True,blank=True)
	#Field to show mentorship status
	assignedmentor=models.BooleanField(default=False)
	physical_address=models.CharField(max_length=200,null=True,blank=True)
	nearest_institution=models.CharField(max_length=200,null=True,blank=True,verbose_name="Nearest Public Institution",help_text="e.g nearest primary school")
	#added_by=models.ForeignKey(User, related_name="user_added_by_user")
	deactivated_by=models.ForeignKey(User, null=True, blank=True,related_name="user_dactivated_by_user", verbose_name="Activated/Deactivated By")
	
	slug=models.SlugField(unique=False,blank=True,null=True)
	twitter=models.CharField(max_length=300,null=True,blank=True,verbose_name="Twitter Profile Link")
	facebook=models.CharField(max_length=300,null=True,blank=True,verbose_name="Facebook Profile Link")
	linkedin=models.CharField(max_length=300,null=True,blank=True,verbose_name="Linkedin Profile Link")
	active = models.BooleanField(default=True)
	def mentor_evaluation(self):

		data=MentorEvaluation.objects.filter(pdtp=self.user)
		coun=MentorEvaluation.objects.filter(pdtp=self.user).count()
		m = 0
		try:
			meet = MentorMeeting.objects.get(pdtp=self.user)
			score=0
			total=0
			e = coun *5
			
			for m in data:
				score += m.score
			if e > 0:
				score =(score*7)/e
			total= score + meet.meeting.score
		except:
			score=0
			total=0
			e = coun *5
			
			for m in data:
				score += m.score
			if e > 0:
				score =(score*7)/e
			total= score 
		
		return round(total,2)

	def private_evaluation(self):
		score=0
		total=0
		onjob =0
		train =0
		privateproject =0
		try:
			me = SupervisorApprovalComment.objects.get(pdtp=self.user)
			privateproject = me.award_marks
		except:
			pass

		data=PrivateSupervisorEvaluation.objects.filter(pdtp=self.user)
		n=PrivateSupervisorEvaluation.objects.filter(pdtp=self.user).count()
		# att =PrivateSectorAttendance.objects.get(pdtp = self.user)
		# pp= PrivateProject.objects.filter(pdtp=self.user).count()
		# if pp ==1:
		# 	privateproject=1
		# elif pp ==2:
		# 	privateproject =1.5
		# elif pp ==3:
		# 	privateproject=2
		# elif pp >4:
		# 	privateproject =5

		# onp =PrivateOnJobTraining.objects.filter(pdtp=self.user).count()
		# if onp ==1:
		# 	onjob=0.2
		# elif  onp ==2:
		# 	onjob = 0.4
		# elif  onp ==3:
		# 	onjob = 0.6
		# elif  onp ==4:
		# 	onjob = 0.8
		# trainp = PrivateTraining.objects.filter(pdtp=self.user).count()
		# if trainp ==1:
		# 	train=0.2
		# elif  trainp ==2:
		# 	train = 0.4
		# elif  trainp ==3:
		# 	train = 0.6
		# elif  trainp ==4:
		# 	train = 0.8
		
		e =n *5
		for m in data:
			score += m.score
		if e > 0:
			score = (score*3)/e
		total= score + int(privateproject) #onjob + train +att.attendance.score + privateproject
		return round(total,2)

	def training_evaluation(self):
		score=0
		total=0
		certs =0
		trains =0
		# sat =TrainingCourse.objects.get(training_option__iexact="Certification")
		# nonsat = TrainingCourse.objects.get(training_category__iexact="Normal Training")
		certifications=TrainingApplication.objects.filter(pdtp=self.user,course__training_option__iexact="Certification")
		trainings =TrainingApplication.objects.filter(pdtp = self.user,course__training_option__iexact="Normal Training")
		if certifications.count() == 0:
			certs =0
		if certifications.count()==1:
			certs =5
		if certifications.count() == 2:
			certs =10
		if certifications.count() == 3:
			certs =10
		if certifications.count() >3:
			certs =15

		if trainings.count() ==0:
			trains = 0
		if trainings.count() ==1:
			trains =3
		if trainings.count() ==2:
			trains = 6
		if trainings.count() == 3:
			trains = 8
		if trainings.count() > 3:
			trains = 10
		
		total= int(certs) + int(trains) 
		return total

	
		
		total= int(certs) + int(trains) 
		return total

	def public_evaluation(self):
		score=0
		total=0
		onjob =0
		evidence =0
		additional = 0
		transform =0
		pubscore =0
		att_total =0
		work_total = 0 
		pub =PublicSupervisorEvaluation.objects.filter(pdtp=self.user)
		n =PublicSupervisorEvaluation.objects.filter(pdtp=self.user).count()
		try:
			me = BuddyApprovalComment.objects.get(pdtp=self.user)
			evidence = me.award_marks
		except:
			pass

		# try:
		# 	attend =MinistryReport.objects.get(pdtp = self.user)
			
		# 	att_total = attend.attendance.score + attend.meeting.score + attend.report.score
		# except:
		# 	att_total = 0
		# try:
		# 	work =WorkAssignment.objects.get(pdtp = self.user)
		# 	work_total = work.daily_activity.score
		# except:
		# 	work_total = 0
		# ev=WorkAssignmentEvidence.objects.filter(pdtp=self.user).count()
		# if ev ==0:
		# 	evidence =0
		# elif ev == 1:
		# 	evidence =1
		# elif ev == 2:
		# 	evidence =2
		# elif ev ==3:
		# 	evidence =3
		# elif ev >=4:
		# 	evidence =4
		# ad= AdditionalActivity.objects.filter(pdtp=self.user).count()
		# if ad ==0:
		# 	additional = 0
		# elif ad ==1:
		# 	additional =0.5
		# elif ad ==2:
		# 	additional =1
		# elif ad == 3:
		# 	additional =1.5
		# elif ad >=4:
		# 	additional =2
		# tr=Transformation.objects.filter(pdtp=self.user).count()
		# if tr ==0:
		# 	transform = 0
		# elif tr ==1:
		# 	transform =1
		# elif tr >=2:
		# 	transform =2
		e =n *5
		for m in pub:
			pubscore += m.score
		if e > 0: 
			pubscore = (pubscore*10)/e
		total= int(pubscore)  +int(evidence) #int(work_total)+ int(transform) + float(additional) +int(evidence) + float(pubscore)
		return round(total,2)



	def save(self,*args,**kwargs):
		self.slug=slugify(self.user.username)
		super(UserProfile, self).save(*args,**kwargs)
	

	def __str__(self):
		return self.user.username

	@staticmethod
	def get_profile(user):
		profile=UserProfile.objects.get(user=user)
		return profile
	@staticmethod
	def is_management(profile):
		return profile.user_category=="MANAGEMENT"


	@staticmethod
	def is_administration(profile):
		return profile.user_category=="ADMINISTRATION"

	@staticmethod
	def is_secretariat(profile):
		return profile.user_category=="SECRETARIAT"
	@staticmethod
	def is_supervisor(profile):
		return profile.user_category=="SUPERVISOR"

	@staticmethod
	def is_pdtp(profile):
		return profile.user_category=="PDTP"
	@staticmethod
	def is_mentor(profile):
		return profile.user_category=="MENTOR"


	#List of all pdtps
	@staticmethod
	def get_pdtps():
		pdtps=UserProfile.objects.filter(user_category="PDTP")
		return pdtps

	@staticmethod
	def get_pdtps_male():
		pdtps=UserProfile.objects.filter(user_category="PDTP",gender=MALE)
		return pdtps
	@staticmethod
	def get_pdtps_female():
		pdtps=UserProfile.objects.filter(user_category="PDTP",gender=FEMALE)
		return pdtps

	@staticmethod
	def get_management():
		directors=UserProfile.objects.filter(user_category="MANAGEMENT")
		return directors

	@staticmethod
	def get_secretariats():
		secretariat=UserProfile.objects.filter(user_category="ADMINISTRATION")
		return secretariat 
	@staticmethod
	def get_buddies():
		buddies=UserProfile.objects.filter(user_category="BUDDY")
		return buddies
	#Method to return a list of all mentors
auditlog.register(UserProfile)
	


class BankDetail(models.Model):
	user=models.OneToOneField(User)
	bank_name=models.CharField(max_length=200,verbose_name="Bank Name")
	bank_code=models.CharField(max_length=200,verbose_name="Bank Branch Code")
	branch=models.CharField(max_length=200,verbose_name="Bank Account Branch")
	account_name=models.CharField(max_length=200,verbose_name="Bank Account Name")
	account_number=models.CharField(max_length=200,verbose_name="Bank Account Number")
	kra_pin=models.CharField(max_length=200,verbose_name="KRA PIN")
	nhif_no=models.CharField(max_length=200,verbose_name="NHIF Number")
	laptop=models.BooleanField(default=False,verbose_name="PDTP laptop hire purchase", help_text="Check if yes")
	serial_no=models.CharField(max_length=200, null=True,blank=True,verbose_name="If Yes, Enter the serial number")
	year=models.CharField(max_length=200,default=0)
	
	def __str__(self):
		return self.user.username
	class Meta:
		verbose_name_plural='Bank Details'
auditlog.register(BankDetail)
	
class MentorMenteeMapping(models.Model):
	mentor=models.ForeignKey(User)
	mentee=models.ForeignKey(User,related_name="mentee")
	year=models.CharField(max_length=200)
	def __str__(self):
		return self.mentee.username
auditlog.register(MentorMenteeMapping)
	
class AcademicDetail(models.Model):
    user=models.ForeignKey(User)
    academic_level=models.CharField(max_length=200, choices=ACADEMIC_QUALIFICATIONS,verbose_name="Qualification")
    course_name=models.CharField(max_length=200,verbose_name="Course Name", help_text="As it appears in the certificate")
    higher_institution_attended=models.CharField(max_length=200,verbose_name="Institution",help_text="As it appears in the certificate")
    year=models.CharField(max_length=200,verbose_name="Year")
    grade=models.CharField(max_length=200,verbose_name="Grade",null=True,blank=True)
    class Meta:
        verbose_name_plural =  'PDTP Academic Details'

    def __str__(self):
        return self.user.username
auditlog.register(AcademicDetail)




class Assignment(models.Model):
		pdtp = models.ForeignKey(User,related_name="buddy_assigned")
		buddy = models.ForeignKey(User)
		reported=models.BooleanField(default=False)
		def __str__(self):
			return self.buddy.username
auditlog.register(Assignment)


	
class PDTPExitRequest(models.Model):
	pdtp=models.OneToOneField(User)
	pdtp_requested=models.BooleanField(default=False)
	exit_request=models.CharField(max_length=300,null=True,blank=True, verbose_name="Why are you leaving? If job opportunity ,which one")
	approved_by_supervisor=models.BooleanField(default=False)
	approved_by_secretariat=models.BooleanField(default=False)
	#Additional
	turn_out=models.CharField(max_length=10,null=True,blank=True,verbose_name= "Did your internship turn out to be as you expected?" )
	training=models.CharField(max_length=10,null=True,blank=True,verbose_name="Did you receive enough training to do DLP assignment effectively?")
	performance_feedback=models.CharField(max_length=10,null=True,blank=True,verbose_name="Did you receive sufficient feedback on your performance?	")
	working=models.CharField(max_length=10,null=True,blank=True,verbose_name="Would you consider working again for ICT Authority in the future?	")
	recommend=models.CharField(max_length=10,null=True,blank=True,verbose_name="Would you recommend this this program to a friend or collegue")
	#exit_request=models.CharField(max_length=300,null=True,blank=True, verbose_name="Why are you leaving? If job opportunity ,which one")
	skills=models.CharField(max_length=10,null=True,blank=True,verbose_name="This internship has helped me to develop skills to solve problems")
	interview_skills=models.CharField(max_length=10,null=True,blank=True,verbose_name="This internship has helped me to develop interviewing skills")
	dlp_skills=models.CharField(max_length=10,null=True,blank=True,verbose_name="Has the DLP program helped you to improve communication skills")	
	professional=models.CharField(max_length=10,null=True,blank=True, verbose_name="This internship has helped me to develop professional competence")
	anticipate=models.CharField(max_length=10,null=True,blank=True,verbose_name="I anticipate career advancement as a result of completing this Internship")
	satisfying=models.CharField(max_length=300,null=True,blank=True,verbose_name="What was most satisfying about the DLP and/or internship experience?")
	unsatisfying=models.CharField(max_length=300,null=True,blank=True,verbose_name="What was least satisfying about the DLP and/or internship experience?")
	suggestion=models.CharField(max_length=300,null=True,blank=True,verbose_name="What suggestions do you have to help improve the overall program and experience?")
	
	
	debriefed_by_secretariat=models.BooleanField(default=False)
	reason_for_leaving=models.TextField(verbose_name="Enter Reason For Clearing" ,null=True,blank=True)
	supervisor_comment=models.TextField(verbose_name="Enter Reason For Clearing",null=True,blank=True)
	debrief_question=models.TextField(verbose_name="Question 1",null=True,blank=True)
	date_of_request=models.DateTimeField(null=True,blank=True)
	date_approved_by_supervisor=models.DateTimeField(auto_now=True,null=True,blank=True)
	date_approved_by_secretariat=models.DateTimeField(null=True,blank=True)
	date_debriefed=models.DateTimeField(null=True,blank=True)

	def __str__(self):
		return self.pdtp.username
auditlog.register(PDTPExitRequest)
	
	
	
class PDTPCV(models.Model):
	pdtp=models.OneToOneField(User)
	cv=models.FileField(upload_to="cvs")
	def __str__(self):
		return self.pdtp.username
auditlog.register(PDTPCV)

class UpdateRequest(models.Model):
	solved=models.BooleanField(default=False)
	message=HTMLField(verbose_name="Describe your Request Here")
	pdtp=models.ForeignKey(User)
	request_date=models.DateTimeField(auto_now_add=True)
	date_solved=models.DateTimeField(auto_now=True)
	year = models.ForeignKey(PdtpYear, null=True,blank=True)
	updated_by=models.ForeignKey(User, related_name="request_solved_by_user", null=True,blank=True)

	def __str__(self):
		return self.pdtp.username
auditlog.register(UpdateRequest)

class Issue(models.Model):
	solved=models.BooleanField(default=False)
	subject=models.CharField(max_length=200,help_text="Max 200 Charcters")
	message=HTMLField(verbose_name="Describe your Issue Here")
	pdtp=models.ForeignKey(User)
	date=models.DateTimeField(auto_now_add=True) 
	year = models.ForeignKey(PdtpYear,null=True,blank=True)
	def __str__(self):
		return self.subject
auditlog.register(Issue)
class IssueStatus(models.Model):
	issue=models.ForeignKey(Issue)
	status=models.CharField(max_length=200,choices=ISSUE_STATUS)
	by=models.ForeignKey(User ,null=True,blank=True)
	comment=HTMLField()
	date=models.DateTimeField(auto_now_add=True) 
	def __str__(self):
		return self.issue.subject
auditlog.register(IssueStatus)

class Event(models.Model):
	attendees=models.CharField(max_length=200,choices=ATTENDEES)
	event=models.CharField(max_length=300,verbose_name="Event Name")
	
	start_date=models.DateTimeField(verbose_name="Sart Date/Time")
	end_date=models.DateTimeField(verbose_name="End Date/Time")
	venue=models.CharField(max_length=200)
	details=HTMLField(verbose_name="More Information")
	cancelled=models.BooleanField(default=False)
	reason=HTMLField(verbose_name="Reason For Cancelling", null=True,blank=True)
	def __str__(self):
		return self.event
auditlog.register(Event)


class SkillType(models.Model):
	skill_type = models.CharField(max_length=300,verbose_name="Skill Specialization")
	def __str__(self):
		return self.skill_type
auditlog.register(SkillType)

class SkillLevel(models.Model):
	skill_level = models.CharField(max_length=300,verbose_name="Skill Level",)
	def __str__(self):
		return self.skill_level
auditlog.register(SkillLevel)

class Project(models.Model):
	user=models.ForeignKey(User, null=True, blank= True)
	project_date = models.DateField(verbose_name="Project Start Date",null=True,blank=True)
	project_Edate = models.DateField(verbose_name="Project End Date", null=True,blank=True)
	link = models.CharField(max_length=200, null=True, blank=True,verbose_name="Project Link", help_text="https://www.example.com")
	#year = models.CharField(max_length=200)
	project_name = models.CharField(max_length=200,verbose_name="Project Name",blank= False, null=False)
	project_description = HTMLField(verbose_name="Project Details")
	def __str__(self):
		return self.project_name
auditlog.register(Project)

class Skill(models.Model):
	user=models.ForeignKey(User, null=True, blank= True)
	skill_type = models.ForeignKey(SkillType, verbose_name="skill Specilization")
	skill_level = models.ForeignKey(SkillLevel)
	skill = models.CharField(max_length=300,verbose_name="Skills Set")
	detail = models.CharField(max_length=300,verbose_name="Description")
	def __str__(self):
		return self.skill_type.skill_type

auditlog.register(Skill)

class Referee(models.Model):
	user=models.ForeignKey(User, null=True, blank= True)
	name = models.CharField(max_length=300,verbose_name="Name")
	company = models.CharField(max_length=300,verbose_name="Company")
	position = models.CharField(max_length=300,verbose_name="Position")
	phone_number =  models.CharField(max_length=100,verbose_name="Phone Number")
	email = models.EmailField(max_length=200,verbose_name="Email")
	country = models.CharField(max_length=200,verbose_name="Country" )
	town = models.CharField(max_length=200, verbose_name="Town")
	def __str__(self):
		return self.user.username

auditlog.register(Referee)



class TrainingInstitution(models.Model):
	institution 	= models.CharField(max_length=300)
	text = HTMLField(null=True,blank=True)

	def __str__(self):
		return self.institution


class TrainingStatus(models.Model):
	status 	= models.CharField(max_length=300)
	def __str__(self):
		return self.status

class TrainingCourseStatus(models.Model):
	status 	= models.CharField(max_length=300)

	class Meta:
		verbose_name_plural = 'Training Course Status'
	def __str__(self):
		return self.status
class TrainingCert(models.Model):
	cert 	= models.CharField(max_length=300)
	def __str__(self):
		return self.cert

class TrainingMode(models.Model):
	training_mode 	= models.CharField(max_length=300)
	def __str__(self):
		return self.training_mode
	class Meta:
		verbose_name_plural = 'Mode of Training'

class TrainingCategory(models.Model):
	training_category 	= models.CharField(max_length=300)
	def __str__(self):
		return self.training_category
	class Meta:
		verbose_name_plural = 'Training Category'
OPTIONS = (
		("Normal Training", "Normal Training"),
		("Certification", "Certification")
	)
class TrainingCourse(models.Model):
	secretariat = models.ForeignKey(User, related_name='admins',null=True)
	institution = models.ForeignKey(TrainingInstitution, null=True)
	category = models.ForeignKey(TrainingCategory, null=True)
	course 	= models.CharField(max_length=250, unique=True)
	status = models.ForeignKey(TrainingCourseStatus, null=True)
	description = HTMLField(null=True)
	year = models.ForeignKey(PdtpYear, null=True)
	training_option = models.CharField(max_length=200,choices=OPTIONS)
	category = models.ForeignKey(TrainingCategory, null=True,blank=True)
	course 	= models.CharField(max_length=250, unique=True)
	status = models.ForeignKey(TrainingCourseStatus, null=True,blank=True)
	description = HTMLField(null=True,blank=True)
	year = models.ForeignKey(PdtpYear, null=True,blank=True)


	def __str__(self):
		return self.course
class TrainingApplication(models.Model):
	pdtp = models.ForeignKey(User, null=True)
	category=models.ForeignKey(TrainingCategory, null=True,blank=True)
	mode = models.ForeignKey(TrainingMode,null=True)
	institution= models.ForeignKey(TrainingInstitution, null=True,verbose_name="Certification Body")
	course = models.ForeignKey(TrainingCourse, null=True, verbose_name="Course")
	status =models.ForeignKey(TrainingStatus, null=True, verbose_name="Status")
	#cert =models.ForeignKey(TrainingCert, null=True, verbose_name="Certificate")
	cert_no =models.CharField(max_length=200, default="To be changed", verbose_name="Certificate No.")
	attended_training = models.BooleanField(default=False)
	year=models.ForeignKey(PdtpYear,null=True)
	time_of_application = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = 'Prefessional Certifications'
		unique_together = ('pdtp','course',)

	def __str__(self):
		return self.pdtp.username
	
# class TrainingApplication(models.Model):
# 	pdtp = models.ForeignKey(User)
# 	institution = models.ForeignKey(TrainingInstitution, null=True,blank=True)
# 	course = models.ForeignKey(TrainingCourse)
# 	def __str__(self):
# 		return self.pdtp.username
class TrainingFeedback(models.Model):
	pdtp = models.ForeignKey(User)
	trainingapp = models.ForeignKey(TrainingCourse)
	date_submitted = models.DateField(auto_now_add=True)
	feedback = HTMLField()

	def __str__(self):
		return self.pdtp.username

CONFIRMED="CONFIRMED"
NOT_CONFIRMED="NOT_CONFIRMED"
CONFIRM_MEETING = (
    (CONFIRMED, "CONFIRMED"),
    (NOT_CONFIRMED, "NOT_CONFIRMED"))


class Meeting(models.Model):
	mentor = models.ForeignKey(User, related_name='mentor', null=True)
	mentee = models.ForeignKey(User, null=True)
	meeting_date = models.DateTimeField()
	venue = models.CharField(max_length=200)
	agenda = models.ForeignKey(MentorParameter, on_delete=models.CASCADE,null=True)
	#more_info = HTMLField(help_text='Guidance to Mentee for preparation before meeting', null=True, blank=True)
	date_booked = models.DateTimeField(auto_now_add=True)
	note = HTMLField(verbose_name="Additional Note to the Mentee")
	confirm = models.CharField(choices=CONFIRM_MEETING, max_length=200, null=True,blank=True)
	confirm_text = models.CharField(max_length=200, null=True, blank=True)
	report = HTMLField(null=True, blank=True)
	feedback = models.TextField(null=True, blank=True)
	def __str__(self):
		return str(self.agenda.parameter)
auditlog.register(Meeting)

class PDTPMentorshipReport(models.Model):
	pdtp=models.ForeignKey(User, on_delete=models.CASCADE)
	#year=models.ForeignKey(PdtpYear,null=True,blank=True)

	#mentorship_report=models.FileField(upload_to="PDTP Mentorship Reports", validators=[validate_file_extension])
	parametors = models.ForeignKey(Meeting, on_delete=models.CASCADE, null=True)
	report = HTMLField()
	def __str__(self):
		return self.parametors
auditlog.register(PDTPMentorshipReport)


class InnovationSubmission(models.Model):
	pdtp = models.ForeignKey(User)
	innovation_name = models.CharField(max_length=500, verbose_name='Innovation Name')
	industry = models.CharField(max_length=200, verbose_name='Innovation industry sector(is it health,agriculture) ')
	innovators_roles = HTMLField(verbose_name='Innovators and Roles')
	need = HTMLField(verbose_name='The need:The proposed innovation must address an existing need.Be sure to distinguish a need(necessity) and a want(a good to have).What impact would the innovation have on government,industry,citizens and the world at large if successfully implemented? ')
	option = HTMLField(verbose_name='Options:Can the need be met differently?Has someone or company addressed the same need?if so,in what way does the proposed innovation differentiate itself from existing options')
	market_potential = HTMLField(verbose_name='Market potential: Who would for the proposed innovation?Address the issue of change and adoption.If implemented what benefits (e.g savings) does it present? ')
	business_model = HTMLField(verbose_name='Business Model: Can it be commercialized and how could this be done? Who could invest in this? what is attractive about it?')
	feasiblity = HTMLField(verbose_name='Feasibility : Can it be done? if so,how? what resources are required ? does the technology exist? what about skills required? ')
	relevance = HTMLField(verbose_name='Relevance : Does it fit with the county government development strategies? Does it fit with nature of the society targeted? Can the target market easily relate to the solution?')
	how_it_works = HTMLField(verbose_name='How it works: A brief explanation on how the proposed innovation works')
	relevant_information = HTMLField()
	bibliography = HTMLField()
	appendices = HTMLField()
	date_submitted = models.DateTimeField(auto_now_add=True)
	year = models.CharField(max_length=10,default=2018)

	def __str__(self):
		return self.innovation_name
auditlog.register(InnovationSubmission)

class InnovationTeam(models.Model):
	pdtp = models.ForeignKey(User)
	innovation = models.ForeignKey(InnovationSubmission)

	def __str__(self):
		return self.pdtp.username


class ReportComment(models.Model):
	mentor = models.ForeignKey(User, related_name='comment', on_delete=models.CASCADE, null=True, blank=True)
	mentee=models.ForeignKey(User, on_delete=models.CASCADE)
	mentorship_report = models.ForeignKey(PDTPMentorshipReport, on_delete=models.CASCADE)
	parametor = models.ForeignKey(Meeting, on_delete=models.CASCADE)
	comment = HTMLField()
	date_submitted = models.DateTimeField(auto_now_add=True)

	def __str__ (self):
		return self.mentor.username
auditlog.register(ReportComment)


class ExitParameter(models.Model):
	year = models.ForeignKey(PdtpYear)
	parameter = models.CharField(max_length=200)
	def __str__(self):
		return self.parameter

class ExitRateParameter(models.Model):
	year = models.ForeignKey(PdtpYear)
	parameter = models.CharField(max_length=200)
	def __str__(self):
		return self.parameter

class ExitSingleQuestionParameter(models.Model):
	year = models.ForeignKey(PdtpYear)
	parameter = models.CharField(max_length=200)
	def __str__(self):
		return self.parameter


class ExitSubmitted(models.Model):
	pdtp = models.ForeignKey(User)
	parameter= models.ForeignKey(ExitParameter)
	jibu = models.CharField(max_length= 500)

	def __str__(self):
		return self.pdtp.username



class ExitRateSubmited(models.Model):
	pdtp = models.ForeignKey(User)
	parameter= models.ForeignKey(ExitRateParameter)
	jibu = models.CharField(max_length= 500)

	def __str__(self):
		return self.pdtp.username

class ExitSingleSubmitted(models.Model):
	pdtp = models.ForeignKey(User)
	parameter= models.ForeignKey(ExitSingleQuestionParameter)
	jibu = models.CharField(max_length= 500)

	def __str__(self):
		return self.pdtp.username


class ExitR(models.Model):
	pdtp = models.OneToOneField(User)
	solved = models.BooleanField(default=False)
	date = models.DateTimeField(auto_now_add=True)
	approved_by_sec= models.ForeignKey(User, null=True,blank=True, related_name="approved_by")
	date_approved = models.DateTimeField(null=True,blank=True)
	reason_for_leaving=models.TextField(verbose_name="Enter Reason For Clearing" ,null=True,blank=True)
	supervisor_comment=models.TextField(verbose_name="Enter Reason For Clearing",null=True,blank=True)
	date_approved_by_supervisor=models.DateTimeField(auto_now=True,null=True,blank=True)
	
	def __str__(self):
		return self.pdtp.username



class LeaveType(models.Model):
	leave_type = models.CharField(max_length=200)
	def __str__(self):
		return self.leave_type

class Leave(models.Model):
	pdtp = models.ForeignKey(User)
	leave_type = models.ForeignKey(LeaveType)
	application_date = models.DateTimeField(auto_now_add=True)
	start_date = models.DateField(verbose_name="Leave Start Date")
	end_date = models.DateField(verbose_name="Leave End Date")
	desk_office = models.CharField(max_length=200, verbose_name="Desk Office", null=True, blank="True")
	leave_details = models.TextField(verbose_name="Leave Details", null=True, blank="True")
	supervisor = models.ForeignKey(User, related_name="leave_approved_by_supervisor", null=True, blank=True)
	supervisor_recommmended_days = models.CharField(max_length=10, verbose_name="Recommended Days", null=True, blank=True)
	duties_delagated_to = models.CharField(max_length=200, null=True, blank=True)
	approved_by_supervisor = models.BooleanField(default=False, verbose_name="Approve")
	supervisor_comment = models.TextField(null=True, blank=True)
	date_approved_by_supervisor= models.DateTimeField(auto_now_add=True)

	internship_contract_date = models.DateField(null=True, blank=True, verbose_name="Date of Internship Contract")
	leave_days_balance= models.CharField(max_length=200,null=True, blank=True, verbose_name="Annual Leave Days Balance")
	
	recommended = models.BooleanField(default=False)
	date_approved_by_secretariat = models.DateTimeField(auto_now_add=True)
	secretariat_comment = models.TextField(verbose_name="Comment", null=True,blank=True)
	secretariat = models.ForeignKey(User, related_name="leave_approved_by_secretariat",null=True,blank=True)
	number_of_days = models.CharField(max_length=10,null=True, blank=True)
	attachment = models.FileField(null=True, blank=True, verbose_name="Attach supporting ")
	year = models.CharField(max_length=10, null=True,blank=True)


	def __str__(self):
		return self.pdtp.username
	def save(self,*args,**kwargs):
		a = self.start_date
		b = self.end_date
		self.number_of_days = (b-a).days
		super(Leave, self).save(*args,**kwargs)
	
	@staticmethod
	def remaining_days(user):
		leaves = Leave.Objects.filter(pdtp =user)
		days = 0
		for leave in leaves:
			days += int(leave.number_of_days)

		return 15 - days



class Message(models.Model):
	recipient = models.ForeignKey(User, related_name="recipient")
	sender = models.ForeignKey(User, related_name="sender")
	subject = models.CharField(max_length=200, blank=True)
	message = models.TextField(blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	sent = models.BooleanField(default=True)

	def __str__(self):
		return 'message from ' + str(self.sender) + '.  Subject ' + str(self.subject)



FEMALE="FEMALE"
MALE="MALE"
PDTPS="PDTPS"
SUPERVISORS="SUPERVISORS"
MENTORS="MENTORS"
ALL="ALL"

RECIPIENT = (
(PDTPS,"PDTPS"),
(SUPERVISORS,"SUPERVISORS"),
(MENTORS,"MENTORS"),
(FEMALE,'FEMALE'),
(MALE,'MALE'),
(ALL,"ALL"))



class Broadcast(models.Model):
	subject = models.CharField(max_length=500)
	sent_by = models.ForeignKey(User)
	message = HTMLField()
	timestamp = models.DateTimeField(auto_now_add=True)
	recipient = models.CharField(max_length=200, choices=RECIPIENT)
	year = models.ForeignKey(PdtpYear, verbose_name="Cohort Year")
	attachment = models.FileField(verbose_name='Attachment',null=True,blank=True )
	class Meta:
		ordering = ('-timestamp',)
	def __str__(self):
		return self.subject



class InnovationEvaluationParameter(models.Model):
	parameter = models.CharField(max_length=500)
	description = models.TextField()
	def __str__(self):
		return self.parameter


class InnovationEvaluationData(models.Model):
	evaluator = models.ForeignKey(User)
	innovation = models.ForeignKey(InnovationSubmission)
	parameter = models.ForeignKey(InnovationEvaluationParameter)
	score = models.IntegerField()
	comment = models.CharField(max_length=1000)
	datetime = models.DateField(auto_now_add=True)
	def __str__(self):
		return self.innovation.innovation_name

	
class InnovationEvaluationPerParam(models.Model):
	innovation = models.ForeignKey(InnovationSubmission)
	parameter = models.ForeignKey(InnovationEvaluationParameter)
	total_score = models.IntegerField(default=0)
	evaluators = models.IntegerField(default=1,null=True)
	average = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
	def __str__(self):
		return self.innovation.innovation_name

	def save(self,*args,**kwargs):
		total = self.total_score
		number = self.evaluators
		self.average = (total/number)
		super(InnovationEvaluationPerParam, self).save(*args,**kwargs)

	




class ApplicationCategory(models.Model):
	category = models.CharField(max_length=200)
	def __str__(self):
		return self.category

class JobApps(models.Model):
	pdtp = models.ForeignKey(User)
	application_category = models.ForeignKey(ApplicationCategory, verbose_name="Applying For?")
	def __str__(self):
		return self.pdtp.username
#Laptop
LAPTOPSTATUS = (
		('available','Available'),
		('out of stock','Out of stock'),
	)
class Laptop(models.Model):
	created_by  = models.ForeignKey(User)
	laptop_name = models.CharField(max_length=200)
	MAC = models.CharField(max_length=200,null=True,blank=True)
	serial_no = models.CharField(max_length=200,null=True,blank=True)
	RAM = models.CharField(max_length=200)
	HDD = models.CharField(max_length=200)
	Processor_Speed = models.CharField(max_length=200)
	Cores = models.CharField(max_length=200,verbose_name="Processor")
	screen_resolution = models.CharField(max_length=200, verbose_name="Screen Resolution")
	other_features = models.CharField(max_length=500, verbose_name="Other Features", help_text="bluetooth,wifi,webcam")
	status = models.CharField(max_length=200,choices=LAPTOPSTATUS, null=True)
	price = models.DecimalField(max_digits=7,decimal_places=2)
	

	def __str__(self):
		return self.laptop_name

class LaptopOrder(models.Model):
	pdtp = models.ForeignKey(User)
	order = models.BooleanField(default=False)
	laptop = models.ForeignKey(Laptop)
	Amount_Due = models.DecimalField(max_digits=7,decimal_places=2)
	deductions = models.DecimalField(max_digits=7,decimal_places=2,null=True)
	order_date = models.DateTimeField(auto_now_add=True)
	year = models.ForeignKey(PdtpYear, verbose_name="Cohort Year")

	def __str__(self):
		return self.pdtp.username


class PaymentHistory(models.Model):
	pdtp = models.ForeignKey(User)
	order = models.ForeignKey(LaptopOrder)
	payment = models.DecimalField(max_digits=7,decimal_places=2)
	payment_date = models.DateTimeField(auto_now_add=True)
	updated_by = models.ForeignKey(User, related_name='payments')

	def __str__(self):
		return self.pdtp.username







class InterRequest(models.Model):
	company = models.CharField(max_length=300,verbose_name='Your Company Name')
	profile = models.TextField(verbose_name='Company Profile. include website link')
	contact_person = models.CharField(max_length=200, verbose_name="Contact Person Name")
	contact = models.IntegerField( verbose_name="Contact Person Phone Number")
	email = models.EmailField(verbose_name="Contact Person Email")
	number = models.IntegerField(verbose_name="Number of Interns Needed")
	specialization = models.CharField(max_length=500, verbose_name="Area of Specialization e.g Networking")
	job_description = models.CharField(max_length=100,verbose_name="Job Description of the Intern")
	date_submitted = models.DateTimeField(auto_now_add=True)
	handled = models.BooleanField(default=False)
	def __str__(self):
		return self.company

class PartnershipCategory(models.Model):
	category = models.CharField(max_length=200)
	def __str__(self):
		return self.category
class PartnerApply(models.Model):
	partnership = models.TextField()
	company = models.CharField(max_length=300,verbose_name='Your Company Name')
	profile = models.TextField(verbose_name='Company Profile. include website link')
	contact_person = models.CharField(max_length=200, verbose_name="Contact Person Name")
	contact = models.IntegerField( verbose_name="Contact Person Phone Number")
	email = models.EmailField(verbose_name="Contact Person Email")
	details = models.TextField()
	date_submitted = models.DateTimeField(auto_now_add=True)
	handled = models.BooleanField(default=False)
	def __str__(self):
		return self.company

class SuccessStory(models.Model):
	publish = models.BooleanField(default=False)
	name = models.CharField(max_length=200)
	role = models.CharField(max_length=200)
	organization = models.CharField(max_length=200)
	description = HTMLField()
	content = HTMLField()
	photo = models.ImageField(upload_to="photos", null=True,blank=True)
	date = models.DateTimeField(auto_now_add=True,  null=True,blank=True)
	slug=models.SlugField(unique=False,blank=True,null=True)

	def __str__(self):
		return self.name
	def save(self,*args,**kwargs):
		self.slug=slugify(self.name)
		super(SuccessStory, self).save(*args,**kwargs)