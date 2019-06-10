
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import View

from pdtpproject.utils import render_to_pdf

from django.shortcuts import render,render_to_response,get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template import RequestContext
from django.contrib import messages
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from app.forms import *
#from deployments.models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout
from django.db.models import Max, F
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.db.models import Count
from deployments.models import *
from deployments.forms import *
from hashlib import sha1
from post_office import mail
from django.utils import timezone
from django import forms
from django.utils.http import is_safe_url
import datetime
today = datetime.datetime.today()
from django.contrib.auth.views import login
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.db import IntegrityError, transaction
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.core.mail import send_mail
from django.template.loader import render_to_string, get_template
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.tasks import *
from pdtpproject import settings
from weasyprint import HTML
import tempfile
import random
#from app.forms import BaseTestFormSet
def index(request):
    successs = SuccessStory.objects.filter(publish=True)[:6]
    return render(request, 'landing/index.html',{'successs':successs,'nbar':'home'} )

def about(request):
    return render(request, 'landing/about.html', )
def partners(request):
    partners = Partner.objects.all()
    return render(request, 'landing2/partners.html',{'partners':partners} )

def stories(request):
    context_dict={}
    stories =SuccessStory.objects.all()
    context_dict['stories']=stories
    # try:
    #     news =paginator.page(page)
    #     context_dict['news']=news
    # except PageNotAnInteger:
    #     news=paginator.page(1)
    #     context_dict['news']=news
    # except EmptyPage:
    #     news=paginator.page(paginator.num_pages)
    #     context_dict['news']=news
    return render(request,'landing2/stories.html',context_dict)
def story(request,id,slug):
    story = SuccessStory.objects.get(id=id)
    stories =SuccessStory.objects.exclude(id=story.id)
    return render(request, 'landing2/story.html',{'story':story, 'stories':stories} )

def partners_application(request):
    raise Http404
    if request.method == "POST":
        post = PartnerApplication()
        post.organization_name = request.POST.get('organization-name')
        post.full_name = request.POST.get('full-name')
        post.position = request.POST.get('position')
        post.department = request.POST.get('department')
        post.address = request.POST.get('address')
        post.office_tel = request.POST.get('tel-number')
        post.mobile = request.POST.get('mobile')
        post.office_mail = request.POST.get('office-email')
        post.email = request.POST.get('email')
        post.telephone = request.POST.get('tel-person-contact')
        post.partnership_category = request.POST.get('partnership-categories')
        post.mentor_intern = request.POST.get('mentor-an-intern')
        post.speaker = request.POST.get('motivate-intern')
        post.trainer = request.POST.get('life-skills')
        post.panelist = request.POST.get('innovation-evaluation')
        post.legal_support = request.POST.get('legal-support')
        post.save()
        messages.add_message(request, messages.SUCCESS, 'You have successfully Submitted  Partner application form')

        return  render(request, 'landing/partnersapplication.html',{})
    else:
        return render(request, 'landing/partnersapplication.html',{})

    return render(request, 'landing/partnersapplication.html',{})

def mentorship(request):
    return render(request, 'landing2/mentorship.html',{})

def mentorship_application(request):
    # form = MentorshipApplicationForm()
    if request.method == "POST":
        # form = MentorshipApplicationForm(request.POST)
        post = MentorshipApplication()
        post.full_name = request.POST.get('full-name')
        post.email = request.POST.get('email')
        post.mobile = request.POST.get('mobile')
        post.company = request.POST.get('company')
        post.position = request.POST.get('position')
        post.academic_profile = request.POST.get('academic')
        post.academic_qualifications = request.POST.get('academic-qualification')
        post.work_experience = request.POST.get('years')
        post.technical_position = request.POST.getlist('position-technical')
        post.achievement = request.POST.get('achievements')
        post.ethics = request.POST.get('ethics')
        post.criminally_liable = request.POST.get('criminal')
        post.availability = request.POST.get('frequent')
        post.shortest_out_of_country = request.POST.get('shortest')
        post.longest_out_of_country = request.POST.get('longest')
        post.personal_obligation = request.POST.get('obligation')
        post.commitment = request.POST.get('handle-mentorship')
        post.suggestions = request.POST.get('suggestions')
        # if form.is_valid():
        #     form.save()
        post.save()

        message = "Mentorship application submission" #to be populated with data eg email name
        email = "mentors@ict.go.ke"
        from_email = 'pdtp@ict.go.ke'
        mail.send([email], from_email,
                    subject="Mentorship application submission",
                    # message='Hi there! Your mentee has responded to your a meeting you scheduled. Log on to the portal to view his response',
                    message=message,
                    )
        messages.add_message(request, messages.SUCCESS, 'Message Sent Successfully')
                    
        return HttpResponseRedirect('/app/index/')
        messages.add_message(request, messages.SUCCESS, 'You have successfully Submitted  Mentorship application form')

        return  render(request, 'landing/mentorshipapplication.html',{'form':form})
    else:
        return render(request, 'landing/mentorshipapplication.html',{'form':form})

    return render(request, 'landing/mentorshipapplication.html',{'form':form})

def index1(request):
    types =SkillType.objects.all()
    query = request.GET.get('q')
    if query:
        skill =SkillType.objects.get(skill_type=query)
        experts = UserProfile.get_pdtps().exclude(bio__isnull=True).exclude(bio__exact='').exclude(title__isnull=True).exclude(title__exact='').exclude(picture__isnull=True).exclude(picture__exact='').filter(user__skill__skill_type=skill).distinct().order_by('?')
    else:
        experts = UserProfile.get_pdtps().exclude(bio__isnull=True).exclude(bio__exact='').exclude(title__isnull=True).exclude(title__exact='').exclude(picture__isnull=True).exclude(picture__exact='').order_by('?')
    page = request.GET.get('page', 1)
    paginator = Paginator(experts, 12)
    try:
        experts = paginator.page(page)
    except PageNotAnInteger:
        experts = paginator.page(1)
    except EmptyPage:
        experts = paginator.page(paginator.num_pages)
    return render(request, 'experts.html', { 'experts':experts,'types':types})
def experts(request):
    specialities = Specialization.objects.all()
    # types =SkillType.objects.all()
    # query = request.GET.get('q')
    # query2 = request.GET.get('q1')
    # top = UserProfile.get_pdtps().filter(user__email="michael.ombwayo@gmail.com")
    # if query:
    #     skill =SkillType.objects.get(skill_type=query)
    #     experts = UserProfile.get_pdtps().exclude(bio__isnull=True).exclude(bio__exact='').exclude(title__isnull=True).exclude(title__exact='').filter(user__skill__skill_type=skill, user__skill__skill__icontains=query2).order_by('?').distinct()
    # else:
    #     # experts = UserProfile.get_pdtps().exclude(bio__isnull=True).exclude(bio__exact='').exclude(title__isnull=True).exclude(title__exact='').order_by('?').distinct()
    #     experts = sorted(UserProfile.get_pdtps().exclude(bio__isnull=True).exclude(bio__exact='').exclude(title__isnull=True).exclude(title__exact='').order_by('?'), key=lambda x: random.random())
    #     top = UserProfile.get_pdtps().filter(user__email="michael.ombwayo@gmail.com")
    # page = request.GET.get('page', 1)
    # paginator = Paginator(experts, 40)
    # try:
    #     experts = paginator.page(page)
    # except PageNotAnInteger:
    #     experts = paginator.page(1)
    # except EmptyPage:
    #     experts = paginator.page(paginator.num_pages)
    return render(request, 'landing2/categories.html', { 'specialities':specialities})

def experts_by_category(request, slug):
    specialities = Specialization.objects.all()
    speciality = Specialization.objects.get(slug=slug)
    types =SkillType.objects.all()
    query = request.GET.get('q')
    query2 = request.GET.get('q1')
    top = UserProfile.get_pdtps().filter(user__email="michael.ombwayo@gmail.com")
    if query:
        skill =SkillType.objects.get(skill_type=query)
        experts = UserProfile.get_pdtps().exclude(bio__isnull=True).exclude(bio__exact='').exclude(title__isnull=True).exclude(title__exact='').filter(speciality=speciality,user__skill__skill_type=skill, user__skill__skill__icontains=query2).order_by('?').distinct()
    else:
        # experts = UserProfile.get_pdtps().exclude(bio__isnull=True).exclude(bio__exact='').exclude(title__isnull=True).exclude(title__exact='').order_by('?').distinct()
        experts = sorted(UserProfile.get_pdtps().filter(speciality=speciality).exclude(bio__isnull=True).exclude(bio__exact='').exclude(title__isnull=True).exclude(title__exact='').order_by('?'), key=lambda x: random.random())
    page = request.GET.get('page', 1)
    paginator = Paginator(experts, 40)
    try:
        experts = paginator.page(page)
    except PageNotAnInteger:
        experts = paginator.page(1)
    except EmptyPage:
        experts = paginator.page(paginator.num_pages)
    form = JobContactForm()
    if request.method == 'POST':
        form = JobContactForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            ex = request.POST['expe']
            expert = User.objects.get(id=int(ex))

            message = request.POST['message']
            email = request.POST['email']
            from_email = 'pdtp@ict.go.ke'
            subject = "Job Opportunity"
            template_html = 'email/interncontact.html'
            template_text = 'email/interncontact.txt'
            f.pdtp_contacted = expert.email
            

            text_content = render_to_string(template_text, {"subject":subject,
                        'message':message, 'email':email,'first_name':expert.first_name,
                        'last_name':expert.last_name,})
            html_content = render_to_string(template_html, {"subject":subject,
                        'message':message, 'email':email,'first_name':expert.first_name,
                        'last_name':expert.last_name,})
            mail.send(
                [expert.email],
                from_email,
                 subject=subject,
                html_message=html_content,
                )
            f.save()
        messages.add_message(request, messages.SUCCESS, 'Message sent Successfully')
        next = request.GET.get('from')
        if next:
            return HttpResponseRedirect(next)
    return render(request, 'landing2/experts2.html', {'form':form,'speciality':speciality,'types':types,'experts':experts,'specialities':specialities})
@login_required
def apply_for_training(request):
    #raise Http404
    institution = TrainingInstitution.objects.get(institution="IBM")
    courses = TrainingCourse.objects.filter(institution=institution)
    if request.method == 'POST':
        courses = request.POST.getlist('courses')
        for course in courses:
            k = TrainingCourse.objects.get(id=course)
            TrainingApplication.objects.create(pdtp=request.user, institution=institution,course=k)
        return HttpResponseRedirect('/app/apply/')
    else:
        return render(request, 'apply.html', {'institution':institution,'courses':courses})


    
def expert_by_skills(request):
    types = SkillType.objects.all()
    if request.method == "POST":
        skill = request.POST['skill']
        skill =SkillType.objects.get(id=skill)
        experts = UserProfile.get_pdtps().exclude(bio__isnull=True).exclude(bio__exact='').exclude(title__isnull=True).exclude(title__exact='').exclude(picture__isnull=True).exclude(picture__exact='').filter(user__skill__skill_type=skill).distinct()
        page = request.GET.get('page', 1)
        paginator = Paginator(experts, 12)
        try:
            experts = paginator.page(page)
        except PageNotAnInteger:
            experts = paginator.page(1)
        except EmptyPage:
            experts = paginator.page(paginator.num_pages)
        return render(request, 'experts.html', {'types':types,'skill':skill ,'experts':experts})
    else:

        experts = UserProfile.get_pdtps().exclude(bio__isnull=True).exclude(bio__exact='').exclude(title__isnull=True).exclude(title__exact='').exclude(picture__isnull=True).exclude(picture__exact='').filter(user__skill__skill_type=skill).distinct()
        page = request.GET.get('page', 1)
        paginator = Paginator(experts, 12)
        try:
            experts = paginator.page(page)
        except PageNotAnInteger:
            experts = paginator.page(1)
        except EmptyPage:
            experts = paginator.page(paginator.num_pages)
        return render(request, 'experts.html', {'types':types,'skill':skill ,'experts':experts})

def expert_profile(request, id, slug):
    expert = UserProfile.objects.get(id=id)
    return render(request,'expert.html', {'expert':expert})


def send_message(request, id):
    expert = User.objects.get(id=id)
    if request.method == 'POST':
        form = JobContactForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)

            message = request.POST['message']
            email = request.POST['email']
            from_email = 'pdtp@ict.go.ke'
            subject = "Job Opportunity"
            template_html = 'email/interncontact.html'
            template_text = 'email/interncontact.txt'
            f.pdtp_contacted = expert.email
            

            text_content = render_to_string(template_text, {"subject":subject,
                        'message':message, 'email':email,'first_name':expert.first_name,
                        'last_name':expert.last_name,})
            html_content = render_to_string(template_html, {"subject":subject,
                        'message':message, 'email':email,'first_name':expert.first_name,
                        'last_name':expert.last_name,})
            mail.send(
                [expert.email],
                from_email,
                 subject=subject,
                html_message=html_content,
                )
            f.save()
        messages.add_message(request, messages.SUCCESS, 'Message sent Successfully')
        next = request.GET.get('from')
        if next:
            return HttpResponseRedirect(next)
    
        # mail.send([expert.email], from_email,
        #             subject="Job Opportunity",
        #             # message='Hi there! Your mentee has responded to your a meeting you scheduled. Log on to the portal to view his response',
        #             message=message,
        #             )
        # messages.add_message(request, messages.SUCCESS, 'Message Sent Successfully')
                    
        # return HttpResponseRedirect('/app/index/')

def custom_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/app/dashboard/')
    else:
        return login(request)

