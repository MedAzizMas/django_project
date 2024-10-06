from django.db import models
from categories.models import Category
from django.core.validators import MaxValueValidator,FileExtensionValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.
class Conference(models.Model):
    titre=models.CharField(max_length=255)
    decription=models.TextField()
    start_date=models.DateField(default=timezone.now().date())
    end_date=models.DateField(default=timezone.now().date())
    location=models.CharField(max_length=255)
    price=models.FloatField()
    capacity=models.IntegerField(validators=[MaxValueValidator(100, message='Capacity must be under 100')])
    program=models.FileField(upload_to="files/",validators=
                             [FileExtensionValidator(allowed_extensions=['pdf','png','jpg','jpeg'],message='only pdf jpg png')])
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,
                               related_name="conferences")
    def clean(self):
        if self.end_date <= self.start_date :
            raise ValidationError(message="end date must be greater than start date")

    class Meta:
        constraints=[
            models.CheckConstraint(
                check=models.Q(
                    start_date__gte=timezone.now().date())
                    ,name='check_start_date_after_today_date'
                        
            )
        ]
