"""Load the real projects as initial portfolio content, with placeholder images.

    podman-compose exec web python manage.py seed_portfolio            # create / update
    podman-compose exec web python manage.py seed_portfolio --reset    # wipe and reload
    podman-compose exec web python manage.py seed_portfolio --no-images

Content comes from each project's README in the parent `proyectos` folder.
Projects whose README is missing or does not describe the app carry a TODO and
are seeded as not public, so the TODO never shows on the live site.
Re-running is safe: projects are matched by slug and technologies by name.
"""
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from PIL import Image, ImageDraw, ImageFont

from portfolio.models import Project, ProjectImage, Technology
from siteprofile.models import Profile

GITHUB = "https://github.com/juliana-rar"

TECHNOLOGIES = {
    # backend
    "Django": "backend", "Python": "backend", "Laravel": "backend", "PHP": "backend",
    ".NET": "backend", "C#": "backend", "SignalR": "backend", "EF Core": "backend",
    # frontend
    "Vanilla JS": "frontend", "Vue": "frontend", "Inertia": "frontend", "Blazor": "frontend",
    "Vite": "frontend", "Leaflet": "frontend",
    # databases
    "PostgreSQL": "db", "MySQL": "db", "MariaDB": "db", "SQLite": "db", "SQL Server": "db",
    # devops
    "Podman": "devops", "Nginx": "devops", "Gunicorn": "devops",
    # mobile
    "Flutter": "mobile", "Dart": "mobile",
}

