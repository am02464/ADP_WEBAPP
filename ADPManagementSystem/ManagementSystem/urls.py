from django.urls import path
from . import views



urlpatterns =[
    path('',views.main, name='main'),
    path('profile',views.profile,name='user_profile'),
    path('logout',views.logout,name='logout_view'),
    path('class-management',views.class_management,name='class_managemnet'),
    path('student-management',views.student_management,name='student_managemnet'),
    path('add-class',views.add_class,name='add_class'),
    path('test',views.test_view,name='test_view'),
    path('add-student',views.add_student,name='add_student'),
    path('update-student/<ID>',views.update_student,name='update_student'),
    path('view-class/<ID>',views.view_class,name='view_class'),
    path('delete-class',views.delete_class,name='delete_class'),
    path('delete-student',views.delete_student,name='delete_student'),

]

