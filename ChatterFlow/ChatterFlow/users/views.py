from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


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


def update_profile(request):
    if request.method == "POST":
        u_form = CustomUserChangeForm(
            request.POST, request.FILES, instance=request.user
        )
        if u_form.is_valid():
            u_form.save()
        messages.success(request, f"Your account has been updated!")
        return redirect("profile")

    else:
        u_form = CustomUserChangeForm(instance=request.user)

    context = {"u_form": u_form}
    return render(request, "users/update_profile.html", context)
