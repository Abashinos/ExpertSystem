

$('.field-button').on('click', function(e){
    var input = $(this).parents('.input-group').find('input')[0];
    var token = $('#csrf-token-form').find('input[name="csrfmiddlewaretoken"]').val();

    $.ajax({
        'url': '/profile/update_field',
        'type': 'POST',
        'data': {
            'field': $(input).attr('name'),
            'value': $(input).val(),
            'csrfmiddlewaretoken': token
        },
        success: function(data) {
            if (data.status == 'ok') {
                toastr.success('Ваши данные обновлены', 'Успех')
            }
            else {
                toastr.error(data.msg, 'Ошибка')
            }
        }
    });
});