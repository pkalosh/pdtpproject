from django.core.files.storage import FileSystemStorage
from django.shortcuts import render,render_to_response,get_object_or_404
from django.contrib.auth.decorators import login_required
from pdtpproject.utils import render_to_pdf
from django.template import RequestContext
from django.contrib import messages
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from app.forms import *
from deployments.models import *
from deployments.forms import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.db.models import Count
    
from django import forms
from django.utils.http import is_safe_url
import datetime
today = datetime.datetime.today()
from django.db.models import Max, F
import datetime
from datetime import timedelta
from datetime import datetime as dt


from dateutil.relativedelta import relativedelta
from django.db import transaction
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from io import BytesIO
from reportlab.pdfgen import canvas
from django.template.loader import get_template
from weasyprint import HTML

from post_office import mail

@login_required
def organizations(request):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    if not user.groups.filter(name__in=['DEPLOYMENT OFFICERS']).exists():
        raise Http404
    organizations=Organization.objects.order_by('organization')
    return render(request,'orgs.html',{'organizations':organizations})



@login_required
def add_organization(request):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    if not user.groups.filter(name__in=['DEPLOYMENT OFFICERS']).exists():
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
        password=make_password(password='pdtp@ict',              
                  salt=None,
                  hasher='default')
        if form.is_valid()and uform.is_valid() and cform.is_valid() and sform.is_valid():
            u=sform.save(commit=False)
            try:
                user=User.objects.create(username=username,first_name=first_name,last_name=last_name,password=password,email=username)
                profile=UserProfile.objects.create(user=user,user_category="SUPERVISOR",phone_number=cell)
            except:
                messages.add_message(request, messages.WARNING, 'That User already exist. Please add him as a supervisor from the company')
                return HttpResponseRedirect('/deployments/add_organization/')
                
            organization=Organization.objects.create(category=category,organization=organization,location=location)
            u.organization=organization
            u.supervisor=user
            u.position=request.POST['position']
            u.is_contact_person=True
            u.save()
           
            messages.add_message(request, messages.SUCCESS, 'Organization Added Successfully, Add more More Organizations')
            return HttpResponseRedirect('/deployments/add_organization/')
    else:
        form=OrganizationForm()
        uform=UserForm()
        cform=ContactPersonForm()
        sform=SupervisorForm()
    context_dict={'form':form,'uform':uform,'cform':cform,'sform':sform
                  }
    return render(request,'addorg.html',context_dict)


@login_required
def organization_update(request,id):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    if not user.groups.filter(name__in=['DEPLOYMENT OFFICERS']).exists():
        raise Http404
    organization = get_object_or_404(Organization, id=id)
    if request.method == 'POST':
        form=OrganizationUpdateForm(request.POST, request.FILES or None, instance=organization)
        if form.is_valid():
            u=form.save(commit=False)
            try:
                newdoc = Organization(logo = request.FILES['logo'])
                newdoc.save
            except:
                pass
            u.save()
            
           
            messages.add_message(request, messages.SUCCESS, 'Organization Details updated Successfully')
            return HttpResponseRedirect('/deployments/organizations')
    else:
        form = OrganizationUpdateForm(instance=organization)
    return render(request,'orgupdate.html',{'form':form,'organization':organization})


@login_required
def deployments(request, year):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    if not user.groups.filter(name__in=['DEPLOYMENT OFFICERS']).exists():
        raise Http404
    year=PdtpYear.objects.get(year=year)
    #data=Deployment.objects.values('pdtp').filter(year=year).annotate(latest_date=Max('date_confirmed'))
    #data=Deployment.objects.annotate(Max('date_confirmed'))
    data=Deployment.objects.annotate(
    # annotate with MAX "baked_at" over all cakes in bakery
    latest_deployed=Max('pdtp__deployment__date_confirmed')
    # compare this cake "baked_at" with annotated latest in bakery
).filter(year=year,latest_deployed=F('date_confirmed'))
    #data=Deployment.objects.annotate(max_date=Max('date_confirmed')).filter(date=F('max_date'))
    #mentors_assigned=User.objects.filter(userprofile__mentor_availability=True,userprofile__user_category="MENTOR").exclude(User.objects__id__in=s)
    return render(request,'deployments/deployments.html',{'deployments':data,'year':year})
    
    
    #return render(request,'deployments/deployments.html',{'deployments':items,'year':year})
    

#Superviors
@login_required
def supervisors(request,id):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    if not user.groups.filter(name__in=['DEPLOYMENT OFFICERS']).exists():
        raise Http404
    organization = get_object_or_404(Organization, id=id)
    supervisors=Supervisor.objects.filter(organization=organization)
    return render(request,'deployments/supervisors.html',{'organization':organization,'supervisors':supervisors})


