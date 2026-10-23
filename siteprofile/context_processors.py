from .models import Profile


def site_profile(request):
    """Expose the site owner's profile as `profile` in every template."""
    return {"profile": Profile.load()}