class UploadFileForm(forms.Form):
    file = forms.FileField(label="Chose an Excel File")

@login_required
def check_password(request):
  user=request.user
  try:
    MustChangePassword.objects.get(user=user)
    request.session['email'] = user.email
    return HttpResponseRedirect('/app/password_change/')
  except MustChangePassword.DoesNotExist:
    return HttpResponseRedirect('/app/dashboard/')

@login_required
def password_change(request):
    user=request.user
    
    if request.method == 'POST':
        password=request.POST['password']
        change=make_password(password)
        user.password=change
        user.save()
        MustChangePassword.objects.get(user=user).delete()
        logout(request)
        return HttpResponseRedirect('/accounts/login/')
    else:
        email = user.email
    return render(request,'account/changeme.html', {'email':email})
   



def alumni_registration(request):
    if request.method == 'POST':
        form = AlummniDatabaseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Details submitted successfully')
        return HttpResponseRedirect('/app/alumni-registration/')
    else:
        form = AlummniDatabaseForm()
        return render(request,'landing2/alumni.html',{'form':form})

@login_required
def alumni_regs(request):
    alumni = AlummniDatabase.objects.all()
    return render(request,'pdtp/alumni_results.html',{'alumni':alumni})


@login_required
def dashboard2(request, slug):
    user = request.user
    profile = request.user.userprofile
    context_dict = {}
    
    #form=UploadFileForm
    #mentors=UserProfile.objects.filter(user_category="MENTOR")
    #public=Organization.objects.filter(category=True)
    #private=Organization.objects.filter(category=False)
    #years= PdtpYear.objects.all()
    #for year in years:
        #y=PdtpYear.objects.filter(year=year)
        #pdtp=UserProfile.objects.filter(user_category="PDTP",year=y)
    #context_dict={'profile':profile,'years':years,'public':public,'private':private,'form':form,'mentors':mentors,'pdtp':pdtp}
    #return render(request,'secretariat/secretariat.html',context_dict)
    year=PdtpYear.objects.get(slug=slug)
    #y=PdtpYear.objects.get(year=year.year)
    #y=year
    #ye=PdtpYear.objects.get(year=y)
    interns=UserProfile.get_pdtps().filter(year=year, active=True).count()
    private_deployments=Deployment.objects.annotate(latest_deployed=Max('pdtp__deployment__date_confirmed')).filter(year=year,organization__category=False,confirmed=True,latest_deployed=F('date_confirmed')).count()

    public_deployments=Deployment.objects.filter(year=year,organization__category=True).count()
    unattached=UserProfile.get_pdtps().filter(year=year, active=True).exclude(user__id__in=Deployment.objects.filter(year=year,pdtp__userprofile__active=True).values_list('pdtp__id',flat=True)).count()
    assignments=MentorMenteeMapping.objects.filter(year=year.year,mentee__userprofile__active=True).distinct().count()
    unmentored=UserProfile.get_pdtps().filter(year=year, active=True).exclude(user__id__in=MentorMenteeMapping.objects.filter(year=year.year,mentee__userprofile__active=True).values_list('mentee__id',flat=True)).distinct().count()


    public=Organization.objects.filter(category=True).count()
    private=Organization.objects.filter(category=False).count()
    events=Event.objects.filter(cancelled=False,end_date__gte=today)[:3]
    issues =Issue.objects.filter(solved=False, year=year).count()
    supervisors =Supervisor.get_supervisors().filter(mentor_availability=True).count()
    mentors =Supervisor.get_mentors().filter(supervisor__userprofile__active=True).count()
    exits =PDTPExitRequest.objects.filter(approved_by_supervisor=False).count()
    exited = UserProfile.get_pdtps().filter(year=year, active=False).count()
    updates=UpdateRequest.objects.filter(solved=False,year=year).count()
    male=UserProfile.get_pdtps_male().filter(year=year,  active=True).count()
    female=UserProfile.get_pdtps_female().filter(year=year,  active=True).count()
    total=UserProfile.get_pdtps().filter(year=year).count()
    years= PdtpYear.objects.order_by('year')
    context_dict={'profile':profile,'interns':interns,'male':male,'female':female,

     'private_deployments':private_deployments,'total':total, 'assignments':assignments,'unmentored':unmentored,'exits':exits,'exited':exited,'updates':updates,
     'unattached':unattached, 'public_deployments':public_deployments,'supervisors':supervisors,'mentors':mentors,
      'year':year, 'years':years,'public':public,'private':private,
      'events':events,'issues':issues}
    
    return render(request,'management/index.html',context_dict)






@login_required
def dashboard(request):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    context_dict = {}
    if request.method == "GET":
        context_dict = {'user':user}
        #name = user.id
        profile = request.user.userprofile
        if request.user.userprofile.is_administration(profile):
            #form=UploadFileForm
            #mentors=UserProfile.objects.filter(user_category="MENTOR")
            #public=Organization.objects.filter(category=True)
            #private=Organization.objects.filter(category=False)
            #years= PdtpYear.objects.all()
            #for year in years:
                #y=PdtpYear.objects.filter(year=year)
                #pdtp=UserProfile.objects.filter(user_category="PDTP",year=y)
            #context_dict={'profile':profile,'years':years,'public':public,'private':private,'form':form,'mentors':mentors,'pdtp':pdtp}
            #return render(request,'secretariat/secretariat.html',context_dict)
            year=PdtpYear.objects.latest('year')
            #y=PdtpYear.objects.get(year=year.year)
            #y=year
            #ye=PdtpYear.objects.get(year=y)
            interns=UserProfile.get_pdtps().filter(year=year, active=True).count()
            private_deployments=Deployment.objects.annotate(latest_deployed=Max('pdtp__deployment__date_confirmed')).filter(year=year,organization__category=False,confirmed=True,latest_deployed=F('date_confirmed')).count()

            public_deployments=Deployment.objects.filter(year=year,organization__category=True).count()
            unattached=UserProfile.get_pdtps().filter(year=year, active=True).exclude(user__id__in=Deployment.objects.filter(year=year,pdtp__userprofile__active=True).values_list('pdtp__id',flat=True)).count()
            assignments=MentorMenteeMapping.objects.filter(year=year,mentee__userprofile__active=True).distinct().count()
            unmentored=UserProfile.get_pdtps().filter(year=year, active=True).exclude(user__id__in=MentorMenteeMapping.objects.filter(year=year.year,mentee__userprofile__active=True).values_list('mentee__id',flat=True)).distinct().count()


            public=Organization.objects.filter(category=True).count()
            private=Organization.objects.filter(category=False).count()
            events=Event.objects.filter(cancelled=False,end_date__gte=today)[:3]
            issues =Issue.objects.filter(solved=False).count()
            supervisors =Supervisor.get_supervisors().filter(mentor_availability=True).count()
            mentors =Supervisor.get_mentors().filter(mentor_availability=True).count()
            exits =PDTPExitRequest.objects.filter(approved_by_supervisor=False).count()
            exited = UserProfile.get_pdtps().filter(year=year, active=False).count()
            updates=UpdateRequest.objects.filter(solved=False).count()
            male=UserProfile.get_pdtps_male().filter(year=year,  active=True).count()
            female=UserProfile.get_pdtps_female().filter(year=year,  active=True).count()
            total=UserProfile.get_pdtps().filter(year=year).count()
            years= PdtpYear.objects.order_by('year')
            context_dict={'profile':profile,'interns':interns,'male':male,'female':female,

             'private_deployments':private_deployments,'total':total, 'assignments':assignments,'unmentored':unmentored,'exits':exits,'exited':exited,'updates':updates,
             'unattached':unattached, 'public_deployments':public_deployments,'supervisors':supervisors,'mentors':mentors,
              'year':year, 'years':years,'public':public,'private':private,
              'events':events,'issues':issues}
            
            return render(request,'management/index.html',context_dict)
        elif request.user.userprofile.is_pdtp(profile):
            form=PicForm()
            rform=UpdateRequestForm()
            academic=AcademicDetail.objects.filter(user=user)
            context_dict={'profile':profile,'rform':rform,'form':form,'academi':academic}
            return render(request,'pdtp/index.html',context_dict)
        elif request.user.userprofile.is_management(profile):
            public=Organization.objects.filter(category=True)
            private=Organization.objects.filter(category=False)
            events=Event.objects.filter(cancelled=False,end_date__gte=today)[:3]
            issues =Issue.objects.filter(solved=False).order_by('-id')[:3]
            years= PdtpYear.objects.order_by('year')
            context_dict={'profile':profile, 'years':years,'public':public,'private':private,'events':events,'issues':issues}
            return render(request,'management/index.html',context_dict)
        
        elif request.user.userprofile.is_supervisor(profile):
            form=PicForm()
            context_dict={'profile':profile,'form':form}
            return render(request,'mentors/index.html',context_dict)
        elif request.user.userprofile.is_mentor(profile):
            form=PicForm()
            academic=AcademicDetail.objects.filter(user=user)
            context_dict={'profile':profile,'form':form}
            return render(request,'mentors/index.html',context_dict)
        else:
            raise Http404
@login_required
def bio_update(request, id ):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    person = User.objects.get(id=id)
    p=person.id
    prof = get_object_or_404(UserProfile, user=p)
    if request.method == 'POST':
        form=BioForm(request.POST or None, instance=prof)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Profile Updated Successfully')
            next = request.GET.get('from')
            if next:
                return HttpResponseRedirect(next)
    else:
        form=BioForm(instance=prof)
    return render(request,'bio.html',{'form':form})
@login_required
def add_pdtp(request):
    user=request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    name=user.id
    me=request.user.userprofile
    form=UserForm(request.POST)
    pform=ManagementAddPdtpForm(request.POST)
    
    if request.method == 'POST':
        form=UserForm(request.POST)
        pform=ManagementAddPdtpForm(request.POST)
        if form.is_valid() and pform.is_valid():
            u=form.save(commit=False)
            email=form.cleaned_data.get('email')
            first_name=form.cleaned_data.get('first_name')
            last_name=form.cleaned_data.get('last_name')
            year=request.POST['year']
            y=PdtpYear.objects.get(id=year)
            password=make_password(password='pdtp@ict',              
                  salt=None,
                  hasher='default')
          
            #president=request.POST['is_pdtp_president']
            #mrep=request.POST['isministry_rep']
            #dept=request.POST['department_attached']
            #intrep=request.POST['isinterests_rep']
            #aspe=request.POST['area_of_specialization']
            try:
                user=User.objects.get(email=email)
                messages.add_message(request, messages.WARNING, 'User with that email already exists')
                return HttpResponseRedirect('/app/add_pdtp')
            except User.DoesNotExist:
                user=User.objects.create(email=email,first_name=first_name,last_name=last_name,username=email,password=password)
                userprofile=UserProfile.objects.create(user_category="PDTP", user=user,
                    year=y)
                messages.add_message(request, messages.SUCCESS, 'Record Added Successfully, Add more Users')
                
                return HttpResponseRedirect('/app/add_pdtp/')
    else:
        form=UserForm()
        pform=ManagementAddPdtpForm()
    context_dict={'form':form,'pform':pform
                  }
    return render(request,'secretariat/addpdtp.html',context_dict)

@login_required
def pdtp_profile(request,year,id):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    person = get_object_or_404(User, id=id)
    p=person.id
    prof = get_object_or_404(UserProfile, user=p)
    form=PDTPClearanceForm()
    return render(request,'secretariat/pdtpprofile.html',{'person':person,'year':year,'form':form})
#Update PDTP Personal Details Profile by the Secretariat or Management
@login_required
def pdtp_profile_update(request,id):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    person = get_object_or_404(User, id=id)
    p=person.id
    prof = get_object_or_404(UserProfile, user=p)
    if request.method == 'POST':
        form=UForm(request.POST or None, instance=person)
        pform=PDTPProfileForm(request.POST or None, instance=prof)
        if form.is_valid() and pform.is_valid():
            u=form.save(commit=False)
            #username=request.POST['username']
            p =pform.save(commit=False)
            pform.user=person
            u.save()
            pform.save()
            messages.add_message(request, messages.SUCCESS, 'Profile Updated Successfully')
            next = request.GET.get('from')
            if next:
                return HttpResponseRedirect(next)
            
            #return HttpResponseRedirect('http://127.0.0.1:8000/app/pdtps/2015/')
    else:
        form = UForm(instance=person)
        pform=PDTPProfileForm(instance=prof)
    
    return render(request,'secretariat/pdtpupdate.html',{'pform':pform,'form':form})
@login_required
def pdtp_clearance(request,year,id):
    user = request.user
    person = get_object_or_404(User, id=id)
    p=person.id
    profile=UserProfile.objects.get(user=person)
    year=profile.year
    y=PdtpYear.objects.get(year=year)
    ye=y.year
    try:
        detail= get_object_or_404(ExitR, pdtp=person)
        form=PDTPClearanceForm(request.POST or None, instance=detail)
        if request.method == 'POST':
            if form.is_valid():
                u=form.save(commit=False)
                u.approved_by_sec=user
                u.solved =True
                u.date_approved=today
                u.save()
                UserProfile.objects.filter(user=person).update(active=False)
                #d.save()
                messages.add_message(request, messages.SUCCESS, 'PDTP Clearance Completed')
                next = request.GET.get('from')
                if next:
                    return HttpResponseRedirect(next)
        else:
            form = PDTPClearanceForm(instance=detail)
    except:
        form=PDTPClearanceForm(request.POST)
        if request.method == 'POST':
            form=PDTPClearanceForm(request.POST)
            if form.is_valid():
                u=form.save(commit=False)
                u.pdtp=person
                u.approved_by_secretariat=True
                u.date_approved_by_secretariat=today
                u.save()
                messages.add_message(request, messages.SUCCESS, 'User has been cleared and deactivated')
                next = request.GET.get('from')
                if next:
                    return HttpResponseRedirect(next)
        else:
            form=PDTPClearanceForm()
    return render(request,'pdtp/clearance.html',{'form':form,'person': person,'year':year})


