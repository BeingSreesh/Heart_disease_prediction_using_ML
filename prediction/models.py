from django.db import models

# Create your models here.

class patient(models.Model):
    patientid =models.IntegerField(primary_key=True,default=False)
    name =models.CharField(max_length=100,default=False)
    age =models.IntegerField(max_length=100,default=False)
    gender =models.CharField(max_length=100,default=False)
    cp=models.CharField(max_length=100,default=False)
    trestbps =models.CharField(max_length=100,default=False)
    chol =models.CharField(max_length=100,default=False)
    fbs =models.CharField(max_length=100,default=False)
    restecg =models.CharField(max_length=100,default=False)
    thalach=models.CharField(max_length=100,default=False)
    exang=models.CharField(max_length=100,default=False)
    oldpeak=models.CharField(max_length=100,default=False)
    slope=models.CharField(max_length=100,default=False)
    ca=models.CharField(max_length=100,default=False)
    thal=models.CharField(max_length=100,default=False)
    status=models.CharField(max_length=100,default=False)
    username =models.CharField(max_length=100,default=False)
    password =models.CharField(max_length=100,default=False)

class result(models.Model):
    patientid=models.IntegerField(primary_key=True,default=False)
    results=models.CharField(max_length=100,default=False)