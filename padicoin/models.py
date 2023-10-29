from django.db import models
from user.models import Users
from django.utils import timezone
import uuid

class PadicoinAccount(models.Model):
    account_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    pin = models.PositiveIntegerField()  # You can adjust the data type as needed
    earned_today = models.DecimalField(max_digits=10, decimal_places=2)
    last_activity_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"PADICOIN Account for {self.user.username}"