from django.shortcuts import render,render_to_response,get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from performance.models import *
from app.models import *
from performance.forms import *
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.contrib.auth.models import User
from post_office import mail
from django.template.loader import render_to_string, get_template
@login_required
def my_performance(request):
	user=request.user
	me=UserProfile.objects.get(user=user)
	if not user.userprofile.is_pdtp(me):
		raise Http404
	if request.method == "POST":
		form = MentorshipReportForm(request.POST,request.FILES)
		# if form.is_valid():
		f = form.save(commit=False)
		f.pdtp =user 
		f.save()
		messages.add_message(request, messages.SUCCESS, 'Record Added Successfully')
		return HttpResponseRedirect('/performance/my_performance/')
	else:
		form =MentorshipReportForm()
		return render(request,'performance/pdtp/index.html',{'form':form})



@login_required
def mentorship_performance_feedback(request):
	user=request.user
	me=UserProfile.objects.get(user=user)
	if not user.userprofile.is_pdtp(me):
		raise Http404
	mentor = MentorMenteeMapping.objects.filter(mentee=user).first()
	if request.method == "POST":
		form = MentorshipInternReportForm(request.POST,request.FILES)
		# if form.is_valid():
		f = form.save(commit=False)
		f.pdtp =user
		f.mentor = mentor.mentor
		f.save()
		messages.add_message(request, messages.SUCCESS, 'Report submitted  Successfully')
		return HttpResponseRedirect('/performance/mentorship-performance-feedback/')
	else:
		form =MentorshipInternReportForm()
		return render(request,'performance/pdtp/feedback.html',{'form':form})


@login_required
def ministry_activities(request):
	user=request.user
	me=UserProfile.objects.get(user=user)
	if not user.userprofile.is_pdtp(me):
		raise Http404

	if request.method == "POST":
		x = request.POST.getlist('pdtps')
		for sup in x:
			supa = User.objects.get(username=sup)
			SupervisorToEvaluate.objects.create(pdtp=user,supervisor=supa)
		messages.add_message(request, messages.SUCCESS, 'Record Added Successfully')
		return HttpResponseRedirect('/performance/ministry_activities/')

	#total_mini_score =int(min_score.attendance.score) + float(min_score.meeting.score)+ int(min_score.report.score)

	

	return render(request,'performance/pdtp/ministry.html',{})




@login_required
def add_ministry_activities(request ):
	user=request.user
	me=UserProfile.objects.get(user=user)
	if not user.userprofile.is_pdtp(me):
		raise Http404
	if request.method == 'POST':
		form=MinistryReportForm(request.POST )
		# uform = UploadForm(request.FILES)
		if form.is_valid():
			u=form.save(commit=False)
			# try:
			# 	for afile in request.FILES.getlist('attachments'):
			# 		ReportAttachment(file=afile, pdtp=user).save()
			# except:
			# 	pass
			u.pdtp =user
			u.save()
		messages.add_message(request, messages.SUCCESS, 'Record Added Successfully')
		return HttpResponseRedirect('/performance/ministry_activities/')
	
	else:
		form=MinistryReportForm( )
		# uform = UploadForm()
	return render(request, 'performance/pdtp/add_min.html', {'form':form,
    })
			
	
@login_required
def add_evidence(request):
	user=request.user
	me=UserProfile.objects.get(user=user)
	if not user.userprofile.is_pdtp(me):
		raise Http404
	EvidenceFormSet = modelformset_factory(WorkAssignmentEvidence, form=EvidenceForm)
	if request.method == 'POST':
		formset = EvidenceFormSet(request.POST)
		form=WorkAssignmentForm(request.POST)
		try:
			if  form.is_valid():
				m= form.save(commit=False)
				m.pdtp=user
				for fs in formset:
					f=fs.save(commit=False)
					f.pdtp=request.user
					f.save()
				m.save()
				messages.add_message(request, messages.SUCCESS, 'Record Added Successfully')
		except:
			messages.add_message(request, messages.WARNING, 'Not  Added, please fill required')
		return HttpResponseRedirect('/performance/ministry_activities/')
	else:
		formset = EvidenceFormSet(queryset=WorkAssignmentEvidence.objects.none())
		form = WorkAssignmentForm()
	return render(request, 'performance/pdtp/addevidence.html', {'form':form,'formset': formset,
    })
	



	