@login_required
def intern_supervisor(request):
    queryset=InternSupervisor.objects.filter(pdtp__userprofile__year__year=2018)
    return render(request,'deployments/intsup.html',{'queryset':queryset})





@login_required
def add_supervisor(request,id):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    if not user.groups.filter(name__in=['DEPLOYMENT OFFICERS']).exists():
        raise Http404
    uform=UserForm()
    form=SupervisorForm()
    organization=Organization.objects.get(id=id)
    cform=ContactPersonForm()
    if request.method == 'POST':
        form=SupervisorForm(request.POST)
        uform=UserForm(request.POST)
        username=request.POST['email']
        email=request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        cell=request.POST['phone_number']
        password=make_password(password='pdtp@ict',              
                  salt=None,
                  hasher='default')
        if form.is_valid()and uform.is_valid():
            u=form.save(commit=False)
            user=User.objects.create(username=username,first_name=first_name,last_name=last_name,password=password,email=email)
            profile=UserProfile.objects.create(user=user,user_category="SUPERVISOR",phone_number=cell)
            u.supervisor=user
            u.is_supervisor=True
            u.organization=organization
            u.save()
           
            messages.add_message(request, messages.SUCCESS, 'Supervisor Added Successfully, Add more More Organizations')
            next = request.GET.get('from')
            if next:
                return HttpResponseRedirect(next)
        form=SupervisorForm()
        uform=UserForm()
        cform=ContactPersonForm()
    context_dict={'form':form,'uform':uform,'cform':cform
                  }
    return render(request,'deployments/addsupervisor.html',context_dict)


#supervisor update
@login_required
def update_supervisor(request,id,user_id):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    if not user.groups.filter(name__in=['DEPLOYMENT OFFICERS']).exists():
        raise Http404
    supervisor = get_object_or_404(Supervisor, id=id)
    user = get_object_or_404(User, id=user_id)
    profile=get_object_or_404(UserProfile,user=user)
    if request.method == 'POST':
        form=SupervisorForm(request.POST or None, instance=supervisor)
        uform=UserForm(request.POST or None, instance=user)
        mform=SupervisorMentorForm(request.POST or None, instance=profile)
        if form.is_valid() and mform.is_valid():
            u=form.save(commit=False)
            m=mform.save(commit=False)
            '''username=request.POST['email']
            email=request.POST['email']
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            user=User.objects.get(id=user_id)
            user.username=username
            user.first_name=first_name
            user.last_name=last_name
            '''
            username=request.POST['email']
            user.email=username
            user.username=username
            user.save()
            '''
            #u.contact_person=user
            #y=mform.cleaned_data['mentor']
            if y==True:
                m.mentor_title=request.POST['position']
                m.mentor_company=supervisor.organization.organization
                m.phone_number=request.POST['phone_number']
            '''
            u.save()
            
            m.save()
           
            messages.add_message(request, messages.SUCCESS, "Supervisor's Details updated Successfully")
            next = request.GET.get('from')
            if next:
                return HttpResponseRedirect(next)
    else:
        form = SupervisorForm(instance=supervisor)
        uform=UserForm(instance=user)
        mform=SupervisorMentorForm(instance=profile)
        
    return render(request,'deployments/supupdate.html',{'form':form,'uform':uform,'mform':mform,'supervisor':supervisor})


@login_required
def private_sector(request,year):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    if not user.groups.filter(name__in=['DEPLOYMENT OFFICERS']).exists():
        raise Http404
    y=PdtpYear.objects.get(year=year)
    #privates=Organization.objects.filter(category=False).exclude(organization__in=Deployment.objects.all())
    privates=Organization.objects.filter(category=False).exclude(id__in = Deployment.objects.filter(year=y).values_list('organization', flat=True))
    data=Deployment.objects.values('organization','organization__organization','organization__id','organization__location','year__year').filter(year=y,sector="Private").annotate(total=Count('organization'))
    
    items = [
        {'organization': g['organization'],'name':g['organization__organization'],'id':g['organization__id'],'location':g['organization__location'],'year':g['year__year'],'total': g['total'] } for g in data
        ]
    
    return render(request,'deployments/private.html',{'privates':privates, 'items':items,'year':year})

