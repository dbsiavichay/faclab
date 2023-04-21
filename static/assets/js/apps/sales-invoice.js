const setSubtotals = () => {
    let subtotal = document.querySelector(".invoice-subtotal");
    let tax = document.querySelector(".invoice-tax");
    let total = document.querySelector(".invoice-total");
    let subtotal_value = 0;
    let tax_value = 0;
    let total_value = 0;

    document.querySelectorAll("[id$=-subtotal]").forEach(elem => {
        if (elem.value && !isNaN(elem.value)) {
            subtotal_value+=parseFloat(elem.value);
        }
    });

    tax_value = subtotal_value * 0.12;
    total_value = subtotal_value + tax_value;

    subtotal.innerHTML = "$" + subtotal_value.toFixed(2);
    tax.innerHTML = "$" + tax_value.toFixed(2);
    total.innerHTML = "$" + total_value.toFixed(2);

}


const initProduct = function (selector) {
    let elem = selector ? $(selector) : $(document)

    elem.find('[id$=-product]').on("select2:select", event => {
        let data = event.params.data;
        let row = event.currentTarget.closest("tr");
        let unit_price = row.querySelector("[id$=-unit_price]");
        let quantity = row.querySelector("[id$=-quantity]");
        let subtotal = row.querySelector("[id$=-subtotal]");
        unit_price.value = data.first_price
        subtotal.value = data.first_price * quantity.value;
        setSubtotals();
    });

    elem.find('[id$=-quantity]').on("change", event => {
        let row = event.currentTarget.closest("tr");
        let unit_price = row.querySelector("[id$=-unit_price]").value || 0;
        let quantity = row.querySelector("[id$=-quantity]").value || 0;
        let subtotal = row.querySelector("[id$=-subtotal]");
        
        subtotal.value = unit_price * quantity;
        setSubtotals();
    });

    elem.find('[id$=-unit_price]').on("change", event => {
        let row = event.currentTarget.closest("tr");
        let unit_price = row.querySelector("[id$=-unit_price]").value || 0;
        let quantity = row.querySelector("[id$=-quantity]").value || 0;
        let subtotal = row.querySelector("[id$=-subtotal]");
        
        subtotal.value = unit_price * quantity;
        setSubtotals();
    });
}


const invoiceForm = () => {
    initProduct();
}


formsetCallbackAdd = row => {
    initSelect2(row);
    initTouchspin(row);
    initProduct(row);
    row[0].querySelector('[id$=-quantity]').value = 1

}


document.addEventListener("DOMContentLoaded", () => {
    invoiceForm();
});