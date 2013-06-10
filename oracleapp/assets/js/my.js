{% load url from future %} {# required for django-1.5 forwards-compatibility #}

$(document).ready(function() {
    var form = $('#search-form')[0];
    if (form.attachEvent) {
        form.attachEvent("submit", processForm);
    } else {
        form.addEventListener("submit", processForm);
    }
});

function processForm(e) {
    if (e.preventDefault) e.preventDefault();

    $.ajax({
        data: $(this).serialize(),
        type: 'get',
        url: '{% url "search" %}',
        success: function(response) {
            $('.search-results').html(response);
        }
    });

    return false;
}