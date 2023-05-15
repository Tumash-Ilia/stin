from django.db import models


# Create your models here.

class SimpleModel(models.Model):
    just_text = models.CharField(
        verbose_name="Just a field",
        max_length=255
    )
