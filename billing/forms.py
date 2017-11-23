from django.forms import ModelForm
from decimal import Decimal
from django.forms.models import inlineformset_factory
from .models import Invoice, InvoiceLine

class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'

    def save(self, commit=True):
        obj = super(InvoiceForm, self).save(commit=False)

        if commit:
            obj.save()

        return obj

class InvoiceLineForm(ModelForm):
    class Meta:
        model = InvoiceLine
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(InvoiceLineForm, self).__init__(*args, **kwargs)
        self.fields['total_price'].required = False        

    def save(self, commit=True):
        obj = super(InvoiceLineForm, self).save(commit=False)        
        obj.total_price = obj.unit_price * Decimal.from_float(obj.quantity)

        if commit:
            obj.save()
            
        return obj

InvoiceLineInlineFormSet = inlineformset_factory(
    Invoice, InvoiceLine, form=InvoiceLineForm, extra = 2, min_num=1
)
