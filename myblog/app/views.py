from django.shortcuts import render,redirect
from app.models import blogs
from app.models import author
from django.contrib import messages

# Create your views here.

def index(request):
    isAuth = request.session.get("isAuth") 
    aid = request.session.get("aid")
    user = author.objects.filter(id=aid).first()
    mydata = blogs.objects.filter(aid=user)
    if isAuth:
        return render(request, "index.html", {'blogs': mydata, 'isAuth': isAuth})
    else:
        return render(request, "login.html")
    
def create_post(request):
    isAuth = request.session.get("isAuth") 
    if request.method == "POST":
        title = request.POST.get("title")
        summary = request.POST.get("summary")
        body = request.POST.get("content")
        aid = request.session.get("aid")
        #author = "abc"
         # request.POST.get("author")
        user = author.objects.filter(id= aid).first()

        b = blogs(title = title, summary = summary, body = body, aid = user)
        b.save()
        return redirect("/")
    if isAuth:
        return render(request, "create-post.html",{'isAuth': isAuth })
    else:
        return render(request, "login.html")

def display_post(request , id):
    isAuth = request.session.get("isAuth") 
    post = blogs.objects.filter(id=id).first()
    if post is None:
        redirect("/")
    return render(request,"post-detail.html", {'post': post,'isAuth': isAuth})

def edit_post(request, id):
    post = blogs.objects.filter(id=id).first()
    if post is None:
        redirect("/")

    if request.method == "POST":
        post.title = request.POST.get("title")
        post.summary = request.POST.get("summary")
        post.body = request.POST.get("content")
        post.save()
        redirect("/")

        
    return render(request, "update.html", {'post': post, 'isAuth':request.session.get("isAuth") })

def delete_post(request, id):
    if request.method == "POST":
        post = blogs.objects.filter(id=id).first()
        post.delete()

    return redirect("/")


def login_author(request):
    if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")

            user = author.objects.filter(email=email, password= password).first()
            if user is not None:
                request.session["aid"]=user.id
                request.session["isAuth"]= True
                print("login successfull")
            else:
                messages.error(request, "Invalid Username of Password")
                return render(request, "login.html")

            return redirect("/")

    return render(request, "login.html",  {'isAuth':request.session.get("isAuth")})

def create_author(request):
    if request.method == "POST":
        name = request.POST.get("aname")
        email = request.POST.get("email")
        password = request.POST.get("password")

        existing_user = author.objects.filter(email=email).first()
        if existing_user:
            messages.error(request, "Email is all ready Registered")    
            render(request, "create-author.html")
        else:
            user = author(name=name, email = email , password=password)
            user.save()
            redirect("/login")

    return render(request, "create-author.html",  {'isAuth':request.session.get("isAuth")})


def logout(request):
    request.session["aid"]=None
    request.session["isAuth"]=None
    return render(request, "login.html")