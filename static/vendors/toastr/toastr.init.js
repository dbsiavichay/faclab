/*=========================================================================================
	File Name: toastr.js
	Description: Toastr notifications
	----------------------------------------------------------------------------------------
	Item Name: Frest HTML Admin Template
	Version: 1.0
	Author: Pixinvent
	Author URL: hhttp://www.themeforest.net/user/pixinvent
==========================================================================================*/
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".toastr-message").forEach(item => { 
    let tags = item.dataset.tags;
    let message = item.dataset.message;
    if (tags == "success") {
      toastr.success(message, "Acción satisfactoria");
    }
  });
});