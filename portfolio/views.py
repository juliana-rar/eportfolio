from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render

from .models import Project, Technology

PROJECTS_PER_PAGE = 9


def public_technologies():
    """Technologies used by at least one public project, with that count."""
    return (
        Technology.objects.annotate(
            public_count=Count("projects", filter=Q(projects__is_public=True))
        )
        .filter(public_count__gt=0)
    )


def home(request):
    technologies = public_technologies()
    context = {
        "featured": Project.objects.featured().prefetch_related("technologies")[:6],
        "stack": Technology.grouped(technologies),
        # Margin notes in the hero: current work and the most used tools.
        "now_projects": Project.objects.public().filter(status=Project.Status.IN_PROGRESS)[:3],
        "top_technologies": technologies.order_by("-public_count", "name")[:5],
    }
    return render(request, "portfolio/home.html", context)


def project_list(request):
    projects = Project.objects.public().prefetch_related("technologies")
    active_tech = None
    tech_slug = request.GET.get("tech")
    if tech_slug:
        active_tech = get_object_or_404(Technology, slug=tech_slug)
        projects = projects.filter(technologies=active_tech)

    page_obj = Paginator(projects, PROJECTS_PER_PAGE).get_page(request.GET.get("page"))
    context = {
        "page_obj": page_obj,
        "projects": page_obj.object_list,
        "technologies": public_technologies().order_by("name"),
        "active_tech": active_tech,
    }
    return render(request, "portfolio/project_list.html", context)


def project_detail(request, slug):
    public = Project.objects.public()
    project = get_object_or_404(public.prefetch_related("technologies", "images"), slug=slug)

    # Neighbours follow the same ordering as the projects list.
    ids = list(public.values_list("pk", flat=True))
    index = ids.index(project.pk)
    prev_pk = ids[index - 1] if index > 0 else None
    next_pk = ids[index + 1] if index + 1 < len(ids) else None
    neighbours = Project.objects.in_bulk([pk for pk in (prev_pk, next_pk) if pk])
    context = {
        "project": project,
        "project_number": index + 1,
        "project_total": len(ids),
        "images": project.images.all(),
        "prev_project": neighbours.get(prev_pk),
        "next_project": neighbours.get(next_pk),
    }
    return render(request, "portfolio/project_detail.html", context)
