from django.urls import reverse

from portfolio.views import PROJECTS_PER_PAGE

from .helpers import LocalizedTestCase, make_project, make_tech


class HomeViewTests(LocalizedTestCase):
    def test_home_renders_featured_public_projects_only(self):
        make_project("Shown featured", is_featured=True)
        make_project("Not featured")
        make_project("Hidden featured", is_featured=True, is_public=False)
        response = self.client.get(reverse("portfolio:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "portfolio/home.html")
        self.assertEqual([p.title for p in response.context["featured"]], ["Shown featured"])
        self.assertNotContains(response, "Hidden featured")

    def test_home_lists_in_progress_work_and_stack(self):
        django = make_tech("Django")
        make_project("Live work", status="in_progress", technologies=[django])
        response = self.client.get(reverse("portfolio:home"))
        self.assertEqual([p.title for p in response.context["now_projects"]], ["Live work"])
        self.assertContains(response, "Django")

    def test_home_in_english_uses_english_fields(self):
        make_project("Galería", title_en="Gallery", summary="Resumen", summary_en="Summary", is_featured=True)
        response = self.client.get("/en/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'lang="en"')
        self.assertContains(response, "Gallery")
        self.assertNotContains(response, "Galería")


class ProjectListViewTests(LocalizedTestCase):
    def setUp(self):
        self.django = make_tech("Django")
        self.laravel = make_tech("Laravel")
        self.gallery = make_project("Gallery", technologies=[self.django])
        self.festes = make_project("Festes", technologies=[self.laravel])
        self.hidden = make_project("Hidden", is_public=False, technologies=[self.django])

    def test_lists_public_projects(self):
        response = self.client.get(reverse("portfolio:project_list"))
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.context["projects"], [self.gallery, self.festes])
        self.assertNotContains(response, "Hidden")

    def test_tech_filter_keeps_only_matching_projects(self):
        response = self.client.get(reverse("portfolio:project_list"), {"tech": "django"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["projects"]), [self.gallery])
        self.assertEqual(response.context["active_tech"], self.django)
        # The active filter is marked for assistive tech and styling.
        self.assertContains(response, 'href="/projects/?tech=django" data-filter-link aria-current="page"')

    def test_unknown_tech_returns_404(self):
        response = self.client.get(reverse("portfolio:project_list"), {"tech": "cobol"})
        self.assertEqual(response.status_code, 404)

    def test_filter_only_offers_technologies_with_public_projects(self):
        make_tech("Unused")
        response = self.client.get(reverse("portfolio:project_list"))
        names = [t.name for t in response.context["technologies"]]
        self.assertEqual(names, ["Django", "Laravel"])
        django = next(t for t in response.context["technologies"] if t.name == "Django")
        self.assertEqual(django.public_count, 1)  # the hidden project is not counted

    def test_pagination_keeps_the_filter(self):
        for i in range(PROJECTS_PER_PAGE + 1):
            make_project(f"Extra {i}", technologies=[self.django])
        response = self.client.get(reverse("portfolio:project_list"), {"tech": "django"})
        self.assertTrue(response.context["page_obj"].has_next())
        self.assertContains(response, "?tech=django&amp;page=2")
        page_two = self.client.get(reverse("portfolio:project_list"), {"tech": "django", "page": 2})
        self.assertEqual(page_two.status_code, 200)
        self.assertEqual(len(page_two.context["projects"]), 2)


class ProjectDetailViewTests(LocalizedTestCase):
    def setUp(self):
        self.first = make_project("First", order=1, description="## Context\n\nSome **text**.")
        self.second = make_project("Second", order=2)
        self.third = make_project("Third", order=3)

    def test_renders_markdown_and_metadata(self):
        response = self.client.get(self.first.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "portfolio/project_detail.html")
        self.assertContains(response, "<strong>text</strong>", html=True)
        self.assertContains(response, '<meta property="og:type" content="article">', html=True)
        self.assertContains(response, 'property="og:title" content="First"')

    def test_previous_and_next_follow_list_order(self):
        response = self.client.get(self.second.get_absolute_url())
        self.assertEqual(response.context["prev_project"], self.first)
        self.assertEqual(response.context["next_project"], self.third)
        self.assertEqual(response.context["project_number"], 2)

    def test_edges_have_a_single_neighbour(self):
        first = self.client.get(self.first.get_absolute_url())
        last = self.client.get(self.third.get_absolute_url())
        self.assertIsNone(first.context["prev_project"])
        self.assertIsNone(last.context["next_project"])

    def test_private_project_returns_404(self):
        hidden = make_project("Secret", is_public=False)
        response = self.client.get(hidden.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_missing_project_returns_404(self):
        response = self.client.get(reverse("portfolio:project_detail", args=["nope"]))
        self.assertEqual(response.status_code, 404)


class SiteWideTests(LocalizedTestCase):
    def test_custom_404_page(self):
        # The test runner runs with DEBUG=False, so the custom template is used.
        response = self.client.get("/this-page-does-not-exist/")
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")
        self.assertContains(response, 'name="robots" content="noindex"', status_code=404)

    def test_about_page(self):
        make_tech("Django")
        response = self.client.get(reverse("siteprofile:about"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["skills"][0][0], "Backend")

    def test_sitemap_lists_public_projects_in_both_languages(self):
        public = make_project("Public one")
        make_project("Private one", is_public=False)
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, public.get_absolute_url())
        self.assertContains(response, f"/en{public.get_absolute_url()}")
        self.assertNotContains(response, "private-one")

    def test_robots_txt(self):
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/plain")
        self.assertContains(response, "Sitemap: http://testserver/sitemap.xml")
        self.assertContains(response, "Disallow: /admin/")

    def test_language_switch_redirects_to_english_url(self):
        project = make_project("Switch me")
        response = self.client.post(
            reverse("set_language"), {"language": "en", "next": project.get_absolute_url()})
        self.assertRedirects(response, f"/en{project.get_absolute_url()}", fetch_redirect_response=False)
