from django.conf.urls import url
from app.views import *


urlpatterns = [
    url(r'^dashboard/$', dashboard ,name = 'dashboard'),
    url(r'^dashboard2/(?P<slug>[-\w]+)/$', dashboard2 ,name = 'dashboard2'),
    url(r'^index/$', index ,name = 'index'),
    url(r'^alumni-database/$', alumni_regs ,name = 'alumni_regs'),
    url(r'^alumni-registration/$', alumni_registration ,name = 'alumni_registration'),
    url(r'^about/$', about ,name = 'about'),
    url(r'^partners/$', partners ,name = 'partners'),
    url(r'^graduates-by-category/(?P<slug>[-\w]+)/$', experts_by_category ,name = 'experts_by_category'),
    url(r'^success-stories/$', stories ,name = 'stories'),
    url(r'^apply-for-partnership/$', partnership_apply ,name = 'partnership_apply'),
    url(r'^request-for-interns/$', request_interns ,name = 'request_interns'),
    url(r'^internsrequests/$', internsrequests ,name = 'internsrequests'),
    url(r'^partnership_requests/$', partnership_requests ,name = 'partnership_requests'),

    url(r'^partnership_application/$', partners_application ,name = 'partners_application'),
    url(r'^mentorship/$', mentorship ,name = 'mentorship'),
    url(r'^mentorship_application/$', mentorship_application ,name = 'mentorship_application'),

    url(r'^experts/$', experts ,name = 'experts'),
    url(r'^apply/$', apply_for_training ,name = 'apply'),
    url(r'^(?P<id>\d+)/bio_update/$', bio_update ,name = 'bio_update'),
    url(r'^pdtp_profile_update/(?P<id>\d+)/$',pdtp_profile_update,name = 'pdtp_profile_update'),
    url(r'^update_bank_details/(?P<id>\d+)/$',update_bank_details,name = 'update_bank_details'),
    url(r'^(?P<id>\d+)/add_academic_detail/$', add_academic_detail ,name = 'add_academic_detail'),
    url(r'^(?P<id>\d+)/academic_update/$', academic_update ,name = 'academic_update'),
    url(r'^(?P<id>\d+)/send_message/$', send_message ,name = 'send_message'),
    url(r'^(?P<id>\d+)/academic_delete/$', academic_delete ,name = 'academic_delete'),
    url(r'^upload_photo/(?P<id>\d+)/$',upload_photo, name='upload_photo'),
    url(r'^new_email/$',new_email, name='new_email'),
    url(r'^activate/$',activate, name='activate'),
    url(r'^deactivate/$',deactivate, name='deactivate'),
    url(r'^request_program_exit/$', request_program_exit ,name = 'request_program_exit'),
    url(r'^(?P<id>\d+)/request_status/$', request_status ,name = 'request_status'),
    url(r'^exit_requests/$',exit_requests,name = 'exit_requests'),
    url(r'^management_profile/$',management_profile, name='management_profile'),

    url(r'^cohort3_registration/$',cohort3_registration, name='cohort3_registration'),
    url(r'^pdtps/(?P<year>[-\w]+)/$',pdtps_all,name = 'pdtps-all'),
    url(r'^story/(?P<id>\d+)/(?P<slug>[-\w]+)/$',story,name = 'story'),
    url(r'^pdtps-active/(?P<year>[-\w]+)/$',pdtps,name = 'pdtps'),
    url(r'^pdtps-female/(?P<year>[-\w]+)/$',pdtps_female,name = 'pdtps-female'),
    url(r'^pdtps-exited/(?P<year>[-\w]+)/$',pdtps_exited,name = 'pdtps-exited'),
    url(r'^pdtps-male/(?P<year>[-\w]+)/$',pdtps_male,name = 'pdtps-male'),
    url(r'^(?P<year>[-\w]+)/pdtps_bankdetails/$',bank_details,name = 'bank_details'),
    url(r'^(?P<year>[-\w]+)/pdtps_academics/$',pdtps_academics,name = 'pdtps_academics'),
    url(r'^expert_profile/(?P<id>\d+)/(?P<slug>[-\w]+)/$',expert_profile,name = 'expert_profile'),

     #mentors urls
    url(r'^mentors/$', mentors ,name = 'mentors'),
    #url(r'^all_mentors/$', all_mentors ,name = 'all_mentors'),
    url(r'^add_mentor/$',add_mentor,name = 'add_mentor'),
    url(r'^(?P<id>\d+)/mentor_profile_update/$',mentor_profile_update,name = 'mentor_profile_update'),
    url(r'^(?P<year>[-\w]+)/mentorship_mapping/$',mentorship_mapping,name = 'mentorship_mapping'),
    url(r'^assignmentees/(?P<id>\d+)/(?P<year>[-\w]+)/$',assignmentees,name = 'assignmentees'),
    url(r'^complete_mentorship_mapping/$', complete_mentorship_mapping ,name = 'complete_mentorship_mapping'),
    


    url(r'^(?P<year>[-\w]+)/secretariat_assign_supervisor/$',secretariat_assign_supervisor,name = 'secretariat_assign_supervisor'),
    url(r'^secretariat_supervisor_assignmentees/(?P<id>\d+)/(?P<year>[-\w]+)/$',secretariat_supervisor_assignmentees,name = 'secretariat_supervisor_assignmentees'),

    
    url(r'^(?P<year>[-\w]+)/mentorship_assignments/$', mentorship_assignment ,name = 'mentorship_assignment'),
    url(r'^add_pdtp/$',add_pdtp,name='add_pdtp'),
    url(r'^(?P<year>[-\w]+)/pdtp_profile/(?P<id>\d+)/$',pdtp_profile,name = 'pdtp_profile'),
    url(r'^(?P<year>[-\w]+)/pdtp_clearance/(?P<id>\d+)/$',pdtp_clearance,name = 'pdtp_clearance'),

    url(r'^(?P<year>[-\w]+)/pdtp_cleared/(?P<id>\d+)/$',pdtp_cleared,name = 'pdtp_cleared'),
    
    
    url(r'^pdtp_supervisor_clearance/(?P<id>\d+)/$',pdtp_supervisor_clearance,name = 'pdtp_supervisor_clearance'),

    url(r'^(?P<id>\d+)/update_request/$',update_request,name = 'update_request'),
    url(r'^events/$',events,name = 'events'),
    url(r'^accounts/login/$', custom_login),

    url(r'^staff_mentors/$', staff_mentors ,name = 'staff_mentors'),

    url(r'^add_staff/(?P<id>\d+)/$', add_staff ,name = 'add_staff'),

    url(r'^edit_event/(?P<id>\d+)/$', edit_event ,name = 'edit_event'),
    url(r'^cancel_event/(?P<id>\d+)/$', cancel_event ,name = 'cancel_event'),

    url(r'^upcoming_events/$', upcoming_events ,name = 'upcoming_events'),
    url(r'^raise_issue/$', raise_issue ,name = 'raise_issue'),

    url(r'^(?P<slug>[-\w]+)/issues_response/(?P<id>\d+)/$',issues_response,name = 'issues_response'),

    url(r'^raised_issues/$', raised_issues ,name = 'raised_issues'),
    url(r'^(?P<slug>[-\w]+)/reports/$',reports,name = 'reports'),
    url(r'^private_sector_reports/$', private_sector_reports ,name = 'private_sector_reports'),
    url(r'^public_sector_reports/$', public_sector_reports ,name = 'public_sector_reports'),
    url(r'^submit_workplan/$',submit_workplan,name='submit_workplan'),
    url(r'^my_workplan/$',my_workplan,name='my_workplan'),
    url(r'^pdf_workplan/(?P<id>\d+)/$', pdf_workplan, name='pdf_workplan'),
    url(r'^sec_quarterpdf/(?P<id>\d+)/$', sec_quarterpdf,name='sec_quarterpdf'),
    url(r'^monthly_workplans/$',monthly_workplans,name='monthly_workplans'),

    url(r'^approve_workplans/$',approve_workplans,name='approve_workplans'),
    url(r'^approve_plan/(?P<id>\d+)/$',approve_plan,name='approve_plan'),


    url(r'^(?P<id>\d+)/add_project/$', add_project ,name = 'add_project'),
    url(r'^(?P<id>\d+)/update_project/$', update_project ,name = 'update_project'),
    url(r'^(?P<id>\d+)/delete_project/$', delete_project ,name = 'delete_project'),

    url(r'^(?P<id>\d+)/add_skill/$', add_skill ,name = 'add_skill'),
    url(r'^(?P<id>\d+)/update_skill/$', update_skill ,name = 'update_skill'),
    url(r'^(?P<id>\d+)/delete_skill/$', delete_skill ,name = 'delete_skill'),

    url(r'^(?P<id>\d+)/add_referee/$', add_referee ,name = 'add_referee'),
    url(r'^(?P<id>\d+)/update_referee/$', update_referee ,name = 'update_referee'),
    url(r'^(?P<id>\d+)/delete_referee/$', delete_referee ,name = 'delete_referee'),

    url(r'^bank_update_requests/$',bank_update_requests,name='bank_update_requests'),

    url(r'^mark_as_solved/(?P<id>\d+)/$',mark_as_solved,name='mark_as_solved'),

    url(r'^trainings_done/$',trainings_done,name='trainings_done'),
    url(r'^add_record/$',add_record,name='add_record'),
    url(r'^(?P<id>\d+)/update_training_record/$', update_training_record ,name = 'update_training_record'),
    url(r'^(?P<id>\d+)/delete_record/$', delete_record ,name = 'delete_record'),

    url(r'^(?P<id>\d+)/applicants/$', get_applicants ,name = 'get_applicants'),
    url(r'^(?P<id>\d+)/update-applicants/$', update_applicants ,name = 'update_applicants'),

    url('^check_password/$', check_password, name='check_password'),
    #url(r'^resetpassword/$',resetpassword, name='resetpassword'),
    #url(r'^new_password/$',new_password, name='new_password'),
    url('^password_change/$', password_change, name='password_change'),
    url(r'^expert_by_skills/(?P<id>\d+)/(?P<slug>[-\w]+)/$',expert_by_skills,name='expert_by_skills'),


    url('^mentors_yet_to_evaluate/$', mentors_yet_to_evaluate, name='mentors_yet_to_evaluate'),
    url('^supervisors_yet_to_evaluate/$', supervisors_yet_to_evaluate, name='supervisors_yet_to_evaluate'),
    url('^not_evaluated_by_private/$', not_evaluated_by_private, name='not_evaluated_by_private'),
    #Training
    url(r'^(?P<year>[-\w]+)/training/$', training, name='training'),
    url(r'^post-training/$', post_training, name='post_training'),
    url(r'^(?P<id>\d+)/update-training/$', update_training, name='update_training'),
    url(r'^training_list/$', training_list ,name = 'training_list'),
    url(r'^(?P<id>\d+)/apply-training/$', apply_training ,name = 'apply_training'),
    url(r'^my-trainings/$', my_trainings ,name = 'my_trainings'),
    url(r'^(?P<id>\d+)/update_my_training/$',update_my_training, name='update_my_training'),
    url(r'^(?P<id>\d+)/training_Feedback/$',training_Feedback, name='training_Feedback'),


    #url(r'^get_applications/(?P<year>[-\w]+)/$',get_applications,name='get_applications'),

    #Innovations
    
    url(r'^submit_innovation/$', submit_innovation, name='submit_innovation'),
    url(r'^innovations/$', innovations, name='innovations'),
    url(r'^pdtpinnovations/$', pdtpinnovations, name='pdtpinnovations'),
    url(r'^edit_innovation/(?P<id>\d+)/$', edit_innovation, name='edit_innovation'),

    #Mentorship report
    url(r'^mentorship_reports/$', mentorship_reports, name='mentorship_reports'),
    url(r'^mentorship_meetings/$', mentorship_meeting_booked, name='mentorship_meeting_booked'),
    url(r'^mentor_report_comment/$', mentor_report_comment, name='mentor_report_comment'),
    url(r'^intern_mentorship_report/$', intern_mentorship_report, name='intern_mentorship_report'),
    url(r'^my_leaves/$', my_leaves, name='my_leaves'),
    url(r'^leave_requests/$', leave_requests, name='leave_requests'),
    url(r'^leave_request/$', leave_request, name='leave_request'),
    url(r'^apply_for_leave/$', apply_for_leave, name='apply_for_leave'),
    url(r'^leave_requests_approval/(?P<leave_id>\d+)/(?P<pk>\d+)$', leave_requests_approval, name='leave_requests_approval'),
    #url(r'^upload_mentorship_report/(?P<id>\d+)/$', upload_mentorship_report, name='upload_mentorship_report'),
    
    url(r'^mentorship_meeting/(?P<id>\d+)/$', mentorship_meeting, name='mentorship_meeting'),
    url(r'^(?P<id>\d+)/report/$', report, name='report'),

    url(r'^my_issues/$', my_issues, name='my_issues'),

    url(r'^broadcast_messages/$', broadcast_messages, name='broadcast_messages'),

    url(r'^pdtp_broadcast_messages/$', pdtp_broadcast_messages, name='pdtp_broadcast_messages'),
    url(r'^send_broadcast_message/$', send_broadcast_message, name='send_broadcast_message'),
    url(r'^supervisors_broadcast_messages/$', supervisors_broadcast_messages, name='supervisors_broadcast_messages'),

    url(r'^secretariat_quarterly_reports/$', secretariat_quarterly_reports, name='secretariat_quarterly_reports'),
    url(r'^add_quarter/$', add_quarter, name='add_quarter'),  
    url(r'^(?P<id>\d+)/update_quarter/$', update_quarter, name='update_quarter'),
    url(r'^(?P<id>\d+)/quarter_reports/$', quarter_reports, name='quarter_reports'),

    url(r'^expert_by_skills/$', expert_by_skills, name='expert_by_skills'),
    url(r'^innovations_evaluations/(?P<year>[-\w]+)/$', innovations_evaluations, name='innovations_evaluations'),
    url(r'^view_innovation/(?P<id>\d+)/$', view_innovation, name='view_innovation'),
    url(r'^evaluate_innovation/(?P<id>\d+)/$', evaluate_innovation, name='evaluate_innovation'),
    url(r'^apply_for_icta_tasks/$', apply_for_icta_tasks, name='apply_for_icta_tasks'),
    url(r'^interests/$', interests, name='interests'),

    #Laptop application urls.
    url(r'^laptop/$', laptop, name='laptop'),
    url(r'^post_laptop/$', post_laptop, name='post_laptop'),
    url(r'^(?P<id>\d+)/update_laptop/$', update_laptop, name='update_laptop'),
    url(r'^(?P<id>\d+)/laptop_applicants/$', laptop_applicants, name='laptop_applicants'),
    url(r'^(?P<id>\d+)/update_laptop_applicants/$', update_laptop_applicants, name='update_laptop_applicants'),
    url(r'^apply_for_laptop/(?P<id>\d+)/$', apply_for_laptop, name='apply_for_laptop'),
    url(r'^laptop_list/$', laptop_list, name='laptop_list'),
    url(r'^my_laptop/$', my_laptop, name='my_laptop'),

    url(r'^innovation-evaluation-results/$', innovations_evaluation_results, name='innovations_evaluation_results'),








    ]
