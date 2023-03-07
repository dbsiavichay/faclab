document.addEventListener("DOMContentLoaded", () => {
    const url = new URL(window.location.href)
    const paginations = document.querySelectorAll(".page-link");

    paginations.forEach(pagination => {
        pagination.addEventListener("click", event => {
            let page = event.target.dataset.page;
            url.searchParams.set("page", page)
            event.target.href = url.search
        })
    })
});