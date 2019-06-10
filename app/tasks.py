from django.utils.crypto import get_random_string
from celery import shared_task, current_task
import socket
import subprocess
from app.models import *
from django.http import HttpResponse, HttpResponseRedirect, Http404
import os, sys, socket
from deployments.models import *
from post_office import mail
from_email = 'pdtp@ict.go.ke'
template_html = 'email/broad.html'
template_text = 'email/broad.txt'
from django.template.loader import render_to_string, get_template



@shared_task(bind=True)
def mentors_emails(self,m,subject,message, em, first_name, last_name):
    mentors =Supervisor.get_mentors()
    for f in mentors:
        text_content = render_to_string(template_text, {"subject":subject,
                    'message':message, 'em':em,'first_name':first_name,
                    'last_name':last_name,'rec':f.supervisor.first_name})
        html_content = render_to_string(template_html, {"subject":subject,
                    'message':message, 'em':em,'first_name':first_name,
                    'last_name':last_name,'rec':f.supervisor.first_name})
        mail =mail.send(
        [f.supervisor.email],
        from_email,
         subject=subject,
         html_message=html_content
         
            )
       

@shared_task(bind=True)
def supervisors_emails(self,m,subject,message, em, first_name, last_name):
    supervisors =Supervisor.get_supervisors()
    for f in supervisors:
        text_content = render_to_string(template_text, {"subject":subject,
                    'message':message, 'em':em,'first_name':first_name,
                    'last_name':last_name,'rec':f.supervisor.first_name})
        html_content = render_to_string(template_html, {"subject":subject,
                    'message':message, 'em':em,'first_name':first_name,
                    'last_name':last_name,'rec':f.supervisor.first_name})
        mail.send(
        [f.supervisor.email],
        from_email,
         subject=subject,
         html_message=html_content
    )
    

@shared_task(bind=True)
def female_emails(self,m,subject,message, em, first_name, last_name):
    females=UserProfile.get_pdtps_female().filter(year__year=m,  active=True)
    for f in females:
        text_content = render_to_string(template_text, {"subject":subject,
                    'message':message, 'em':em,'first_name':first_name,
                    'last_name':last_name,'rec':f.user.first_name})
        html_content = render_to_string(template_html, {"subject":subject,
                    'message':message, 'em':em,'first_name':first_name,
                    'last_name':last_name,'rec':f.user.first_name})
        mail.send(
        [f.user.email],
        from_email,
         subject=subject,
         html_message=html_content
         )
    

@shared_task(bind=True)
def male_emails(self,m,subject,message, em, first_name, last_name):
    males=UserProfile.get_pdtps_male().filter(year__year=m,  active=True)
    for f in males:
        text_content = render_to_string(template_text, {"subject":subject,
                    'message':message, 'em':em,'first_name':first_name,
                    'last_name':last_name,'rec':f.user.first_name})
        html_content = render_to_string(template_html, {"subject":subject,
                    'message':message, 'em':em,'first_name':first_name,
                    'last_name':last_name,'rec':f.user.first_name})
        mail.send(
        [f.user.email],
        from_email,
         subject=subject,
         html_message=html_content
        )
# pdtps = UserProfile.get_pdtps().filter(year__year=m, active=True)
# for f in pdtps: 
@shared_task(bind=True)
def pdtps_emails(self,m,subject,message, em, first_name, last_name):
    pdtps = UserProfile.get_pdtps().filter(year__year=m, active=True)
    for f in pdtps:
        text_content = render_to_string(template_text, {"subject":subject,
                    'message':message, 'em':em,'first_name':first_name,
                    'last_name':last_name,'rec':f.user.first_name})
        html_content = render_to_string(template_html, {"subject":subject,
                    'message':message, 'em':em,'first_name':first_name,
                    'last_name':last_name,'rec':f.user.first_name})
        mail.send(
        [f.user.email],
        from_email,
         subject=subject,
         html_message=html_content
    )
    
@shared_task(bind=True)
def all_emails(self,m,subject,message, em, first_name, last_name):
    all_users =UserProfile.objects.filter(active=True)
    for f in all_users:
        text_content = render_to_string(template_text, {"subject":subject,
                    'message':message, 'em':em,'first_name':first_name,
                    'last_name':last_name,'rec':f.user.first_name})
        html_content = render_to_string(template_html, {"subject":subject,
                    'message':message, 'em':em,'first_name':first_name,
                    'last_name':last_name,'rec':f.user.first_name})
        mail.send(
        [f.user.email],
        from_email,
         subject=subject,
         html_message=html_content
    )
    