from django.db import models
from user.models import Users  # Assuming you're using Django's built-in User model
import uuid

class Wallet(models.Model):
    wallet_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    account_number = models.CharField(max_length=10, unique=True)
    account_name = models.CharField(max_length=255)
    pin = models.PositiveIntegerField()
    bvn = models.CharField(max_length=20, null=True, blank=True)
    currency = models.CharField(max_length=10, default="Naira")  # Default to Naira
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wallet for {self.user.username}"

    def save(self, *args, **kwargs):
        # Auto-generate account number if not set
        if not self.account_number:
            last_wallet = Wallet.objects.order_by('-account_number').first()
            if last_wallet:
                self.account_number = last_wallet.account_number + 1
            else:
                self.account_number = 1001  # Initial account number

        # Set account name based on user's first name and last name
        if not self.account_name:
            self.account_name = f"{self.user.first_name} {self.user.last_name}"

        super(Wallet, self).save(*args, **kwargs)