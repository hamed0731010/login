from random import random
from django.shortcuts import render
from rest_framework.generics import ListAPIView,ListCreateAPIView,CreateAPIView
from rest_framework.views import APIView
from .models import User,Log
from django.shortcuts import redirect ,HttpResponse
from .serializer import UserSerializer
import socket
import datetime
from django.contrib import messages
import random
from ippanel import Client
from django.db.models import Q
# you api key that generated from panel
from django.core.exceptions import ValidationError
from django.db.transaction import TransactionManagementError
from django.views.decorators.http import condition
from .forms import UserForm
import time
from django.contrib.auth.hashers import make_password
#signup

def signup(request):
        userform=UserForm()
        if request.method=="POST":
                userform=UserForm(request.POST)
                if userform.is_valid():
                        userform.save(commit=False)
                        userform.password=make_password(userform.cleaned_data['password'])
                        userform.save()
                        return redirect("/login")
                else:
                        userform=UserForm()    
        context={'form' :userform}
        return render(request,'login/signup.html',context)                    
# def sign(request):
     
     
#         phone=request.POST.get("phone")
#         password=request.POST.get("pass")
     
#         if password !=None and phone !=None:
#                 try:
#                         user=User.objects.create(number=phone,password=password)
#                         return redirect("/login")
#                 except:
#                       TransactionManagementError("incorrrect") 
#         return render(request,"login/signup.html")        
#for checking the user login     
def login(request):

        if request.method=="POST":
                phone=request.POST.get("phone")
                password=request.POST.get("pass")
                try:
                        auth_user=User.objects.get(Q(number=phone) & Q(password=password))
                        Log.objects.create(num=auth_user,type_log='pass')
                except:
                        TransactionManagementError("incorrect")
                        return redirect("/login") 
                else:
                     return HttpResponse("you logged in succesfully")
                     
        return render(request,"login/login.html")  



# for checking the code
def otp(request):
        # if request.session['time'] in globals():
        #        now=request.session['time']
        # else :
        #        now=0
        try:
               request.session['time']
        except:
               now=0    
        else:
               now=request.session['time']       
        finally:
                t=time.time()          
                if (request.method=="POST" and  now==0) or (request.method=="POST" and t>now+600):
                        
                        
                        api_key = "Fs2SgWGY9SmClVJUBlOiCxyjAD7LCLsQBlnl-oSyp4U="
                        sms = Client(api_key)
                        # return float64 type credit amount
                        #credit = sms.get_credit()
                        phone=request.POST.get("phone")
                        if phone:
                                request.session['code']=int(random.randrange(10000,99999))  
                                code=request.session['code']
                                user,  created=User.objects.get_or_create(number=phone)
                                request.session['user']=user.id
                                
                                if user:
                                                
                                        message_id = sms.send(
                                                        "+9890000145",          # originator
                                                        [f'{user.number}'],    # recipients
                                                        f"خوش آمدید  {code}   شرکت رسانه جدید",# message
                                                        "description"        # is logged
                                                        )
                                        request.session['time']=time.time()
                                        now=request.session['time']
                                        return redirect("/check") 
                                else:
                                        ValidationError("incorrect")

                elif (request.method=="POST" and t<now+600):
                        return render(request,"login/otp.html")                              


        return render(request,"login/otp.html")  


#check code

def check_code(request):
       if request.method=="POST":
                code=request.POST.get("code")
                if code  and request.session['code']==int(code):  #
                        del request.session['code'] 
                        try:
                               Log.objects.create(num=User.objects.get(id=request.session['user']),type_log='otp')
                        except:
                               TransactionManagementError("inc")  
                        finally:
                                return HttpResponse("successfully import")            
                else:
                       return render(request,"login/check.html") 

       return render(request,"login/check.html")                  
