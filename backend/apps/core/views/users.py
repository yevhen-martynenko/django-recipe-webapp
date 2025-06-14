from django.views.generic import TemplateView
from django.utils.timezone import make_aware
from datetime import datetime
from django.core.paginator import Paginator


class UserDetailView(TemplateView):
    template_name = "pages/user.html"


class UserMeDetailView(TemplateView):
    template_name = "pages/user_me.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "User me",
            "is_partials": True,
        })
        return context

class UserMeDeleteView(TemplateView):
    template_name = "pages/user_delete.html"


user_detail_view = UserDetailView.as_view()
user_me_detail_view = UserMeDetailView.as_view()
user_me_delete_view = UserMeDeleteView.as_view()