@login_required
def to_private(request,id,year):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    if not user.groups.filter(name__in=['DEPLOYMENT OFFICERS']).exists():
        raise Http404
    context_dict={}
    organization=Organization.objects.get(id=id)
    request.session['organization'] = organization
    request.session['year'] = year
    y=PdtpYear.objects.get(year=year)
    if request.method=="POST":
        deployments=request.POST.getlist('pdtps')
        for pdtp in deployments:
            user=User.objects.get(username=pdtp)
            deployed = Deployment.objects.create(organization=organization, pdtp=user,year=y,sector="Private")
        messages.add_message(request, messages.SUCCESS, "PDTPs list sent succeffully to the company")
        return HttpResponseRedirect('.')

    
    form=DeploymentForm()
    #pdtps= UserProfile.get_pdtps().filter(year=y)
    pdtps=UserProfile.get_pdtps().filter(year=y).exclude(user__id__in = Deployment.objects.filter(year=y,sector="Private").values_list('pdtp', flat=True))
    
    
    return render(request,'deployments/newprivate.html',{'form':form,'pdtps':pdtps,'organization':organization,'year':year})

def pdtps_to_interview(request,id):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    try:
        company=Organization.objects.get(id=id)
        pdtps=Deployment.objects.filter(organization=company,confirmed=False)
        interviewees=Deployment.objects.filter(organization=company,confirmed=False,interview=False)
        intakes=Deployment.objects.filter(organization=company,confirmed=True)
        form=DeploymentForm()
        iform=InterviewForm()
        if request.method=="POST":
            deployments=request.POST.getlist('pdtps')
            date=request.POST.get('date')
            instructions=request.POST['reporting_details']
            two_months = datetime.date.today() + relativedelta(months=+2)
            pdtps=Deployment.objects.filter(organization=company,confirmed=False)
            Deployment.objects.filter(id__in=deployments).update(confirmed=True,date_confirmed=datetime.date.today(),completion_date=two_months,reporting_details=instructions, reporting_date=date)
            Deployment.objects.filter(organization=company,confirmed=False).exclude(id__in=deployments).delete() 
            messages.add_message(request, messages.SUCCESS, "Confirmation Successful, The pdtps and the secretariat has been notified")
            return HttpResponseRedirect('.')
        return render(request,'deployments/interview.html',{'pdtps':pdtps, 'interviewees':interviewees,'iform':iform,'form':form,'organization':company,'intakes':intakes})
    except:
        raise Http404
def interns_pending_confirmation(request,year):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    #company=Organization.objects.get(id=id)
    year=PdtpYear.objects.get(year=year)
    pdtps=Deployment.objects.filter(year=year,confirmed=False)
    return render(request,'deployments/pending.html',{'pdtps':pdtps,'year':year})

def pdtpts_attached(request,id,slug):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    try:
        company=Organization.objects.filter(slug=slug).get(id=id)
        intakes=Deployment.objects.filter(organization=company,confirmed=True).order_by('-id')
    except:
        raise Http404
    return render(request,'deployments/attached.html',{'organization':company,'intakes':intakes})

def organization_supervisors(request,id,slug):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    company=Organization.objects.filter(slug=slug).get(id=id)
    intakes=Supervisor.objects.filter(organization=company,is_supervisor=True).order_by('-id')
    return render(request,'deployments/orgsups.html',{'organization':company,'intakes':intakes})

def interview_invitation(request,id):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    company=Organization.objects.get(id=id)
    if request.method=="POST":
        deployments=request.POST.getlist('interviewees')
        date=request.POST.get('interviewdate')
        instructions=request.POST['interview_instructions']
        #two_months = datetime.date.today() + relativedelta(months=+2)
        Deployment.objects.filter(id__in=deployments).update(interview=True,date_invited=datetime.date.today(),interview_instructions=instructions, interview_date=date)
        Deployment.objects.filter(organization=company,confirmed=False,interview=False).exclude(id__in=deployments).delete() 
        
        messages.add_message(request, messages.SUCCESS, "Interview Invitation has been sent successfully")
        next = request.GET.get('from')
        if next:
            return HttpResponseRedirect(next)
    #return render(request,'deployments/interview.html',{'pdtps':pdtps, 'interviewees':interviewees,'iform':iform,'form':form,'organization':company,'intakes':intakes})


@login_required
def public_sector(request,year):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    if not user.groups.filter(name__in=['DEPLOYMENT OFFICERS']).exists():
        raise Http404
    y=PdtpYear.objects.get(year=year)
    #privates=Organization.objects.filter(category=False).exclude(organization__in=Deployment.objects.all())
    privates=Organization.objects.filter(category=True).exclude(id__in = Deployment.objects.filter(year=y).values_list('organization', flat=True))
    data=Deployment.objects.values('organization','organization__organization','organization__id','organization__location','year__year').filter(year=y,sector="Public").annotate(total=Count('organization'))
    
    items = [
        {'organization': g['organization'],'name':g['organization__organization'],'id':g['organization__id'],'location':g['organization__location'],'year':g['year__year'],'total': g['total'] } for g in data
        ]
    
    return render(request,'deployments/public.html',{'privates':privates, 'items':items,'year':year})

