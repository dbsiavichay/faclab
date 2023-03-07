const select2create = function (btn) {
  const text = btn.closest('ul').id
  const er = /select2-(.+)-results/
  const id = text.match(er)[1]
  const select = document.getElementById(id)
  $(`#${id}`).select2("close")
  render(select.dataset.app, select.dataset.model, id)
}

const get_data = async (app, model) => {
  const url = `/insoles/forms/${app}/${model}/`
  let response = await fetch(url)
  return response.json()
}

const render = async (app, model, element) => {
  try {
    const modal = document.getElementById('insoles')
    let {create_url, template} = await get_data(app, model)
    modal.querySelector('form').action = create_url
    modal.querySelector('form').dataset.element = element
    modal.querySelector('.modal-body').innerHTML = '';
    modal.querySelector('.modal-body').insertAdjacentHTML('beforeend', template);
    check_if_taxpayers(app)
    $(modal).modal('show');
    initSelect2();
  } catch (e) {
    toastr.error('Los sentimos no tienes los permisos para realizar esta acción.', 'No autorizado');
  }
}

const check_if_taxpayers = function (app) {
  let radios = document.querySelectorAll('input[name=person_type]')
  if (radios) {
    for (let i = 0; i < radios.length; i++) {
      radios[i].addEventListener('change', function () {
        if (this.checked) {
          let model = this.value
          render_taxpayers(app, model)
        }
      })
    }
  }
}

const render_taxpayers = async (app, model) => {
  try {
    const modal = document.getElementById('insoles');
    let {create_url, template} = await get_data(app, model)
    modal.querySelector('form').action = create_url;
    template = `<div class="taxpayer-form">${template}</div>`
    let frm = modal.querySelector('.modal-body').querySelector('.taxpayer-form');
    if (frm) frm.remove();
    modal.querySelector('.modal-body').insertAdjacentHTML('beforeend', template);
  } catch (e) {
    toastr.error('Los sentimos no tienes los permisos para realizar esta acción.', 'No autorizado');
  }
}


const save_form = async (url, form_data) => {
  let response = await fetch(url, {
    method: "POST",
    body: form_data,
    credentials: 'include',
  })
  return response.json();
}

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("insoles-form");
  if (form) {
    form.addEventListener("submit", async function (e) {
      e.preventDefault()
      let url = this.action;
      let form_data = new FormData(this);
      let data = await save_form(url, form_data)
      let element = document.getElementById(this.dataset.element)
      let option = new Option(data.text, data.id, false, false);
      option.selected = true
      $(element).append(option);
      $(element).trigger('change');
      const modal = document.getElementById('insoles');
      $(modal).modal('hide');
    });
  }
});
