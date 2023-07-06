from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stripe_charge_id = models.CharField(max_length=50)
    amount = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_display_amount(self):
        return "{0:.2f}".format(self.amount / 100)
