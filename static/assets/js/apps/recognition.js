const process_ocr = document.getElementById("process_ocr")
process_ocr.addEventListener("click", async ev => {
  ev.preventDefault()
  await get_data_ocr()
})

const process_formset = (key, data) => {
  const total_forms = document.getElementById(key+"_set-TOTAL_FORMS").value;
  const forms_to_create = data.length - parseInt(total_forms) + 1
  if (forms_to_create > 0){
    addBtn = document.getElementById("actors").querySelector(".add-row")
    for (let i=0;i<forms_to_create;i++){
      addBtn.click();
    }
  }

  for (let i = 0; i< data.length; i++){
    taxpayer = data[i]
    const sel = document.getElementById("id_actor_set-"+i+"-taxpayer")
    let text = "business_name" in taxpayer?taxpayer.business_name:taxpayer.last_name +" "+ taxpayer.name
    let option = new Option(text, taxpayer.id, false, false);
    $(sel).append(option);
    $(sel).val(taxpayer.id)
    $(sel).trigger('change');
  }

}

const get_data_ocr = async (url = "/get-ocr-data/") => {
  const form = document.getElementsByTagName("form")[0]
  const form_data = new FormData(form)
  let response = await fetch(url, {
    method: "POST",
    body: form_data,
    credentials: 'include',
  })
  console.log(response)
  let data = await response.json()
  console.log(data)
  for (const key in data) {
    try{
      let el = document.getElementById(key)
      let res = data[key]
      if (Array.isArray(res)) {
        process_formset(key, res)
      }else{
        el.value = res
      }
    } catch (error) {
      console.log(error)
    }
  }
  $.unblockUI()
}

// Block page
$('.block-page').on('click', function () {
  $.blockUI({
    message: '<p class="font-medium-3"><span class="bx bx-revision icon-spin text-left"></span>&nbsp; Procesando ...</p>',
    overlayCSS: {
      backgroundColor: '#000',
      opacity: 0.3,
      cursor: 'wait'
    },
    css: {
      border: 0,
      padding: 0,
      backgroundColor: 'transparent'
    }
  });
});
