
from django.conf.urls import url
from deployments.views import *
from app.views import *
#Organizations and deployment
urlpatterns = [
    url(r'^organizations/$', organizations ,name = 'organizations'),
    url(r'^add_organization/$', add_organization ,name = 'add_organization'),
    url(r'^organization_update/(?P<id>\d+)/$', organization_update ,name = 'organization_update'),
    url(r'^(?P<year>[-\w]+)/deployments/$', deployments ,name = 'deployments'),
    url(r'^(?P<year>[-\w]+)/private_sector/$', private_sector ,name = 'private_sector'),
    url(r'^to_private/(?P<id>\d+)/(?P<year>[-\w]+)/$',to_private,name = 'to_private'),
    url(r'^(?P<year>[-\w]+)/public_sector/$', public_sector ,name = 'public_sector'),
    url(r'^to_public/(?P<id>\d+)/(?P<year>[-\w]+)/$',to_public,name = 'to_public'),
    #Supevisors
    url(r'^supervisors/(?P<id>\d+)/$',supervisors,name = 'supervisors'),
    url(r'^(?P<id>\d+)/add_supervisor/$', add_supervisor ,name = 'add_supervisor'),
    url(r'^update_supervisor/(?P<id>\d+)/(?P<user_id>\d+)/$', update_supervisor ,name = 'update_supervisor'),
    url(r'^pdtps_to_interview/(?P<id>\d+)/$', pdtps_to_interview ,name = 'pdtps_to_interview'),
    url(r'^pdtpts_attached/(?P<id>\d+)/(?P<slug>[-\w]+)/$', pdtpts_attached ,name = 'pdtpts_attached'),
    url(r'^interview_invitation/(?P<id>\d+)/$', interview_invitation ,name = 'interview_invitation'),
    url(r'^redeploy/(?P<year>[-\w]+)/(?P<user_id>\d+)/(?P<organization_id>\d+)/$',redeploy, name="redeploy"),
    url(r'^pick_supervisor/(?P<id>\d+)/$',pick_supervisor,name = 'pick_supervisor'),
    url(r'^supervisor_evaluation/(?P<id>\d+)/$',supervisor_evaluation,name = 'supervisor_evaluation'),

    url(r'^interns_pending_confirmation/(?P<year>[-\w]+)/$',interns_pending_confirmation,name = 'interns_pending_confirmation'),
    url(r'^my_interns/$', my_interns ,name = 'my_interns'),
    url(r'^my_mentees/$', my_mentees,name = 'my_mentees'),
    url(r'^(?P<id>\d+)/add_orgsupervisor/(?P<slug>[-\w]+)$', add_orgsupervisor ,name = 'add_orgsupervisor'),

    url(r'^organization_supervisors/(?P<id>\d+)/(?P<slug>[-\w]+)/$',organization_supervisors,name = 'organization_supervisors'),
    url(r'^update_orgsupervisor/(?P<slug>[-\w]+)/(?P<id>\d+)/(?P<user_id>\d+)/$', update_orgsupervisor ,name = 'update_orgsupervisor'),
    url(r'^assign_supervisor/(?P<slug>[-\w]+)/(?P<id>\d+)/$',assign_supervisor,name='assign_supervisor'),

    url(r'^pdtps_in_private_sector/(?P<year>[-\w]+)/$',pdtps_in_private_sector,name='pdtps_in_private_sector'),
    url(r'^pdtps_in_public_sector/(?P<year>[-\w]+)/$',pdtps_in_public_sector,name='pdtps_in_public_sector'),
    url(r'^pdtps_not_deployed/(?P<year>[-\w]+)/$',pdtps_not_deployed,name='pdtps_not_deployed'),

    url(r'^all_supervisors/$',all_supervisors,name='all_supervisors'),

    url(r'^interns_with_mentors/(?P<year>[-\w]+)/$',interns_with_mentors,name='interns_with_mentors'),
    url(r'^interns_without_mentors/(?P<year>[-\w]+)/$',interns_without_mentors,name='interns_without_mentors'),

    url(r'^intern_supervisor/$',intern_supervisor,name='intern_supervisor'),   
    #url(r'^print_report/(?P<id>\d+)/$', print_report, name='print_report'),

    #Monitoring and Evaluation Reports
    #secretariat
    url(r'^create_me_phase/$', create_me_phase, name='create_me_phase'),
    url(r'^update_phase/(?P<id>\d+)/$', update_phase, name='update_phase'),
    url(r'^monitoring_evaluation_phases/$',monitoring_evaluation_phases, name="monitoring_evaluation_phases"),
    url(r'^monitoring_and_evaluation_reports/(?P<id>\d+)/$',monitoring_and_evaluation_reports, name="monitoring_and_evaluation_reports"),
    #pdtp
    url(r'^(?P<id>\d+)/monitoring_evaluation/$', monitoring_evaluation, name='monitoring_evaluation'),
    url(r'^my_me_reports/$', my_me_reports, name='my_me_reports'),
    url(r'^phase_list/$', phase_list, name='phase_list'),
    url(r'^me_intern/(?P<id>\d+)/$', me_intern, name='me_intern'),
    

    #supervisor
    url(r'^(?P<id>\d+)/view_Internmereport/$', view_Internmereport, name='view_Internmereport'),
    url(r'^supervisor_monitoring_report/(?P<id>\d+)/$', supervisor_monitoring_report, name='supervisor_monitoring_report'),
    url(r'^me_report/(?P<id>\d+)/$', me_report, name='me_report'),

    #end of M&E 

    url(r'^attendance/$', attendance, name='attendance'),
    url(r'^attendance_report/$', attendance_report, name='attendance_report'),
    url(r'^(?P<id>\d+)/quarterly_reports/$', quarterly_reports, name='quarterly_reports'),
    url(r'^quarter_list/$', quarter_list, name='quarter_list'),
    url(r'^my_quarterly_reports/$', my_quarterly_reports, name='my_quarterly_reports'),
    url(r'^pdf_QuarterReport/(?P<id>\d+)/$', pdf_QuarterReport,name='pdf_QuarterReport'),
    url(r'^reports_quarterly/(?P<id>\d+)/$', reports_quarterly,name='reports_quarterly'),

    url(r'^approve_reports_quarterly/(?P<id>\d+)/$', approve_reports_quarterly, name='approve_reports_quarterly'),
    
    ]