@login_required
def add_additional(request):
	user=request.user
	me=UserProfile.objects.get(user=user)
	if not user.userprofile.is_pdtp(me):
		raise Http404
	AdditionalFormSet = modelformset_factory(AdditionalActivity, form=AdditionalActivityForm)
	if request.method == 'POST':
		formset = AdditionalFormSet(request.POST)
		if formset.is_valid():
			for form in formset:
				f=form.save(commit=False)
				f.pdtp=request.user
				f.save()
			messages.add_message(request, messages.SUCCESS, 'Record Added Successfully')
			return HttpResponseRedirect('/performance/ministry_activities/')
	else:
		formset = AdditionalFormSet(queryset=AdditionalActivity.objects.none())
	return render(request, 'performance/pdtp/additional.html', {'formset': formset,
    })
	
@login_required
def add_flagship_project(request):
	user=request.user
	me=UserProfile.objects.get(user=user)
	if not user.userprofile.is_pdtp(me):
		raise Http404
	TransformationFormSet = modelformset_factory(Transformation, form=TransformationForm)
	if request.method == 'POST':
		formset = TransformationFormSet(request.POST)
		if formset.is_valid():
			for form in formset:
				f=form.save(commit=False)
				f.pdtp=request.user
				f.save()
			messages.add_message(request, messages.SUCCESS, 'Record Added Successfully')
			return HttpResponseRedirect('/performance/ministry_activities/')
	else:
		formset = TransformationFormSet(queryset=Transformation.objects.none())
	return render(request, 'performance/pdtp/transform.html', {'formset': formset,
    })
	

@login_required
def add_private_project(request):
	user=request.user
	me=UserProfile.objects.get(user=user)
	if not user.userprofile.is_pdtp(me):
		raise Http404
	PrivateProjectFormSet = modelformset_factory(PrivateProject, form=PrivateProjectForm)
	if request.method == 'POST':
		formset = PrivateProjectFormSet(request.POST)
		if formset.is_valid():
			for form in formset:
				f=form.save(commit=False)
				f.pdtp=request.user
				f.save()
			messages.add_message(request, messages.SUCCESS, 'Record Added Successfully')
			return HttpResponseRedirect('/performance/private_sector_activities/')
	else:
		formset = PrivateProjectFormSet(queryset=Transformation.objects.none())
	return render(request, 'performance/pdtp/project.html', {'formset': formset,
    })
#Private Sector Reports Pages
@login_required
def private_sector_activities(request):
	user=request.user
	me=UserProfile.objects.get(user=user)
	if not user.userprofile.is_pdtp(me):
		raise Http404
	return render(request,'performance/pdtp/private.html',{})

@login_required
def add_private_attendance(request ):
	user=request.user
	me=UserProfile.objects.get(user=user)
	if not user.userprofile.is_pdtp(me):
		raise Http404
	if request.method == 'POST':
		form=PrivateSectorAttendanceForm(request.POST, request.FILES)
		if form.is_valid():
			u=form.save(commit=False)
			u.pdtp =user
			try:
				request.FILES['attachment']
				newdoc=PrivateSectorAttendance(attachment = request.FILES['attachment'])
				return   newdoc.save()
			except:
				pass
			
			u.save()
		messages.add_message(request, messages.SUCCESS, 'Record Added Successfully')
		return HttpResponseRedirect('/performance/private_sector_activities/')
	
	else:
		form=PrivateSectorAttendanceForm( )
	return render(request, 'performance/pdtp/add_pattend.html', {'form':form
    })
			
@login_required
def add_soft_training(request):
	user=request.user
	me=UserProfile.objects.get(user=user)
	if not user.userprofile.is_pdtp(me):
		raise Http404
	PrivateOnJobTrainingFormSet = modelformset_factory(PrivateOnJobTraining, form=PrivateOnJobTrainingForm)
	if request.method == 'POST':
		formset = PrivateOnJobTrainingFormSet(request.POST)
		if formset.is_valid():
			for form in formset:
				f=form.save(commit=False)
				f.pdtp=request.user
				f.save()
			messages.add_message(request, messages.SUCCESS, 'Record Added Successfully')
			return HttpResponseRedirect('/performance/private_sector_activities/')
	else:
		formset = PrivateOnJobTrainingFormSet(queryset=PrivateOnJobTraining.objects.none())
	return render(request, 'performance/pdtp/onjob.html', {'formset': formset,
    })

