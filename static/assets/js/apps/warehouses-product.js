const addIvaEvents = (netInput, grossInput, revenuePercentInput=null, revenueInput=null) => {
    const ivaRate = 0.12;
    const costNetInput = document.getElementById("id_cost_price");

    const setPrices = event => {
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

    netInput.addEventListener("keyup", event => {
       setPrices(event);
    })

    grossInput.addEventListener("keyup", event => {
        let price = event.currentTarget.value;
        let netPrice = price / (ivaRate + 1);
        netInput.value = netPrice.toFixed(5);
        setPrices(event);
    });   

    if (revenuePercentInput) {
        revenuePercentInput.addEventListener("keyup", event => {
            let costNet = parseFloat(costNetInput.value) || 0;
            let percent = (event.currentTarget.value/100) + 1;
            let priceNet = costNet * percent;
            netInput.value = priceNet.toFixed(5);
            setPrices(event);
        });   
    }

    if (revenueInput) {
        revenueInput.addEventListener("keyup", event => {
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
    let net = row[0].querySelector('[id$=-amount]');
    let gross = row[0].querySelector('[id$=-gross_amount]');
    let percent = row[0].querySelector('[id$=-percent_revenue]');
    let revenue = row[0].querySelector('[id$=-revenue]')
    addIvaEvents(net, gross, percent, revenue)
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
}  

document.addEventListener("DOMContentLoaded", () => {
    productForm();
});