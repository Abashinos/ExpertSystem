from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def view_profile(request):
    return render(request, "profile/view_profile.html")