var taxes = {}

var getTaxes = function () {	
	var listTaxes = $('select[name*=taxes]>option').map(function () {
		return $(this).val();
	});

	listTaxes.each(function (index, pk) {		
		var url = '/billing/tax/' + pk + '/';
		$.get(url, function (data) {
			taxes[pk] = data;
		});
	});
}

var getCurrentRow = function (child) {	
	var currentRow = $(child).parents('tr');

	return {
		quantity: currentRow.find('input[name*=quantity]'),
		unitPrice: currentRow.find('input[name*=unit_price]'),
		totalPrice: currentRow.find('input[name*=total_price]'),
	}
}

var getProductDetail = function () {
	var self = $(this);
	var pk = self.val();
	if (!pk) return;
	var url = '/inventory/product/' + pk + '/';
	$.get(url, function (data) {
		var cr = getCurrentRow(self);
		//Set inputs
		cr.unitPrice.val(data['price']);
		cr.quantity.val(1);
		cr.quantity.trigger('change');
	});
}

var calculateTotal = function () {
	var inputs = $('input[name*=total_price]');
	var totalAmount = 0;
	inputs.each(function (index, elem) {
		var value = $(elem).val();
		if (value) totalAmount+=parseFloat($(elem).val());			
		
	});

	$('input[name*=untaxed_amount]').val(totalAmount);
	$('input[name*=total_amount]').val(totalAmount);
	calculateTaxAmount();
}

var calculateTotalPrice = function () {
	var cr = getCurrentRow(this);
	if (!cr.quantity.val() || !cr.unitPrice.val()) return;
	var total = parseFloat(cr.quantity.val() * cr.unitPrice.val())
	cr.totalPrice.val(total)
	calculateTotal();
}

var calculateTaxAmount = function () {	
	var taxAmount = 0;
	$('select[name*=taxes]').each(function() {
		var pks = $(this).val();
		pks = pks!=null?pks:[];
		var $row = getCurrentRow(this);		
		if (pks.length > 0 && $row.totalPrice.val()) {
			var rowTax = 0;
			var total = $row.totalPrice.val();

			for (var i in pks) {
				var tax = taxes[pks[i]]
				rowTax+=(total * parseFloat(tax.amount))/100;
			}
			taxAmount+=rowTax;
		}
	});
	$('input[name*=tax_amount').val(taxAmount)
}

var addListeners = function ($row) {
	$row.find('select[name*=product]').on('change', getProductDetail);
	$row.find('input[name*=quantity]').on('change', calculateTotalPrice);
	$row.find('input[name*=unit_price]').on('change', calculateTotalPrice);	
	$row.find('select[name*=taxes]').on('change', calculateTaxAmount);
}

var init = function () {
	var $row = $('tbody tr').first();
	addListeners($row);
	getTaxes();	
}

$(function () {
	init();	
});