@login_required
def pdtp_profile_update(request,id):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    person = get_object_or_404(User, id=id)
    p=person.id
    prof = get_object_or_404(UserProfile, user=p)
    if request.method == 'POST':
        form=UForm(request.POST or None, instance=person)
        pform=PDTPProfileForm(request.POST or None, instance=prof)
        if form.is_valid() and pform.is_valid():
            u=form.save(commit=False)
            #username=request.POST['username']
            p =pform.save(commit=False)
            pform.user=person
            u.save()
            pform.save()
            messages.add_message(request, messages.SUCCESS, 'Profile Updated Successfully')
            next = request.GET.get('from')
            if next:
                return HttpResponseRedirect(next)
            
            #return HttpResponseRedirect('http://127.0.0.1:8000/app/pdtps/2015/')
    else:
        form = UForm(instance=person)
        pform=PDTPProfileForm(instance=prof)
    year =prof.year.year
    return render(request,'secretariat/pdtpupdate.html',{'pform':pform,'form':form,'year':year})
@login_required
def update_bank_details(request,id):
    user = request.user
    
    if user.userprofile.active == False:
        messages.add_message(request, messages.WARNING, 'Your Account is inactive, you cannot perform this action')

        return HttpResponseRedirect('/app/dashboard/')

    person = get_object_or_404(User, id=id)
    p=person.id
    profile=UserProfile.objects.get(user=person)
    year=profile.year
    y=PdtpYear.objects.get(year=year)
    ye=y.year
    try:
        detail= get_object_or_404(BankDetail, user=p)
        form=BankDetailForm(request.POST or None, instance=detail)
        if request.method == 'POST':
            if form.is_valid():
                u=form.save(commit=False)
                u.user=person
                u.year=ye
                u.save()
                messages.add_message(request, messages.SUCCESS, 'Details Updated Successfully')
                next = request.GET.get('from')
                if next:
                    return HttpResponseRedirect(next)
        else:
            form = BankDetailForm(instance=detail)
    except:
        form=BankDetailForm(request.POST)
        if request.method == 'POST':
            form=BankDetailForm(request.POST)
            if form.is_valid():
                u=form.save(commit=False)
                u.user=person
                u.year=ye
                u.save()
                messages.add_message(request, messages.SUCCESS, 'Details Added Successfully')
                next = request.GET.get('from')
                if next:
                    return HttpResponseRedirect(next)
                #return HttpResponseRedirect('http://127.0.0.1:8000/app/pdtps/2015/')
        else:
            form=BankDetailForm()

    
        #pform=UserProfileForm(instance=prof)

    return render(request,'secretariat/bankupdate.html',{'form':form})
@login_required
def add_academic_detail(request,id):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    person = get_object_or_404(User, id=id)
    p=person.id
    uform=AcademicForm(request.POST)
    if request.method == 'POST':
        uform=AcademicForm(request.POST)
        if uform.is_valid():
            u=uform.save(commit=False)
            u.user=person
            u.save()
            messages.add_message(request, messages.SUCCESS, 'Record Added Successfully')
            next = request.GET.get('from')
            if next:
                return HttpResponseRedirect(next)       
    else:
        uform=AcademicForm()
    
    return render(request,'pdtp/academic.html',{'uform':uform})

@login_required
def academic_update(request,id):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    academic= AcademicDetail.objects.get(pk=id)
    user=request.user
    if request.method == 'POST':
        uform=AcademicForm(request.POST or None, instance=academic)
        if uform.is_valid():
            u=uform.save(commit=False)
            u.user=user
            u.save()
            messages.add_message(request, messages.SUCCESS, 'Record Updated Successfully')
            next = request.GET.get('from')
            if next:
                return HttpResponseRedirect(next)        
    else:
        uform=AcademicForm(instance=academic)
    return render(request,'pdtp/academic.html',{'uform':uform})

@login_required
def academic_delete(request,id):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    academic=AcademicDetail.objects.get(id=id).delete()
    messages.add_message(request, messages.SUCCESS, 'Record Deleted successfully')
    next = request.GET.get('from')
    if next:
        return HttpResponseRedirect(next) 
@login_required
def upload_photo(request, id):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    person = get_object_or_404(User, id=id)
    p=person.id
    try:
        ac = get_object_or_404(UserProfile, user=p)
        form=PicForm(request.POST, request.FILES or None, instance=ac)
        if request.method == 'POST':
            try:
                if form.is_valid():
                    
                    u=form.save(commit=False)
                    newdoc = UserProfile(picture = request.FILES['picture'])
                    u.user=person
                    u.save()
                    newdoc.save
                    messages.add_message(request, messages.SUCCESS, 'Photo Updated Successfully')
                    next = request.GET.get('from')
                    if next:
                        return HttpResponseRedirect(next)
            except:
                messages.add_message(request, messages.WARNING, 'You did not upload any photo')
                next = request.GET.get('from')
                if next:
                    return HttpResponseRedirect(next)
        else:
            form = PicForm(instance=ac)
    except:
        form=PicForm(request.POST, request.FILES)
        if request.method == 'POST':
            form=PicForm(request.POST, request.FILES)
            try:
                if form.is_valid():
                    u=form.save(commit=False)
                    newdoc = UserProfile(picture = request.FILES['picture'])
                    u.user=person
                    u.save()
                    newdoc.save
                    messages.add_message(request, messages.SUCCESS, 'Photo Updated Successfully')
                    next = request.GET.get('from')
                    if next:
                        return HttpResponseRedirect(next)
            except:
                messages.add_message(request, messages.WARNING, 'You did not upload any photo')
                next = request.GET.get('from')
                if next:
                    return HttpResponseRedirect(next)
        else:
            form=PicForm()
    return  HttpResponseRedirect('/app/dashboard/')

@login_required
def new_email(request):
    user=request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    if request.method == 'POST':
            email=request.POST['password']
            try:
                user=User.objects.get(email=email)
                messages.add_message(request, messages.WARNING, 'That Email is already in Use, Chose another one')
                next = request.GET.get('from')
                if next:
                    return HttpResponseRedirect(next) 
            except User.DoesNotExist:
                user.email=email
                user.username=email
                user.save()
                logout(request)
                messages.add_message(request, messages.SUCCESS, 'You have been logged out, Please log in to continue')
                return HttpResponseRedirect('/accounts/login/')
    next = request.GET.get('from')
    if next:
        return HttpResponseRedirect(next) 
#Activate and Deactivate Directors

@login_required
def request_program_exit(request):
    pdtp=request.user
    u=request.user.userprofile
    parameters =ExitParameter.objects.all()
    parametersrate =ExitRateParameter.objects.all()
    parameterssingle =ExitSingleQuestionParameter.objects.all()
    if request.method == "POST":
        for p in parameters:
            k ='1'+str(p.id)
            jibu =  request.POST.get(k)
            ExitSubmitted.objects.create(pdtp=pdtp,parameter=p,jibu=jibu)
        for m in parametersrate:
            n ='2'+str(m.id)
            jibu =  request.POST.get(n)
            ExitRateSubmited.objects.create(pdtp=pdtp,parameter=m,jibu=jibu)
        for u in parameterssingle:
            i =str(u.id)
            jibu =  request.POST.get(i)
            ExitSingleSubmitted.objects.create(pdtp=pdtp,parameter=u,jibu=jibu)
        ExitR.objects.create(pdtp=pdtp)
        messages.add_message(request, messages.SUCCESS, 'Your Exit Request has been succefylly sent. Check out your portal frequently for the updates')
       
        
        return HttpResponseRedirect('/app/request_status/')
    else:
        return render(request,'pdtp/exit.html',{'parameters':parameters,'parametersrate':parametersrate,'parameterssingle':parameterssingle})

@login_required
def request_status(request,id):
    user=User.objects.get(id=id)
    status=ExitR.objects.get(pdtp=user)
    return render(request,'pdtp/status.html',{'status':status})


@login_required
def management_profile(request):
    user=request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    prof = get_object_or_404(UserProfile, user=user)
    form=PicForm()
    uform=UForm(request.POST or None, instance=user)
    pform=ManProfileForm(request.POST or None, instance=prof)
    if request.method == 'POST':
        uform=UForm(request.POST or None, instance=user)
        pform=ManProfileForm(request.POST or None, instance=prof)
        if uform.is_valid() and pform.is_valid():
            u=uform.save(commit=False)
            p =pform.save(commit=False)
            pform.user=user
            u.save()
            pform.save()
            messages.add_message(request, messages.SUCCESS, 'Profile Updated Successfully')
            next = request.GET.get('from')
            if next:
                return HttpResponseRedirect(next)
    else:
        uform = UserForm(instance=user)
        pform=ManProfileForm(instance=prof)
    context_dict={'form':form,'pform':pform,'uform':uform}
    return render(request,'manprofile.html',context_dict)
@login_required
def pdtps(request,year):
    user=request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    user_year=PdtpYear.objects.get(year=year)
    pdtps=UserProfile.get_pdtps().filter(year=user_year,active=True)
    return render(request,'pdtps.html',{'year':user_year,'pdtps':pdtps})

@login_required
def pdtps_female(request,year):
    user=request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    user_year=PdtpYear.objects.get(year=year)
    pdtps=UserProfile.get_pdtps_female().filter(year=user_year, active=True)
    return render(request,'pdtps.html',{'year':user_year,'pdtps':pdtps})

@login_required
def pdtps_male(request,year):
    user=request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    user_year=PdtpYear.objects.get(year=year)
    pdtps=UserProfile.get_pdtps_male().filter(year=user_year, active=True)
    return render(request,'pdtps.html',{'year':user_year,'pdtps':pdtps})

@login_required
def pdtps_exited(request,year):
    user=request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    user_year=PdtpYear.objects.get(year=year)
    pdtps=UserProfile.get_pdtps_female().filter(year=user_year,active=False)
    return render(request,'pdtps.html',{'year':user_year,'pdtps':pdtps})

@login_required
def pdtps_all(request,year):
    user=request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    user_year=PdtpYear.objects.get(year=year)
    pdtps=UserProfile.get_pdtps().filter(year=user_year)
    return render(request,'pdtps.html',{'year':user_year,'pdtps':pdtps})

@login_required
def bank_details(request,year):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    details=BankDetail.objects.filter(year=year)
    return render(request,'secretariat/bank.html',{'details':details,'year':year})





@login_required
def pdtps_academics(request,year):
    
    pdtps=UserProfile.get_pdtps().filter(year=year)
    academics = AcademicDetail.objects.filter(user__id__in=pdtps)
  
    return render(request,'secretariat/academic.html',{'details':academics,'year':year})





#Display a list of all Mentors in the system with their status as available or not available
@login_required
def mentors(request):
    user=request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    if not user.groups.filter(name__in=['MENTORSHIP OFFICERS']).exists():
        raise Http404
    user=request.user
    mentors=Supervisor.get_mentors()
    return render(request,'secretariat/mentors.html',{'mentors':mentors,})



'''
@login_required
def all_mentors(request):
    user=request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    if not user.groups.filter(name__in=['MENTORSHIP OFFICERS']).exists():
        raise Http404
    user=request.user
    mentors=UserProfile.objects.filter(user_category="SUPERVISOR").exclude(user__id__in=Supervisor.objects.filter(is_mentor=True).values_list('supervisor', flat=True))
    #.update(confirmed=True,date_confirmed=datetime.date.today(),completion_date=two_months,reporting_details=instructions, reporting_date=date)
    #Deployment.objects.filter(organization=company,confirmed=False).exclude(id__in=deployments).delete() 
            
    #mentors=Supervisor.get_mentors()
    return render(request,'secretariat/allmentors.html',{'mentors':mentors,})
'''

@login_required
def add_mentor(request):
    user=request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    if not user.groups.filter(name__in=['MENTORSHIP OFFICERS']).exists():
        raise Http404
    uform=UserForm()
    form=OrganizationForm()
    cform=ContactPersonForm()
    sform=SupervisorForm()
    if request.method == 'POST':
        form=OrganizationForm(request.POST)
        uform=UserForm(request.POST)
        cform=ContactPersonForm(request.POST)
        sform=SupervisorForm(request.POST)
        username=request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        category=request.POST['category']
        organization=request.POST['organization']
        location=request.POST['location']
        cell=request.POST['phone_number']
        password=make_password(password='changeme',              
                  salt=None,
                  hasher='default')
        if  uform.is_valid() and cform.is_valid() and sform.is_valid():
            u=sform.save(commit=False)
            try:
                organization=Organization.objects.get(organization=organization)
            except:
                organization=Organization.objects.create(category=category,organization=organization,location=location)
                
            try:
                user=User.objects.get(username=username)
            except:
                user=User.objects.create(username=username,first_name=first_name,last_name=last_name,password=password,email=username)
                profile=UserProfile.objects.create(user=user,user_category="SUPERVISOR",phone_number=cell)
            u.organization=organization
            try:
                supervisor=Supervisor.objects.get(supervisor=user)
                supervisor.is_mentor=True
                messages.add_message(request, messages.WARNING, 'That User already Exist. He/She is now updated as a mentor')
                return HttpResponseRedirect('/app/add_mentor/')
            except:
                u.supervisor=user
                u.is_mentor=True
                u.save()
           
            messages.add_message(request, messages.SUCCESS, 'MentorAdded Successfully, Add more More Mentors')
            return HttpResponseRedirect('/app/add_mentor/')
    else:
        form=OrganizationForm()
        uform=UserForm()
        cform=ContactPersonForm()
        sform=SupervisorForm()
    context_dict={'form':form,'uform':uform,'cform':cform,'sform':sform
                  }
    return render(request,'secretariat/addmentor.html',context_dict)

