const initSelect2 = function (selector) {
  let elem = selector ? $(selector) : $(document)
  elem.find('.django-select2').djangoSelect2({
    dropdownAutoWidth: true,
    width: '100%',
    language: {
    noResults: function () {
      return  `<button class="btn btn-block btn-primary" onClick="select2create(this)">
                  <i class="bx bx-plus"></i>Crear nuevo
              </button>`;
    }
    },
    escapeMarkup: function (markup) {
      return markup;
    }
  });
}


document.addEventListener("DOMContentLoaded", function () {
  setTimeout(function () {
    let selects = document.querySelectorAll('.django-select2')
    if(selects.length){
      $(selects).select2("destroy");
      initSelect2();
    }
  }, 100);
});