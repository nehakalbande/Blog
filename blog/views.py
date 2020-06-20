from django.shortcuts import render, HttpResponse

# Create your views here.

def blogHome(request):
    return render(request, 'blog/blogHome.html')
    #return HttpResponse('This is blogHome. we will keep all the blog posts here')

def blogPost(request, slug):
    return render(request, 'blog/blogPost.html')
    #return HttpResponse(f'This is BlogPost: {slug}')