@login_required
def mentor_profile_update(request,id):
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    person = get_object_or_404(User, id=id)
    p=person.id
    prof = get_object_or_404(UserProfile, user=p)
    sup= get_object_or_404(Supervisor, supervisor=p)
    if request.method == 'POST':
        uform=UForm(request.POST or None, instance=person)
        cform=ContactPersonForm(request.POST or None, instance=prof)
        sform=SupervisorForm(request.POST or None, instance=sup)
        if uform.is_valid() and cform.is_valid() and sform.is_valid():
            u=uform.save(commit=False)
            p =cform.save(commit=False)
            s =sform.save(commit=False)
            if sform.cleaned_data.get('mentor_availability') == False:
                MentorMenteeMapping.objects.filter(mentor=person).delete()
            p.user=person
            s.is_mentor=True
            u.save()
            p.save()
            s.save()
            messages.add_message(request, messages.SUCCESS, 'Profile Updated Successfully')
            next = request.GET.get('from')
            if next:
                return HttpResponseRedirect(next)
            #return HttpResponseRedirect('/app/mentors')
    else:
        uform = UForm(instance=person)
        cform=ContactPersonForm( instance=prof)
        sform=SupervisorForm(instance=sup)
    return render(request,'secretariat/mentorupdate.html',{'cform':cform,'sform':sform,'uform':uform})

@login_required
def mentorship_assignment(request, year):
    user=request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    if not user.groups.filter(name__in=['MENTORSHIP OFFICERS']).exists():
        raise Http404
    #m=Supervisor.get_mentors().filter(supervisor__id__in = MentorMenteeMapping.objects.filter(year=year))
    data=MentorMenteeMapping.objects.values('mentor').filter(year=year).annotate()
   
            #genders = Person.objects.values('gender').annotate(cnt=Count('gender')).order_by('gender')
       
    items = [
        {'data': g['mentor']} for g in data
        ]
    assignements=MentorMenteeMapping.objects.filter(year=year)
    return render(request,'secretariat/massignments.html',{'m':data,'mentors':mentors,'year':year,'assignments':assignements})

@login_required
def mentorship_mapping(request, year):
    user=request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    if not user.groups.filter(name__in=['MENTORSHIP OFFICERS']).exists():
        raise Http404
    y=PdtpYear.objects.get(year=year)
    #privates=Organization.objects.filter(category=False).exclude(organization__in=Deployment.objects.all())
    s=Supervisor.get_mentors().filter(mentor_availability=True).exclude(supervisor__in = MentorMenteeMapping.objects.filter(year=year).values_list('mentor', flat=True))

    #mentors=UserProfile.get_mentors().filter(mentor_availability=True)#.filter(user__in=mentormenteemapping)
    mentors_assigned=MentorMenteeMapping.objects.filter(year=year)
    data=MentorMenteeMapping.objects.values('mentor','mentor__supervisor__mentor_availability',
                                            'mentor__id','mentor__email','mentor__userprofile__phone_number','mentor__supervisor__organization__organization',
                                            'mentor__supervisor__position',
                                            'mentor__supervisor__honors','mentor__first_name',
                                            'mentor__last_name').filter(year=year).annotate(
        total=Count('mentor'))
    items = [
        {'mentor': g['mentor'],'availability':g['mentor__supervisor__mentor_availability'],
         'id':g['mentor__id'],'email':g['mentor__email'],
         'lname':g['mentor__last_name'],'cell':g['mentor__userprofile__phone_number'],
         'company':g['mentor__supervisor__organization__organization'],
         'honors':g['mentor__supervisor__honors'],
         'title':g['mentor__supervisor__position'],
         'fname': g['mentor__first_name'], 'total': g['total'] } for g in data
        ]
    #mentors_assigned=User.objects.filter(userprofile__mentor_availability=True,userprofile__user_category="MENTOR").exclude(User.objects__id__in=s)
    return render(request,'secretariat/mapinglist.html',{'mentors':s,'year':year,'assigned':items})



@login_required
def secretariat_assign_supervisor(request, year):
    user=request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    if not user.groups.filter(name__in=['MENTORSHIP OFFICERS']).exists():
        raise Http404
    
    #privates=Organization.objects.filter(category=False).exclude(organization__in=Deployment.objects.all())
    supervisors=Supervisor.get_supervisors()
    return render(request,'secretariat/suplist.html',{'supervisors':supervisors,'year':year})    
@login_required
def assignmentees(request,id,year):
    user=request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    if not user.groups.filter(name__in=['MENTORSHIP OFFICERS']).exists():
        raise Http404
    mentor=User.objects.get(id=id)
    request.session['mentor'] = mentor
    request.session['year'] = year
    y=PdtpYear.objects.get(year=year)
    mentees=MentorMenteeMapping.objects.filter(mentor=mentor).filter(year=year)
    pdtps= UserProfile.objects.filter(user_category="PDTP").filter(assignedmentor=False).filter(year=y)
    return render(request,'secretariat/mapping.html',{'pdtps':pdtps,'mentor':mentor,'year':year,'mentees':mentees})

@login_required
def secretariat_supervisor_assignmentees(request,id,year):
    user=request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    if not user.groups.filter(name__in=['MENTORSHIP OFFICERS']).exists():
        raise Http404
    supervisor=User.objects.get(id=id)
    y=PdtpYear.objects.get(year=year)
    pdtps= UserProfile.objects.filter(user_category="PDTP").filter(year=y)
    org = Supervisor.objects.filter(supervisor=supervisor)[0]
    if request.method=="POST":
        interns=request.POST.getlist('pdtps')
        for intan in interns:
            selected_intan=User.objects.get(username=intan)
            assigned = InternSupervisor.objects.create(company=org.organization, pdtp=selected_intan,supervisor=supervisor)
        messages.add_message(request, messages.SUCCESS, "Assignment Successful")
        return HttpResponseRedirect('.')

    return render(request,'secretariat/newprivate.html',{'pdtps':pdtps,'supervisor':supervisor,'year':year})

@login_required
def complete_mentorship_mapping(request):
    user=request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    if not user.groups.filter(name__in=['MENTORSHIP OFFICERS']).exists():
        raise Http404
    mentor=request.session['mentor']
    year=request.session['year']
    if request.method == 'POST':
        id = request.POST.get('id', None)
        user=User.objects.get(pk=id)
        p=UserProfile.objects.get(user=user)
        try:
            mentee=MentorMenteeMapping.objects.get(mentee=user)
            ctx = {'targ':'warning', 'message': 'That Mentee. has already been assigned a mentor, Please refresh this page'}
            return HttpResponse(json.dumps(ctx), content_type='application/json')
        except MentorMenteeMapping.DoesNotExist:
            mapping=MentorMenteeMapping.objects.create(mentor=mentor,mentee=user,year=year)
            p.assignedmentor=True
            p.save()
            ctx = { 'targ':'success', 'message': 'Assignment Successfull. Assign more Mentors to this mentor then refresh your page'}
            return HttpResponse(json.dumps(ctx), content_type='application/json')


@login_required
def activate(request):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    if request.method == 'POST':
        u=request.user
        id = request.POST.get('id', None)
        user=User.objects.get(pk=id)
        user.is_active=True
        user.userprofile.deactivated_by=u
        user.save()
    ctx = { 'message': 'User has been Activated. Refresh the page to see the effects'}
    return HttpResponse(json.dumps(ctx), content_type='application/json')

@login_required
def deactivate(request):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    if request.method == 'POST':
        u=request.user
        id = request.POST.get('id', None)
        user=User.objects.get(pk=id)
        user.is_active=False
        user.userprofile.deactivated_by=u
        user.save()
    ctx = { 'message': 'User has been deactivated. Refresh the page to see the effects'}
    return HttpResponse(json.dumps(ctx), content_type='application/json')
@login_required
def update_request(request,id):
    user=request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    if request.method=="POST":
        rform=UpdateRequestForm(request.POST)
        if rform.is_valid():
            r=rform.save(commit=False)
            r.pdtp=user
            r.save()
            messages.add_message(request, messages.SUCCESS, 'Request Submitted Successfully')
            return HttpResponseRedirect('/app/dashboard/')
@login_required
def exit_requests(request):
    user = request.user
    requests=ExitR.objects.filter(solved=False)
    return render(request,'pdtp/exitrequests.html',{'requests':requests})



@login_required
def pdtp_supervisor_clearance(request,id):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    person = get_object_or_404(User, id=id)
    p=person.id
    profile=UserProfile.objects.get(user=person)
    #try:
    detail= get_object_or_404(PDTPExitRequest, pdtp=person)
    form=PClearanceForm(request.POST or None, instance=detail)
    if request.method == 'POST':
        if form.is_valid():
            u=form.save(commit=False)
            u.approved_by_supervisor=True
            #u.date_approved_by_supervisor=today
            u.save()
            #d.save()
            messages.add_message(request, messages.SUCCESS, 'User has been cleared and deactivated')
            next = request.GET.get('from')
            if next:
                return HttpResponseRedirect(next)
        else:
            form = PClearanceForm(instance=detail)
    return render(request,'pdtp/sclearance.html',{'form':form,'person': person})
@login_required
def events(request):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    if request.method == 'POST':
        form=EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Event Scheduled Successfully')
            return HttpResponseRedirect('.')
    else:
        form= EventForm()
        events=Event.objects.filter(end_date__gte=today)
    return render(request,'secretariat/events.html',{'form':form,'events':events})

@login_required
def edit_event(request,id):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    event = get_object_or_404(Event, id=id)
    form=EventForm(request.POST or None, instance=event)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            
            messages.add_message(request, messages.SUCCESS, 'Event updated Successfully')
            next = request.GET.get('from')
            if next:
                return HttpResponseRedirect(next)
        else:
            form = EventForm(instance=event)
    return render(request,'secretariat/editevent.html',{'form':form,'event': event})

@login_required
def cancel_event(request,id):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    event = get_object_or_404(Event, id=id)
    form=EventCancelForm(request.POST or None, instance=event)
    if request.method == 'POST':
        if form.is_valid():
            u=form.save(commit=False)
            u.cancelled=True
            u.save()
            
            messages.add_message(request, messages.SUCCESS, 'Event updated Successfully')
            next = request.GET.get('from')
            if next:
                return HttpResponseRedirect(next)
        else:
            form = EventCancelForm(instance=event)
    return render(request,'secretariat/editevent.html',{'form':form,'event': event})

@login_required
def staff_mentors(request):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    if not user.groups.filter(name__in=['MENTORSHIP OFFICERS']).exists():
        raise Http404
    management=UserProfile.get_management()
    secretariat=UserProfile.get_secretariats()
    return render(request,'secretariat/staff_mentors.html',{'management':management,'secretariat':secretariat})


@login_required
def add_staff(request,id):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    if not user.groups.filter(name__in=['MENTORSHIP OFFICERS']).exists():
        raise Http404
    staff=User.objects.get(id=id)
    organization=Organization.objects.get(organization="ICT Authority")
    mentor=Supervisor.objects.create(organization=organization,supervisor=staff,is_mentor=True)
    messages.add_message(request, messages.SUCCESS, 'Added Successfully')
    next = request.GET.get('from')
    if next:
        return HttpResponseRedirect(next)

@login_required
def upcoming_events(request):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    if user.userprofile.user_category == "PDTP":
        events=Event.objects.filter(Q(attendees="PDTPS") | Q(attendees="ALL")).filter(end_date__gte=today)
    elif user.userprofile.user_category == "SUPERVISOR":
        events=Event.objects.filter(Q(attendees="SUPERVISORS") | Q(attendees="MENTORS") | Q(attendees="ALL")).filter(end_date__gte=today)
    elif user.userprofile.user_category == "ADMINISTRATION":
        events=Event.objects.filter(end_date__gte=today)
    elif user.userprofile.user_category == "MANAGEMENT":
        events=Event.objects.filter(end_date__gte=today)
    return render(request,'events.html',{'events':events})

@login_required
def raise_issue(request):
    user = request.user
    
    if user.userprofile.active == False:
        messages.add_message(request, messages.WARNING, 'Your account is inactive. contact the Secretariat')
        return HttpResponseRedirect('/app/dashboard/')
   
    if request.method == "POST":
        form =IssueForm(request.POST)
        if form.is_valid():
            f=form.save(commit=False)
            subject=request.POST['subject']
            message=request.POST['message']
            f.pdtp=user
            f.date=today
            issue=Issue.objects.create(pdtp=user,date=today,subject=subject,message=message)
            status=IssueStatus.objects.create(issue=issue,status="RECIEVED",date=today,comment="Recieved by the secretariat")
            messages.add_message(request, messages.SUCCESS, 'Your issue has been submitted to the secretariat')
            next = request.GET.get('from')
            if next:
                return HttpResponseRedirect(next)
            
    else:
        form =IssueForm()

    return render(request,'pdtp/raise_issue.html',{'form':form})

def my_issues(request):
    user = request.user
    issues = Issue.objects.filter(pdtp=user)
    return render(request,'pdtp/my_issues.html',{'issues':issues})

