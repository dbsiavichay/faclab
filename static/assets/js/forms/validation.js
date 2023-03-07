const check_groups = function (form) {
    const groups = form.querySelectorAll(".input-group");
    groups.forEach(group => {
        const input = group.querySelector("input, select, textarea");
        const was_validated = input.closest(".was-validated")
        if ((!input.checkValidity() && was_validated) || input.classList.contains("is-invalid")) {
            group.nextElementSibling.classList.add("d-block")
        }
    });
}


document.addEventListener("DOMContentLoaded", () => {  
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const form = document.querySelector("#main-form");
    const errors = JSON.parse(form.dataset.errors);
    if (Object.keys(errors).length) {
        toastr.error("Existen errores por corregir.", "Error");
    }
    // Loop over them and prevent submission
    form.addEventListener("submit", event => {
        if (form.checkValidity() === false) {
            event.preventDefault();
            event.stopPropagation();
            toastr.error("Existen errores por corregir.", "Error");
        }
        form.classList.add("was-validated");
        check_groups(form);
    });

    document.querySelectorAll(".is-invalid").forEach(input => {
        input.addEventListener("change", () => {
            if(input.checkValidity()) {
                input.classList.remove("is-invalid");
            }
        });
    })

    document.querySelectorAll(".custom-file-input").forEach(input => {
        input.addEventListener("change", () => {
            if(input.checkValidity()) {
                let group = input.closest(".input-group");
                group.nextElementSibling.classList.remove("d-block")
            }
        });
    })

    const formsets = document.querySelectorAll(".inline-group");
    formsets.forEach(formset => {
        const errors = JSON.parse(formset.dataset.errors)
        const min_forms = formset.querySelector("[name$=MIN_NUM_FORMS]").value
        if (errors.length && parseInt(min_forms)) {
            toastr.error("Debe ingresar al menos un registro.", formset.dataset.label);
        }
    });
    check_groups(form);
});

