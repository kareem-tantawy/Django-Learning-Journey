from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import Post


class home(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/home.html'
    ordering = ['-date_posted']
    
class post(DetailView):
    model = Post
    # context_object_name = 'post-detail'

# default template_name = <app>/<model>_<viewtype>.html

    
class about(TemplateView):
    template_name = 'blog/about.html'
    