@login_required
def to_public(request,id,year):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    if not user.groups.filter(name__in=['DEPLOYMENT OFFICERS']).exists():
        raise Http404
    context_dict={}
    organization=Organization.objects.get(id=id)
    request.session['organization'] = organization
    request.session['year'] = year
    y=PdtpYear.objects.get(year=year)
    if request.method=="POST":
        deployments=request.POST.getlist('pdtps')
        for pdtp in deployments:
            user=User.objects.get(username=pdtp)
            deployed = Deployment.objects.create(organization=organization, pdtp=user,year=y,sector="Public")
        messages.add_message(request, messages.SUCCESS, "PDTPs list sent succeffully to the company")
        return HttpResponseRedirect('.')

    
    form=DeploymentForm()
    #pdtps= UserProfile.get_pdtps().filter(year=y)
    pdtps=UserProfile.get_pdtps().filter(year=y).exclude(user__id__in = Deployment.objects.filter(year=y,sector="Public").values_list('pdtp', flat=True))
    
    
    return render(request,'deployments/newpublic.html',{'form':form,'pdtps':pdtps,'organization':organization,'year':year})

@login_required
@transaction.atomic
def redeploy(request,year,user_id,organization_id):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    organization=Organization.objects.get(id=organization_id)
    pdtp=User.objects.get(id=user_id)
    organizations=Organization.objects.all()
    y=PdtpYear.objects.get(year=year)
    if request.method=="POST":
        deployments=request.POST.getlist('company')
        for company in deployments:
            org=Organization.objects.get(id=company)
            sector=org.category
            if sector ==False:
                sec ="Private"
            else:
                sec="Public"
            deployed = Deployment.objects.create(organization=org, confirmed=False, pdtp=pdtp,year=y,sector=sec)
            messages.add_message(request, messages.SUCCESS, "PDTP list sent succeffully to the company")
        return HttpResponseRedirect('.')
    return render(request,'deployments/redeploy.html',{'year':year,'pdtp':pdtp,'organization':organization,'organizations':organizations})

@login_required
@transaction.atomic
def pick_supervisor(request,id):
    raise Http404
'''
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    #organization=Organization.objects.get(id=org_id)
    pdtp=User.objects.get(id=id)
    supervisors=Supervisor.objects.filter(Q(is_supervisor=True) | Q(is_contact_person=True))
    if request.method=='POST':
        sups=request.POST.getlist('pdtps')
        for sup in sups:
            #s=User.objects.get(id=sup)
        #sup=User.objects.get(id=supervisor)
            sx=Supervisor.objects.get(id=sup)
            s=sx.supervisor
            org =sx.organization
            internsup=InternSupervisor.objects.create(pdtp=pdtp,supervisor=s,company=org)
        messages.add_message(request, messages.SUCCESS, "Supervisor Added Successfully")
        return HttpResponseRedirect('/app/dashboard/')
    return render(request,'deployments/pick_supervisor.html',{'pdtp':pdtp,'supervisors':supervisors})
'''
# @login_required
# def my_interns(request,id):
#     user = request.user
#     try:
#         if MustChangePassword.objects.get(user=user):
#             request.session['email'] = user.email
#             return HttpResponseRedirect('/app/password_change/')
#     except:
#         pass
#     pdtp=User.objects.get(id=id)
#     return render(request,'pdtp/pick.html',{'pdtp':pdtp,})

@login_required
@transaction.atomic
def supervisor_evaluation(request,id):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    sup=Supervisor.objects.get(supervisor=user)
    if not sup.is_supervisor:
        raise Http404
    pdtp=User.objects.get(id=id)
    parametors=Parametor.objects.all()
    return render(request,'mentors/evaluate.html',{'pdtp':pdtp,'parametors':parametors})

@login_required
def my_interns(request):
    user = request.user
    interns = InternSupervisor.objects.filter(supervisor=user,pdtp__userprofile__year__year=2018) #,year="2018"
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    #supervisor=User.objects.get(id=id)
    #interns=Supervisor.objects.filter(supervisor=supervisor)
    return render(request,'mentors/interns.html',{'interns':interns})
