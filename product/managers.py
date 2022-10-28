from django.db import models


class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(available= True)


# class ProductManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(available= True)



# class ProductQuerySet(models.QuerySet):
#     def is_availble(self):
#         return self.filter(available=False)

#     def search(self, query, user=None):
#         lookup = Q(title__icontains=query) | Q(content__icontains=query)
#         qs = self.is_public().filter(lookup)
#         if user is not None:
#             qs2 = self.filter(user=user).filter(lookup)
#             qs = (qs | qs2).distinct()
#         return qs

# class ProductManager(models.Manager):
#     def get_queryset(self):
#         return ProductQuerySet(self.model, using=self._db)

#     def search(self, query, user=None):
#         return self.get_queryset().search(query, user=user)