from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from pathlib import Path

User = get_user_model()

class ResourceAbstract(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class Activity(ResourceAbstract):
    pass

class Course(ResourceAbstract):
    pass

class Crop(ResourceAbstract):
    pass

class Currency(ResourceAbstract):
    pass

class Department(ResourceAbstract):
    pass

class Grade(ResourceAbstract):
    pass

class Harvest(ResourceAbstract):
    pass

class Input(ResourceAbstract):
    pass

class Livestock(ResourceAbstract):
    pass

class Market(ResourceAbstract):
    pass

class Material(ResourceAbstract):
    pass

class Process(ResourceAbstract):
    pass

class RawMaterial(ResourceAbstract):
    pass

class Timeline(ResourceAbstract):
    start_date = models.DateField()
    end_date = models.DateField()

class Unit(ResourceAbstract):
    supervisor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class Location(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name

class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def clean(self):
        # Validate the file type
        file_extension = Path(self.file.name).suffix.lower()
        if file_extension != '.pdf':
            raise ValidationError('Only PDF files are allowed.')

        # Validate the file size
        file_size = self.file.size
        max_size_in_mb = 2
        if file_size > max_size_in_mb * 1024 * 1024:  # Convert MB to Bytes
            raise ValidationError(f'The file size should not exceed {max_size_in_mb}MB.')

    def save(self, *args, **kwargs):
        self.clean()  # Ensure the file is validated before saving
        super().save(*args, **kwargs)