login_required
def issues_response(request,slug, id):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    try:
        user=User.objects.get(id=id)
        profile=UserProfile.objects.filter(slug=slug).get(user=user)
    except:
        raise Http404
    issues =Issue.objects.filter(pdtp=user).order_by('-id')
    if request.method == "POST":
        form=IssueStatusForm(request.POST)
        issueid=request.POST['issueid']
        issue=Issue.objects.get(id=issueid)
        status=request.POST['status']
        if form.is_valid():
            f = form.save(commit=False)
            f.issue=issue
            f.by=user 
            f.date= today
            f.save()
            if status == "SOLVED":
                Issue.objects.filter(id=issueid).update(solved=True)

            messages.add_message(request, messages.SUCCESS, 'Response Sent Successfully')
            next = request.GET.get('from')
            if next:
                return HttpResponseRedirect(next)
    else:
        form=IssueStatusForm()
    return render(request,'pdtp/issue_response.html',{'form':form, 'issues':issues})

login_required
def raised_issues(request):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    issues =Issue.objects.filter(solved=False).order_by('-id')
    if request.method == "POST":
        form=IssueStatusForm(request.POST)
        issueid=request.POST['issueid']
        issue=Issue.objects.get(id=issueid)
        status=request.POST['status']
        if form.is_valid():
            f = form.save(commit=False)
            f.issue=issue
            f.by=user 
            f.date= today
            f.save()
            if status == "SOLVED":
                Issue.objects.filter(id=issueid).update(solved=True)
            messages.add_message(request, messages.SUCCESS, 'Response Sent Successfully')
            next = request.GET.get('from')
            if next:
                return HttpResponseRedirect(next)
    else:
        form=IssueStatusForm()
    return render(request,'secretariat/issue_response.html',{'issues':issues,'form':form})

@login_required 
def reports(request,slug):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    year=PdtpYear.objects.get(slug=slug)
    data=Deployment.objects.annotate(
    # annotate with MAX "baked_at" over all cakes in bakery
    latest_deployed=Max('pdtp__deployment__date_confirmed')
    # compare this cake "baked_at" with annotated latest in bakery
    ).filter(year=year,confirmed=True,latest_deployed=F('date_confirmed'))
    pdtps=UserProfile.get_pdtps().filter(year=year)
    private_deployments=Deployment.objects.filter(year=year,organization__category=False)
    public_deployments=Deployment.objects.filter(year=year,organization__category=True)
    unattached=UserProfile.get_pdtps().filter(year=year).exclude(id__in=Deployment.objects.all())
    assignements=MentorMenteeMapping.objects.filter(year=year)
    unmentored=UserProfile.get_pdtps().filter(year=year).exclude(id__in=MentorMenteeMapping.objects.filter(year=year))
    context_dict={'unmentored':unmentored,'assignements':assignements,'year':year,'unattached':unattached,'private_deployments':private_deployments,'public_deployments':public_deployments}
    return render(request,'management/report.html', context_dict)
@login_required 
def private_sector_reports(request):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    public=Organization.objects.filter(category=True)
    private=Organization.objects.filter(category=False)
    return render(request,'management/private.html',{'privates':private})

@login_required 
def public_sector_reports(request):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    private=Organization.objects.filter(category=True)
    #private=Organization.objects.filter(category=False)
    return render(request,'management/public.html',{'privates':private})
'''
@login_required 
def test(request):
    form=TestForm()
    LinkFormSet = formset_factory(TestForm)
    formset = LinkFormSet
    if request.method== 'POST':
        formset = LinkFormSet(request.POST)
        test1=request.POST.getlist('test1')
        test2=request.POST.getlist('test2')
        test3 =request.POST.getlist('test3')
        formset.save()
        #Test.objects.create(user=request.user,test1=test1,test2=test2,test3=test3)
        return HttpResponseRedirect('.')
    return render(request,'pdtp/workplan.html',{'formset':formset})
'''
#def (request):
    #form=WorkPlanForm()
   # return render(request,'pdtp/workplan.html',{'form':form})


@login_required
def my_workplan(request):
    user = request.user

    if user.userprofile.active == False:
        messages.add_message(request, messages.WARNING, 'Your account is inactive. contact the Secretariat')
        return HttpResponseRedirect('/app/dashboard/')
   
    workplan = WorkPlan.objects.filter(pdtp=user)[:5]

    return render(request, 'pdtp/my_workplan.html', {'workplan':workplan})

@login_required
def submit_workplan(request):
    user = request.user
    if user.userprofile.active == False:
        messages.add_message(request, messages.WARNING, 'Your account is inactive. contact the Secretariat')
        return HttpResponseRedirect('/app/dashboard/')
   
    
    WorkPlanFormSet = modelformset_factory(WorkPlan, form=WorkPlanForm)
    if request.method == 'POST':
        
        formset = WorkPlanFormSet(request.POST)
        if formset.is_valid():
            
            for form in formset:
                f=form.save(commit=False)
                try:
                    supervisor= InternSupervisor.objects.filter(pdtp=user).order_by('-id')[0]
                    f.supervisor=supervisor.supervisor
                    f.organization=supervisor.company
                    f.pdtp=request.user
                    f.save()
                    messages.add_message(request, messages.SUCCESS, 'You have succesfully submitted your Monthly Report')
                    u = supervisor.supervisor.email
                    mail.send([u], 'pdtp@ict.go.ke',
                subject='SUBMISION OF WORKPLAN',
                # message='Hi there! Your mentee has responded to your a meeting you scheduled. Log on to the portal to view his response',
                html_message='Hi there!<br><p> Your Intern has submitted monthly  workplan for approval<br> Kindly visit <a href="http://pdtpportal.icta.go.ke/" /></p>',
                )
                except:
                    f.pdtp=request.user
                    f.save()
                
                
            #
            return HttpResponseRedirect('/app/my_workplan/')
    else:
        formset = WorkPlanFormSet(queryset=WorkPlan.objects.none())

    return render(request, 'pdtp/workplan.html', {
    'formset': formset,
    })


# def pdf_workplan(request, id):
#     user = request.user
#     html_template = get_template('pdtp/wpdf.html')
#     pdtp = User.objects.get(id=id)
#     name =pdtp.userprofile.user
#     fname = name + ".pdf"

#     rendered_html = html_template.render(RequestContext(request, {'pdtp': pdtp})).encode(encoding="UTF-8")

#     pdf_file = HTML(string=rendered_html).write_pdf()

#     http_response = HttpResponse(pdf_file, content_type='application/pdf')
#     http_response['Content-Disposition'] = 'attachment; filename='+ fname

    #return  http_response
def pdf_workplan(request,*args, id):
    
    pdtp = request.user
    report = WorkPlan.objects.filter(pdtp=pdtp,id=id)
    template = get_template('pdtp/monthly.html')
    
    context = {

        'report': report,

    }
    html = template.render(context)
    pdf = render_to_pdf('pdtp/monthly.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "montlyreport.pdf"
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")




@login_required
def monthly_workplans(request):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    context_dict={}
    if request.method == 'POST':
        start=request.POST['startdate']
        end=request.POST['enddate']
        plans=WorkPlan.objects.filter(date_submitted__range=[start, end])
        context_dict['plans']=plans
        
    return render(request,'wplans.html',context_dict)
@login_required
def approve_workplans(request):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    plans=WorkPlan.objects.filter(supervisor=user)
    return render(request,'mentors/approve.html',{'plans':plans})

@login_required
def approve_plan(request,id):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    plan = get_object_or_404(WorkPlan, id=id)
    form=PlanForm(request.POST or None, instance=plan)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            date_approved = WorkPlan.objects.update(date_approved=today)
            mail.send([user.email], 'pdtp@ict.go.ke',
                subject='Workplan Approval',
                # message='Hi there! Your mentee has responded to your a meeting you scheduled. Log on to the portal to view his response',
                html_message="Hi there!<br><p> You have successfully approved Intern's workplan.</p>",
                )

            messages.add_message(request, messages.SUCCESS, 'Approval Successful')
            return HttpResponseRedirect('/app/approve_workplans/')
        else:
            form = PlanForm(instance=plan)
    return render(request,'mentors/papprove.html',{'plan':plan,'form':form})


@login_required
def add_project(request,id):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    person = get_object_or_404(User, id=id)
    p=person.id
    projform=ProjectForm(request.POST)
    if request.method == 'POST':
        projform=ProjectForm(request.POST)
        if projform.is_valid():
            u=projform.save(commit=False)
            u.user=person
            u.save()
            messages.add_message(request, messages.SUCCESS, 'Record Added Successfully')
            next = request.GET.get('from')
            if next:
                return HttpResponseRedirect(next)       
    else:
        projform=ProjectForm()
    
    return render(request,'pdtp/projects.html',{'projform':projform})

@login_required
def update_project(request,id):
    project= Project.objects.get(pk=id)
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    if request.method == 'POST':
        projform=ProjectForm(request.POST or None, instance=project)
        if projform.is_valid():
            u=projform.save(commit=False)
            u.user=user
            u.save()
            messages.add_message(request, messages.SUCCESS, 'Record Updated Successfully')
            next = request.GET.get('from')
            if next:
                return HttpResponseRedirect(next)        
    else:
        projform=ProjectForm(instance=project)
    return render(request,'pdtp/projects.html',{'projform':projform})

@login_required
def delete_project(request,id):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    project=Project.objects.get(id=id).delete()
    messages.add_message(request, messages.SUCCESS, 'Record Deleted successfully')
    next = request.GET.get('from')
    if next:
        return HttpResponseRedirect(next)

def add_skill(request,id):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    person = get_object_or_404(User, id=id)
    p=person.id
    sform=SkillForm(request.POST)
    if request.method == 'POST':
        sform=SkillForm(request.POST)
        if sform.is_valid():
            u=sform.save(commit=False)
            u.user=person
            u.save()
            messages.add_message(request, messages.SUCCESS, 'Record Added Successfully')
            #next = request.GET.get('from')
            #if next:
            return HttpResponseRedirect('.')       
    else:
        sform=SkillForm()
    
    return render(request,'pdtp/skills.html',{'sform':sform})

@login_required
def update_skill(request,id):
    skill= Skill.objects.get(pk=id)
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    if request.method == 'POST':
        sform=SkillForm(request.POST or None, instance=skill)
        if sform.is_valid():
            u=sform.save(commit=False)
            u.user=user
            u.save()
            messages.add_message(request, messages.SUCCESS, 'Record Updated Successfully')
            next = request.GET.get('from')
            if next:
                return HttpResponseRedirect(next)        
    else:
        sform=SkillForm(instance=skill)
    return render(request,'pdtp/skills.html',{'sform':sform})

@login_required
def delete_skill(request,id):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    skill=Skill.objects.get(id=id).delete()
    messages.add_message(request, messages.SUCCESS, 'Record Deleted successfully')
    next = request.GET.get('from')
    if next:
        return HttpResponseRedirect(next)

def add_referee(request,id):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    person = get_object_or_404(User, id=id)
    p=person.id
    rform=RefereeForm(request.POST)
    if request.method == 'POST':
        rform=RefereeForm(request.POST)
        if rform.is_valid():
            u=rform.save(commit=False)
            u.user=person
            u.save()
            messages.add_message(request, messages.SUCCESS, 'Record Added Successfully')
            next = request.GET.get('from')
            if next:
                return HttpResponseRedirect(next)       
    else:
        rform=RefereeForm()
    
    return render(request,'pdtp/referees.html',{'rform':rform})

@login_required
def update_referee(request,id):
    referee= Referee.objects.get(pk=id)
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    if request.method == 'POST':
        rform=RefereeForm(request.POST or None, instance=referee)
        if rform.is_valid():
            u=rform.save(commit=False)
            u.user=user
            u.save()
            messages.add_message(request, messages.SUCCESS, 'Record Updated Successfully')
            next = request.GET.get('from')
            if next:
                return HttpResponseRedirect(next)        
    else:
        rform=RefereeForm(instance=referee)
    return render(request,'pdtp/referees.html',{'rform':rform})

@login_required
def delete_referee(request,id):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    referee=Referee.objects.get(id=id).delete()
    messages.add_message(request, messages.SUCCESS, 'Record Deleted successfully')
    next = request.GET.get('from')
    if next:
        return HttpResponseRedirect(next)

def pdtps_in_private_sector(request, year):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    year=PdtpYear.objects.get(year=year)
    private_deployments=Deployment.objects.filter(year=year,organization__category=False)
    return render(request,'management/inprivate.html',{'private_deployments':private_deployments,'year':year})

def pdtps_in_public_sector(request, year):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    year=PdtpYear.objects.get(year=year)
    private_deployments=Deployment.objects.filter(year=year,organization__category=True)
    return render(request,'management/inpublic.html',{'private_deployments':private_deployments,'year':year})

def pdtps_not_deployed(request, year):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    year=PdtpYear.objects.get(year=year)
    private_deployments=UserProfile.get_pdtps().filter(year=year).exclude(id__in=Deployment.objects.all())
    return render(request,'management/notdeployed.html',{'private_deployments':private_deployments,'year':year})

def all_supervisors(request):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    #year=PdtpYear.objects.get(year=year)
    supervisors=Supervisor.get_supervisors()
    return render(request,'management/supervisors.html',{'supervisors':supervisors})
#mentorship
def interns_with_mentors(request, year):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    year=PdtpYear.objects.get(year=year)
    assignments=MentorMenteeMapping.objects.filter(year=year,mentee__userprofile__active=True)
    # assignments=MentorMenteeMapping.objects.filter(year=year.year,mentee__userprofile__active=True).distinct().count()
    return render(request,'management/withmentors.html',{'assignments':assignments,'year':year})
def interns_without_mentors(request, year):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    year=PdtpYear.objects.get(year=year)
    unmentored=UserProfile.get_pdtps().filter(year=year, active=True).exclude(user__id__in=MentorMenteeMapping.objects.filter(year=year.year,mentee__userprofile__active=True).values_list('mentee__id',flat=True)).distinct()
    return render(request,'management/withoutmentors.html',{'unmentored':unmentored,'year':year})

def bank_update_requests(request):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    #year=PdtpYear.objects.get(year=year)
    requests=UpdateRequest.objects.filter(solved=False)
    return render(request,'management/requests.html',{'requests': requests})



def mark_as_solved(request, id):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    requests=UpdateRequest.objects.filter(id=id).update(solved=True,updated_by=user)
    return HttpResponseRedirect('/app/bank_update_requests/')

@login_required
def trainings_done(request):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    trainings =TrainingApplication.objects.filter(pdtp=user)
    return render(request,'pdtp/train_done.html',{'trainings':trainings})


@login_required
def add_record(request):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    TrainingFormSet = modelformset_factory(Training, form=TrainingForm)
    if request.method == 'POST':
        formset = TrainingFormSet(request.POST)
        if formset.is_valid():
            
            for form in formset:
                f=form.save(commit=False)
            
                f.pdtp=request.user
                f.year = user.userprofile.year
                f.save()
            messages.add_message(request, messages.SUCCESS, 'Record Added Successfully')
            return HttpResponseRedirect('.')
    else:
        formset = TrainingFormSet(queryset=TrainingApplication.objects.none())

    return render(request, 'pdtp/add_record.html', {
    'formset': formset,
    })


@login_required
def update_training_record(request,id):
    record= Training.objects.get(pk=id)
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass

    if request.method == 'POST':
        form=TrainingForm(request.POST or None, instance=record)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Record Updated Successfully')
            next = request.GET.get('from')
            if next:
                return HttpResponseRedirect(next)        
    else:
        form=TrainingForm(instance=record)
    return render(request,'pdtp/update_record.html',{'form':form})

@login_required
def delete_record(request,id):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    record=Training.objects.get(id=id).delete()
    messages.add_message(request, messages.SUCCESS, 'Record Deleted successfully')
    next = request.GET.get('from')
    if next:
        return HttpResponseRedirect(next)


@login_required
def mentors_yet_to_evaluate(request):
    user=request.user
  
   
    #mentors=Supervisor.get_mentors().exclude(user__id__in=MentorEvaluation.objects.all())

    interns=UserProfile.get_pdtps().exclude(user__id__in = MentorMeeting.objects.all().values_list('pdtp__id', flat=True))
    return render(request,'secretariat/menpending.html',{'mentors':interns})


@login_required
def supervisors_yet_to_evaluate(request):
    user=request.user
    interns=UserProfile.get_pdtps().exclude(user__id__in = PublicSupervisorEvaluation.objects.all().values_list('pdtp__id', flat=True))
    return render(request,'secretariat/suppending.html',{'mentors':interns,})


@login_required
def not_evaluated_by_private(request):
    user=request.user
    interns=UserProfile.get_pdtps().exclude(user__id__in = PrivateSupervisorEvaluation.objects.all().values_list('pdtp__id', flat=True))
    return render(request,'secretariat/supprivate.html',{'mentors':interns,})



def cohort3_registration(request):
    form=UserForm(request.POST)
    pform=ManagementAddPdtpForm(request.POST)
    
    if request.method == 'POST':
        form=UserForm(request.POST)
        pform=ManagementAddPdtpForm(request.POST)
        if form.is_valid() and pform.is_valid():
            u=form.save(commit=False)
            email=form.cleaned_data.get('email')
            first_name=form.cleaned_data.get('first_name')
            last_name=form.cleaned_data.get('last_name')
            year=request.POST['year']
            y=PdtpYear.objects.get(id=year)
            password=make_password(password='pdtp@ict',              
                  salt=None,
                  hasher='default')
          
            #president=request.POST['is_pdtp_president']
            #mrep=request.POST['isministry_rep']
            #dept=request.POST['department_attached']
            #intrep=request.POST['isinterests_rep']
            #aspe=request.POST['area_of_specialization']
            try:
                user=User.objects.get(email=email)
                messages.add_message(request, messages.WARNING, 'User with that email already exists')
                return HttpResponseRedirect('/app/add_pdtp')
            except User.DoesNotExist:
                user=User.objects.create(email=email,first_name=first_name,last_name=last_name,username=email,password=password)
                userprofile=UserProfile.objects.create(user_category="PDTP", user=user,
                    year=y)
                messages.add_message(request, messages.SUCCESS, 'Record Added Successfully, Add more Users')
                
                return HttpResponseRedirect('/app/add_pdtp/')
    else:
        form=UserForm()
        pform=ManagementAddPdtpForm()
    context_dict={'form':form,'pform':pform
                  }
    return render(request,'secretariat/registration.html',context_dict)


#Training -secretariat
@login_required
def training(request, year):
    user = request.user
    year =PdtpYear.objects.latest('year')
    course = TrainingCourse.objects.all()
    
    return render(request, 'secretariat/training.html', {'course':course,'year':year})

@login_required
def post_training(request):
    user = request.user
    if request.method == 'POST':
        form = TrainingForm(request.POST)
        if form.is_valid():

            f = form.save(commit=False)
            f.secretariat = user
            f.save()
            messages.add_message(request, messages.SUCCESS, 'You have Successfully created training/certification')
            return HttpResponseRedirect('/app/2018/training/')
    else:
        form = TrainingForm()
    return render(request, 'secretariat/post_training.html',{'form':form})
@login_required
def update_training(request,id):
    user = request.user
    training = get_object_or_404(TrainingCourse, id=id)
    form = TrainingForm()
    if request.method == 'POST':
        form = TrainingForm(request.POST or None, instance=training)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'You have Successfully updated Training')
            return HttpResponseRedirect('/app/2018/training/')
    else:

       form = TrainingForm(instance=training)

    return render(request, 'secretariat/update_training.html',{'form':form})




