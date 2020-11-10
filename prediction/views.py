from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.files.storage import FileSystemStorage
from .models import patient,result
from .forms import PatientForm,ResultForm
import mysql.connector
import cv2 as cv
import numpy as np
import pandas as pd

# Create your views here.
def home(request):
    return render(request,'home.html')

def adminLogin(request):
    return render(request,'adminLogin.html')

def logindao(request):
    try:
        username=request.GET['username']
        password=request.GET['password']
        print(username)
        print(password)
        
        val=(username,password)
        mydb=mysql.connector.connect(host="localhost",user="root",passwd="",database="heartdisease")
        mycursor = mydb.cursor()
        sql = "select*from admin where username=%s and password=%s"
        mycursor.execute(sql,val)
        for i in mycursor:
            print(i)

        if mycursor.rowcount==1:
            return HttpResponse("<script>alert('success');window.location.href='adminHome'</script>")
        else:
            return HttpResponse("<script>alert('invalid credentials');window.location.href='adminLogin'</script>")
    except:
        return HttpResponse("<script>alert('sorry');window.location.href='adminLogin'</script>")

    finally:
        if (mydb.is_connected()):
            mydb.close()    
            print("MySQL connection is closed")       

def adminHome(request):
    return render(request,'adminHome.html')            


def viewPatients(request):
    context={'patients':patient.objects.all()}

    return render(request,'viewPatients.html',context)  


def addPatient(request):
    return render(request,'addPatient.html')  


def insert(request):
    try:
        name=request.GET['name']
        patientid=request.GET['pid']
        age=request.GET['age']
        gender=request.GET['gender']
        username=request.GET['username']
        password=request.GET['password']
        
        trestbps=request.GET['trestbps']
        chol=request.GET['chol']
        restecg=request.GET['restecg']
        thalach=request.GET['thalach']
        exang=request.GET['exang']
        oldpeak=request.GET['oldpeak']
        slope=request.GET['slope']
        ca=request.GET['ca']
        cp=request.GET['cp']
        fbs=request.GET['fbs']
        thal=request.GET['thal']
        status="Not available"
        pid=int(patientid)
        
        p=patient(patientid,name,age,gender,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal,status,username,password)
        p.save()
        res="Not Tested yet"
        r=result(patientid,res)
        r.save()
        
        
        return HttpResponse("<script>alert('success');window.location.href='adminHome'</script>")
    except mysql.connector.Error as error:
        print(error)
        return HttpResponse("<script>alert('sorry');window.location.href='viewPatients'</script>")
    finally:
        print("MySQL connection is closed")        

def patientdetails(request,patientid):
    patients=patient.objects.get(pk=patientid)
    
    form=PatientForm(instance=patients)   
    return render(request,'patientDetails.html',{"form":form})

def prediction(request,patientid):
    patients=patient.objects.get(pk=patientid)
    
    form=PatientForm(instance=patients)
    p=pred(patients)
    if p[0]==0:
        result="Patient has no chance to get heartdisease"
    else:
        result="Patient has a chance to get heartdisease"

    return render(request,'prediction.html',{"form":form,"p":result})    


def pred(patients):
    
    age=int(patients.age)
    sex=patients.gender
    cp=patients.cp
    trestbps=int(patients.trestbps)
    chol=int(patients.chol)
    fbs=patients.fbs
    restecg=patients.restecg
    thalach=int(patients.thalach)
    exang=int(patients.exang)
    oldpeak=float(patients.oldpeak)
    slope=patients.slope
    ca=int(patients.ca)
    thal=patients.thal

    if cp=="Atypical Angina":
        newcp=2
    elif cp=="Non-anginal pain":
        newcp=3
    elif cp=="Typical Angina":
        newcp=1
    else:
        newcp=4 

    if sex=="Male":
        nsex=1
    else:
        nsex=0

    if fbs=="greater than 120":
        newfbs=1
    else:
        newfbs=0           
   
    if restecg=="Normal":
        newrestecg=0
    elif restecg=="having ST-T wave abnormality":
        newrestecg=1
    else:
        newrestecg=2


    if slope=="Upsloping":
        newslope=1
    elif slope=="flat":
        newslope=2
    else:
        newslope=3


    if thal=="Normal":
        newthal=3
    elif thal=="Fixed Defect":
        newthal=6
    else:
        newthal=7    


      

    ndata=[age,nsex,newcp,trestbps,chol,newfbs,newrestecg,thalach,exang,oldpeak,newslope,ca,newthal]
    print(ndata)

    tdata=np.matrix(ndata,dtype=np.float32)
    print(tdata)
    url=staticfiles_storage.path('model/rtree.xml')
    rtree=cv.ml.RTrees_load(url)
    res=rtree.predict(tdata)[1]
    print(res[0])                   



    return res[0] 

def userDetails(request,patientid): 
    patients=patient.objects.get(pk=patientid)
    
    form=PatientForm(instance=patients)   
    return render(request,'profile.html',{"form":form}) 

def logout(request):
    for sesskey in request.session.keys():
        del request.session[sesskey]
    return render(request,'home.html')              

def sendresult(request):
    try:
        patientid=int(request.GET['patientid'])
        name=request.GET['name']
        
        results=request.GET['result']

        if results=="Patient has a chance to get heartdisease":
            res="You have a chance to get heart disease. Please contact the doctor immediately!"
        else:
            res="You are perfectly alright :) "    
        
        print(results)   
               
        
        r=patient.objects.get(pk=patientid)
        r.status=results
        r.save()

        p=result.objects.get(pk=patientid)
        p.results=res
        p.save()

        return HttpResponse("<script>alert('success');window.location.href='viewPatients'</script>")
    except mysql.connector.Error as error:
        print(error)
        return HttpResponse("<script>alert('sorry');window.location.href='prediction'</script>")
    finally:
        print("MySQL connection is closed")   



def adminLogin(request):
    return render(request,'adminLogin.html') 



def userLogin(request):
    return render(request,'userLogin.html')  

def userlogindao(request):
    try:
        username=request.POST['username']
        password=request.POST['password']
        print(username)
        print(password)
        
        val=(username,password)
        mydb=mysql.connector.connect(host="localhost",user="root",passwd="",database="heartdisease")
        mycursor = mydb.cursor()
        sql = "select*from prediction_patient where username=%s and password=%s"
        mycursor.execute(sql,val)
        resul=mycursor.fetchall()
        res=[lis[0] for lis in resul]
        print(res[0])
        id=res[0]
        
        context={'id':id}
        request.session['dict']=context
    
        #form=StudentForm(instance=student)
        

        for i in mycursor:
            print(i)
        

        if mycursor.rowcount!=0:
            return HttpResponseRedirect('/userHome')
            
        else:
            return HttpResponse("<script>alert('success');window.location.href='userLogin'</script>")
    except:
        return HttpResponse("<script>alert('sorry');window.location.href='userLogin'</script>")

    finally:
        if (mydb.is_connected()):
            mydb.close()
            print("MySQL connection is closed")


def userHome(request):
    value=request.session.pop('dict',None)
    print(value)
    return render(request,'userHome.html',value)     


def back(request,patientid):
    context={'id':patientid}
    request.session['dict']=context
    return redirect(userHome)       

def viewResult(request,patientid):
    results=result.objects.get(pk=patientid)
    form=ResultForm(instance=results)
    users=patient.objects.get(pk=patientid)
    form1=PatientForm(instance=users)
    return render(request,'result.html',{"form":form,"form1":form1}) 