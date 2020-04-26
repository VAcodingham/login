from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

# Create your views here.
def index(request):
    if 'userid' not in request.session:
        return render(request, 'index.html')
    else:
        return redirect('/success')


#register verification
def register(request):
    errors=User.objects.user_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    
    else:
        hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        User.objects.create(username=request.POST['username'],first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],birthdate=request.POST['birthdate'],password=hash1)
        usern=request.POST['username']
        newuser=User.objects.get(username=usern)
        request.session['userid']=newuser.id
        return redirect('/success')

def login(request):
    #login verification/authorization
    usern=User.objects.filter(username=request.POST['username'])
    errors={}
    if not usern:
        errors['username'] = "Username or Password is Invalid!"
    else:
        logged_user=usern[0]
        if bcrypt.checkpw(request.POST['password'].encode(),logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect('/success')
        else:
            errors['password'] = "Username or Password is Invalid!"
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request,value)
            return redirect('/')
        else:
            return redirect('/success')

def success(request):
    if 'userid' not in request.session:
        return redirect('/')
    else:
        user=User.objects.get(id=request.session['userid'])
        context={
            'user':user
        }
        return render(request, 'success.html', context)

def logout(request):
    request.session.clear()
    return redirect("/")




