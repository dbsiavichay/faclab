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
	var untaxedAmount = 0;
	inputs.each(function (index, elem) {
		var value = $(elem).val();
		if (value) untaxedAmount+=parseFloat($(elem).val());			
		
	});

	console.log(untaxedAmount)

	var taxAmount = calculateTaxAmount();
	var totalAmount = taxAmount + untaxedAmount;
	$('#untaxed_amount').text('$' + untaxedAmount.toFixed(2));
	$('#total_amount').text('$' + totalAmount.toFixed(2));
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
				if (tax.amount_type==1) rowTax+=total + parseFloat(tax.amount);
				if (tax.amount_type==2) rowTax+=(total * parseFloat(tax.amount))/100;
			}
			taxAmount+=rowTax;
		}
	});
	$('#tax_amount').text('$' + taxAmount.toFixed(2))
	return taxAmount;
}

var addListeners = function (row) {
	$(row).find('select[name*=product]').on('change', getProductDetail);
	$(row).find('input[name*=quantity]').on('change', calculateTotalPrice);
	$(row).find('input[name*=unit_price]').on('change', calculateTotalPrice);	
	$(row).find('select[name*=taxes]').on('change', calculateTotalPrice);
}

var init = function () {
	var $rows = $('tbody tr.inline');
	$rows.each(function (index, row) {
		addListeners(row);		
	});
	getTaxes();	
}

$(function () {
	init();	
});