from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='login')
def HomePage(request):
    return render (request,'home.html')
    
@login_required(login_url='login')
def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if User.objects.filter(username=uname).exists():
            # رسالة الخطأ عند تكرار اسم المستخدم
            error_message = 'اسم المستخدم موجود بالفعل'
            return render(request, 'signup.html', {'error_message': error_message})

        elif pass1!=pass2:
            error_message = 'كلمه السر غير مطابقة'
            return render(request, 'signup.html', {'error_message1': error_message})

            #return HttpResponse("Your password and confrom password are not Same!!")
        elif User.objects.filter(email=email).exists():
                # رسالة الخطأ عند تكرار اسم المستخدم
            error_message = 'البريد الالكتروني مستخدم بالفعل'
            return render(request, 'signup.html', {'error_message': error_message})


        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        



    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            error_message = 'اسم المستخدم او كلمه السر غير صحيح'
            return render(request, 'login.html', {'error_message': error_message})


            #return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')