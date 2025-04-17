from django.views.generic import TemplateView
from django.utils.timezone import make_aware
from datetime import datetime


class MainView(TemplateView):
    template_name = "pages/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Main",
            "is_partials": True,
        })
        return context


class UserAuthView(TemplateView):
    template_name = "pages/auth.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Auth",
            "is_partials": False,
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


main_view = MainView.as_view()
user_auth_view = UserAuthView.as_view()
coming_soon_view = ComingSoonView.as_view()
