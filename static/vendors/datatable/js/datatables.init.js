// List datatables js //

document.addEventListener("DOMContentLoaded", function () {
    const table = document.querySelector(".list-datatable")
    if (table) {
        const datatable = initDatatable(table);
        appendActions(datatable);
        checkboxes();
    }
});

const initDatatable = function (table) {
    let dataListView = $(table).DataTable({
        paging: false,
        ordering: false,
        searching: false,
        
        columnDefs: [
            {
            targets: 0,
            className: "control"
            },
            {
            orderable: true,
            targets: 1,
            checkboxes: { selectRow: true }
            },
            {
            targets: [0, 1],
            orderable: false
            },
        ],
        order: [2, 'asc'],
        /*
        dom:
            '<"top d-flex flex-wrap"<"action-filters flex-grow-1"f><"actions action-btns d-flex align-items-center">><"clear">rt<"bottom"p>',*/
        dom:
            '<"top d-flex flex-wrap"<"dt-search flex-grow-1"f><"dt-actions d-flex align-items-center">><"clear">rt<"table-footer">',
        select: {
            style: "multi",
            selector: "td:first-child",
            items: "row"
        },
        
        responsive: {
            details: {
            type: "column",
            target: 0
            }
        }
    });
    return dataListView
}

const appendActions = function(datatable) {
    // To append actions dropdown inside action-btn div
    let search_box = $(".table-search")
    let filter_box = $(".table-filter");
    let actions_box = $(".table-actions");
    let columns_box = $(".table-columns");
    $(".dt-search").append(search_box);
    $(".dt-actions").append(filter_box, actions_box, columns_box);

    const listActions = document.querySelectorAll(".list-action");
    for (let i=0; i<listActions.length; i++) {
        listActions[i].addEventListener("click", function (e) {
            let action = this.dataset.action
            let checkboxes = document.querySelectorAll("td.dt-checkboxes-cell input[type=checkbox]:checked");
            if (checkboxes.length) {
                $(`#mass-${action}-modal`).modal("show");
            }else{
                toastr.info("Debe seleccionar al menos un elemento para realizar esta acción.", "Información")
            }
        });
    }

    const get_data = async (app, model, field) => {
        const url = `/insoles/forms/${app}/${model}/${field}/`
        let response = await fetch(url)
        return response.json()
    }

    const fetch_field = document.querySelector('#id_fetch_field');
    fetch_field.addEventListener('change', async event => {
        let modal = event.currentTarget.closest(".modal");
        let app_name = modal.dataset.app;
        let model_name = modal.dataset.model;
        let form = modal.querySelector('.form');
        if (form.childElementCount > 2) {
            form.lastElementChild.remove();
        }
        data = await get_data(app_name, model_name, event.currentTarget.value)
        form.insertAdjacentHTML('beforeend', data.template);
        initSelect2(form);
    });

    const mass_update_btn = document.querySelector('#mass-update-btn');
    mass_update_btn.addEventListener('click', async event => {
        let ids = []
        let modal = event.currentTarget.closest('.modal');
        let url = modal.dataset.url;
        let field = document.querySelector('#id_fetch_field').value
        let value = modal.querySelector('.form').lastElementChild.querySelector('.form-control').value;
        let token = modal.querySelector('input[name=csrfmiddlewaretoken]').value;
        let checkboxes = document.querySelectorAll("td.dt-checkboxes-cell input[type=checkbox]:checked");
        checkboxes.forEach(checkbox => {
            ids.push(checkbox.closest('tr').dataset.id)
        });

        let form_data = new FormData()
        ids.forEach(id => {
            form_data.append('ids', id);
        });
        form_data.append('value', value);
        form_data.append('field', field)
        form_data.append('csrfmiddlewaretoken', token);
        
        try {
            let res = await save(url, form_data)
            location.reload();
        } catch (error) {
            console.log(error)
        }


    });

    const save = async (url, form_data) => {
        let response = await fetch(url, {
          method: "POST",
          body: form_data,
          credentials: 'include',
        })
        return response.json();
      }



    let searchInput = document.querySelector("input[type=search]");
    let url = new URL(window.location.href)
    searchInput.value = url.searchParams.get("search");
    searchInput.addEventListener("keypress", function (e) {
        if (e.keyCode == 13) {
            url.search = "";
            url.searchParams.set("search", this.value)
            window.location.search = url.search
        }
    });


    let columns = document.querySelectorAll('.dropdown-menu .data-columns a');
    columns.forEach(link => {
        link.addEventListener('click', event => {
            event.preventDefault();
            event.stopPropagation();
            
            let target = event.currentTarget;
            let input = target.querySelector('input');
            input.checked = !input.checked;
            datatable.column(target.dataset.column).visible(input.checked)    
        }) 
    });


    const results = document.querySelector('.table-results');
    const pagination = document.querySelector('.pagination')
    document.querySelector('.table-footer').append(results, pagination || '')

    const paginator = document.querySelector('#id_paginate_by');
    if (paginator) {
        let paginate_by = url.searchParams.get('paginate_by')
        paginator.value = paginate_by || '10';
        paginator.addEventListener('change', event => {
            paginate_by = this.event.currentTarget.value
            let search = url.searchParams.get('search');
            url.search = '';
            if (search) {
                url.searchParams.set('search', search);
            }
            url.searchParams.set('paginate_by', paginate_by);
            window.location.search = url.search
        });
    }
}

const checkboxes = function () {
    // add class in row if checkbox checked
    $(".dt-checkboxes-cell")
        .find("input")
        .on("change", function () {
            var $this = $(this);
            if ($this.is(":checked")) {
                $this.closest("tr").addClass("selected-row-bg");
            } else {
                $this.closest("tr").removeClass("selected-row-bg");
            }
        });
    
    // Select all checkbox
    $(document).on("change", ".dt-checkboxes-select-all input", function () {
        if ($(this).is(":checked")) {
        $(".dt-checkboxes-cell")
            .find("input")
            .prop("checked", this.checked)
            .closest("tr")
            .addClass("selected-row-bg");
        } else {
        $(".dt-checkboxes-cell")
            .find("input")
            .prop("checked", "")
            .closest("tr")
            .removeClass("selected-row-bg");
        }
    });
}
