from django.shortcuts import render, HttpResponse, redirect
from blog.models import Post, BlogComment
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from blog.templatetags import extras

# Create your views here.

def blogHome(request):
    allPosts = Post.objects.all()
    context = {'allPosts': allPosts}
    return render(request, 'blog/blogHome.html', context)

def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    post.views = post.views + 1
    post.save()

    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    context = {'post': post, 'comments': comments, 'user': request.user, 'replyDict': replyDict}
    return render(request, 'blog/blogPost.html', context)

def postComment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get("parentSno")
        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)

            comment.save()
            messages.success(request, "Your reply has been posted successfully")

    return redirect(f"/blog/{post.slug}")

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
