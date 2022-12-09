#all urls of the web application is specified here
# name=" "; this name will be use for linking withing HTML
#views.func() indicates that func() defined in views will be called once the url is opened 

from django.urls import path
from matplotlib.pyplot import title
from .import  views
from django.urls import path

urlpatterns=[
     path('register/',views.register, name='register'),#path(url,function name, name of link)
     path('student_register/',views.student_register.as_view(), name='student_register'),
     path('alumni_register/',views.alumni_register.as_view(), name='alumni_register'),
     path('company_register/',views.company_register.as_view(), name='company_register'),
     path('company_info/',views.company_info.as_view(), name='company_info'),
     path('student_edit_details/',views.editStudProfile.as_view(), name='student_edit'),
     path('company_edit_details/',views.editCompProfile.as_view(), name='company_edit'),
     path('alumni_edit_details/',views.editAlumProfile.as_view(), name='alumni_edit'),
     path('request_feedback/',views.request_feedback, name='request_feedback'),
     path('feedback/',views.feedback, name='feedback'),
     path('apply_for_companies/',views.apply_company, name='apply_company'),
     path('company_details/',views.company_details, name='company_details'),
     path('stud_chat/',views.stud_chat, name='stud_chat'),
     path('chats/',views.chats, name='chats'),
     path('list_of_students/',views.list_of_students, name='list_of_students'),
     path('get_student_cv/',views.get_stud_cv, name='get_stud_cv'),
     path('get_cv/',views.get_cv, name='get_cv'),
     path('',views.index, name='index'),
     path('login/',views.login_request, name='login'),
     path('logout/',views.logout_view, name='logout'),
]