@login_required
def my_mentees(request):
    user = request.user
    mentees = MentorMenteeMapping.objects.filter(mentor=user,mentee__userprofile__year__year=2018)
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    form = MeetingForm()
    #supervisor=User.objects.get(id=id)
    #interns=MentorMenteeMapping.objects.filter(supervisor=supervisor)
    if request.method == "POST":
        form = MeetingForm(request.POST)
        if form.is_valid():
            f=form.save(commit=False)
            m = request.POST['mentee']
            mentee = User.objects.get(id=m)
            f.mentee = User.objects.get(id=m)
            f.mentor = request.user
            f.save()
            messages.add_message(request, messages.SUCCESS, 'Meeting Booked Successfully')
            recipients =[mentee.email]
            mail.send([mentee.email], 'pdtp@ict.go.ke',
                    subject='Mentorship Meeting',
                    message='Hi there! Your mentor has scheduled a meeting with you. Login to the portal to view details',
                    html_message='Hi there!<br><p> Your mentor has scheduled a meeting with you. Login to the portal to view details</p>',
                    )
            mail.send(
                    [request.user.email], # List of email addresses also accepted
                    'pdtp@ict.go.ke',
                    subject='Mentorship Meeting',
                    message='Hi there! You have succesfully scheduled a meeting  with your mentee',
                    html_message='Hi there!<br><p> You have succesfully scheduled a meeting  with your mentee. Login to the portal to view details</p>',
                    )
            
            return HttpResponseRedirect('/deployments/my_mentees/')
            
        else:
            form = MeetingForm()
            return HttpResponseRedirect('/deployments/my_mentees/')
    return render(request,'mentors/mentees.html',{'form':form,'mentees':mentees})

@login_required
def add_orgsupervisor(request,id,slug):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    if not Organization.objects.filter(slug=slug).get(id=id):
        raise Http404
    uform=UserForm()
    form=OrgSupervisorForm()
    organization=Organization.objects.get(id=id)
    cform=ContactPersonForm()
    if request.method == 'POST':
        form=OrgSupervisorForm(request.POST)
        uform=UserForm(request.POST)
        username=request.POST['email']
        email=request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        cell=request.POST['phone_number']
        password=make_password(password='pdtp@ict',              
                  salt=None,
                  hasher='default')
        if form.is_valid()and uform.is_valid():
            u=form.save(commit=False)
            user=User.objects.create(username=username,first_name=first_name,last_name=last_name,password=password,email=email)
            profile=UserProfile.objects.create(user=user,user_category="SUPERVISOR",phone_number=cell)
            u.supervisor=user
            u.is_supervisor=True
            u.organization=organization
            u.save()
           
            messages.add_message(request, messages.SUCCESS, 'Supervisor Added Successfully, Add more More Organizations')
            next = request.GET.get('from')
            if next:
                return HttpResponseRedirect(next)
        form=OrgSupervisorForm()
        uform=UserForm()
        cform=ContactPersonForm()
    context_dict={'form':form,'uform':uform,'cform':cform,'organization':organization
                  }
    return render(request,'deployments/addorgsup.html',context_dict)

#supervisor update
@login_required
def update_orgsupervisor(request,id,slug,user_id):
    user = request.user
    try:
        if MustChangePassword.objects.get(user=user):
            request.session['email'] = user.email
            return HttpResponseRedirect('/app/password_change/')
    except:
        pass
    if not Organization.objects.filter(slug=slug).get(id=id):
        raise Http404
    supervisor = get_object_or_404(Supervisor, id=user_id)
    organization=Organization.objects.filter(slug=slug).get(id=id)
    user = get_object_or_404(User, id=user_id)
    profile=get_object_or_404(UserProfile,user=user)
    if request.method == 'POST':
        form=OrgSupervisorForm(request.POST or None, instance=supervisor)
        uform=UserForm(request.POST or None, instance=user)
        if form.is_valid():
            u=form.save(commit=False)
            '''username=request.POST['email']
            email=request.POST['email']
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            user=User.objects.get(id=user_id)
            user.username=username
            user.first_name=first_name
            user.last_name=last_name
            '''
            username=request.POST['email']
            user.email=username
            user.username=username
            user.save()
            '''
            #u.contact_person=user
            #y=mform.cleaned_data['mentor']
            if y==True:
                m.mentor_title=request.POST['position']
                m.mentor_company=supervisor.organization.organization
                m.phone_number=request.POST['phone_number']
            '''
            u.save()
            
    
           
            messages.add_message(request, messages.SUCCESS, "Supervisor's Details updated Successfully")
            next = request.GET.get('from')
            if next:
                return HttpResponseRedirect(next)
    else:
        form = OrgSupervisorForm(instance=supervisor)
        uform=UserForm(instance=user)
        
        
    return render(request,'deployments/orgsupupdate.html',{'form':form,'uform':uform,'organization':organization,'supervisor':supervisor})

