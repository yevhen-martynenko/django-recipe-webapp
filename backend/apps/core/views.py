from django.views.generic import TemplateView


class MainView(TemplateView):
    template_name = "pages/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Main",
            "is_partials": True,
        })
        return context


class UserRegisterView(TemplateView):
    template_name = "pages/registration.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Register",
            "is_partials": False,
        })
        return context


class ComingSoonView(TemplateView):
    template_name = "pages/coming_soon.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Coming soon",
            "is_partials": True,
        })
        return context


main_view = MainView.as_view()
user_register_view = UserRegisterView.as_view()
coming_soon_view = ComingSoonView.as_view()
