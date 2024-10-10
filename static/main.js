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
        url: '/register',
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
        url: '/login',
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
                $('#login-form')[0].reset();
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
$(document).on('click', '.work-panel_add-btn', function (e) {
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
            url: '/register_car',
            success: function (data) {
                if (data) {
                    $('.output').addClass("active")
                    $('.output').text('Автомобиль успешно добавлен').show();
                    $('#register_new-car')[0].reset();
                    $.ajax({
                        url: '/get_updated_cars',
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
            url: '/register_problem',
            success: function (data) {
                if (data) {
                    $('.output').addClass("active")
                    $('.output').text('Проблема успешно добавлена').show();
                    $('#register_new-problem')[0].reset();
                    $.ajax({
                        url: '/get_updated_cars', 
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
            url: '/delete_car',
            success: function (data) {
                if (data) {
                    $('.output-agree').removeClass('active');
                    $.ajax({
                        url: '/get_updated_cars',
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
            url: '/delete_problem',
            success: function (data) {
                if (data) {
                    $('.output-agree').removeClass('active');
                    $.ajax({
                        url: '/get_updated_cars',
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


$(document).on('click', 'button.edit', function (e) {
    var timeNow = new Date();
    var datetime = timeNow.getFullYear() + "-"
        + ("0" + (timeNow.getMonth() + 1)).slice(-2) + "-"
        + ("0" + timeNow.getDate()).slice(-2) + "T"
        + ("0" + timeNow.getHours()).slice(-2) + ":"
        + ("0" + timeNow.getMinutes()).slice(-2);
    $('#edit-car_window-reg_time').val(datetime);
    $('#update-car_window-reg_time').val(datetime);
    var carId = $(this).data('id');
    $('#edit-car_window-' + carId).addClass("active");
    $('#edit-car_window_form' + carId).on('submit', function (e) {
        e.preventDefault();
        $.ajax({
            data: {
                car_id: carId,
                description: $("#edit-car_window_description").val(),
                date_start: $("#edit-car_window-reg_time").val(),
                date_finish: $("#update-car_window-reg_time").val(),
            },
            type: 'POST',
            url: '/update_car_information',
            success: function (data) {
                if (data) {
                    $('.output').addClass("active")
                    $('.output').text('Проблема успешно добавлена').show();
                    $('#edit-car_window_form')[0].reset();
                    $.ajax({
                        url: '/get_updated_cars',
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
    $('#cancel_edit-car-window_button').on('click', function () {
        $('#edit-car_window_form')[0].reset();
        $('#edit-car_window-' + carId).removeClass("active");
    });
});

