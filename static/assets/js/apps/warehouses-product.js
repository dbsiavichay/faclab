const product_form = () => {
    const ivaRate = 0.12;
    const costPriceNet = document.getElementById("id_cost_price");
    const costPriceGross = document.getElementById("id_cost_price_gross");
    
    costPriceNet.addEventListener("keyup", event => {
        let price = event.currentTarget.value;
        let price_gross = price * (ivaRate + 1);
        costPriceGross.value = price_gross.toFixed(5)
    })

    costPriceGross.addEventListener("keyup", event => {
        let price = event.currentTarget.value;
        let price_net = price / (ivaRate + 1);
        costPriceNet.value = price_net.toFixed(5)
    });    
}
  

document.addEventListener("DOMContentLoaded", () => {
    product_form();
});