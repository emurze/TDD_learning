import reprlib

from django.db import models
from django.urls import reverse


class List(models.Model):
    slug = models.SlugField(unique=True)
    created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        indexes = (
            models.Index(fields=('slug',)),
        )

    def get_absolute_url(self) -> str:
        return reverse('lists', args=(self.slug,))


class ListItem(models.Model):
    content = models.CharField(max_length=256)
    list = models.ForeignKey(List, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return reprlib.repr(self.content)
