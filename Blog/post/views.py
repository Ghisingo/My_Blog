from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import BlogPost, Category
from .forms import PostForm
from django.contrib import messages
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

# def index(request):
#     data = {
#         'name' : "Aasish Ghising",
#         'address' : "Pokhara",
#     }
#     return HttpResponse(data)

# def index(request):
#     return render(request, 'post/index.html')

def index(request):
  posts = BlogPost.objects.all().filter(is_active=True)
  categories = Category.objects.all()

  context = {
    'posts':posts,
    'categories':categories
  }
  return render(request, 'post/index.html', context)

def post_details(request, id):
  post = BlogPost.objects.get(id=id)
  context = {
    'post':post,
  }
  return render(request, 'post/post-details.html', context)

def create_post(request):
    form = PostForm()
    categories = Category.objects.all();

    if request.method == "POST":
        title = request.POST.get('title')
        if title == "":
            messages.error(request, "Title field is required.")
            return HttpResponseRedirect('/create-post')
        category = Category.objects.get(id=request.POST.get('category'))   
        content = request.POST.get('content')
        if content == "":
            messages.error(request, "Content field is required.")
            return HttpResponseRedirect('/create-post')
        image = request.FILES.get('image')
        if image == "":
            messages.error(request, "Image field is required.")
            return HttpResponseRedirect('/create-post')
        is_active = request.POST.get('is_active')
        is_featured = request.POST.get('is_featured')

        if is_active == "on":
            is_active = True
        else:
            is_active = False

        if is_featured == "on":
            is_featured = True
        else:
            is_featured = False

        post = BlogPost.objects.create(
            title = title,
            category = category,
            author = request.user,
            content = content,
            image = image,
            is_active = is_active,
            is_featured = is_featured,
        )
        post.save()
        messages.success(request, f"{title} is Created Successfully.")
        return HttpResponseRedirect('/create-post')

    context = {
        'form':form,
        'categories':categories,
    }
    return render(request, 'post/create-post.html', context)


def registerUser(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == "POST":
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')

            if username and email and password:
                if password == password2:
                    user = User.objecte.create(
                        email=email, 
                        username = username, 
                        password = password)
                    user.save()
                    login(request,user)
                    return redirect('/')
                else:
                    messages.error(request, "The two password fields didn'/t match.")
                    return HttpResponseRedirect('/register')
            else:
              messages.error(request, "All fields are required.")
              return HttpResponseRedirect('/register')
    return render(request, 'post/register.html')

def logout_result(request):
    logout(request)
    return HttpResponseRedirect('/register.html')
