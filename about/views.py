from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User


# Create your views here.

def about(request):
   return render(request, 'home/about.html')

def handleSignup(request):
    if request.method == 'POST':
     # Get the post parameters
       username = request.POST['username']
       fname = request.POST['fname']
       lname = request.POST['lname']
       email = request.POST['email']
       pass1 = request.POST['pass1']
       pass2 = request.POST['pass2']

       # Check for errorneous inputs
       #userna,e should be under 10 characters
       if len(username) > 10:
         messages.error(request, "Username must be under 10 chracters")
         return redirect('home')

       #username shouls be alphanumeric
       if not username.isalnum():
         messages.error(request, "Username should only contain letters and numbers")
         return redirect('home')

       #password should match
       if pass1 != pass2:
          messages.error(request, "Username must be under 10 chracters")
          return redirect('home')

      # Create The user
       myuser = User.objects.create_user(username, email, pass1)
       myuser.first_name = fname
       myuser.last_name = lname
       myuser.save()
       messages.success(request, "Your Account has been Successfully Created")
       return redirect('home')

    else:
       return HttpResponse('404 - Not Found')

def handleLogin(request):
    if request.method == 'POST':
     # Get the post parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials, Please try Again")
            return redirect('home')

    return HttpResponse('404 - Not Found')



def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('home')
