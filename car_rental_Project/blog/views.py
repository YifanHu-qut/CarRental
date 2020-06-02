from django.shortcuts import render
from django.shortcuts import render_to_response
from blog.models import BlogPost
from django.http import HttpResponse
# Create your views here.

def archive(request):
    posts = BlogPost.objects.all()
    return render_to_response('blog/archive.html',{'posts':posts})
