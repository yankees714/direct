{% load url from future %} {# required for django-1.5 forwards-compatibility #}

$(document).ready(function() {
    var form = $('.search-form')[0];
    if (form.attachEvent) {
        form.attachEvent("submit", processForm);
    } else {
        form.addEventListener("submit", processForm);
    }

    var thread = null;
    
    $('.search-box').keyup(function() {
        clearTimeout(thread);
        var $this = $(this); thread = setTimeout(function(){ajax_query()}, 0);
    });
});

function processForm(e) {
    if (e.preventDefault) e.preventDefault();

    ajax_query();

    return false;
}

function ajax_query(){
    $.ajax({
        data: $('.search-form').serialize(),
        type: 'get',
        url: '{% url "search" %}',
        success: function(response) {
            $('.results-list').html(response);
        }
    });
}