PROJECTS = [
    {
        "slug": "pos-tpv",
        "title": "PosTPV — Punto de venta para restaurante",
        "title_en": "PosTPV — Restaurant point of sale",
        "summary": "TPV para restaurante/pizzería con cocina en tiempo real, plano de mesas editable y facturación exportable.",
        "summary_en": "Restaurant/pizzeria point of sale with a real-time kitchen display, an editable floor plan and exportable billing.",
        "description": (
            "Punto de venta construido con **.NET 9** y **Blazor Web App** (Interactive Server), "
            "**EF Core + SQL Server** y **SignalR** para avisar a cocina en tiempo real.\n\n"
            "## Arquitectura\n\n"
            "Clean Architecture en cuatro capas: *Domain*, *Application* (DTOs, servicios, "
            "AutoMapper, FluentValidation), *Infrastructure* (DbContext, repositorios, hash PBKDF2) "
            "y *Web* (Blazor, autenticación por cookie, hub de SignalR).\n\n"
            "## Funcionalidades\n\n"
            "- TPV con categorías, rejilla de productos, extras, atajos de teclado y **pago dividido**.\n"
            "- Pantalla de cocina (KDS) con tickets en tiempo real.\n"
            "- Editor de **plano de mesas** con arrastrar y soltar, y unión de mesas para grupos grandes.\n"
            "- Reservas, comandas abiertas y facturación con **gráficos dibujados en SVG/CSS** "
            "(sin librería de gráficos) y exportación a CSV, Excel y PDF.\n"
            "- CSS escrito a mano con tokens y modo claro/oscuro, sin Bootstrap ni Tailwind."
        ),
        "description_en": (
            "A point of sale built with **.NET 9** and **Blazor Web App** (Interactive Server), "
            "**EF Core + SQL Server** and **SignalR** to notify the kitchen in real time.\n\n"
            "## Architecture\n\n"
            "Clean Architecture in four layers: *Domain*, *Application* (DTOs, services, AutoMapper, "
            "FluentValidation), *Infrastructure* (DbContext, repositories, PBKDF2 hashing) and "
            "*Web* (Blazor, cookie auth, SignalR hub).\n\n"
            "## Features\n\n"
            "- POS with categories, product grid, add-ons, keyboard shortcuts and **split payment**.\n"
            "- Kitchen display (KDS) with real-time tickets.\n"
            "- Drag-and-drop **floor-plan editor**, with joined tables for large parties.\n"
            "- Reservations, open orders and billing with **hand-drawn SVG/CSS charts** "
            "(no chart library) and export to CSV, Excel and PDF.\n"
            "- Hand-written CSS with tokens and light/dark mode, no Bootstrap or Tailwind."
        ),
        "technologies": [".NET", "C#", "Blazor", "SignalR", "EF Core", "SQL Server", "Podman"],
        "role": "Full-stack",
        "year": 2026,
        "status": Project.Status.FINISHED,
        "repo": "pos-tpv",
        "featured": True,
        "accent": (168, 65, 26),
    },
    {
        "slug": "festes-majors-de-catalunya",
        "title": "Festes Majors de Catalunya",
        "title_en": "Festes Majors de Catalunya",
        "summary": "Mapa, calendario y carrusel de las fiestas mayores de los municipios catalanes, con panel de administración.",
        "summary_en": "Map, calendar and carousel of the festes majors of Catalan towns, with a full admin panel.",
        "description": (
            "Aplicación web que muestra las *festes majors* de los municipios de Cataluña: un carrusel "
            "de próximas fiestas, una lista «cerca de ti» (distancia Haversine), y un **mapa interactivo** "
            "y un **calendario mensual** sincronizados. Permite compartir en Instagram Stories e incluye "
            "un panel de administración completo.\n\n"
            "## Técnica\n\n"
            "- **Laravel 13** (PHP 8.3), **MariaDB 11** y plantillas Blade.\n"
            "- ES modules en JavaScript *vanilla* empaquetados con **Vite**, mapa con **Leaflet**.\n"
            "- Imágenes generadas en servidor con Intervention Image; tests con **Pest 4**.\n"
            "- **Sin framework CSS**: todo el CSS está escrito a mano, con la paleta «nit de festa».\n"
            "- Entorno completo en contenedores **Podman**."
        ),
        "description_en": (
            "A web app showing the *festes majors* of Catalonia's municipalities: an upcoming-festivals "
            "carousel, a \"near you\" list (Haversine distance), and an **interactive map** and **month "
            "calendar** that stay in sync. It supports Instagram Story sharing and ships with a full "
            "admin panel.\n\n"
            "## Under the hood\n\n"
            "- **Laravel 13** (PHP 8.3), **MariaDB 11** and Blade templates.\n"
            "- Vanilla JavaScript ES modules bundled with **Vite**, maps with **Leaflet**.\n"
            "- Server-side images with Intervention Image; tests with **Pest 4**.\n"
            "- **No CSS framework**: every line of CSS is hand-written, with the \"nit de festa\" palette.\n"
            "- The whole environment runs in **Podman** containers."
        ),
        "technologies": ["Laravel", "PHP", "MariaDB", "Vanilla JS", "Vite", "Leaflet", "Podman"],
        "role": "Full-stack",
        "year": 2026,
        "status": Project.Status.FINISHED,
        "repo": "fest",
        "featured": True,
        "accent": (15, 16, 32),
    },
    {
        "slug": "podman-gallery",
        "title": "Galería de artista (Django)",
        "title_en": "Artist gallery (Django)",
        "summary": "Web de artista con galería de obra, productos, exposiciones, miscelánea y perfiles, en Django y PostgreSQL.",
        "summary_en": "Artist website with a work gallery, products, exhibitions, miscellany and profiles, in Django and PostgreSQL.",
        "description": (
            "Sitio web Django para una artista: galería de obra, productos, exposiciones, miscelánea "
            "y perfiles, con edición de contenido enriquecido mediante CKEditor.\n\n"
            "## Técnica\n\n"
            "- **Django 5.2** (Python 3.12) y **PostgreSQL 16**, con usuario personalizado y login por email.\n"
            "- API REST de proyectos con Django REST Framework.\n"
            "- Desarrollo y producción con **Podman Compose**: *runserver* en desarrollo; **Gunicorn**, "
            "WhiteNoise y **Nginx** como proxy inverso en producción."
        ),
        "description_en": (
            "A Django website for an artist: work gallery, products, exhibitions, miscellany and "
            "profiles, with rich-text editing through CKEditor.\n\n"
            "## Under the hood\n\n"
            "- **Django 5.2** (Python 3.12) and **PostgreSQL 16**, with a custom user model and email login.\n"
            "- A REST API for projects with Django REST Framework.\n"
            "- Development and production with **Podman Compose**: *runserver* in development; "
            "**Gunicorn**, WhiteNoise and **Nginx** as reverse proxy in production."
        ),
        "technologies": ["Django", "Python", "PostgreSQL", "Podman", "Gunicorn", "Nginx"],
        "role": "Full-stack",
        "year": 2024,
        "status": Project.Status.FINISHED,
        "repo": "podman-gallery",
        "featured": True,
        "accent": (79, 99, 38),
    },
    {
        "slug": "gallery-flutter",
        "title": "Galería multimedia (Flutter)",
        "title_en": "Media gallery (Flutter)",
        "summary": "App de galería offline-first para fotos, vídeos y documentos, con editores de foto y vídeo integrados.",
        "summary_en": "Offline-first gallery app for photos, videos and documents, with built-in photo and video editors.",
        "description": (
            "App de galería multimedia *offline-first* en **Flutter/Dart**, pensada para Play Store y "
            "preparada para iOS sin cambios de código.\n\n"
            "## Funcionalidades\n\n"
            "- Galería, carpetas, papelera y documentos sobre un esquema **SQLite**.\n"
            "- Editor de fotos propio: filtros, ajustes, recorte y rotación libres, deshacer/rehacer y "
            "comparación antes/después.\n"
            "- Editor de vídeo con FFmpeg: recorte, rotación, velocidad, volumen, filtros y exportación con progreso.\n"
            "- Tema claro/oscuro, i18n en español, inglés y francés, y copia de seguridad en ZIP.\n\n"
            "Pendiente antes de publicar: probar en un dispositivo real y configurar la firma de *release*."
        ),
        "description_en": (
            "An *offline-first* media gallery app in **Flutter/Dart**, aimed at the Play Store and "
            "ready for iOS without code changes.\n\n"
            "## Features\n\n"
            "- Gallery, folders, trash and documents on top of a **SQLite** schema.\n"
            "- Custom photo editor: filters, adjustments, free crop and rotation, undo/redo and "
            "before/after comparison.\n"
            "- FFmpeg video editor: trim, rotate, speed, volume, filters and export with progress.\n"
            "- Light/dark theme, i18n in Spanish, English and French, and ZIP backups.\n\n"
            "Still to do before release: test on a real device and set up release signing."
        ),
        "technologies": ["Flutter", "Dart", "SQLite"],
        "role": "Mobile",
        "year": 2026,
        "status": Project.Status.IN_PROGRESS,
        "repo": "gallery-flutter",
        "featured": True,
        "accent": (11, 110, 105),
    },
    {
        "slug": "reserva-dhores",
        "title": "Reserva d'hores",
        "title_en": "Reserva d'hores — appointment booking",
        "summary": "Aplicación de reserva de horas con presentación, reservas y panel de administración, en Laravel y Vue.",
        "summary_en": "Appointment booking app with a landing page, bookings and an admin panel, in Laravel and Vue.",
        "description": (
            "Aplicación de **reserva de horas** con página de presentación, flujo de reservas y panel "
            "de administración.\n\n"
            "## Infraestructura\n\n"
            "Tres servicios orquestados con **Podman Compose**:\n\n"
            "- `api`: **Laravel 13** (PHP 8.4) con **Vue** e **Inertia**, compilado con **Vite**.\n"
            "- `admin`: SPA en **Vue 3** + Vite.\n"
            "- `db`: **MySQL 8**, con migraciones y datos de ejemplo al arrancar."
        ),
        "description_en": (
            "An **appointment booking** app with a landing page, a booking flow and an admin panel.\n\n"
            "## Infrastructure\n\n"
            "Three services orchestrated with **Podman Compose**:\n\n"
            "- `api`: **Laravel 13** (PHP 8.4) with **Vue** and **Inertia**, built with **Vite**.\n"
            "- `admin`: a **Vue 3** + Vite SPA.\n"
            "- `db`: **MySQL 8**, with migrations and seed data on start-up."
        ),
        "technologies": ["Laravel", "PHP", "Vue", "Inertia", "Vite", "MySQL", "Podman"],
        "role": "Full-stack",
        "year": 2026,
        "status": Project.Status.IN_PROGRESS,
        "repo": "base-podman",
        "featured": False,
        "accent": (91, 58, 94),
    },
    {
        "slug": "gallery-laravel",
        "title": "Galería de artista (Laravel)",
        "title_en": "Artist gallery (Laravel)",
        "summary": "La web de artista, portada de Django a Laravel 11 con PostgreSQL, Blade y Eloquent.",
        "summary_en": "The artist website, ported from Django to Laravel 11 with PostgreSQL, Blade and Eloquent.",
        "description": (
            "Port a **Laravel 11** (PHP 8.3) del sitio Django de la galería de artista: galería, "
            "productos, exposiciones, miscelánea y perfiles.\n\n"
            "- **PostgreSQL 16**, plantillas **Blade** y ORM Eloquent.\n"
            "- Rutas con nombres que replican el esquema `app:name` del proyecto Django original.\n"
            "- Desarrollo con **Podman Compose**; producción con php-fpm y **Nginx**."
        ),
        "description_en": (
            "A **Laravel 11** (PHP 8.3) port of the Django artist-gallery site: gallery, products, "
            "exhibitions, miscellany and profiles.\n\n"
            "- **PostgreSQL 16**, **Blade** templates and the Eloquent ORM.\n"
            "- Route names mirror the `app:name` scheme of the original Django project.\n"
            "- Development with **Podman Compose**; production with php-fpm and **Nginx**."
        ),
        "technologies": ["Laravel", "PHP", "PostgreSQL", "Podman", "Nginx"],
        "role": "Full-stack",
        "year": 2026,
        "status": Project.Status.FINISHED,
        "repo": "gallery-laravel",
        "featured": False,
        "accent": (138, 81, 0),
    },
    {
        # TODO: no README in the repository. Stack taken from ultimatum/ultimatum.csproj
        # and podman/podman-compose.yml. Write the summary and make it public.
        "slug": "sushibuffet",
        "title": "Sushi buffet",
        "title_en": "Sushi buffet",
        "summary": "TODO: describir el proyecto (el repositorio no tiene README).",
        "summary_en": "TODO: describe the project (the repository has no README).",
        "description": "TODO: el repositorio no tiene README. Stack deducido de `ultimatum.csproj` y `podman-compose.yml`.",
        "description_en": "TODO: the repository has no README. Stack taken from `ultimatum.csproj` and `podman-compose.yml`.",
        "technologies": [".NET", "C#", "Blazor", "EF Core", "SQL Server", "Podman"],
        "role": "Full-stack",
        "year": 2025,
        "status": Project.Status.FINISHED,
        "repo": "sushibuffet",
        "featured": False,
        "public": False,
        "accent": (31, 58, 95),
    },
    {
        # TODO: README.podman.md only documents the container setup, not the app itself.
        "slug": "medicinalternativa",
        "title": "Medicinalternativa",
        "title_en": "Medicinalternativa",
        "summary": "TODO: describir la aplicación (el README solo documenta el contenedor Podman).",
        "summary_en": "TODO: describe the app (the README only documents the Podman container).",
        "description": (
            "TODO: describir la aplicación.\n\n"
            "Lo que documenta el README: proyecto **Django 5.1** empaquetado en un contenedor **Podman**, "
            "servido con **Gunicorn** sobre **SQLite**, con `migrate` y `collectstatic` al arrancar."
        ),
        "description_en": (
            "TODO: describe the app.\n\n"
            "What the README documents: a **Django 5.1** project packaged in a **Podman** container, "
            "served by **Gunicorn** on **SQLite**, running `migrate` and `collectstatic` on start-up."
        ),
        "technologies": ["Django", "Python", "SQLite", "Gunicorn", "Podman"],
        "role": "Full-stack",
        "year": 2025,
        "status": Project.Status.FINISHED,
        "repo": "medicinalternativa",
        "featured": False,
        "public": False,
        "accent": (59, 74, 84),
    },
]