def assign_supervisor(request,slug,id):
    user = request.user
    if user.userprofile.active == False:
        messages.add_message(request, messages.WARNING, 'Your account is inactive. contact the Secretariat')
        return HttpResponseRedirect('/app/dashboard/')
    org=Organization.objects.filter(slug=slug).get(id=id)
    #interns=Deployment.objects.filter(organization=org,confirmed=True).exclude(pdtp_user__in=InternSupervisor.objects.filter(company=org))
    interns=Deployment.objects.filter(organization=org,confirmed=True).exclude(pdtp__in = InternSupervisor.objects.filter(company=org).values_list('pdtp', flat=True))
    supervisors=Supervisor.objects.filter(organization=org,is_supervisor=True)
    if request.method=="POST":
        interns=request.POST.getlist('interns')
        supervisor=request.POST['supervisor']
        for intan in interns:
            inta =User.objects.get(id=intan)
            sup=User.objects.get(id=supervisor)
            InternSupervisor.objects.create(pdtp=inta,supervisor=sup,company=org)
        messages.add_message(request, messages.SUCCESS, "Supervisor Assignment Successful")
        return HttpResponseRedirect('.')
    return render(request,'deployments/assign.html',{'interns':interns,'supervisors':supervisors})



@login_required
def my_me_reports(request):
    user = request.user
    reports = MonitoringAndEvaluation.objects.filter(pdtp=user)
    return render(request,'pdtp/myreports.html', {'reports':reports})

@login_required
def phase_list(request):
    phases = MonitoringAndEvaluationPhase.objects.filter(status__status__iexact='Open')        
    return render(request, 'pdtp/phaselist.html', {'phases':phases})



@login_required
def monitoring_evaluation(request,id):
    user = request.user
    if user.userprofile.active == False:
        messages.add_message(request, messages.WARNING, 'Your account is inactive. contact the Secretariat')
        return HttpResponseRedirect('/app/dashboard/')

    phas = get_object_or_404(MonitoringAndEvaluationPhase,id=id,)
    itern_me_params = InternMEParameter.objects.all()
    supervisor = InternSupervisor.objects.filter(pdtp=user)

    if request.method == 'POST':
        form = InternMEForm(request.POST)
        if form.is_valid():
            f= form.save(commit=False)
            x = request.POST.get('supervis')
            supa = User.objects.get(username=x)
            f.pdtp=request.user

            f.year= user.userprofile.year
            f.phase = phas
            f.supervisor = supa
        
        
            try:
                monitor = MonitoringAndEvaluation.objects.get(pdtp=f.pdtp,phase=f.phase, supervisor=f.supervisor)
                messages.add_message(request, messages.WARNING, 'Already submitted  Report for this Phase')
                return HttpResponseRedirect('/deployments/phase_list/')
            except MonitoringAndEvaluation.DoesNotExist:
                f.save()
        
          
                parameters =InternMEParameter.objects.all()
                for p in parameters:
                    k = str(p.id)
                    rate =  request.POST.get(k)
                    InternMERate.objects.create(pdtp=f.pdtp,intern_parameter=p,phase=phas,rate=rate)
                messages.add_message(request, messages.SUCCESS, 'You have Successful submitted You M&E report')
                return HttpResponseRedirect('/deployments/phase_list/')         
    else:
        form = InternMEForm(instance=phas)             


    return render(request, 'pdtp/monitoring_evaluation.html', {'phase':phas, 'supervisor':supervisor,'itern_me_params':itern_me_params, 'form':form})


@login_required
def supervisor_monitoring_report(request,id):
    user = request.user
    if user.userprofile.active == False:
        messages.add_message(request, messages.WARNING, 'Your account is inactive. contact the Secretariat')
        return HttpResponseRedirect('/app/dashboard/')
    supervisor_me_param = SupervisorMEParameter.objects.all()
    report = get_object_or_404(MonitoringAndEvaluation, id=id)
    if request.method == 'POST':
        supervisor = request.user
        intern_strength= request.POST.get('me-intern_strength')
        areas_improvement= request.POST.get('areas_improvement')


        
        MonitoringAndEvaluation.objects.update(
                    supervisor= supervisor,
                    intern_strength=intern_strength,
                    areas_improvement=areas_improvement,
                    date_supervisor_submitted=today
                    )
        supervisor_me_param = SupervisorMEParameter.objects.all()
        for p in supervisor_me_param:

            report = get_object_or_404(MonitoringAndEvaluation, id=id)
            pdtp = report.pdtp
            phas = report.phase
            k = str(p.id)
            Jibu =  request.POST.get(k)
            SupervisorMERate.objects.create(supervisor=supervisor,pdtp=pdtp,supervisor_parameter=p,phase=phas,Jibu=Jibu)
        
            
            
        messages.add_message(request, messages.SUCCESS, 'You have Successful submitted You M&E report')
        return HttpResponseRedirect('/deployments/my_interns/')
    return render(request, 'pdtp/monitoring_evaluation.html', {'supervisor_me_param':supervisor_me_param})



