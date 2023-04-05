const renderFormset = (prefix, addText = "Añadir Nuevo Item", additionalFunction = () => {}) => {
  $(`.inline.${prefix}`).formset({
    prefix: prefix,
    addText: `<i class="bx bx-plus"></i> ${addText}`,
    addCssClass: "btn btn-success add-row",
    deleteCssClass: "btn btn-icon btn-danger rounded-circle delete-row",
    deleteText: "<i class=\"bx bx-x\"></i>",
    added: function ($row) {
      additionalFunction($row)
    }
  })
}


document.addEventListener('DOMContentLoaded', () => {
  const formsets = document.querySelectorAll('.inline-group');
  for (let i=0;i<formsets.length;i++){
    const prefix = formsets[i].dataset.prefix
    renderFormset(prefix, 'Agregar elemento', initSelect2)
  }
});