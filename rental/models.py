from django.db import models
from django.contrib.auth.models import User


class Bicycle(models.Model):
    bicycle_id = models.CharField(max_length=10, unique=True)
    type = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default="available")
    image = models.ImageField(upload_to="bicycles/", null=True, blank=True)
    price_per_hour = models.DecimalField(
        max_digits=5, decimal_places=2, default=2.00
    )  # New field

    def __str__(self):
        return f"{self.bicycle_id} ({self.type})"

    def average_rating(self):
        rentals = self.rental_set.filter(rating__isnull=False)
        if rentals.exists():
            avg = rentals.aggregate(models.Avg("rating"))["rating__avg"]
            return round(avg, 1)
        return None

    def feedback_count(self):
        return self.rental_set.filter(rating__isnull=False).count()


class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bicycle = models.ForeignKey(Bicycle, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField()
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.IntegerField(
        null=True, blank=True, choices=[(i, i) for i in range(1, 6)]
    )
    review = models.TextField(null=True, blank=True)
    transaction_id = models.CharField(max_length=12, null=True, blank=True, unique=True)

    def __str__(self):
        return f"{self.user.username} rented {self.bicycle}"