@login_required
def view_Internmereport(request,id):
    user = request.user
    if user.userprofile.active == False:
        messages.add_message(request, messages.WARNING, 'Your account is inactive. contact the Secretariat')
        return HttpResponseRedirect('/app/dashboard/')
    pdtp = get_object_or_404(User, id=id)
    reports=MonitoringAndEvaluation.objects.filter(pdtp=pdtp)
    return render(request,'mentors/m&e.html', {'reports':reports})

#secretariat

@login_required
def monitoring_evaluation_phases(request):
    user = request.user
    if user.userprofile.active == False:
        messages.add_message(request, messages.WARNING, 'Your account is inactive. contact the Secretariat')
        return HttpResponseRedirect('/app/dashboard/')

    reports = MonitoringAndEvaluationPhase.objects.all()

    return render(request, 'secretariat/mephase.html', {"reports":reports})
    # ,'intern_param':intern_param,
    #     'supervisor_param':supervisor_param
@login_required
def create_me_phase(request):
    user = request.user
    if user.userprofile.active == False:
        messages.add_message(request, messages.WARNING, 'Your account is inactive. contact the Secretariat')
        return HttpResponseRedirect('/app/dashboard/')

    form = PhaseForm()
    if request.method == 'POST':

        form = PhaseForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.secretariat = user
            f.save()
            messages.add_message(request, messages.SUCCESS, 'You have Successfully added  new Monitoring and Evaluation phase')
            return HttpResponseRedirect('/deployments/monitoring_evaluation_phases/')
    else:
        form = PhaseOrQuarterForm()

    return render(request, 'secretariat/new_phase.html', {'form':form})
@login_required
def update_phase(request, id):
    user = request.user
    if user.userprofile.active == False:
        messages.add_message(request, messages.WARNING, 'Your account is inactive. contact the Secretariat')
        return HttpResponseRedirect('/app/dashboard/')

    report = get_object_or_404(MonitoringAndEvaluationPhase, id=id)
    form = PhaseForm()
    if request.method == 'POST':

        form = PhaseForm(request.POST or None , instance=report)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'You have Successfully updated Moniotring and Evaluation phase')
            return HttpResponseRedirect('/deployments/monitoring_evaluation_phases/')
    else:
        form = PhaseForm(instance=report)

    return render(request, 'secretariat/phaseupdate.html', {'form':form})

def monitoring_and_evaluation_reports(request, id):
    report = get_object_or_404(MonitoringAndEvaluationPhase, id=id)

    mereport = MonitoringAndEvaluation.objects.filter(phase=report)
    return render(request,'secretariat/sec_m&e.html', {'mereport':mereport})

