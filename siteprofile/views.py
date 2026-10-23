from django.shortcuts import render

from portfolio.models import Technology


def about(request):
    skills = Technology.grouped(Technology.objects.all())
    return render(request, "siteprofile/about.html", {"skills": skills})
