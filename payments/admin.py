from django.contrib import admin
from .models import Payment


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_display_amount',
                    'stripe_charge_id', 'timestamp')
    readonly_fields = ('user', 'get_display_amount',
                       'stripe_charge_id', 'timestamp')


admin.site.register(Payment, PaymentAdmin)