@login_required
def add_org_training(request):
	user=request.user
	me=UserProfile.objects.get(user=user)
	if not user.userprofile.is_pdtp(me):
		raise Http404
	PrivateTrainingFormSet = modelformset_factory(PrivateTraining, form=PrivateTrainingForm)
	if request.method == 'POST':
		formset = PrivateTrainingFormSet(request.POST, request.FILES)
		if formset.is_valid():
			for form in formset:
				f=form.save(commit=False)
				f.pdtp=request.user
				try:
					request.FILES['attachment']
					newdoc=PrivateTraining(attachment = request.FILES['attachment'])
					return   newdoc.save()
				except:
					pass
				f.save()
			messages.add_message(request, messages.SUCCESS, 'Record Added Successfully')
			return HttpResponseRedirect('/performance/private_sector_activities/')
	else:
		formset = PrivateTrainingFormSet(queryset=PrivateTraining.objects.none())
	return render(request, 'performance/pdtp/orgtrain.html', {'formset': formset,
    })

@login_required
def supervisor_evaluate(request, id):
	user=request.user
	pdtp=User.objects.get(id=id)
	parameters =Parameter.objects.all()
	form = SupervisorCommentForm()
	if request.method == "POST":
		form=SupervisorCommentForm(request.POST)
		f=form.save(commit=False)
		f.pdtp =pdtp
		f.supervisor =user
		try:

			for p in parameters:
				k =str(p.id)
				score =  request.POST.get(k)
				PrivateSupervisorEvaluation.objects.create(pdtp=pdtp,parameter=p,score=score,supervisor=user)
			f.save()
			messages.add_message(request, messages.SUCCESS, 'You have successfully evaluated the intern. Thank you for your time')
		except:
			messages.add_message(request, messages.WARNING, 'Data not Submitted ')
		from_email = 'pdtp@ict.go.ke'
		template_html = 'performance/private_email.html'
		template_text = 'performance/private_email.txt'
		subject ="Evaluation"
		text_content = render_to_string(template_text, {"subject":subject,
		            'first_name':pdtp.first_name,
		            'last_name':pdtp.last_name})
		html_content = render_to_string(template_html, {"subject":subject,
		        'first_name':pdtp.first_name,
		        'last_name':pdtp.last_name, })
		mail.send(
		[pdtp.email],
		from_email,
		 subject=subject,
		 html_message=html_content,
		)
		return HttpResponseRedirect('/deployments/my_interns/')
	return render(request, 'performance/private/evaluate.html', {'form':form,'pdtp':pdtp,'parameters':parameters})

@login_required
def supervisor_approval(request, id):
	user=request.user
	
	pdtp=User.objects.get(id=id)
	try:
		attendance =PrivateSectorAttendance.objects.get(pdtp=pdtp)
	except:
		attendance=""
	try:
		onjobs =PrivateOnJobTraining.objects.filter(pdtp=pdtp)
	except:

		onjobs =""
	try:
		trainings =PrivateTraining.objects.filter(pdtp=pdtp)
	except:
		trainings=""
	try:
		projects =PrivateProject.objects.filter(pdtp=pdtp)
	except:
		projects=""
	form = SupervisorApprovalCommentForm()
	if request.method == "POST":
		form=SupervisorApprovalCommentForm(request.POST)
		f=form.save(commit=False)
		f.pdtp =pdtp
		f.supervisor =user
		#att =PrivateSectorAttendance.objects.get(pdtp=pdtp).update(supervisor_approved=True,
			#supervisor=user)
		onjob =PrivateOnJobTraining.objects.filter(pdtp=pdtp).update(supervisor_approved=True,
			supervisor=user)
		training =PrivateTraining.objects.filter(pdtp=pdtp).update(supervisor_approved=True,
			supervisor=user)
		f.save()
		from_email = 'pdtp@ict.go.ke'
		template_html = 'performance/private_email.html'
		template_text = 'performance/private_email.txt'
		subject ="Evaluation"
		text_content = render_to_string(template_text, {"subject":subject,
		            'first_name':pdtp.first_name,
		            'last_name':pdtp.last_name})
		html_content = render_to_string(template_html, {"subject":subject,
		        'first_name':pdtp.first_name,
		        'last_name':pdtp.last_name, })
		mail.send(
		[pdtp.email],
		from_email,
		 subject=subject,
		 html_message=html_content,
		)
		messages.add_message(request, messages.SUCCESS, 'You have successfully evaluated the intern. Thank you for your time')
		return HttpResponseRedirect('/deployments/my_interns/')
	return render(request, 'performance/private/sup_approve.html', {'form':form,
		'pdtp':pdtp,'attendance':attendance,'projects':projects,
		'onjobs':onjobs,'trainings':trainings})

