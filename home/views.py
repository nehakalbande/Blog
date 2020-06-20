from django.shortcuts import render, HttpResponse
from home. models import Contact
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, 'home/home.html ')

def contact(request):
    if request.method == 'POST':
      name = request.POST['name']
      email = request.POST['email']
      phone = request.POST['phone']
      content = request.POST['content']
      print(name, email, phone, content)


      if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
          messages.error(request, "Please fill the form correctly")
      else:
           contact = Contact(name=name, email=email, phone=phone, content=content)
           contact.save()
           messages.success(request, "Your message has been delivered")

    return render(request, 'home/contact.html')

def about(request):
    return render(request, 'home/about.html')
