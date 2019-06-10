from django.conf.urls import url
from performance.views import *


urlpatterns = [
	#Pdtd ministry urls
    url(r'^my_performance/$', my_performance ,name = 'my_performance'),
    url(r'^mentorship-performance-feedback/$', mentorship_performance_feedback ,name = 'mentorship_performance_feedback'),
    url(r'^ministry_activities/$', ministry_activities ,name = 'ministry_activities'),
    url(r'^add_ministry_activities/$', add_ministry_activities ,name = 'add_ministry_activities'),
    url(r'^add_evidence/$', add_evidence ,name = 'add_evidence'),
    url(r'^add_additional/$', add_additional ,name = 'add_additional'),
    url(r'^add_flagship_project/$', add_flagship_project ,name = 'add_flagship_project'),
    url(r'^add_private_project/$', add_private_project ,name = 'add_private_project'),

    #PDTP Private Sector Urls
    url(r'^private_sector_activities/$', private_sector_activities ,name = 'private_sector_activities'),
    url(r'^add_private_attendance/$', add_private_attendance ,name = 'add_private_attendance'),
    url(r'^add_soft_training/$', add_soft_training ,name = 'add_soft_training'),
    url(r'^add_org_training/$', add_org_training ,name = 'add_org_training'),

    #Private Sector Supervisor Evaluate Interns
    url(r'^supervisor_evaluate/(?P<id>\d+)/$',supervisor_evaluate,name = 'supervisor_evaluate'),
    url(r'^public_supervisor_evaluate/(?P<id>\d+)/$',public_supervisor_evaluate,name = 'public_supervisor_evaluate'),
    url(r'^supervisor_approval/(?P<id>\d+)/$',supervisor_approval,name = 'supervisor_approval'),
    url(r'^public_supervisor_approval/(?P<id>\d+)/$',public_supervisor_approval,name = 'public_supervisor_approval'),
    url(r'^mentor_evaluate/(?P<id>\d+)/$',mentor_evaluate,name = 'mentor_evaluate'),
    url(r'^(?P<year>[-\w]+)/innovations/$', innovations ,name = 'innovations'),
    url(r'^(?P<year>[-\w]+)/pdtps_performance/$', pdtps_performance ,name = 'pdtps_performance'),

    url(r'^innovation_performance/$', innovation_performance ,name = 'innovation_performance'),
    url(r'^pivate_performance/$', pivate_performance ,name = 'pivate_performance'),
    url(r'^public_performance/$', public_performance ,name = 'public_performance'),
    url(r'^mentors_performance/$', mentors_performance ,name = 'mentors_performance'),
    url(r'^training_performance/$', training_performance ,name = 'training_performance'),
    url(r'^programme-evaluation/$', programme_evaluation ,name = 'programme_evaluation'),
    
    url(r'^(?P<year>[-\w]+)/pdtp_performance/(?P<id>\d+)/$', pdtp_performance ,name = 'pdtp_performance'),
]