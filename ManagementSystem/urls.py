from django.urls import path
from . import views



urlpatterns =[
    path('view-class-modal/<int:ID>',views.view_class_modal,name = 'view_class_modal'),
    path('view-student-modal/<int:ID>',views.view_student_modal,name = 'view_student_modal'),



    #index page 
    path('',views.index, name='index'),

    #dash board 
    path('dashboard',views.dash, name='dash'),
    #path('table',views.table, name='table'),
    
    ##have to change
    path('login',views.main, name='main'),
    path('profile',views.profile,name='user_profile'),
    path('logout',views.logout,name='logout_view'),
    #--xxx--
    
    path('class-management',views.class_management,name='class_management'),
    
    path('student-management',views.student_management,name='student_management'),
    
    path('add-class',views.add_class,name='add_class'),
    
    path('update-classes',views.class_table_update,name='update_classes'),

    path('delete-class',views.delete_class,name='delete_class'),
    
    path('update-students',views.student_table_update,name='update_student_table'),
    
    
    
    path('add-student',views.add_student,name='add_student'),
    
    path('update-student/<ID>',views.update_student,name='update_student'),
    
    path('view-class/<ID>',views.view_class,name='view_class'),
    
    path('delete-student',views.delete_student,name='delete_student'),

    path('enrol-student',views.enrol_from_class_view,name = 'enrol_from_class_view'),
    path('enrol-student-in-class',views.enrol_from_student_view,name = 'enrol_from_student_view'),

]

