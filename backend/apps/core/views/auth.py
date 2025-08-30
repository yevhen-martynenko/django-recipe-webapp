from django.views.generic import TemplateView


class AuthView(TemplateView):
    template_name = "pages/auth.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Auth",
            "is_partials": False,
        })
        return context


class ActivateView(TemplateView):
    template_name = "pages/activate.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Activate",
            "is_partials": False,
        })
        return context


class AuthPasswordResetView(TemplateView):
    template_name = "pages/password_reset.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Password reset",
            "is_partials": False,
        })
        return context


class AuthPasswordResetConfirmView(TemplateView):
    template_name = "pages/password_reset_confirm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Password reset confirm",
            "is_partials": False,
        })
        return context


auth_view = AuthView.as_view()
activate_view = ActivateView.as_view()
auth_password_reset_view = AuthPasswordResetView.as_view()
auth_password_reset_confirm_view = AuthPasswordResetConfirmView.as_view()
