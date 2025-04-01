from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .forms import (
    CustomUserCreationForm,
    ProfileUpdateForm,
    UserUpdateForm,
)
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.middleware.csrf import get_token
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


def profile_detail(request, profile_id):
    # Fetch the profile based on the profile_id
    profile = get_object_or_404(Profile, id=profile_id)

    is_following = False
    if request.user.is_authenticated:
        is_following = request.user.profile.is_following(profile)

    context = {
        "profile": profile,
        "is_following": is_following,
        "csrf_token": get_token(request),
    }

    return render(request, "users/profile-detail.html", context)


@login_required
def update_profile(request, profile_id):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect("profile-detail", profile_id=request.user.profile.id)
        else:
            # Print out form errors for debugging
            print("User Form Errors:", user_form.errors)
            print("Profile Form Errors:", profile_form.errors)
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, "users/update_profile.html", context)


@require_POST
@login_required
def toggle_follow(request, profile_id):
    # Get the current user's profile
    try:
        current_user_profile = request.user.profile

        # Get the profile to be followed
        target_profile = get_object_or_404(Profile, id=profile_id)

        if current_user_profile == target_profile:
            return JsonResponse({"error": "You cannot follow yourself!"}, status=400)

        if current_user_profile.is_following(target_profile):
            current_user_profile.unfollow(target_profile)
            is_following = False
        else:
            current_user_profile.follow(target_profile)
            is_following = True

        return JsonResponse(
            {
                "is_following": is_following,
                "followers_count": target_profile.get_followers_count(),
                "following_count": target_profile.get_following_count(),
            }
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def followers_list(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    followers = profile.followers.all()

    context = {
        "profile": profile,
        "followers": followers,
        "followers_count": profile.get_followers_count(),
        "is_own_profile": request.user.is_authenticated
        and request.user.profile.id == profile.id,
    }
    return render(request, "users/followers_list.html", context)


def following_list(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    following = profile.following_set.all()

    context = {
        "profile": profile,
        "following": following,
        "following_count": profile.get_following_count(),
        "is_own_profile": request.user.is_authenticated
        and request.user.profile.id == profile.id,
    }
    return render(request, "users/following_list.html", context)
