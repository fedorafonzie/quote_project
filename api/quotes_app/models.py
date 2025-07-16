# django_app/quotes_app/models.py
from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

# --- HIER IS HET BELANGRIJKE NIEUWE MODEL ---
class Source(models.Model):
    name = models.CharField(max_length=255, unique=True)
    author_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Quote(models.Model):
    text = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True, blank=True, related_name='quotes')
    
    # DE FIX: Voeg blank=True toe om dit veld optioneel te maken in de admin
    categories = models.ManyToManyField(Category, related_name='quotes', blank=True)
    
    added_date = models.DateTimeField(auto_now_add=True)
    
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'In afwachting'),
        (STATUS_APPROVED, 'Goedgekeurd'),
        (STATUS_REJECTED, 'Afgekeurd'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        db_index=True
    ) 

    def __str__(self):
        return f'"{self.text[:50]}..."'