PROFILE = {
    "name": "Juliana",
    "headline": "Desarrollo web full-stack: Django, Laravel, .NET y Flutter, del contenedor al último píxel.",
    "headline_en": "Full-stack web development: Django, Laravel, .NET and Flutter, from the container to the last pixel.",
    "bio": (
        "Construyo aplicaciones web de principio a fin: modelos y APIs en **Django**, **Laravel** "
        "y **.NET**, interfaces con CSS escrito a mano y JavaScript sin frameworks, y entornos "
        "reproducibles con **Podman**.\n\n"
        "Este portafolio es un ejemplo: Django, PostgreSQL y CSS sin frameworks, servido desde contenedores."
    ),
    "bio_en": (
        "I build web applications end to end: models and APIs in **Django**, **Laravel** and "
        "**.NET**, interfaces with hand-written CSS and framework-free JavaScript, and reproducible "
        "environments with **Podman**.\n\n"
        "This portfolio is an example: Django, PostgreSQL and framework-free CSS, served from containers."
    ),
    "github_url": GITHUB,
    # TODO: fill in from the admin. Left empty on purpose (not in any README).
    "location": "",
    "email": "",
}

PAPER = (246, 243, 236)
INK = (34, 32, 27)


def _font(size):
    try:
        return ImageFont.load_default(size=size)
    except TypeError:  # Pillow built without FreeType
        return ImageFont.load_default()


