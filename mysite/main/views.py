from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseForbidden
from .models import Post
from .forms import Postform
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
@login_required(login_url="/login/")
def hello(request):
    posts = Post.objects.all()
    return render(request, "main/hello.html",{"posts": posts})


def logout_view(request):
    logout(request)
    return redirect("login")

def login_view(request):
    if request.method=="POST":
        form= AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('hello')
    else:
        form = AuthenticationForm()
    return render(request,"main/login.html",{"form":form})



def post_id(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    return render(request,"main/post_id.html",{"post":post})
def add_postform(request):
    if request.method=="POST":
        form=Postform(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("hello")
    else:
        form=Postform()
    return render(request,"main/add_postform.html",{"form":form})

def delete_post(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    if post.author != request.user:
        return HttpResponseForbidden("你沒有權限刪除這篇文章")
    if request.method=="POST":
        post.delete()
        return redirect("hello")
    return render(request,"main/post_id.html",{"post":post})
# Create your views here.