@login_required
def get_applicants(request, id):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    
    try:
        cours = get_object_or_404(TrainingCourse, id=id)

        #year =PdtpYear.objects.get(year=year)
        trainings =TrainingApplication.objects.filter(course=cours).order_by('-id')
        return render(request,'pdtp/trainings.html',{'trainings':trainings,'course':cours})
    except TrainingApplication.DoesNotExist:
        raise Http404

@login_required
def update_applicants(request,id):
    trainings =TrainingApplication.objects.get(id=id)
    # year =PdtpYear.objects.get(year=year)
    form = TrainingApplicationUpdateForm()
    if request.method == 'POST':
        form = TrainingApplicationUpdateForm(request.POST or None, instance=trainings)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'You have Successfully updated Training')
            return HttpResponseRedirect('/app/2018/training/')

    else:
        form = TrainingApplicationUpdateForm(instance=trainings)
    
    return render(request, 'secretariat/update_applications.html',{'form':form,'pdtps':trainings})

#Training-Intern
@login_required
def my_trainings(request):
    user = request.user
    
    my_certitications =TrainingApplication.objects.filter(pdtp=user).order_by('-id')
    return render(request, 'pdtp/my_trainings.html', {'train':my_certitications})

@login_required
def training_list(request):
    courses = TrainingCourse.objects.filter(status__status__iexact='Open').order_by('-id')       
    return render(request, 'pdtp/training_list.html', {'courses':courses})

@login_required
def apply_training(request, id):
    user = request.user
    profileyear = UserProfile.objects.get(user = request.user)
    pdtpyear = PdtpYear.objects.all()
    training = get_object_or_404(TrainingCourse, id=id)
    category = TrainingCategory.objects.all()
    mode = TrainingMode.objects.all()
    form = InternTrainingApplicationForm()
    if request.method == 'POST':
        form = InternTrainingApplicationForm(request.POST)

        if form.is_valid():
            f = form.save(commit=False)
            f.pdtp = request.user
            
            f.year =profileyear.year
            f.course =training


            try:
                train = TrainingApplication.objects.get(pdtp=f.pdtp,course=f.course)
                messages.add_message(request, messages.WARNING, 'Already applied for that Training/Certification')
                return HttpResponseRedirect('/app/my-trainings/')
            except TrainingApplication.DoesNotExist:
                f.save()
                messages.add_message(request, messages.SUCCESS, 'You have Successfully applied for Training')
                return HttpResponseRedirect('/app/my-trainings/')

    else:

       form = InternTrainingApplicationForm()

    return render(request, 'pdtp/apply_training.html',{
        'form':form,
        'training':training,
        'mode':mode,
        'category':category,
        'pdtpyear':pdtpyear
        }
        )
@login_required
def update_my_training(request,id):
    user = request.user
    trainings =TrainingApplication.objects.get(id=id,pdtp=user)
    # year =PdtpYear.objects.get(year=year)
    form = ApplicationUpdateForm()
    if request.method == 'POST':
        form = ApplicationUpdateForm(request.POST or None, instance=trainings)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'You have Successfully updated Training')
            return HttpResponseRedirect('/app/my-trainings/')

    else:
        form = ApplicationUpdateForm(instance=trainings)
    
    return render(request, 'secretariat/update_applications.html',{'form':form,'pdtps':trainings})
#Training Feedback
@login_required
def training_Feedback(request,id):
    user = request.user
    training = get_object_or_404(TrainingApplication,id=id,pdtp=user)
    # form = TrainFeedbackForm()
    if request.method == 'POST':
        feed = request.POST.get('feed')
        pdtp = request.user
        train = request.POST.get('training')
        tt = TrainingCourse.objects.get(course=train)
        t = TrainingCourse.objects.get(course=tt)

        try:
            trainfeed = TrainingFeedback.objects.get(pdtp=pdtp,trainingapp = t)
            messages.add_message(request,messages.WARNING, 'You have already submitted feedback for this training/Certification')
            return HttpResponseRedirect('/app/my-trainings/')
        except TrainingFeedback.DoesNotExist:

            trainfeed = TrainingFeedback.objects.create(pdtp=pdtp,feedback=feed, trainingapp = t)
     
            messages.add_message(request, messages.SUCCESS, 'You have succefully submitted Training/Certification Feedback')
            return HttpResponseRedirect('/app/my-trainings/')
    # else:
    #     form= TrainFeedbackForm(instance=training)
    return render(request, 'pdtp/trainingfeedback.html', {'training':training})
#Intern Mentorship Reports

@login_required
def mentorship_reports(request):
    user = request.user
    if user.userprofile.active == False:
        messages.add_message(request, messages.WARNING, 'Your account is inactive. contact the Secretariat')
        return HttpResponseRedirect('/app/dashboard/')
    param = Meeting.objects.filter(mentee=user)
    confirmform = MeetingConfirmForm()
    reportform = MeetingReportForm()
    if request.method == 'POST' and 'mconfirm' in request.POST:
        m = Meeting.objects.get(id = request.POST['meeting'])
        confirm = request.POST['confirm']
        text = request.POST['confirm_text']
        template_html = 'email/cmeeting.html'
        template_text = 'email/cmeeting.txt'
        mentee_first = m.mentee.first_name
        mentee_last = m.mentee.last_name
        mentor__first_name = m.mentor.first_name
        mentor__last_name = m.mentor.last_name
        url = "http://digitalent.go.ke"
        meeting = Meeting.objects.filter(id = request.POST['meeting']).update(
            confirm=confirm,confirm_text=text)
        
        # mail.send([m.mentor.email], 'pdtp@ict.go.ke',
        #         subject='Mentorship Meeting Confirmation',
        #         # message='Hi there! Your mentee has responded to your a meeting you scheduled. Log on to the portal to view his response',
        #         html_message='Hi there!<br><p> Your mentee has responded to your a meeting you scheduled.<br>  Log on to the portal to view his response</p>',
        #         )
        text_content = render_to_string(template_text, {"first_name":mentee_first,
                    'last_name':mentee_last, 'url':url,'mentor': mentor__last_name})
        html_content = render_to_string(template_html, {"first_name":mentee_first,
                    'last_name':mentee_last, 'url':url,'mentor': mentor__last_name})
        mail.send(
            [m.mentor.email],
            from_email,
            subject='Mentorship Meeting Confirmation',
            html_message=html_content,
        )
        messages.add_message(request, messages.SUCCESS, 'Meeting Confirmation Submitted Successfully')
        return HttpResponseRedirect('/app/mentorship_reports/')
    elif request.method == 'POST' and 'mreport' in request.POST:
        template_html = 'email/mreport.html'
        template_text = 'email/mreport.txt'
        report = request.POST['report']
        meeting = Meeting.objects.filter(id = request.POST['meeting']).update(
            report=report)
        m = Meeting.objects.get(id = request.POST['meeting'])
        mentee_first = m.mentee.first_name
        mentee_last = m.mentee.last_name
        mentor__first_name = m.mentor.first_name
        mentor__last_name = m.mentor.last_name
        url = "http://digitalent.go.ke"
        # mail.send([m.mentor.email], 'pdtp@ict.go.ke',
        #         subject='Mentorship Meeting Confirmation',
        #         # message='Hi there! Your mentee has responded to your a meeting you scheduled. Log on to the portal to view his response',
        #         html_message='Hi there!<br><p> Your mentee has sent a report.<br>  Log on to the portal to view his response</p>',
        #         )
        text_content = render_to_string(template_text, {"first_name":mentee_first,
                    'last_name':mentee_last, 'url':url,'mentor': mentor__last_name})
        html_content = render_to_string(template_html, {"first_name":mentee_first,
                    'last_name':mentee_last, 'url':url,'mentor': mentor__last_name})
        mail.send(
            [m.mentor.email],
            from_email,
            subject='Mentorship Report',
            html_message=html_content,
        )
        messages.add_message(request, messages.SUCCESS, 'Report Submitted Successfully')
        return HttpResponseRedirect('/app/mentorship_reports/')


    else:
        form = PdtpMentorshipReportForm(user)
        
    return render(request, 'pdtp/mentorshipreport.html', {'confirmform':confirmform,
        'param':param,'reportform':reportform})



