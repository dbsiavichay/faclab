const initTouchspin = function (selector) {
  let elem = selector ? $(selector) : $(document)

  elem.find(".touchspin-price").TouchSpin({
    buttondown_class: "btn btn-primary",
    buttonup_class: "btn btn-primary",
    max: 9000000000,
    step: 0.01,
    decimals: 5,
    prefix: "$"
  });

  elem.find(".touchspin-percent").TouchSpin({
    buttondown_class: "btn btn-primary",
    buttonup_class: "btn btn-primary",
    max: 100,
    step: 0.01,
    decimals: 2,
    postfix: "%"
  });

  elem.find(".touchspin").TouchSpin({
    buttondown_class: "btn btn-primary",
    buttonup_class: "btn btn-primary",
    max: 9000000000
  });
}


document.addEventListener("DOMContentLoaded", function () {
  initTouchspin();
});
