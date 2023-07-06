from .models import Payment
from django import forms


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount']

    # change the field name to something more user-friendly
    amount = forms.DecimalField(
        label='Amount (in dollars)', max_digits=5, decimal_places=2)
    amount.widget.attrs.update({'placeholder': 'Enter amount (e.g $8.50)'})
