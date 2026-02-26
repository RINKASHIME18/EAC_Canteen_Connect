from django.db import models
from django.contrib.auth.models import User

STALL_CHOICES = [
    ("Maren's Food Cart", "Maren's Food Cart"),
    ('Rhoxy Canteen', 'Rhoxy Canteen'),
    ('M.D Mangubat Canteen', 'M.D Mangubat Canteen'),
    ('Stall 4', 'Stall 4'),
    ('Goldfranz Canteen', 'Goldfranz Canteen'),
    ('K-Pop House', 'K-Pop House'),
    ('kCairo Johns Food Hub', 'kCairo Johns Food Hub'),
    ('Tiger Crunch', 'Tiger Crunch'),
]

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_length=10, decimal_places=2, max_digits=10)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Report(models.Model):
    STATUS_CHOICES = [
        ('Received', 'Received'),
        ('Investigating', 'Investigating'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ]

    GENDER_CHOICES = [
        ('Female', 'Female'),
        ('Male', 'Male'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    reporter_name = models.CharField(max_length=100, blank=True, null=True)
    grade_section = models.CharField(max_length=100)
    stall = models.CharField(max_length=100, choices=STALL_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    is_anonymous = models.BooleanField(default=False)
    concern_text = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Received')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        username = self.user.username if self.user else "Anonymous"
        return f"Report #{self.id} by {username}"

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings', null=True, blank=True)
    stall = models.CharField(max_length=100, choices=STALL_CHOICES)
    rating = models.IntegerField(default=5)
    food_name = models.CharField(max_length=200)
    feedback = models.TextField()
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating for {self.stall} - {self.rating} stars"

class Suggestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='suggestions', null=True, blank=True)
    stall = models.CharField(max_length=100, choices=STALL_CHOICES)
    suggestion_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        username = self.user.username if self.user else "Anonymous"
        return f"Suggestion for {self.stall} by {username}"
