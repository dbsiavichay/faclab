$(function () {
    var showDeleteButton = function () {            
        $('#table-delete-select').show();
    }

    var hideDeleteButton = function () {
        $('#table-delete-select').hide();   
    }


    $('#table-all').on('click', function () {
        if ($(this).is(':checked')) {
            $('input[id*=table-row]:not(:checked)').each(function (index, checkbox) {
                $(checkbox).prop('checked', true);                    
            });
            showDeleteButton();
        } else {
            $('input[id*=table-row]:checked').each(function (index, checkbox) {
                $(checkbox).prop('checked', false);
            });
            hideDeleteButton();
        }

    });

    $('[id*=table-row]').on('click', function () {
        var checked_count =  $('[id*=table-row]:checked').length;
        var unchecked_count =  $('[id*=table-row]:not(:checked)').length;
        if (checked_count) {
            showDeleteButton();
            if (!unchecked_count) $('#table-all').prop('checked', true);
        } else {
            hideDeleteButton();
            $('#table-all').prop('checked', false);
        }

    });
});