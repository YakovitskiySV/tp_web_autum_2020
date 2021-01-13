
$('.js-vote').click(function(event) {
    event.preventDefault();
    var $this = $(this),
        action = $this.data('action'),
        qpk = $this.data('qpk');
        $.ajax('/voteQuestion/', {
        method: 'POST',
        data: {
            action: action,
            qpk: qpk
        },
        dataType: 'json',
        success: function(response) {
            if (action === 'up-vote') {
                like_counter = $this.next().next()
                like_counter.text(response.rating)
            } else if (action === 'down-vote') {
                like_counter = $this.next()
                like_counter.text(response.rating)
            }
        }
    }) .done(function(data) {
    });
});

$('.js-answer-vote').click(function(event) {
    event.preventDefault();
    var $this = $(this),
        action = $this.data('action'),
        apk = $this.data('apk');
        $.ajax('/voteAnswer/', {
        method: 'POST',
        data: {
            action: action,
            apk: apk
        },
        dataType: 'json',
        success: function(response) {
            if (action === 'up-vote') {
                like_counter = $this.next().next()
                like_counter.text(response.rating)
            } else if (action === 'down-vote') {
                like_counter = $this.next()
                like_counter.text(response.rating)
            }
        }
    }) .done(function(data) {
    });
});

$('.js-set-right').click(function(event) {
    event.preventDefault();
    var $this = $(this),
    apk = $this.data('apk');
    $.ajax('/setRight/', {
        method: 'POST',
        data: {
            apk: apk,
        },
        dataType: 'json',
        success: function(response) {
            $('#checkbox' + apk).prop("checked", response.checked);
            console.log(response.checked);
        },
        error: function(response) {
            alert(response.responseJSON.error);
            console.log(response.responseJSON.error);
        }
    })
});