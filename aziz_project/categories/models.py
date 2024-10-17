from django.db import models
import re 
from django.core.exceptions import ValidationError
def validate_letters_only(value):
    if not re.match(r'^[A-Za-z\s]+$', value):  # Validates letters and spaces
        raise ValidationError('This field must contain letters only.')
# Create your models here.
class Category(models.Model):
    title = models.CharField(
        max_length=255,
        validators=[validate_letters_only]  # Applying the custom validator
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
    def __str__(self) :
        return f"title category : {self.title}  "