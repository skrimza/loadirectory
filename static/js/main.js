// register user form
$('#register-form').on('submit', function (e) {
    e.preventDefault(); 
    $.ajax({
        data: {
            name: $('#name').val(),
            lastname: $('#lastname').val(),
            email: $('#email').val(),
            password: $("#password").val()
        },
        type: 'POST',
        url: '/router/register',
        success: function (data) {
            var dataString = JSON.parse(data);
            if (dataString.response.error) {
                $('.output').addClass("active");
                $('.output').text(dataString.response.error).show();
                $('#register-form')[0].reset();

            } else if (dataString.response.text) {
                $('.output').addClass("active");
                $('.output').text(dataString.response.text).show();
                $('#register-form')[0].reset();
            }
        setTimeout(function () {
            $('.output').removeClass('active');
        }, 3000);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            // Обработка ошибок AJAX-запроса
            $('.output').text('An error occurred: ' + textStatus).show();
            setTimeout(function () {
                $('.output').removeClass('active').hide();
            }, 3000);
        }
    });
});

// login user form
$('#login-form').on('submit', function (e) {
    e.preventDefault();
    $.ajax({
        data: {
            email: $('#login-email').val(),
            password: $("#login-password").val()
        },
        type: 'POST',
        url: '/router/login',
        success: function (data) {
            var dataString = JSON.parse(data);
            if (dataString.response.message) {
                $('.output').addClass("active")
                $('.output').text(dataString.response.message + ' ' + dataString.response.name).show();
                $('#login-form')[0].reset();
                setTimeout(function () {
                    $('.output').removeClass('active');
                    window.location.href = dataString.redirect;
                }, 3000);
            } else {
                $('.output').addClass("active");
                $('.output').text(dataString.response.error).show();
                setTimeout(function () {
                    $('.output').removeClass('active');
                    $('#login-form')[0].reset();
                }, 3000);
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            // Обработка ошибок AJAX-запроса
            $('.output').text('An error occurred: ' + textStatus).show();
            setTimeout(function () {
                $('.output').removeClass('active').hide();
            }, 3000);
        }
    });
});

// update active icons
function updateActiveIcons() {
    var activeColumn = $('td#active');
    activeColumn.each(function () {
        var value = $(this).data('value');
        if (value === 'True') {
            $(this).html('<img src="../static/images/check.png" alt="Active" style="width: 20px; height: 20px;">');
        } else {
            $(this).html('<img src="../static/images/delete.png" alt="Inactive" style="width: 20px; height: 20px;">');
        }
    });
}
updateActiveIcons();

// add new car form
$(document).on('click', '#work-panel_add-btn', function (e) {
    $('.work-panel_add-cars').addClass("active")
    var timeNow = new Date();
    var datetime = timeNow.getFullYear() + "-"
        + ("0" + (timeNow.getMonth() + 1)).slice(-2) + "-"
        + ("0" + timeNow.getDate()).slice(-2) + "T"
        + ("0" + timeNow.getHours()).slice(-2) + ":"
        + ("0" + timeNow.getMinutes()).slice(-2);
    $('#register_new-car__time').val(datetime);
    $('#register_new-car').on('submit', function (e) {
        e.preventDefault();
        $.ajax({
            data: {
                car_name: $('#register_new-car__name').val(),
                car_number: $("#register_new-car__number").val(),
                load_capacity: $("#register_new-car__weight").val(),
                date_publish: $("#register_new-car__time").val(),
                user_id: $("#register").val(),
            },
            type: 'POST',
            url: '/base/register_car',
            success: function (data) {
                if (data) {
                    $('.output').addClass("active")
                    $('.output').text('Автомобиль успешно добавлен').show();
                    $('#register_new-car')[0].reset();
                    $.ajax({
                        url: '/base/get_updated_cars',
                        data: {
                            register: 'car'
                        },
                        type: 'GET',
                        success: function (response) {
                            $('.work-panel_block').html(response);
                            updateActiveIcons();
                        }
                    });
                    setTimeout(function () {
                        $('.output').removeClass('active');
                        $('.work-panel_add-cars').removeClass('active');
                    }, 3000);
                } else {
                    $('.output').addClass("active");
                    $('.output').text('Проблемы с сохранением, попробуйте позже').show();
                    $('#register_new-car')[0].reset();
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                $('.output').text('An error occurred: ' + textStatus).show();
                setTimeout(function () {
                    $('.output').removeClass('active').hide();
                }, 3000);
            }
        });
    });
});
$('#cancel_new-car_button').on('click', function () {
    $('#register_new-car')[0].reset();
    $('.work-panel_add-cars').removeClass('active');
});

// add new problem form
$(document).on('click', '.work-panel_problem-add', function (e) {
    $('.work-panel_add-problems-block').addClass("active")
    var timeNow = new Date();
    var datetime = timeNow.getFullYear() + "-"
        + ("0" + (timeNow.getMonth() + 1)).slice(-2) + "-"
        + ("0" + timeNow.getDate()).slice(-2) + "T"
        + ("0" + timeNow.getHours()).slice(-2) + ":"
        + ("0" + timeNow.getMinutes()).slice(-2);
    $('#register_new-problem_time').val(datetime);
    $('#update_new-problem_time').val(datetime);
    $('#register_new-problem').on('submit', function (e) {
        e.preventDefault();
        $.ajax({
            data: {
                title: $('#register_new-problem_title').val(),
                description: $("#register_new-problem_description").val(),
                car_id: $("#register_car-number").val(),
                date_start: $("#register_new-problem_time").val(),
                date_finish: $("#update_new-problem_time").val(),
            },
            type: 'POST',
            url: '/base/register_problem',
            success: function (data) {
                if (data) {
                    $('.output').addClass("active")
                    $('.output').text('Проблема успешно добавлена').show();
                    $('#register_new-problem')[0].reset();
                    $.ajax({
                        url: '/base/get_updated_cars', 
                        type: 'GET',
                        success: function (response) {
                            $('.work-panel_block').html(response);
                            updateActiveIcons();
                        }
                    });
                    setTimeout(function () {
                        $('.output').removeClass('active');
                        $('.work-panel_add-problems-block').removeClass('active');
                    }, 3000);
                } else {
                    $('.output').addClass("active");
                    $('.output').text('Проблемы с сохранением, попробуйте позже').show();
                    $('#register_new-problem')[0].reset();
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                $('.output').text('An error occurred: ' + textStatus).show();
                setTimeout(function () {
                    $('.output').removeClass('active').hide();
                }, 3000);
            }
        });
    });
});
$('#cancel_new-problem_button').on('click', function () {
    $('#register_new-problem')[0].reset();
    $('.work-panel_add-problems-block').removeClass('active');
});

// delete car button
$(document).on('click', 'button.delete', function (e) {
    e.preventDefault();
    $('.output-agree').addClass("active");
    var carId = $(this).data('id');
    $('.output-agree_yes').on('click', function () {
        $.ajax({
            data: {
                id: carId,
            },
            type: 'POST',
            url: '/base/delete_car',
            success: function (data) {
                if (data) {
                    $('.output-agree').removeClass('active');
                    $.ajax({
                        url: '/base/get_updated_cars',
                        type: 'GET',
                        success: function (response) {
                            $('.work-panel_block').html(response);
                            updateActiveIcons();
                        }
                    });
                } else {
                    $('.output-agree_problems').text("Возникли непредвиденные проблемы, попробуйте еще раз");
                    setTimeout(function () {
                        $('.output-agree').removeClass('active').hide();
                    }, 2000);
                }
            },
        });
    });
    $('.output-agree_no').on('click', function () {
        $('.output-agree').removeClass('active');
    });
});

// delete problem button
$(document).on('click', 'button.problem-delete', function (e) {
    e.preventDefault();
    $('.output-agree').addClass("active");
    var problemId = $(this).data('id');
    $('.output-agree_yes').on('click', function () {
        $.ajax({
            data: {
                id: problemId,
            },
            type: 'POST',
            url: '/base/delete_problem',
            success: function (data) {
                if (data) {
                    $('.output-agree').removeClass('active');
                    $.ajax({
                        url: '/base/get_updated_cars',
                        type: 'GET',
                        success: function (response) {
                            $('.work-panel_block').html(response);
                            updateActiveIcons();
                        }
                    });
                } else {
                    $('.output-agree_problems').text("Возникли непредвиденные проблемы, попробуйте еще раз");
                    setTimeout(function () {
                        $('.output-agree').removeClass('active').hide();
                    }, 2000);
                }
            },
        });
    });
    $('.output-agree_no').on('click', function () {
        $('.output-agree').removeClass('active');
    });
});


$(document).on('click', '#edit-car_problem', function () {
    var carId = $(this).data('id');
    var timeNow = new Date();
    var datetime = timeNow.getFullYear() + "-"
        + ("0" + (timeNow.getMonth() + 1)).slice(-2) + "-"
        + ("0" + timeNow.getDate()).slice(-2) + "T"
        + ("0" + timeNow.getHours()).slice(-2) + ":"
        + ("0" + timeNow.getMinutes()).slice(-2);
    $('#edit-car_window-reg_time-' + carId).val(datetime);
    $('#update-car_window-reg_time-' + carId).val(datetime);
    $('#edit-car_window-' + carId).addClass("active");
    $('#edit-car_window_form-' + carId).on('submit', function (e) {
        e.preventDefault();
        $.ajax({
            data: {
                car_id: carId,
                description: $("#edit-car_window_description-" + carId).val(),
                date_start: $("#edit-car_window-reg_time-" + carId).val(),
                date_finish: $("#update-car_window-reg_time-" + carId).val(),
            },
            type: 'POST',
            url: '/base/update_car_information',
            success: function (data) {
                if (data) {
                    $('.output').addClass("active")
                    $('.output').text('Проблема успешно добавлена').show();
                    $('#edit-car_window_form-' + carId)[0].reset();
                    $.ajax({
                        url: '/base/get_updated_cars',
                        type: 'GET',
                        success: function (response) {
                            $('.work-panel_block').html(response);
                            updateActiveIcons();
                        }
                    });
                    setTimeout(function () {
                        $('.output').removeClass('active');
                        $('#edit-car_window-' + carId).removeClass("active");
                    }, 3000);
                } else {
                    $('.output').addClass("active");
                    $('.output').text('Проблемы с сохранением, попробуйте позже').show();
                    $('#edit-car_window_form')[0].reset();
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                $('.output').text('An error occurred: ' + textStatus).show();
                setTimeout(function () {
                    $('.output').removeClass('active').hide();
                }, 3000);
            }
        });
    });
    $(document).on('click', '#cancel_edit-car-window_button', function () {
        $('#edit-car_window-' + carId).removeClass("active");
    });
});

$(document).on('click', '#update-problem_button', function () {
    var problemId = $(this).data('id');
    var timeNow = new Date();
    var datetime = timeNow.getFullYear() + "-"
        + ("0" + (timeNow.getMonth() + 1)).slice(-2) + "-"
        + ("0" + timeNow.getDate()).slice(-2) + "T"
        + ("0" + timeNow.getHours()).slice(-2) + ":"
        + ("0" + timeNow.getMinutes()).slice(-2);
    $('#update-problem_first-time-' + problemId).val(datetime);
    $('#update-problem_second-time-' + problemId).val(datetime);
    $('#update-problem-block-' + problemId).addClass("active");
    $('#update-problem_form-' + problemId).on('submit', function (e) {
        e.preventDefault();
        $.ajax({
            data: {
                problem_id: problemId,
                title: $("#update-problem_title-" + problemId).val(),
                car_id: $("#update-problem_car-number-" + problemId).val(),
                description: $("#update-problem_description-" + problemId).val(),
                date_start: $("#update-problem_first-time-" + problemId).val(),
                date_finish: $("#update-problem_second-time-" + problemId).val(),
            },
            type: 'POST',
            url: '/base/update_problem_information',
            success: function (data) {
                if (data) {
                    $('.output').addClass("active")
                    $('.output').text('Проблема успешно обновлена').show();
                    $('#update-problem_form-' + problemId)[0].reset();
                    $.ajax({
                        url: '/base/get_updated_cars',
                        type: 'GET',
                        success: function (response) {
                            $('.work-panel_block').html(response);
                            updateActiveIcons();
                        }
                    });
                    setTimeout(function () {
                        $('.output').removeClass('active');
                        $('#update-problem_form-' + problemId).removeClass("active");
                    }, 3000);
                } else {
                    $('.output').addClass("active");
                    $('.output').text('Проблемы с сохранением, попробуйте позже').show();
                    $('#update-problem_form-' + problemId)[0].reset();
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                $('.output').text('An error occurred: ' + textStatus).show();
                setTimeout(function () {
                    $('.output').removeClass('active').hide();
                }, 3000);
            }
        });
    });
    $(document).on('click', '#cancel_problem_button', function () {
        $('#update-problem-block-' + problemId).removeClass("active");
    });
});

$('#quit_user').on('click', function (e) {
    e.preventDefault();
    $.ajax({
        url: '/router/quit',
        type: 'POST',
        success: function (response) {
            window.location.href = '/router/';
        },
        error: function (xhr, status, error) {
            console.error('Ошибка при выходе:', error);
            alert('Произошла ошибка при выходе. Попробуйте снова.');
        }
    });
});
