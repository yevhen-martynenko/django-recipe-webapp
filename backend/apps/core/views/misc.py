from django.views.generic import TemplateView
from django.utils.timezone import make_aware
from datetime import datetime
from django.core.paginator import Paginator


# class MainView(TemplateView):
#     template_name = "pages/index.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update({
#             "title": "Main",
#             "is_partials": True,
#         })
#         return context


class MainView(TemplateView):
    template_name = "pages/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Mock data for featured recipe
        featured_recipe = {
            "title": "Homemade Italian Pizza",
            "description": "Master the art of pizza making with our authentic Italian recipe. Perfect crispy crust and melty cheese guaranteed.",
            "get_absolute_url": "/recipes/homemade-italian-pizza"
        }

        # Mock data for popular recipes
        popular_recipes = [
            {
                "id": "123",
                "title": "Classic Beef Burger",
                "slug": "classic-beef-burger",
                "description": "The perfect juicy burger recipe with all the fixings",
                "image": None,
                "views": "1.2k",
                "is_liked": True,
            }
            for _ in range(10)
        ]

        # Mock data for recommended recipes
        recommended_recipes = [
            {
                "id": "234",
                "title": "Perfect Pizza",
                "slug": "perfect-pizza",
                "description": "Master the art of pizza making with our authentic Italian recipe. Perfect crispy crust and melty cheese guaranteed.",
                "image": None,
                "views": "1,20000 views",
                "is_liked": False,
            }
            for _ in range(10)
        ]

        # Paginated recommended recipes (mock pagination)
        # paginator = Paginator(recommended_recipes, 3)
        # page_number = self.request.GET.get('page')
        # page_obj = paginator.get_page(page_number)

        context.update({
            "title": "Main",
            "is_partials": True,
            "featured_recipe": featured_recipe,
            "popular_recipes": popular_recipes,
            "recommended_recipes": recommended_recipes,
        })
        return context


class ComingSoonView(TemplateView):
    template_name = "pages/coming_soon.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        target_time = datetime(2026, 1, 1, 0, 0, 0)
        aware_time = make_aware(target_time)
        social_media_urls = (
            # ('X', 'https://x.com'),
            ('Instagram', 'https://www.instagram.com'),
            ('Facebook', 'https://www.facebook.com'),
            ('LinkedIn', 'https://www.linkedin.com'),
            ('Pinterest', 'https://www.pinterest.com'),
            ('Reddit', 'https://www.reddit.com'),
        )

        context.update({
            "title": "Coming soon",
            "is_partials": True,
            "future_time": aware_time.isoformat(),
            "social_media_urls": social_media_urls
        })
        return context


class FeedbackView(TemplateView):
    template_name = "pages/feedback.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        feedbacks = [
            {
                "uuid": "1",
                "date": "2025-01-15",
                "date_iso": "2025-01-15",
                "type": "Bug Report",
                "type_slug": "bug",
                "subject": "Issue 1",
                "message": "This is an issue message.",
            },
            {
                "uuid": "2",
                "date": "2025-01-16",
                "date_iso": "2025-01-16",
                "type": "Suggestion",
                "type_slug": "suggestion",
                "subject": "Question 1",
                "message": "This is a question message.",
            },
            {
                "uuid": "3",
                "date": "2025-01-17",
                "date_iso": "2025-01-17",
                "type": "Question",
                "type_slug": "question",
                "subject": "Suggestion 1",
                "message": "This is a suggestion message.",
            },
        ]

        context.update({
            "title": "Feedback",
            "is_partials": True,
            "feedbacks": feedbacks,
        })
        return context


class SiteMapView(TemplateView):
    template_name = "pages/site_map.html"

    def get_context_data(self, **kwargs):
        BASE_URL = "http://127.0.0.1:8000"
        urls = {
            "Main Page": {
                "urls": {
                    "Home": "/",
                },
                "badge": "main",
            },
            "Authentication": {
                "urls": {
                    "Sign in/Sign up": "/auth",
                    "Activate": "/activate",
                    "Password reset": "/password-reset",
                    "Password reset confirm": "/password-reset/confirm",
                },
                "badge": "auth",
            },
            "Recipes": {
                "urls": {
                    "All Recipes": "/recipes",
                    "Create Recipe": "/recipes/create",
                    "Random Recipe": "/recipes/random",
                },
                "badge": "recipe",
            },
            "User Management": {
                "urls": {
                    "My Profile": "/users/me",
                    "Update Profile": "/users/me/update",
                    "User Profiles": "/users",
                },
                "badge": "user",
            },
            "Additional Pages": {
                "urls": {
                    "Feedback": "/feedback",
                    "Coming Soon": "/coming-soon",
                    "Site Map": "/site-map",
                },
                "badge": "misc",
            }
        }

        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Site map",
            "is_partials": True,
            "urls": urls,
            "base_url": BASE_URL,
        })
        return context


main_view = MainView.as_view()
coming_soon_view = ComingSoonView.as_view()
feedback_view = FeedbackView.as_view()
site_map_view = SiteMapView.as_view()