#Innovation submission
@login_required
def submit_innovation(request):
    # raise Http404
    user = request.user
    
    if user.userprofile.active == False:
        messages.add_message(request, messages.WARNING, 'Your account is inactive.. Contact the secretariat ')
        return HttpResponseRedirect('/app/dashboard/')

    u=get_object_or_404(UserProfile, user=user)
    form=InnovationSubmissionForm(request.POST)
    if request.method=='POST':
        form=InnovationSubmissionForm(request.POST)
        if form.is_valid():
            f=form.save(commit=False)
            f.pdtp = request.user
            
            f.save()
            messages.add_message(request, messages.SUCCESS, 'You have successfuly submitted your Innovation. The secreteriat will keep in touch. Good luck ')

            return HttpResponseRedirect('/app/pdtpinnovations/')
    else:
        form=InnovationSubmissionForm()
        
    return render(request,'pdtp/submitinnovation.html',{'form':form})

@login_required
def pdtpinnovations(request):
    # raise Http404
    user = request.user

    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass

    my_innovation = InnovationSubmission.objects.filter(pdtp=user)[:5]

    return render(request, 'pdtp/pdtpinnovation.html', {'my_innovation':my_innovation})

@login_required
def edit_innovation(request,id):
    # raise Http404
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    innovation = get_object_or_404(InnovationSubmission, id=id)
    i=innovation.id
    prof = get_object_or_404(UserProfile, user=user)
    if request.method == 'POST':
        form=InnovationSubmissionForm(request.POST or None, instance=innovation)
        team = request.POST.getlist('pdtps')
        if form.is_valid():
            
            for t in team:
                u = User.objects.get(id=int(t))
                InnovationTeam.objects.update_or_create(pdtp=u,innovation=innovation)
            u=form.save(commit=False)
            u.user = request.user
            u.save()
            messages.add_message(request, messages.SUCCESS, 'Innovation Updated Successfully')
            next = request.GET.get('from')
            if next:
                return HttpResponseRedirect(next)
            
    else:
        form = InnovationSubmissionForm(instance=innovation)
        interns=UserProfile.get_pdtps().filter(year=user.userprofile.year).exclude(user__id__in = InnovationTeam.objects.filter(innovation=innovation).values_list('innovation', flat=True))
    return render(request,'pdtp/innovationupdate.html',{'iform':form,'interns':interns})

@login_required
def innovations(request):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    context_dict={}

    innovations = InnovationSubmission.objects.all()
    context_dict['innovations']=innovations
    
    return render(request, 'secretariat/Innovationsub.html', context_dict)

@login_required
def mentorship_meeting(request, id):
    user=request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    mente = get_object_or_404(User, id=id)
    form = MeetingForm()
    mentee_email = mente.username
    mentor_email = user.username
    if request.method == "POST":
        form = MeetingForm(request.POST)
        if form.is_valid():

            f=form.save(commit=False)
            f.mentee = mente
            f.mentor = request.user
            f.save()
            messages.add_message(request, messages.SUCCESS, 'You have successfully submitted your report')
            return HttpResponseRedirect('/app/dashboard/')
            
        else:
            form = MeetingForm()
            messages.add_message(request, messages.SUCCESS, 'You have already booked a meeting for this parameter')
            next = request.GET.get('from')
            if next:
                return HttpResponseRedirect(next)
    return render(request,'mentors/meeting.html', {'form':form})
         

@login_required
def report(request, id):
    user = request.user
   
    mentee = User.objects.get(id=id)
    param = Meeting.objects.filter(mentee=mentee)
    feedbackform = FeedbackForm()
    if request.method == 'POST' and 'ffeed' in request.POST:
        text = request.POST['feedback']
        meeting = Meeting.objects.filter(id = request.POST['meeting']).update(
            feedback=text)
        m = Meeting.objects.get(id = request.POST['meeting'])
        mail.send([m.mentee.email], 'pdtp@ict.go.ke',
                subject='Mentors Feedback',
                # message='Hi there! Your mentee has responded to your a meeting you scheduled. Log on to the portal to view his response',
                html_message='Hi there!<br><p> Your mentor has given a feedback on one of your reports.<br>  Log on to the portal to view his response</p>',
                )


        messages.add_message(request, messages.SUCCESS, 'Feedback Submitted Successfully')
        return HttpResponseRedirect('/deployments/my_mentees/')
    return render(request, 'mentors/comments.html', {'mentee':mentee,'param':param,'feedbackform':feedbackform,
        })

@login_required
def mentorship_meeting_booked(request):
    user = request.user
    meetings = Meeting.objects.all()
    return render(request, 'secretariat/mentorshipmeetings.html', {'meetings':meetings})



@login_required
def mentor_report_comment(request):
    comments = ReportComment.objects.all()
    return render(request, 'secretariat/mentorcomment.html', {'comments':comments})

@login_required
def intern_mentorship_report(request):
    reports = PDTPMentorshipReport.objects.all()
    return render(request, 'secretariat/internmentorshipreport.html', {'reports':reports})

@login_required
def pdtp_cleared(request,year,id):
    user = request.user
    person = get_object_or_404(User, id=id)
    ExitR.objects.filter(pdtp=person).update(solved=True, approved_by_sec=user)
    UserProfile.objects.filter(user=person, active=False)
    messages.add_message(request, messages.SUCCESS, 'User has been cleared and deactivated')
    
    return HttpResponseRedirect('/app/exit_requests/')

@login_required
def my_leaves(request):
    user = request.user
    leaves = Leave.objects.filter(pdtp=user)
    return render(request, 'pdtp/leaves.html', {'leaves':leaves})
@login_required
def apply_for_leave(request):
    user = request.user
    form = LeaveApplicationForm()
    if request.method == 'POST':
        form = LeaveApplicationForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            template_html = 'email/coporate.html'
            template_text = 'email/coporate.txt'
            email=request.POST['email']
            leave_type=request.POST['leave_type']
            start_date=request.POST['start_date']
            end_date=request.POST['end_date']
            url='pdtpportal.icta.go.ke/app/approve_leaves/'
            try:
                sup =InternSupervisor.objects.get(supervisor__email=email,pdtp=user)
                f.supervisor =sup.supervisor
                f.pdtp =user
                f.save()
                subject="Leave  Request"
                from_email = 'pdtp@ict.go.ke'
                supervisor = sup.supervisor.first_name
                text_content = render_to_string(template_text, {"email":email,"supervisor":supervisor,
                    'leave_type':leave_type, 'start_date':start_date,'end_date':end_date,
                    'url':url,'intern':user.first_name,'intern_email':user.email})
                html_content = render_to_string(template_html, {"email":email,"supervisor":supervisor,
                    'leave_type':leave_type, 'start_date':start_date,'end_date':end_date,
                    'url':url,'intern':user.first_name,'intern_email':user.email})

                # mail.send([user.email],from_email,subject, html_message='Hi there!<br><p> Your mentor has given a feedback on one of your reports.<br>  Log on to the portal to view his response</p>')
                mail.send([sup.supervisor.email,], from_email,
                    subject=subject,
                    # message='Hi there! Your mentee has responded to your a meeting you scheduled. Log on to the portal to view his response',
                    html_message=html_content,
                    )
                    
              
                messages.add_message(request, messages.SUCCESS, 'Your Leave request has been submitted successfully')
                return HttpResponseRedirect('/app/my_leaves/')
            except:
                messages.add_message(request, messages.WARNING, 'Supervisor Does not exist. Contact secretariat to assign him to you and try a gain!')
                return HttpResponseRedirect('/app/my_leaves/')
        else:
            return render(request, 'pdtp/leave_apply.html', {'form':form})
    else:
        return render(request, 'pdtp/leave_apply.html', {'form':form})



