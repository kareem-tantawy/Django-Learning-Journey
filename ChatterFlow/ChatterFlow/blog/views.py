from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Post

# Create your views here.
# def home(request):
#     return render(request, 'blog/home.html')

class home(TemplateView):
    context = {
        'posts': Post.objects.all()
    }
    template_name = 'blog/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        return context
    
# def about(request):
#     return render(request, 'blog/about.html')

class about(TemplateView):
    template_name = 'blog/about.html'
    
    
# class HelloView(TemplateView):
#     """A class-based view rendering a template named 'hello.html'."""
#     template_name = 'hello.html'