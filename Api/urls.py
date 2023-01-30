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

    ######################## decorrators #################################

    ############# APIVIEW ########################


    path('student/',StudentApi.as_view()),
   
  
]
