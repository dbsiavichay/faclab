let selectedTaxes = []

const addIvaEvents = (netInput, grossInput, revenuePercentInput=null, revenueInput=null) => {
    const costNetInput = document.getElementById("id_cost_price");

    const getIvaRate = () => {
        const ivaTaxes = selectedTaxes.filter(tax => tax.type == 'iva')
        const ivaRate = ivaTaxes.length>0?ivaTaxes[0].fee/100:0
        return ivaRate
    }

    const setPrices = event => {
        const ivaRate = getIvaRate();
        let costNet = parseFloat(costNetInput.value) || 0;
        let target = event.currentTarget;
        let netPrice = parseFloat(netInput.value);

        let grossPrice = netPrice * (ivaRate + 1);
        if (target != grossInput) grossInput.value = grossPrice.toFixed(5);

        if (revenuePercentInput && revenueInput) {
            let revenue = netPrice - costNet;
            if (target != revenueInput) revenueInput.value = revenue.toFixed(5);

            let percent = (revenue * 100) / costNet;
            if (target != revenuePercentInput) revenuePercentInput.value = percent.toFixed(5);
        }
    }

    $(netInput).on("change", event => {
       setPrices(event);
    })

    $(grossInput).on("change", event => {
        let price = event.currentTarget.value;
        let netPrice = price / (ivaRate + 1);
        netInput.value = netPrice.toFixed(5);
        setPrices(event);
    });   

    if (revenuePercentInput) {
        $(revenuePercentInput).on("change", event => {
            let costNet = parseFloat(costNetInput.value) || 0;
            let percent = (event.currentTarget.value/100) + 1;
            let priceNet = costNet * percent;
            netInput.value = priceNet.toFixed(5);
            setPrices(event);
        });   
    }

    if (revenueInput) {
        $(revenueInput).on("change", event => {
            let costNet = parseFloat(costNetInput.value) || 0;
            let revenue = parseFloat(event.currentTarget.value);
            let priceNet = costNet + revenue;
            netInput.value = priceNet.toFixed(5);
            setPrices(event);
        });   
    }
}


formsetCallbackAdd = row => {
    initSelect2(row)
    initTouchspin(row)
    let net = row[0].querySelector('[id$=-amount]');
    let gross = row[0].querySelector('[id$=-gross_amount]');
    let percent = row[0].querySelector('[id$=-percent_revenue]');
    let revenue = row[0].querySelector('[id$=-revenue]')
    addIvaEvents(net, gross, percent, revenue)
}

const initTaxes = () => {
    $(document.getElementById('id_taxes')).on("select2:select", event => {
        const {id, type, fee} = event.params.data;
        selectedTaxes.push({id, type, fee})
    });

    $(document.getElementById('id_taxes')).on("select2:unselect", event => {
        const {id} = event.params.data;
        selectedTaxes = selectedTaxes.filter(tax => tax.id != id);
    });
}

const productForm = () => {
    const costNet = document.getElementById("id_cost_price");
    const costGross = document.getElementById("id_cost_price_gross");

    let nets = document.querySelectorAll('[id$=-amount]');
    let grosses = document.querySelectorAll('[id$=-gross_amount]');
    let percents = document.querySelectorAll('[id$=-percent_revenue]');
    let revenues = document.querySelectorAll('[id$=-revenue]');

    nets.forEach((net, index) => {
        if (!net.id.includes("__prefix__")) {
            let gross = grosses[index];
            let percent = percents[index]
            let revenue = revenues[index]
            addIvaEvents(net, gross, percent, revenue);
        }
    });

    addIvaEvents(costNet, costGross);
    initTaxes();
}  

document.addEventListener("DOMContentLoaded", () => {
    productForm();
});