from django.conf.urls import url, include
from django.views.generic import TemplateView
from . import views

urlpatterns = [

    url(r'^search/internship/$', views.internship_search, name='internship_search'),
    # url(r'^search/$', TemplateView.as_view(template_name='app/search_base.html'), name='search'),

    url(r'dashboard/$', views.my_dashboard, name='dashboard'),
    url(r'^my_internships$', views.internship_my, name='internship_my'),
    url(r'^my_resources$', views.resources_my, name='resources_my'),
    url(r'^my_resources/new$', views.resources_new, name='resources_new'),

    url(r'^who/(?P<user_id>.+)$', views.user_page, name='user_page'),

    # url(r'^org/$', views.org_list, name='org_list'),
    url(r'^org/new$', views.org_new, name='org_new'),
    url(r'^org/(?P<org_name>.+)$', views.org_info, name='org_info'),

    url(r'^internship/new$', views.internship_new, name='internship_new'),
    url(r'^internship/(?P<internship_id>.+)/$', views.internship_view, name='internship_view'),
    # url(r'^internship/edit=(?P<internship_id>.+)$', views.edit_internship, name='edit_internship'),
    url(r'^internship/(?P<internship_id>.+)/apply$', views.register_intern, name='inter_application'),
    url(r'^internship/connect_intern$', views.connect_intern, name='connect_intern'),
    url(r'^internship/(?P<application_id>.+)/edit_application$', views.edit_application, name='edit_application'),

    url(r'^task/new=(?P<internship_id>.+)$', views.task_new, name='task_new'),
    #url(r'^task/(?P<task_id>.+)$', views.task_view, name='task_view'),
    #url(r'^task/(?P<task_id>.+)/edit$', views.new_internship, name='task_edit'),
    url(r'^task/(?P<task_id>.+)/progress_new$', views.task_progress, name='task_progress'),
    url(r'^task/(?P<task_id>.+)/progress_update=(?P<progress_id>.+)$', views.task_progress, name='task_progress_update'),
    url(r'^task/(?P<task_id>.+)/done_questions$', views.task_progress_done, name='task_progress_done'),

    url(r'^task/(?P<task_id>.+)/question_new$', views.task_question_new, name='task_question_new'),
    url(r'^question/(?P<question_id>.+)/answer$', views.task_question_answer, name='task_question_answer'),

    url(r'^focus/new=(?P<internship_id>.+)$', views.focus_new, name='focus_new'),
    url(r'^focus/(?P<focus_id>.+)/answer$', views.focus_answer, name='focus_answer'),
               
    url(r'^feedback/new=(?P<internship_id>.+)$', views.performance_new, name='feedback_new'),
    url(r'^feedback/(?P<feedback_id>.+)/answer$', views.performance_answer, name='feedback_answer'),

    url(r'^counselor/$', views.counselor_view, name='counselor_view'),


    url(r'^profile/$', views.update_profile, name='update_profile'),
    url(r'^$', TemplateView.as_view(template_name='app/index.html'), name='index'),
               
    url(r'^contact/$', views.contact_us, name='contact_us'),

]
