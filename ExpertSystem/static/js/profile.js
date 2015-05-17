

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


var deleteHistory = $('.delete-history');

var optionsRemoveHistory = {
    'title': "Удалить запись?",
    'singletone': true,
    'popout': true,
    'btnOkLabel': "Да",
    'btnCancelLabel': "Нет"
};
deleteHistory.confirmation(optionsRemoveHistory);

deleteHistory.on('click', function(){
    var history_id = $(this).data('id');
    $.get('/delete_history/' + history_id, function() {})
        .done(function(data) {
            if ('OK' in data) {
                $("#history" + history_id).remove();
                toastr.success('Запись удалена', 'Успех!');
            }
            else {
                toastr.error('Не удалось удалить запись', 'Потрачено!');
            }
        })
        .fail(function(data) {
            toastr.error('Что-то пошло не так', 'Entschuldigung!');
        })
});