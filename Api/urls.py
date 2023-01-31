from django.contrib import admin
from django.urls import path,include

from .views import *

urlpatterns = [

    ######################## decorrators #################################
    path('',home),
    path('post_student/',post_student),
    path('update_student/<id>',update_student),
    path('update_studentpartially/<id>',update_studentpartially),
    path('delete_student/<id>',delete_student),


    path('get_book',get_book),
    path('generatedata',generatedata),

    ######################## decorrators #################################

    ############# APIVIEW ########################


    path('student/',StudentApi.as_view()),
    path('register/',UserRegistration.as_view()),

    ############# genericView ########################
   
    path('generic-student/',StudentGeneric.as_view()),
    path('generic-student/<int:id>/',StudentGeneric1.as_view()),
    path('pdf/',GeneratePdf.as_view()),
    path('excel/',ExporImportExcel.as_view()),
    path('userregister/',RegisterView.as_view()),

  
]
