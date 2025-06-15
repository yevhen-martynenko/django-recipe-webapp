from django.views.generic import TemplateView
from django.utils.timezone import make_aware
from datetime import datetime
from django.core.paginator import Paginator


class RecipeListView(TemplateView):
    template_name = "pages/recipe_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        mock_recipes = [
            {
                "id": 1,
                "title": "Avocado Toast with Poached Eggs",
                "description": "A delicious and nutritious breakfast option that's ready in minutes. Perfect for busy mornings!",
                "image": "/static/images/avocado-toast.jpg",
                "tags": ["breakfast", "quick"],
                "cooking_time": 15,
                "difficulty": "easy",
                "ingredients": 6,
                "rating": 4.5,
                "likes": 1200,
                "date_added": "2023-05-15",
                "is_favorite": False
            },
            {
                "id": 2,
                "title": "Creamy Mushroom Risotto",
                "description": "A comforting Italian classic that's worth the effort. Creamy arborio rice with savory mushrooms and herbs.",
                "image": "/static/images/mushroom-risotto.jpg",
                "tags": ["dinner", "vegetarian"],
                "cooking_time": 45,
                "difficulty": "medium",
                "ingredients": 8,
                "rating": 4.7,
                "likes": 875,
                "date_added": "2023-04-28",
                "is_favorite": True
            },
            {
                "id": 3,
                "title": "Chocolate Avocado Mousse",
                "description": "A healthy twist on a classic dessert. Rich, creamy, and no one will guess it's made with avocados!",
                "image": "/static/images/chocolate-mousse.jpg",
                "tags": ["dessert", "gluten-free"],
                "cooking_time": 20,
                "difficulty": "easy",
                "ingredients": 5,
                "rating": 4.3,
                "likes": 1500,
                "date_added": "2023-06-02",
                "is_favorite": False
            },
            {
                "id": 4,
                "title": "Greek Chickpea Salad",
                "description": "A protein-packed Mediterranean salad that's perfect for meal prep. Refreshing, healthy and satisfying.",
                "image": "/static/images/chickpea-salad.jpg",
                "tags": ["lunch", "quick", "vegan"],
                "cooking_time": 10,
                "difficulty": "easy",
                "ingredients": 9,
                "rating": 4.6,
                "likes": 945,
                "date_added": "2023-05-21",
                "is_favorite": False
            },
            {
                "id": 5,
                "title": "Sweet Potato & Black Bean Tacos",
                "description": "These plant-based tacos are bursting with flavor. Roasted sweet potatoes, spicy black beans, and fresh toppings.",
                "image": "/static/images/sweet-potato-tacos.jpg",
                "tags": ["dinner", "vegan"],
                "cooking_time": 35,
                "difficulty": "medium",
                "ingredients": 12,
                "rating": 4.8,
                "likes": 1100,
                "date_added": "2023-06-08",
                "is_favorite": True
            },
            {
                "id": 6,
                "title": "Berry Chia Seed Pudding",
                "description": "Make this overnight pudding for a nutritious grab-and-go breakfast. Packed with omega-3s and antioxidants.",
                "image": "/static/images/chia-pudding.jpg",
                "tags": ["breakfast", "gluten-free"],
                "cooking_time": 5,
                "difficulty": "easy",
                "ingredients": 7,
                "rating": 4.4,
                "likes": 532,
                "date_added": "2023-05-30",
                "is_favorite": False
            },
            {
                "id": 7,
                "title": "Spicy Thai Basil Stir Fry",
                "description": "Quick and flavorful Thai-inspired stir fry with fresh basil and vegetables. Ready in under 20 minutes.",
                "image": "/static/images/thai-stir-fry.jpg",
                "tags": ["dinner", "quick", "vegan"],
                "cooking_time": 18,
                "difficulty": "easy",
                "ingredients": 10,
                "rating": 4.5,
                "likes": 689,
                "date_added": "2023-06-12",
                "is_favorite": False
            },
            {
                "id": 8,
                "title": "Classic French Onion Soup",
                "description": "Rich, deeply flavored soup with caramelized onions and melted Gruyère cheese. Perfect for cold days.",
                "image": "/static/images/french-onion-soup.jpg",
                "tags": ["lunch", "vegetarian"],
                "cooking_time": 90,
                "difficulty": "medium",
                "ingredients": 8,
                "rating": 4.6,
                "likes": 756,
                "date_added": "2023-03-15",
                "is_favorite": True
            },
            {
                "id": 9,
                "title": "Quinoa Buddha Bowl",
                "description": "Nutritious and colorful bowl packed with quinoa, roasted vegetables, and tahini dressing.",
                "image": "/static/images/buddha-bowl.jpg",
                "tags": ["lunch", "vegan", "gluten-free"],
                "cooking_time": 30,
                "difficulty": "easy",
                "ingredients": 11,
                "rating": 4.4,
                "likes": 823,
                "date_added": "2023-04-10",
                "is_favorite": False
            },
            {
                "id": 10,
                "title": "Homemade Pizza Margherita",
                "description": "Classic Italian pizza with fresh mozzarella, basil, and San Marzano tomatoes on homemade dough.",
                "image": "/static/images/pizza-margherita.jpg",
                "tags": ["dinner", "vegetarian"],
                "cooking_time": 120,
                "difficulty": "hard",
                "ingredients": 8,
                "rating": 4.9,
                "likes": 2150,
                "date_added": "2023-05-05",
                "is_favorite": True
            },
        ]

        tags = [
            {
                "id": 1,
                "slug": "lunch",
                "name": "Lunch",
            },
            {
                "id": 2,
                "slug": "dinner",
                "name": "Dinner",
            },
            {
                "id": 3,
                "slug": "quick",
                "name": "Quick",
            },
            {
                "id": 4,
                "slug": "healthy",
                "name": "Healthy",
            },
            {
                "id": 5,
                "slug": "gluten-free",
                "name": "Gluten-free",
            },
        ]

        recipe_detail = "/recipe/view/%s/"

        context.update({
            "title": "Recipe list",
            "is_partials": True,
            "recipes": mock_recipes,
            "tags": tags,
            "recipe_detail": recipe_detail,
        })
        return context


class RecipeCreateView(TemplateView):
    template_name = "pages/recipe_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Recipe create",
            "is_partials": True,
        })
        return context


class RecipeDetailView(TemplateView):
    template_name = "pages/recipe_detail.html"


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
