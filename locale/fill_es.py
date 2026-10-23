"""Fill locale/es/LC_MESSAGES/django.po with the Spanish strings below.

Run after `makemessages -l es` (inside the container):
    podman-compose exec web python locale/fill_es.py
Only empty msgstr entries are filled, so manual edits are never overwritten.
"""
import re
from pathlib import Path

PO = Path(__file__).resolve().parent / "es" / "LC_MESSAGES" / "django.po"

ES = {
    # Navigation and layout
    "Skip to content": "Saltar al contenido",
    "Menu": "Menú",
    "Main": "Principal",
    "Home": "Inicio",
    "Projects": "Proyectos",
    "About": "Sobre mí",
    "Contact": "Contacto",
    "Dark mode": "Modo oscuro",
    "Email": "Correo",
    "Built with Django and hand-written CSS.": "Hecho con Django y CSS escrito a mano.",
    "Spanish": "Español",
    "English": "Inglés",
    # Home
    "Portfolio": "Portafolio",
    "See my projects": "Ver mis proyectos",
    "Download CV": "Descargar CV",
    "Get in touch": "Contactar",
    "Portrait of %(name)s": "Retrato de %(name)s",
    "Featured projects": "Proyectos destacados",
    "All projects": "Todos los proyectos",
    "No featured projects yet.": "Todavía no hay proyectos destacados.",
    "Tech stack": "Tecnologías",
    # Projects list
    "%(tech)s projects": "Proyectos con %(tech)s",
    "Projects with screenshots, the tech stack and links.": "Proyectos con capturas, tecnologías y enlaces.",
    "Things I have designed, built and shipped. Filter them by technology.":
        "Cosas que he diseñado, construido y publicado. Fíltralas por tecnología.",
    "Filter by technology": "Filtrar por tecnología",
    "All": "Todos",
    "No projects match this filter yet.": "Todavía no hay proyectos con este filtro.",
    "Pagination": "Paginación",
    "Previous": "Anterior",
    "Next": "Siguiente",
    "Page %(current)s of %(total)s": "Página %(current)s de %(total)s",
    "Technologies": "Tecnologías",
    # Project detail
    "Screenshot of %(title)s": "Captura de %(title)s",
    "%(title)s, screenshot %(n)s": "%(title)s, captura %(n)s",
    "Visit the live site": "Ver la web",
    "View the code": "Ver el código",
    "Description": "Descripción",
    "Screenshots": "Capturas",
    "Project details": "Detalles del proyecto",
    "Role": "Rol",
    "Year": "Año",
    "Status": "Estado",
    "Built with": "Hecho con",
    "More projects": "Más proyectos",
    "Previous project": "Proyecto anterior",
    "Next project": "Proyecto siguiente",
    "Screenshot viewer": "Visor de capturas",
    "Close": "Cerrar",
    "Previous image": "Imagen anterior",
    "Next image": "Imagen siguiente",
    # About
    "About me": "Sobre mí",
    "Skills": "Habilidades",
    # Contact
    "Have a project in mind or a question? Write to me and I will get back to you.":
        "¿Tienes un proyecto en mente o una pregunta? Escríbeme y te responderé.",
    "Prefer email?": "¿Prefieres el correo?",
    "Fields marked with * are required.": "Los campos marcados con * son obligatorios.",
    "Send message": "Enviar mensaje",
    "Leave this field empty": "Deja este campo vacío",
    "Thank you! Your message has been sent.": "¡Gracias! Tu mensaje se ha enviado.",
    "Please fix the errors below.": "Corrige los errores indicados abajo.",
    # 404
    "Page not found": "Página no encontrada",
    "The page you are looking for does not exist or has been moved.":
        "La página que buscas no existe o se ha movido.",
    "Back to home": "Volver al inicio",
    "See projects": "Ver proyectos",
    # Models and admin
    "Frontend": "Frontend",
    "Backend": "Backend",
    "DevOps": "DevOps",
    "Mobile": "Móvil",
    "Database": "Base de datos",
    "Finished": "Terminado",
    "In progress": "En curso",
    "name": "nombre",
    "slug": "slug",
    "icon": "icono",
    "category": "categoría",
    "technology": "tecnología",
    "technologies": "tecnologías",
    "title (ES)": "título (ES)",
    "title (EN)": "título (EN)",
    "summary (ES)": "resumen (ES)",
    "summary (EN)": "resumen (EN)",
    "description (ES, Markdown)": "descripción (ES, Markdown)",
    "description (EN, Markdown)": "descripción (EN, Markdown)",
    "cover image": "imagen de portada",
    "cover": "portada",
    "role": "rol",
    "year": "año",
    "status": "estado",
    "repository URL": "URL del repositorio",
    "live URL": "URL en producción",
    "featured": "destacado",
    "public": "público",
    "order": "orden",
    "created": "creado",
    "project": "proyecto",
    "projects": "proyectos",
    "image": "imagen",
    "caption (ES)": "pie (ES)",
    "caption (EN)": "pie (EN)",
    "screenshot": "captura",
    "screenshots": "capturas",
    "preview": "vista previa",
    "Content (Spanish)": "Contenido (español)",
    "Content (English)": "Contenido (inglés)",
    "Details": "Detalles",
    "Links": "Enlaces",
    "Visibility": "Visibilidad",
    "Profile": "Perfil",
    "profile": "perfil",
    "headline (ES)": "titular (ES)",
    "headline (EN)": "titular (EN)",
    "bio (ES, Markdown)": "biografía (ES, Markdown)",
    "bio (EN, Markdown)": "biografía (EN, Markdown)",
    "avatar": "avatar",
    "CV (PDF)": "CV (PDF)",
    "email": "correo electrónico",
    "GitHub URL": "URL de GitHub",
    "LinkedIn URL": "URL de LinkedIn",
    "location": "ubicación",
    "Links and files": "Enlaces y archivos",
    "message": "mensaje",
    "messages": "mensajes",
    "received": "recibido",
    "read": "leído",
    "Mark selected messages as read": "Marcar los mensajes seleccionados como leídos",
    # Editorial redesign
    "Web development": "Desarrollo web",
    "What's next": "¿Y ahora?",
    "Have a project in mind? <em>Let's talk.</em>": "¿Tienes un proyecto en mente? <em>Hablemos.</em>",
    "Write to me": "Escríbeme",
    "Designed and coded by hand. Django, PostgreSQL and framework-free CSS, served from Podman containers.":
        "Diseñado y programado a mano. Django, PostgreSQL y CSS sin frameworks, servido desde contenedores Podman.",
    "Hi, I'm <span class=\"scribble\">%(first)s</span>.": 'Hola, soy <span class="scribble">%(first)s</span>.',
    "See my work": "Ver mi trabajo",
    "More about me": "Más sobre mí",
    "At a glance": "De un vistazo",
    "Right now": "Ahora mismo",
    "Based in": "Desde",
    "Usual tools": "Herramientas habituales",
    "Index": "Índice",
    "Selected <em>work</em>": "Trabajo <em>seleccionado</em>",
    "Toolbox": "Caja de herramientas",
    "What I <em>build with</em>": "Con qué <em>construyo</em>",
    "Archive": "Archivo",
    "Project %(n)s of %(total)s": "Proyecto %(n)s de %(total)s",
    "The project": "El proyecto",
    "I'm <em>%(first)s</em>.": "Soy <em>%(first)s</em>.",
    "Elsewhere": "En la red",
    "Skills, <em>by area</em>": "Habilidades, <em>por área</em>",
    "Let's <em>talk</em>.": "<em>Hablemos</em>.",
    "This page <em>got lost</em>.": "Esta página <em>se ha perdido</em>.",
}