@login_required
def public_supervisor_evaluate(request, id):
	user=request.user
	pdtp=User.objects.get(id=id)
	parameters =Parameter.objects.all()
	form = BuddyCommentForm()
	if request.method == "POST":
		form=BuddyCommentForm(request.POST)
		f=form.save(commit=False)
		f.pdtp =pdtp
		f.supervisor =user
		try:

			for p in parameters:
				k =str(p.id)
				score =  request.POST.get(k)
				PublicSupervisorEvaluation.objects.create(pdtp=pdtp,parameter=p,score=score,supervisor=user)
			f.save()
			messages.add_message(request, messages.SUCCESS, 'Record Added Successfully')
		except:
			messages.add_message(request, messages.WARNING, 'Data not Submitted ')
		from_email = 'pdtp@ict.go.ke'
		template_html = 'performance/private_email.html'
		template_text = 'performance/private_email.txt'
		subject ="Evaluation"
		text_content = render_to_string(template_text, {"subject":subject,
		            'first_name':pdtp.first_name,
		            'last_name':pdtp.last_name})
		html_content = render_to_string(template_html, {"subject":subject,
		        'first_name':pdtp.first_name,
		        'last_name':pdtp.last_name, })
		mail.send(
		[pdtp.email],
		from_email,
		 subject=subject,
		 html_message=html_content,
		)
		return HttpResponseRedirect('/deployments/my_interns/')
	return render(request, 'performance/private/evaluate.html', {'form':form,'pdtp':pdtp,'parameters':parameters})

@login_required
def public_supervisor_approval(request, id):
	user=request.user
	pdtp=User.objects.get(id=id)
	try:
		attendance =MinistryReport.objects.get(pdtp=pdtp)
	except:
		attendance=""
	try:
		assignments =WorkAssignmentEvidence.objects.filter(pdtp=pdtp)
	except:
		assignments=""
	try:
		additional =AdditionalActivity.objects.filter(pdtp=pdtp)
	except:
		additional =""
	try:
		flagships =Transformation.objects.filter(pdtp=pdtp)
	except:
		flagships=""
	form = BuddyApprovalCommentForm()
	if request.method == "POST":
		form=BuddyApprovalCommentForm(request.POST)
		f=form.save(commit=False)
		f.pdtp =pdtp
		f.supervisor =user
		#att =PrivateSectorAttendance.objects.get(pdtp=pdtp).update(supervisor_approved=True,
			#supervisor=user)
		onjob =WorkAssignmentEvidence.objects.filter(pdtp=pdtp).update(supervisor_approved=True,
			supervisor=user)
		training =AdditionalActivity.objects.filter(pdtp=pdtp).update(supervisor_approved=True,
			supervisor=user)
		training =Transformation.objects.filter(pdtp=pdtp).update(supervisor_approved=True,
			supervisor=user)
		f.save()
		from_email = 'pdtp@ict.go.ke'
		template_html = 'performance/private_email.html'
		template_text = 'performance/private_email.txt'
		subject ="Evaluation"
		text_content = render_to_string(template_text, {"subject":subject,
		            'first_name':pdtp.first_name,
		            'last_name':pdtp.last_name})
		html_content = render_to_string(template_html, {"subject":subject,
		        'first_name':pdtp.first_name,
		        'last_name':pdtp.last_name, })
		mail.send(
		[pdtp.email],
		from_email,
		 subject=subject,
		 html_message=html_content,
		)
		messages.add_message(request, messages.SUCCESS, 'Submitted Successfully')
		return HttpResponseRedirect('/deployments/my_interns/')
	return render(request, 'performance/private/psup_approve.html', {'form':form,
		'pdtp':pdtp,'attendance':attendance,
		'assignments':assignments,'additional':additional,'flagships':flagships})


