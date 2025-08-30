import random

from django.shortcuts import render
from django.views.generic import TemplateView

from apps.recipes.models import Recipe


class RecipeListView(TemplateView):
    template_name = "pages/recipe_list.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Recipe List",
            "is_partials": True,
        })
        return context


class RecipeCreateView(TemplateView):
    template_name = "pages/recipe_create.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Recipe Create",
            "is_partials": True,
        })
        return context


class RecipeDetailView(TemplateView):
    template_name = "pages/recipe_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # TODO: mock
        # mock_recipe = self._create_mock_recipe()
        
        context.update({
            "title": "Recipe Detail",
            # "recipe": mock_recipe,
            "user_liked": True,
            "is_partials": True,
        })
        
        return context


class RandomRecipeDetailView(TemplateView):
    template_name = "pages/recipe_detail.html"
    
    def get(self, request):
        recipes = Recipe.objects.filter(is_banned=False, is_deleted=False, status='PUBLISHED')
        recipe = random.choice(list(recipes)) if recipes.exists() else None
        
        if not recipe:
            return render(request, "pages/recipe_not_found.html", {})
        
        return render(request, "pages/recipe_detail.html", {"recipe": recipe})


class RecipeUpdateView(TemplateView):
    template_name = "pages/recipe_update.html"


class RecipeRestoreView(TemplateView):
    template_name = "pages/recipe_restore.html"


class RecipeReportView(TemplateView):
    template_name = "pages/recipe_report.html"


recipe_list_view = RecipeListView.as_view()
recipe_create_view = RecipeCreateView.as_view()
recipe_detail_view = RecipeDetailView.as_view()
recipe_update_view = RecipeUpdateView.as_view()
recipe_restore_view = RecipeRestoreView.as_view()
recipe_report_view = RecipeReportView.as_view()
random_recipe_detail_view = RandomRecipeDetailView.as_view()