@login_required
def me_report(request,*args, id):
    report = MonitoringAndEvaluation.objects.get(id=id)
    inta = report.pdtp.username
    supervi = report.supervisor.username
    print(supervi)
    phae = report.phase.phase
    phaz = MonitoringAndEvaluationPhase.objects.get(phase=phae)
    intun = User.objects.get(username=inta)
    superv = User.objects.get(username=supervi)
    rates = InternMERate.objects.filter(pdtp=intun,phase=phaz)
    jibu = SupervisorMERate.objects.filter(supervisor=superv,pdtp=intun,phase=phaz)
    template = get_template('secretariat/mepdf.html')
    
    context = {

        'report': report,
        'rate':rates,
        'jibu':jibu,

    }
    html = template.render(context)
    pdf = render_to_pdf('secretariat/mepdf.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "monitoring&evaluation.pdf"
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

@login_required
def me_intern(request,*args, id):
    report = MonitoringAndEvaluation.objects.get(id=id)
    inta = report.pdtp.username
    phae = report.phase.phase
    phaz = MonitoringAndEvaluationPhase.objects.get(phase=phae)
    intun = User.objects.get(username=inta)
    rates = InternMERate.objects.filter(pdtp=intun,phase=phaz)
    template = get_template('pdtp/intern.html')
    
    context = {

        'report': report,
        'rate':rates,

    }
    html = template.render(context)
    pdf = render_to_pdf('pdtp/intern.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "monitoring&evaluation.pdf"
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
@login_required
def attendance(request):
    user = request.user
    if user.userprofile.active == False:
        messages.add_message(request, messages.WARNING, 'Your account is inactive. contact the Secretariat')
        return HttpResponseRedirect('/app/dashboard/')
    form = AttendanceForm()
    
    interns=InternSupervisor.objects.filter(supervisor=user)
    if request.method == 'POST':
        pdtp = request.POST.getlist('pdtp')
        days = request.POST.getlist('days')
        
        # interns=request.POST.getlist('interns')
        # supervisor=request.POST.get('supervisor')
        data = dict((str(k), v) for k, v in zip(pdtp,days)) 
        # for k,v in data.items():
        for x in data:
            day = data[x]
            inta = User.objects.get(username=x)

      

            Attendance.objects.create(pdtp=inta, days_attended=day,supervisor=user)
        messages.add_message(request, messages.SUCCESS, "Successfully submitted This Month attendance")
        
            

            

              
        return HttpResponseRedirect('/app/dashboard/')
    else:
        form = AttendanceForm()

    return render(request, 'mentors/attendance.html', {'form':form,'interns':interns})

@login_required
def attendance_report(request):
    user = request.user
    if user.userprofile.active == False:
        messages.add_message(request, messages.WARNING, 'your account is inactive. Contact the secretariat')
        return HttpResponseRedirect('/app/dashboard/')
    context_dict={}
    if request.method == 'POST':
        start=request.POST['startdate']
        end=request.POST['enddate']
        attendance = Attendance.objects.filter(date_submitted__range=[start, end])
        
        context_dict['attendance']=attendance

    return render(request, 'secretariat/attendancereport.html', context_dict)

@login_required
def my_quarterly_reports(request):
    user = request.user
    quarter = QuarterlyReport.objects.filter(pdtp=user)
    return render(request,'pdtp/myquaters.html', {'reports':quarter})

@login_required
def quarter_list(request):
    quarters = PhaseOrQuarter.objects.filter(status__status__iexact='Open')        
    return render(request, 'pdtp/quarterlist.html', {'quarters':quarters})

def quarterly_reports(request, id):
    user = request.user
    if user.userprofile.active == False:
        messages.add_message(request, messages.WARNING, 'Your account is inactive. contact the Secretariat')
        return HttpResponseRedirect('/app/dashboard/')

    quarter = get_object_or_404(PhaseOrQuarter, id=id)
    project_cat = ProjectSection.objects.all()
    superviso = InternSupervisor.objects.filter(pdtp=user)

    if request.method == 'POST':
        
        form = QuarterlyReportForm(request.POST)
        
        
        if form.is_valid():
            x = request.POST.get('supervis')
            supa = User.objects.get(username=x)

            f = form.save(commit=False)
            f.year = user.userprofile.year
            f.quater = quarter
            f.pdtp = request.user
            f.supervisor =supa
            
            try:
                re = QuarterlyReport.objects.get(pdtp=f.pdtp, quater=f.quater)
                messages.add_message(request, messages.WARNING, 'Report for this User and Quarter Already exist')
                return HttpResponseRedirect('/deployments/quarter_list/')
            except QuarterlyReport.DoesNotExist:
                f.save()
                messages.add_message(request, messages.SUCCESS, 'You have Successfully submitted your report')
                return HttpResponseRedirect('/deployments/quarter_list/')


    else:
        form = QuarterlyReportForm()
    return render(request, 'pdtp/quarterly.html', {'supervisor':superviso,'form':form,'project_cat':project_cat, 'quarter':quarter})


#for supervisor starts here
@login_required
def reports_quarterly(request, id):
    user = request.user
    if user.userprofile.active == False:
        messages.add_message(request, messages.WARNING, 'Your account is inactive. contact the Secretariat')
        return HttpResponseRedirect('/app/dashboard/')

    
    pdtp = get_object_or_404(User, id=id)
    report = QuarterlyReport.objects.filter(pdtp=pdtp,supervisor=user)

    return render(request, 'mentors/approve_quarterly.html',{'report':report})

@login_required
def approve_reports_quarterly(request,id):
    user = request.user
    if user.userprofile.active == False:
        messages.add_message(request, messages.WARNING, 'Your account is inactive. contact the Secretariat')
        return HttpResponseRedirect('/app/dashboard/')
    report = get_object_or_404(QuarterlyReport, id=id)

    form = SupervisorQuarterlyCommentForm(request.POST)
    if request.method == "POST":
        form = SupervisorQuarterlyCommentForm(request.POST)
        if form.is_valid():
            i = form.save(commit=False)
            i.supervisor = user
            i.pdtp = report.pdtp
            comment = form.cleaned_data.get('comments')
            QuarterlyReport.objects.update(approved=True,comments=comment)

            messages.add_message(request, messages.SUCCESS, 'You have succefully Approved and submitted your report comments')
            return HttpResponseRedirect('/deployments/my_interns/')

    else:
        form = SupervisorQuarterlyCommentForm()

    return render(request, 'mentors/approve_report.html',{'report':report,'form':form})

#for supervisor ends here

def pdf_QuarterReport(request,*args, id):
    
    pdtp = request.user
    report = QuarterlyReport.objects.filter(pdtp=pdtp,id=id)
    template = get_template('pdtp/QuarterReport.html')
    
    context = {

        'report': report,

    }
    html = template.render(context)
    pdf = render_to_pdf('pdtp/QuarterReport.html', context)
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