@login_required
def leave_requests(request):
    user = request.user
    leaves = Leave.objects.filter(supervisor=user)
    form = LeaveApplicationSupervisor()
    if request.method == 'POST':
        form = LeaveApplicationSupervisor(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            template_html = 'email/approve_sup.html'
            supervisor_recommmended_days=request.POST['supervisor_recommmended_days']
            duties_delagated_to=request.POST['duties_delagated_to']
            supervisor_comment=request.POST['supervisor_comment']
          
            leave_id=request.POST['leave_id']
            leave_type=request.POST['leave_type']
            le = Leave.objects.get(id=int(leave_id))

            Leave.objects.filter(id=int(leave_id)).update(supervisor_recommmended_days=supervisor_recommmended_days,
                duties_delagated_to=duties_delagated_to,supervisor_comment=supervisor_comment,approved_by_supervisor=True)
            url='pdtpportal.icta.go.ke'
            subject="Leave  Approval"
            from_email = 'pdtp@ict.go.ke'
        
            
            html_content = render_to_string(template_html, {
                    'leave_type':leave_type,'url':url,'intern':user.first_name,})

                # mail.send([user.email],from_email,subject, html_message='Hi there!<br><p> Your mentor has given a feedback on one of your reports.<br>  Log on to the portal to view his response</p>')
            # mail.send([le.pdtp.email], from_email,
            #         subject=subject,
            #         # message='Hi there! Your mentee has responded to your a meeting you scheduled. Log on to the portal to view his response',
            #         message=html_content,
            #         )
            mail.send(
                [le.pdtp.email],
                from_email,
                subject=subject,
                html_message=html_content,
                )
                    
              
            messages.add_message(request, messages.SUCCESS, 'Your Leave request has been submitted successfully')
            return HttpResponseRedirect('.')
    else:
        return render(request, 'pdtp/leave_requests.html', {'leaves':leaves,'form':form})

@login_required
def leave_request(request):
    user = request.user
    leaves = Leave.objects.filter(recommended=False)
    
    return render(request, 'pdtp/leave_request.html', {'leaves':leaves,})



@login_required
def leave_requests_approval(request,leave_id, pk):
    pdtp = User.objects.get(id=pk)
    user =request.user
    leaves = Leave.objects.filter(pdtp=pdtp)
    leve = Leave.objects.get(id=leave_id)
    if request.method == 'POST':
        form = LeaveApplicationSecretariat(request.POST, instance=leve)
        if form.is_valid():
            f = form.save(commit=False)
            template_html = 'email/approve_sup.html'
           
    
            le = Leave.objects.get(id=int(leave_id))
            pemail =le.pdtp.email
            f.secretariat = user
            f.save()
            url='pdtpportal.icta.go.ke'
            subject="Leave  Approval"
            from_email = 'pdtp@ict.go.ke'
        
            
            html_content = render_to_string(template_html, {
                    'url':url,'intern':pdtp.first_name,})

                # mail.send([user.email],from_email,subject, html_message='Hi there!<br><p> Your mentor has given a feedback on one of your reports.<br>  Log on to the portal to view his response</p>')
            # mail.send([le.pdtp.email], from_email,
            #         subject=subject,
            #         # message='Hi there! Your mentee has responded to your a meeting you scheduled. Log on to the portal to view his response',
            #         message=html_content,
            #         )
            text_content = render_to_string(template_text, {"subject":subject,
                    'first_name':le.pdtp.first_name,
                    'last_name':le.pdtp.last_name, 'url':url})
            html_content = render_to_string(template_html, {"subject":subject,
                    'first_name':le.pdtp.first_name,
                    'last_name':le.pdtp.last_name, 'url':url})
            mail.send(
            [pemail],
            from_email,
             subject=subject,
             html_message=html_content,
            )
                    
              
            messages.add_message(request, messages.SUCCESS, 'Approval submitted successfully')
            return HttpResponseRedirect('/app/leave_request/')
    else:
        form = LeaveApplicationSecretariat(instance=leve)
        return render(request, 'pdtp/leave_approval.html', {'pdtp':pdtp,'leaves':leaves,'leve':leve,'form':form})





@login_required
def broadcast_messages(request):
    broadcasts = Broadcast.objects.all()
  
    return render(request, 'pdtp/broad_casts.html', {'broadcasts':broadcasts,})




@login_required
def send_broadcast_message(request):
    user = request.user
    form = BroadcastForm()
    if request.method == 'POST':
        form = BroadcastForm(request.POST, request.FILES)
        rec = request.POST['recipient']
        year = request.POST['year']
        message = request.POST['message']
        subject = request.POST['subject']
        y = PdtpYear.objects.get(id=year)
        m=y.year
        em =user.email 
        first_name = user.first_name
        last_name =user.last_name
        if form.is_valid():
            f = form.save(commit=False)
            f.sent_by = user
            
            if rec == 'FEMALE':
                f.save()
                task =female_emails.delay(m,subject,message,em,first_name,last_name)
            elif rec == "MALE":
                f.save()
                task =male_emails.delay(m,subject,message,em,first_name,last_name)
            elif rec == "PDTPS":
                f.save()
                task=pdtps_emails.delay(m,subject,message,em,first_name,last_name)
                
            elif rec == "SUPERVISORS":
                f.save()
                task =supervisors_emails.delay(m,subject,message,em,first_name,last_name)
            elif rec == "MENTORS":
                f.save()
                task = mentors_emails.delay(m,subject,message,em,first_name,last_name)
                

            elif rec == "ALL":
                f.save()
                task= all_emails.delay(m,subject,message,em,first_name,last_name)
            else:
                pass

        
            
                
    
                    
              
            messages.add_message(request, messages.SUCCESS, 'Message Sent Successfully')
            return HttpResponseRedirect('/app/broadcast_messages/')
            
        else:
            messages.add_message(request, messages.SUCCESS, 'Message Sent Successfully')
            return HttpResponseRedirect('/app/broadcast_messages/')
    else:
        return render(request, 'pdtp/send_message.html', {'form':form})




@login_required
def pdtp_broadcast_messages(request):
    user = request.user 
    broadcasts = Broadcast.objects.filter(year = user.userprofile.year,recipient= "ALL")
    if user.userprofile.gender == MALE:
        male_broadcasts = Broadcast.objects.filter(year = user.userprofile.year,recipient= "MALE PDTPS")

    elif user.userprofile.gender == FEMALE:
        male_broadcasts = Broadcast.objects.filter(year = user.userprofile.year,recipient= "FEMALE PDTPS")
    else:
        male_broadcasts = ''
    return render(request, 'pdtp/pdtpbroad_casts.html', {'broadcasts':broadcasts,'male_broadcasts':male_broadcasts})




@login_required
def supervisors_broadcast_messages(request):
    user = request.user 
    broadcasts = Broadcast.objects.filter(year = user.userprofile.year,recipient= "ALL")


    sup_broadcasts = Broadcast.objects.filter(recipient= "SUPERVISORS")


    men_broadcasts = Broadcast.objects.filter(recipient= "MENTORS")
    return render(request, 'pdtp/supbroad_casts.html', {'broadcasts':broadcasts,'male_broadcasts':sup_broadcasts,'men_broadcasts':men_broadcasts})




@login_required
def innovations_evaluations(request, year):
    user = request.user 
    innovations = InnovationSubmission.objects.filter(year=year)
    return render(request, 'pdtp/submitted_innovations.html', {'innovations':innovations})


@login_required
def view_innovation(request, id):
    user =request.user
    innovation = InnovationSubmission.objects.get(id=id)
    parameters =InnovationEvaluationParameter.objects.all()
    import datetime
    today = datetime.date.today()
    if request.method == "POST":
        if InnovationEvaluationData.objects.filter(datetime__month=today.month,innovation =innovation,evaluator=user).exists():
            messages.add_message(request, messages.WARNING, 'You had evaluated this innovation')
            url = reverse('view_innovation', kwargs={'id': innovation.id})
            return HttpResponseRedirect(url)
        else:
            for p in parameters:
                k =str(p.id)
                nn= 'n'+k
                rr ='r'+ k
                score =  request.POST.get(nn)
                remarks = request.POST.get(rr)
                InnovationEvaluationData.objects.create(evaluator=user,
                    innovation=innovation,score=score,comment=remarks,parameter=p)
                if InnovationEvaluationPerParam.objects.filter(innovation=innovation,parameter=p).exists():
                    update = InnovationEvaluationPerParam.objects.filter(innovation=innovation,parameter=p).first()
                    update.evaluators += 1
                else:
                    update=InnovationEvaluationPerParam.objects.create(innovation=innovation,parameter=p)
                update.total_score  += int(score)
                update.save()
        messages.add_message(request, messages.SUCCESS, 'Data Submitted ')

        url = reverse('view_innovation', kwargs={'id': innovation.id})
        return HttpResponseRedirect(url)
    else:
        return render(request, 'pdtp/view_innovation.html', {'parameters':parameters,'innovation':innovation})

@login_required
def innovations_evaluation_results(request):
    user =request.user

    data =InnovationEvaluationPerParam.objects.values('innovation','innovation__innovation_name').all().annotate(sum_score=Sum('average')).order_by('-sum_score')
    # data=InnovationEvaluationPerParam.objects.values('innovation','innovation__innovation_name').all().annotate(total=Count('innovation')).order_by('-average')
    # items = [
    # {'data': g['innovation__innovation_name'], 'value': g['total'] } for g in data
    # ]
    innovations =InnovationSubmission.objects.all()
    return render(request, 'pdtp/innovation_results.html', {'innovations':innovations,'data':data})

@login_required
def evaluate_innovation(request, id):
    parameters = InnovationEvaluationParameter.objects.all()
    innovation = InnovationSubmission.objects.get(id=id)
    return render(request, 'pdtp/evaluate_innovation.html', {'parameters':parameters,'innovation':innovation})

@login_required
def secretariat_quarterly_reports(request):
    user = request.user
    if user.userprofile.active == False:
        messages.add_message(request, messages.WARNING, 'Your account is inactive. contact the Secretariat')
        return HttpResponseRedirect('/app/dashboard/')

    reports = PhaseOrQuarter.objects.all()
    return render(request, 'secretariat/sec_quarterlyreports.html', {'reports':reports})

@login_required
def add_quarter(request):
    user = request.user
    if user.userprofile.active == False:
        messages.add_message(request, messages.WARNING, 'Your account is inactive. contact the Secretariat')
        return HttpResponseRedirect('/app/dashboard/')

    form = PhaseOrQuarterForm()
    if request.method == 'POST':

        form = PhaseOrQuarterForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.secretariat = user
            f.save()
            messages.add_message(request, messages.SUCCESS, 'You have Successfully added  new quarter/phase')
            return HttpResponseRedirect('/app/secretariat_quarterly_reports/')
    else:
        form = PhaseOrQuarterForm()

    return render(request, 'secretariat/new_quarter.html', {'form':form})
@login_required
def update_quarter(request, id):
    user = request.user
    if user.userprofile.active == False:
        messages.add_message(request, messages.WARNING, 'Your account is inactive. contact the Secretariat')
        return HttpResponseRedirect('/app/dashboard/')

    reports = get_object_or_404(PhaseOrQuarter, id=id)
    form = PhaseOrQuarterForm()
    if request.method == 'POST':

        form = PhaseOrQuarterForm(request.POST or None , instance=reports)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'You have Successfully update quarter/phase')
            return HttpResponseRedirect('/app/secretariat_quarterly_reports/')
    else:
        form = PhaseOrQuarterForm(instance=reports)

    return render(request, 'secretariat/quarterupdate.html', {'form':form})

def quarter_reports(request, id):
    report = get_object_or_404(PhaseOrQuarter, id=id)
    quarter = QuarterlyReport.objects.filter(quater=report)
    return render(request,'secretariat/quarters.html', {'quarter':quarter})

def sec_quarterpdf(request,*args, id):
    
    report = QuarterlyReport.objects.filter(id=id)
    template = get_template('secretariat/QuarterReport.html')
    
    context = {

        'report': report,

    }
    html = template.render(context)
    pdf = render_to_pdf('secretariat/QuarterReport.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "QuarterReport.pdf"
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")



@login_required
def apply_for_icta_tasks(request):
    if request.method == "POST":
        form = InternalApplicationForm(request.POST)
        if form.is_valid():
            user = request.user
            d = request.POST['application_category']
            f =form.save(commit= False)
            try:
                JobApps.objects.get(pdtp= user,application_category__id=d)
                messages.add_message(request, messages.WARNING, 'You have already Applied')
                return HttpResponseRedirect('/app/apply_for_icta_tasks/')
            except:
                f.pdtp = user
                f.save()
                messages.add_message(request, messages.SUCCESS, 'Your Application has been successfully submitted')
                return HttpResponseRedirect('/app/apply_for_icta_tasks/')
        else:
            messages.add_message(request, messages.WARNING, 'An Error Occured. Kindly try again and note you can only apply once')
            return HttpResponseRedirect('/app/apply_for_icta_tasks/')
    else:
        form = InternalApplicationForm()
        return render(request,'pdtp/submit_application.html',{'form':form})

def interests(request):
    interests = JobApps.objects.all()
    return render(request,'pdtp/interests.html',{'interests':interests})

#Laptop Processes;
@login_required
def laptop(request):
    user = request.user
    laptops = Laptop.objects.all()
    
    
    return render(request, 'secretariat/laptop.html', {'laptops':laptops})

@login_required
def post_laptop(request):
    user = request.user
    form = LaptopForm()
    if request.method == 'POST':
        form = LaptopForm(request.POST)
        if form.is_valid():

            f = form.save(commit=False)
            f.created_by = user
            f.save()
            messages.add_message(request, messages.SUCCESS, 'You have Successfully created a Loptop')
            return HttpResponseRedirect('/app/laptop/')
    else:
        form = LaptopForm()
    return render(request, 'secretariat/post_laptop.html',{'form':form})

def update_laptop(request,id):
    user = request.user
    laptop =  get_object_or_404(Laptop, id=id)
    form = LaptopForm()
    if request.method == 'POST':
        form = LaptopForm(request.POST or None, instance=laptop)
        if form.is_valid():
            f = form.save(commit=False)
            f.created_by = user
            f.save()
            messages.add_message(request, messages.SUCCESS, 'Laptop update was successful')
            return HttpResponseRedirect('/app/laptop/')
    else:
        form = LaptopForm(instance=laptop)

    return render(request, 'secretariat/post_laptop.html',{'form':form})

@login_required
def laptop_applicants(request, id):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    
    try:
        machine = get_object_or_404(Laptop, id=id)

        #year =PdtpYear.objects.get(year=year)
        applicants = LaptopOrder.objects.filter(laptop=machine).order_by('-id')
        return render(request,'pdtp/laptop.html',{'machine':machine,'applicants':applicants})
    except LaptopOrder.DoesNotExist:
        raise Http404

@login_required
def update_laptop_applicants(request,id):
    user = request.user
    order =LaptopOrder.objects.get(id=id)
    # year =PdtpYear.objects.get(year=year)
    form = LaptopApplicantsForm()
    if request.method == 'POST':
        form = LaptopApplicantsForm(request.POST or None, instance=order)
        if form.is_valid():
            Amount_Due = form.cleaned_data.get('Amount_Due')
            deduct = form.cleaned_data.get('deductions')
            pdtp = form.cleaned_data.get('pdtp')
            orda =order


            f = form.save(commit=False)
            f.Amount_Due = (Amount_Due-deduct)
            f.deductions = deduct
            payment_history = PaymentHistory.objects.create(pdtp=pdtp,payment=deduct,order=orda,updated_by=user)
            f.save()

            messages.add_message(request, messages.SUCCESS, 'You have Successfully updated Laptop Order')
            return HttpResponseRedirect('/app/laptop')

    else:
        form = LaptopApplicantsForm(instance=order)
    
    return render(request, 'secretariat/laptopapplication.html',{'form':form})


def my_laptop(request):
    user = request.user
    #history = PaymentHistory.objects.filter(pdtp=user)
    my_laps = LaptopOrder.objects.filter(pdtp=user).order_by('-id')
    return render(request, 'pdtp/my_laptop.html',{'my_laps':my_laps})
    

def laptop_list(request):
    user = request.user
    
    laptops = Laptop.objects.filter(status__icontains='available').order_by('-id')
    return render(request,'pdtp/laptoplist.html', {'laptops':laptops})

    

def apply_for_laptop(request,id):
    user = request.user
    yea = PdtpYear.objects.all()
    lptop = get_object_or_404(Laptop, id=id,status__icontains='available')
    prix = lptop.price
    if request.method =='POST':
        pdtp = request.user
        order = True
        laptop = request.POST.get('name')
        amount = prix
        year = request.POST.get('yeah')

        lapname= get_object_or_404(Laptop,laptop_name=laptop)
        
        yer= get_object_or_404(PdtpYear,year=year)  
        cohort = UserProfile.objects.get(user=pdtp)
        cohort_year = cohort.year    

        if yer == cohort_year:

            orda = LaptopOrder.objects.create(
                    pdtp=pdtp,
                    order=order,
                    laptop=lapname,
                    Amount_Due=amount,
                    year=yer
                )
           
            messages.add_message(request,messages.SUCCESS, 'You have succefully submitted your order')
            return HttpResponseRedirect('/app/my_laptop/')
        
        else:
            messages.add_message(request,messages.WARNING, 'Your cohort year does not match our records. ')
            return HttpResponseRedirect('/app/laptop_list/')

    return render(request,'pdtp/laptopapplication.html',{'year':yea,'laptop':lptop})


def request_interns(request):
    if request.method == "POST":
        form = InternRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.WARNING, 'Request Submitted Successfully. Our Secretariat will contact you soon')
            return HttpResponseRedirect('/app/request-for-interns/')
    else:
        form = InternRequestForm()
        return render(request, 'landing2/request.html',{'form':form})


def partnership_apply(request):
    if request.method == "POST":
        form = PartnerApplyForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            partnersship_reasons =[]
            reasons = request.POST.getlist('vehicle')
            for reasons in reasons:
                partnersship_reasons.append(reasons)
            f.partnership = partnersship_reasons
            form.save()
            messages.add_message(request,messages.WARNING, 'Request Submitted Successfully. Our Secretariat will contact you soon')
        return HttpResponseRedirect('/app/apply-for-partnership/')
    else:
        form = PartnerApplyForm()
        return render(request, 'landing2/apply.html',{'form':form})

def internsrequests(request):
    requests = InterRequest.objects.order_by('-id')
    return render(request, 'secretariat/requests.html', {'requests': requests})

def partnership_requests(request):
    requests = PartnerApply.objects.order_by('-id')
    return render(request, 'secretariat/prequests.html', {'requests': requests})