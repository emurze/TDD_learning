import reprlib

from django.db import models


class ListItem(models.Model):
    content = models.CharField(max_length=256)

    def __str__(self) -> str:
        return reprlib.repr(self.content)