# Spanish catalogs use three plural forms (one, many, other); see Plural-Forms in the header.
ES_PLURAL = {
    "%(counter)s project": ("%(counter)s proyecto", "%(counter)s proyectos", "%(counter)s proyectos"),
}


def unquote(lines):
    return "".join(re.findall(r'"(.*)"', "\n".join(lines))).replace('\\"', '"')


def quote(text):
    return '"' + text.replace('"', '\\"') + '"'


def fill(block):
    lines = block.split("\n")
    def field(name):
        start = next((i for i, l in enumerate(lines) if l.startswith(name + " ")), None)
        if start is None:
            return None, None, None
        end = start + 1
        while end < len(lines) and lines[end].startswith('"'):
            end += 1
        return start, end, unquote(lines[start:end])

    _s, _e, msgid = field("msgid")
    if not msgid:
        # Header: drop the fuzzy flag so the catalog compiles cleanly.
        return block.replace("#, fuzzy\n", "")

    # makemessages may "guess" a translation from a similar old string and mark
    # it fuzzy. Those guesses are wrong more often than not: when we know the
    # real translation, drop the guess (flag + "#|" previous msgid) and refill.
    fuzzy = any(l.startswith("#,") and "fuzzy" in l for l in lines)
    known = msgid in ES_PLURAL if "msgid_plural" in block else msgid in ES
    overwrite = fuzzy and known
    if overwrite:
        cleaned = []
        for line in lines:
            if line.startswith("#|"):
                continue
            if line.startswith("#,"):
                flags = [f for f in line[2:].replace(" ", "").split(",") if f and f != "fuzzy"]
                if not flags:
                    continue
                line = "#, " + ", ".join(flags)
            cleaned.append(line)
        lines[:] = cleaned

    if "msgid_plural" in block and msgid in ES_PLURAL:
        forms = ES_PLURAL[msgid]
        for idx, text in enumerate(forms):
            s, e, value = field(f"msgstr[{idx}]")
            if s is None:
                # Form missing from the template: append it after the previous one.
                last = max(i for i, l in enumerate(lines) if l.startswith("msgstr["))
                lines.insert(last + 1, f"msgstr[{idx}] {quote(text)}")
            elif overwrite or not value:
                lines[s:e] = [f"msgstr[{idx}] {quote(text)}"]
        return "\n".join(lines)
    s, e, value = field("msgstr")
    if s is not None and (overwrite or not value) and msgid in ES:
        lines[s:e] = [f"msgstr {quote(ES[msgid])}"]
    return "\n".join(lines)


def untranslated(block):
    lines = block.split("\n")
    if any(l.startswith("#~") for l in lines):
        return None  # obsolete entry
    ids = [i for i, l in enumerate(lines) if l.startswith("msgid ")]
    strs = [i for i, l in enumerate(lines) if l.startswith("msgstr")]
    if not ids or not strs:
        return None
    msgid = unquote(lines[ids[0]:strs[0]])
    msgstr = unquote(lines[strs[0]:])
    fuzzy = any(l.startswith("#,") and "fuzzy" in l for l in lines)
    return msgid if msgid and (not msgstr or fuzzy) else None


text = PO.read_text(encoding="utf-8")
blocks = [fill(b) for b in text.split("\n\n")]
PO.write_text("\n\n".join(blocks), encoding="utf-8")
missing = [m for m in map(untranslated, blocks) if m]
print(f"Filled {PO}. Untranslated or fuzzy: {missing or 'none'}")
