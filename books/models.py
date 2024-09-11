from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    price = models.CharField(max_length=10)
    cover = models.ImageField(upload_to="covers/", blank=True, null=True)
    author = models.ForeignKey(
        "users.CustomUser", verbose_name=("author"), on_delete=models.CASCADE
    )
