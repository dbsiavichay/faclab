from django.forms import ModelForm
from decimal import Decimal
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from .models import Invoice, InvoiceLine

class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = ('date', 'customer')

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

class InvoiceLineFormSet(BaseInlineFormSet):
    def save(self, commit=True):
        untaxed_amount = 0
        tax_amount = 0        
        for form in self.forms:
            if not form.has_changed():
                continue
            untaxed_amount+=form.cleaned_data.get('total_price')                        
            for tax in form.cleaned_data.get('taxes'):
                if tax.amount_type == tax.AMOUNT_TYPE_FIXED:
                    tax_amount+=form.cleaned_data.get('total_price') + Decimal.from_float(tax.amount)
                else:
                    tax_amount+=(form.cleaned_data.get('total_price') * Decimal.from_float(tax.amount))/100

        total_amount=untaxed_amount+tax_amount
        self.instance.untaxed_amount = untaxed_amount
        self.instance.tax_amount = tax_amount
        self.instance.total_amount = total_amount
        
        return super(InvoiceLineFormSet, self).save(commit=commit)

InvoiceLineInlineFormSet = inlineformset_factory(
    Invoice, InvoiceLine, form=InvoiceLineForm, extra = 2, min_num = 1,
    formset=InvoiceLineFormSet
)
