/*=========================================================================================
	File Name: input-groups.js
	Description: Input Groups js
	----------------------------------------------------------------------------------------
	Item Name: Frest HTML Admin Template
	Version: 1.0
	Author: PIXINVENT
	Author URL: http://www.themeforest.net/user/pixinvent
==========================================================================================*/

(function (window, document, $) {
  'use strict';
  var $html = $('html');


  $(".touchspin-price").TouchSpin({
    buttondown_class: "btn btn-primary",
    buttonup_class: "btn btn-primary",
    max: 9000000000,
    step: 0.01,
    decimals: 5,
    prefix: "$"
  });

  $(".touchspin-percent").TouchSpin({
    buttondown_class: "btn btn-primary",
    buttonup_class: "btn btn-primary",
    max: 100,
    step: 0.01,
    decimals: 2,
    postfix: "%"
  });

})(window, document, jQuery);
