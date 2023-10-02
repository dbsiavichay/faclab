document.addEventListener('DOMContentLoaded', () => {
    $('.pickadate').pickadate({
        formatSubmit: 'dd/mm/yyyy',
        hiddenName: true,
        today: 'Hoy',
        clear: '',
        close: 'Cerrar'
    });
});