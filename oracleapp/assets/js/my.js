{% load url from future %} {# required for django-1.5 forwards-compatibility #}

$(document).ready(function() {
    $('.form').submit(function() { // catch the form's submit event
        $.ajax({ // create an AJAX call...
            data: $(this).serialize(), // get the form data
            type: $(this).attr('GET'), // GET or POST
            url: $(this).attr({% url 'search' %}), // the file to call
            success: function(response) { // on success..
                alert(response);
                // $('#DIV_CONTAINING_FORM').html(response);
            }
        });
        return false;
    });
});