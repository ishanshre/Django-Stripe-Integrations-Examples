from django.db.models import Manager


class ActiveManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)