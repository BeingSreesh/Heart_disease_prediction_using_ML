from django.contrib import admin

from django.urls import path

from.import views

urlpatterns = [
    path('', views.home,name='home'),
    path('home', views.home,name='home'),
    path('adminLogin', views.adminLogin,name='adminLogin'),
    path('logindao', views.logindao,name='logindao'),
    path('adminHome', views.adminHome,name='adminHome'),
    path('viewPatients', views.viewPatients,name='viewPatients'),
    path('addPatient', views.addPatient,name='addPatient'),
    path('insert', views.insert,name='insert'),
    path('sendresult', views.sendresult,name='sendresult'),
    path('userLogin', views.userLogin,name='userLogin'),
    path('userlogindao', views.userlogindao,name='userlogindao'),
    path('userHome', views.userHome,name='userHome'),
    path('back/<int:patientid>/', views.back,name='back'),
    path('logout', views.logout,name='logout'),
    path('viewResult/<int:patientid>/', views.viewResult,name='viewResult'),
    path('userDetails/<int:patientid>/', views.userDetails,name='userDetails'),
    path('patientdetails/<int:patientid>/', views.patientdetails,name='patientdetails'),
    path('prediction/<int:patientid>/', views.prediction,name='prediction'),

    ]