@login_required
def mentor_evaluate(request, id):
	user=request.user
	pdtp=User.objects.get(id=id)
	parameters =MentorParameter.objects.all()
	form = MentorMeetingForm()
	eform =MentorCommentForm()
	if request.method == "POST":
		form = MentorMeetingForm(request.POST)
		eform =MentorCommentForm(request.POST)
		u=eform.save(commit=False)
		f=form.save(commit=False)
		f.pdtp=pdtp
		u.pdtp =pdtp
		u.mentor =user
		f.save()
		u.save()
		for p in parameters:
			k =str(p.id)
			score =  request.POST.get(k)
			MentorEvaluation.objects.create(pdtp=pdtp,parameter=p,score=score,mentor=user)

		messages.add_message(request, messages.SUCCESS, 'You have successfully evaluated the intern. Thank you for your time')
		#except:
			#messages.add_message(request, messages.WARNING, 'Data not Submitted ')
		return HttpResponseRedirect('/deployments/my_mentees/')
		from_email = 'pdtp@ict.go.ke'
		template_html = 'performance/mentor_email.html'
		template_text = 'performance/mentor_email.txt'
		subject ="Evaluation"
		text_content = render_to_string(template_text, {"subject":subject,
		            'first_name':pdtp.first_name,
		            'last_name':pdtp.last_name})
		html_content = render_to_string(template_html, {"subject":subject,
		        'first_name':pdtp.first_name,
		        'last_name':pdtp.last_name, })
		mail.send(
		[pdtp.email],
		from_email,
		 subject=subject,
		 html_message=html_content,
		)
	return render(request, 'performance/private/mentor.html', {'form':form,
		'eform':eform,'pdtp':pdtp,'parameters':parameters})

@login_required
def innovations(request,year):
    user=request.user
    year =PdtpYear.objects.get(year=year)
    all_pdtps=UserProfile.get_pdtps().filter(year=year).exclude(user__id__in = InnovationEvaluation.objects.all().values_list('pdtp', flat=True))
    if request.method == 'POST':
    	form = InnovationsForm(request.POST)
    	if form.is_valid():
    		pdtps_list=request.POST.getlist('pdtps')
    		initiative = request.POST['initiative']
    		presentation =request.POST['presentation']
    		evaluation = request.POST['evaluation']
    		final = request.POST['final']
    		form = form.save(commit=False)
    		for pdtp in pdtps_list:
    			get_pdtp=User.objects.get(username=pdtp)
    			pdtp = InnovationEvaluation.objects.create(pdtp=get_pdtp,final=final,initiative=initiative,
    				presentation=presentation,evaluation=evaluation)
    		messages.add_message(request, messages.SUCCESS, 'Record Added Successfully')
    		return HttpResponseRedirect('.')
    else:
    	form = InnovationsForm()
    return render(request,'secretariat/innovations.html',{'year':year,'form':form,'pdtps':all_pdtps})

def pdtps_performance(request,year):
    #company=Organization.objects.get(id=id)
    #raise 
    y=PdtpYear.objects.get(year=year)
    pdtps =UserProfile.get_pdtps().filter(year=y, active=True)
    for obj in pdtps:
    	try:
    		inn = InnovationEvaluation.objects.get(pdtp=obj.user)
    		t = round(inn.total,2)
    	except:
    		t = 0.0
    	obj.total = float(obj.mentor_evaluation()) +float(t)+float(obj.private_evaluation())+float(obj.public_evaluation())+float(obj.training_evaluation())
    	obj.new_total =round(obj.total,2)
    return render(request,'performance/secretariat/performance.html',{'year':year,'pdtps':pdtps})



@login_required
def innovation_performance(request):
	innovations=InnovationEvaluation.objects.all()
	return render(request,'performance/secretariat/innovations.html',{'innovations':innovations})
@login_required
def pivate_performance(request):
    return render(request,'performance/secretariat/privates.html',{})
@login_required
def public_performance(request):
    return render(request,'performance/secretariat/publics.html',{})
@login_required
def mentors_performance(request):
    return render(request,'performance/secretariat/mentors.html',{})
@login_required
def training_performance(request):

    return HttpResponseRedirect('/app/2016/trainings/')



@login_required
def pdtp_performance(request,year,id):

    user=request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    user_year=PdtpYear.objects.get(year=year)
    pdtp= User.objects.get(id=id)
    return render(request,'performance/secretariat/pdtp_performance.html',{'year':user_year,'pdtp':pdtp})


def programme_evaluation(request):
	if request.method == 'POST':
		form = BasicForm(request.POST)
		if form.is_valid():
			form.save()
	else:
		form = BasicForm()
		return render(request,'landing2/programme_evaluation.html',{'form':form})

