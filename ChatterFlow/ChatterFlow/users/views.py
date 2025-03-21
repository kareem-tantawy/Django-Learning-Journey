from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


# def register(request):
#     if request.method == "POST":
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get("username")
#             messages.success(
#                 request, f"Account created for {username}! You can now log in."
#             )
#             return redirect("login-form")
#     else:
#         form = CustomUserCreationForm()
#     return render(request, "users/register.html", {"register_form": form})


class register(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login-form")
    template_name = "users/register.html"

    def form_valid(self, form):

        response = super().form_valid(form)

        username = form.cleaned_data.get("username")
        messages.success(
            self.request, f"Account created for {username}! You can now log in."
        )

        return response


@login_required
def profile(request):
    return render(request, "users/profile.html")
