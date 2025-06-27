from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.recipes.models import Recipe


class Command(BaseCommand):
    help = "Permanently delete recipes soft-deleted more than 7 days ago."

    def handle(self, *args, **kwargs):
        now = timezone.now()
        cutoff = now - timezone.timedelta(days=7)
        recipes_to_delete = Recipe.objects.filter(is_deleted=True, deleted_at__lte=cutoff)

        count = recipes_to_delete.count()

        if count == 0:
            self.stdout.write("No recipes to delete.")
            return

        self.stdout.write(f"{count} recipe(s) will be permanently deleted.")
        for recipe in recipes_to_delete:
            self.stdout.write(f"- {recipe.title} (deleted at: {recipe.deleted_at})")

        confirm = input("Are you sure you want to delete these recipes? [y/N]: ")
        if confirm.lower() != 'y':
            self.stdout.write(self.style.WARNING("Aborted. No recipes were deleted."))
            return

        recipes_to_delete.delete()
        self.stdout.write(self.style.SUCCESS(f"Permanently deleted {count} recipes."))