def _png(image):
    buffer = BytesIO()
    image.save(buffer, "PNG", optimize=True)
    return ContentFile(buffer.getvalue())


def make_cover(title, accent):
    """1600x1000 placeholder: accent field, ruled grid, title set large."""
    w, h = 1600, 1000
    img = Image.new("RGB", (w, h), accent)
    draw = ImageDraw.Draw(img)
    light = tuple(min(255, c + 40) for c in accent)
    for x in range(0, w, 160):
        draw.line([(x, 0), (x, h)], fill=light, width=1)
    for y in range(0, h, 160):
        draw.line([(0, y), (w, y)], fill=light, width=1)
    draw.text((96, 96), "PLACEHOLDER", font=_font(28), fill=PAPER)
    draw.multiline_text((96, h - 330), title.replace(" — ", "\n"), font=_font(92), fill=PAPER, spacing=18)
    draw.line([(96, h - 110), (520, h - 110)], fill=PAPER, width=4)
    return _png(img)


def make_screen(title, accent, number):
    """1280x800 placeholder wireframe of an app screen."""
    w, h = 1280, 800
    img = Image.new("RGB", (w, h), PAPER)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, w, 64], fill=INK)
    # Pillow's built-in font has no em dash glyph.
    draw.text((32, 18), title.replace(" — ", " / "), font=_font(26), fill=PAPER)
    draw.rectangle([0, 64, 240, h], fill=(238, 233, 223))
    for i in range(6):
        draw.rounded_rectangle([32, 104 + i * 56, 208, 132 + i * 56], radius=6, fill=(220, 212, 198))
    cols = [(280 + c * 330, 104) for c in range(3)]
    for c, (x, y) in enumerate(cols):
        fill = accent if (c + number) % 3 == 0 else (220, 212, 198)
        draw.rounded_rectangle([x, y, x + 300, y + 260], radius=10, fill=fill)
        draw.rounded_rectangle([x, y + 290, x + 300, y + 320], radius=6, fill=(220, 212, 198))
    draw.rounded_rectangle([280, 470, 1240, 760], radius=10, outline=accent, width=3)
    draw.text((308, 494), f"Placeholder screenshot {number}", font=_font(30), fill=INK)
    return _png(img)


