from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post



class Home(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "blog/home.html"
    ordering = ["-date_posted"]


class post(DetailView):
    model = Post
    context_object_name = "post"
    # context_object_name = 'post-detail'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "blog/create_post.html"
    fields = ["title", "content"]
    
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = "blog/create_post.html"
    fields = ["title", "content"]
    
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
            
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"
    template_name = "blog/post_delete_confirm.html"
    
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
# default template_name = <app>/<model>_<viewtype>.html


class About(TemplateView):
    template_name = "blog/about.html"
