from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import (
    CustomUserCreationForm,
    ProfileUpdateForm,
    UserUpdateForm,
)
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Profile


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


def profile(request, profile_id):
    # Fetch the profile based on the profile_id
    profile = get_object_or_404(Profile, id=profile_id)
    return render(request, "users/profile.html", {"profile": profile})


@login_required
def update_profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect("profile")  # Replace 'profile' with the correct URL name
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, "users/update_profile.html", context)
