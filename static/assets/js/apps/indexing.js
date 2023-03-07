const record_form = () => {
  const id_cancelled = document.getElementById("id_cancelled")
  
  if (id_cancelled) {
    const id_cancellation_date = document.getElementById("id_cancellation_date")
    const div_cancellation_date = id_cancellation_date.parentElement.parentElement
    const id_cancellation_notary = document.getElementById("id_cancellation_entity")
    const div_cancellation_entity = id_cancellation_notary.parentElement
    
    div_cancellation_entity.classList.add("hide-animation")
    div_cancellation_date.classList.add("hide-animation")
    
    const change_visibility = () => {
      if (id_cancelled.checked) {
        div_cancellation_date.style.display = ""
        div_cancellation_entity.style.display = ""
      } else {
        div_cancellation_date.style.display = "none"
        div_cancellation_entity.style.display = "none"
      }
    }
    
    window.setTimeout(change_visibility, 100)
    
    id_cancelled.addEventListener("change", ev => {
      change_visibility()
    })
  }
}

const extended_record_list = () => {  
  const fieldsets = [...document.getElementsByTagName("fieldset")]
  fieldsets.map(fieldset => {
    let new_first_child = document.createRange().createContextualFragment(`
      <div class="input-group"></div>
    `).firstElementChild
    
    let button = document.createRange().createContextualFragment(`
        <div class="input-group-append">
            <button class="btn btn-primary date-btn" type="button" id="${fieldset.firstElementChild.name}">
                Hoy
            </button>
        </div>`).firstElementChild;
    fieldset.firstElementChild.insertAdjacentElement("afterend", button)
    
    let children = [...fieldset.children]
    children.map(child => {
      fieldset.removeChild(child)
    })
    
    fieldset.insertAdjacentElement("afterbegin", new_first_child)
    children.map(child => {
      new_first_child.appendChild(child)
    })
  })

  let url = new URL(window.location.href)
  let from_param = document.querySelector('input[name=from_param]');
  let to_param = document.querySelector('input[name=to_param]');
  let user = document.querySelector('select[name=user]');
  from_param.value = url.searchParams.get('from_param')
  to_param.value = url.searchParams.get('to_param')
  user.value = url.searchParams.get('user')



  const date_buttons = [...document.getElementsByClassName("date-btn")]
  date_buttons.map(date_button => {
    date_button.addEventListener("click", event => {
      event.preventDefault()
      let date = new Date()
      let day = ("0" + date.getDate()).slice(-2)
      let string_date = `${day}/${date.getMonth()+1}/${date.getFullYear()}`
      console.log(event.target.id)
      let input = document.getElementsByName(event.target.id)[0]
      input.value = string_date
    })
  })
  
}

document.addEventListener("DOMContentLoaded", () => {
  record_form();
  extended_record_list();
});