from django import forms

from viewpack import ModelPack


class BasePack(ModelPack):
    # Templates
    list_template_name = "base/base_list.html"
    form_template_name = "base/base_form.html"
    detail_template_name = "base/base_detail.html"
    delete_template_name = "base/base_confirm_delete.html"


class PriceInput(forms.NumberInput):
    input_type = "price"


class PercentInput(forms.NumberInput):
    input_type = "percent"
