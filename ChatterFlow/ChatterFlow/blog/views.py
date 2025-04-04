from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from users.models import CustomUser
from .forms import CommentForm


class Home(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "blog/home.html"
    ordering = ["-date_posted"]
    paginate_by = 5

class UserPosts(ListView):
    model = Post
    context_object_name = "user_posts"
    template_name = "blog/user-posts.html"
    paginate_by = 5
    
    def get_queryset(self):
        user = get_object_or_404(CustomUser, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by("-date_posted")


class PostDetailView(DetailView, FormView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = Comment.objects.filter(
            post=self.object, parent__isnull=True
        ).order_by("-created_at")
        context["form"] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = self.object
            parent_id = request.POST.get("parent_id")
            if parent_id:
                parent_comment = get_object_or_404(Comment, id=parent_id)
                comment.parent = parent_comment

            comment.save()
            return redirect(self.object.get_absolute_url())

        return self.form_invalid(form)


## FBV for post_detail
# def post_detail(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     comments = Comment.objects.filter(post=post, parent__isnull=True).order_by('-created_at')
#     form = CommentForm

#     if request.method=="GET":
#         form = CommentForm(request.GET)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.user = request.user
#             comment.post = request.post
#             comment.save()
#             return redirect('post_detail', post_id=post.id)
#     return render(request, 'blog/post_detail.html', {'post':Post, 'comments':comments, 'form':form})


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