class Command(BaseCommand):
    help = "Load the real projects (from the sibling folders' READMEs) as initial portfolio content."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true",
                            help="Delete all projects, technologies and their images first, and overwrite the profile.")
        parser.add_argument("--no-images", action="store_true",
                            help="Skip generating placeholder covers and screenshots.")

    @transaction.atomic
    def handle(self, *args, reset=False, no_images=False, **options):
        if reset:
            self._reset()

        technologies = {}
        for name, category in TECHNOLOGIES.items():
            tech, _ = Technology.objects.update_or_create(name=name, defaults={"category": category})
            technologies[name] = tech

        created_count = 0
        for order, data in enumerate(PROJECTS, start=1):
            project, created = Project.objects.update_or_create(
                slug=data["slug"],
                defaults={
                    "title": data["title"],
                    "title_en": data["title_en"],
                    "summary": data["summary"],
                    "summary_en": data["summary_en"],
                    "description": data["description"],
                    "description_en": data["description_en"],
                    "role": data["role"],
                    "year": data["year"],
                    "status": data["status"],
                    "repo_url": f"{GITHUB}/{data['repo']}",
                    "is_featured": data["featured"],
                    "is_public": data.get("public", True),
                    "order": order,
                },
            )
            created_count += created
            project.technologies.set(technologies[name] for name in data["technologies"])
            if not no_images:
                self._images(project, data)

        self._profile(overwrite=reset)
        self.stdout.write(self.style.SUCCESS(
            f"Seeded {len(PROJECTS)} projects ({created_count} new) and {len(TECHNOLOGIES)} technologies."
        ))
        todo = [p["slug"] for p in PROJECTS if not p.get("public", True)]
        if todo:
            self.stdout.write(self.style.WARNING(
                "Hidden until their TODO is resolved in the admin: " + ", ".join(todo)
            ))

    def _reset(self):
        for image in ProjectImage.objects.all():
            image.image.delete(save=False)
        for project in Project.objects.all():
            project.cover.delete(save=False)
        Project.objects.all().delete()
        Technology.objects.all().delete()

    def _images(self, project, data):
        # Never overwrite images uploaded through the admin.
        title = data["title_en"]
        if not project.cover:
            project.cover.save(f"{project.slug}-cover.png", make_cover(title, data["accent"]), save=True)
        if not project.images.exists():
            for n in range(1, 4):
                ProjectImage.objects.create(
                    project=project,
                    image=ContentFile(make_screen(title, data["accent"], n).read(), name=f"{project.slug}-screen-{n}.png"),
                    caption=f"Captura provisional {n}",
                    caption_en=f"Placeholder screenshot {n}",
                    order=n,
                )

    def _profile(self, overwrite):
        profile = Profile.load()
        for field, value in PROFILE.items():
            if overwrite or not getattr(profile, field) or (field == "name" and profile.name == "Portfolio"):
                setattr(profile, field, value)
        profile.save()
