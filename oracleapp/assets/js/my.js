{% load url from future %} {# required for django-1.5 forwards-compatibility #}

$(document).ready(function() {
    $('.search-textarea').focus();

    $('.search-form').on("submit", processForm);

    var thread = null;
    
    $('.search-box').keyup(function() {
        clearTimeout(thread);
        var $this = $(this); 
        thread = setTimeout(function(){ajax_query()}, 0);
    });
});

var ajax_query = function (){
    $.ajax({
        data: $('.search-form').serialize(),
        type: 'get',
        url: '{% url "search" %}',
        success: function(response) {
            $('.results-list').html(response);
            fadeOpacity();
            $('.result-item').on("click tap", function(){
                $orig_html = $(this).html();
                $(this).html(ajax_detail($(this).attr("id")));
                $(this).on("click tap", function(){
                    $(this).html($orig_html);
                });
            });
        }
    });
};

var ajax_detail = function (id){
    $.ajax({
        type: 'get',
        url: '/info/'+id,
        success: function(response) {
            $details = response;
        }
    });
    return $details;
};

var fadeOpacity = function(){
    $('li').each(function(){
        var $li = $(this);
        $li.css("opacity", $li.attr("op"));
    });
};

var processForm = function (e) {
    if (e.preventDefault) e.preventDefault();
    return false;
};
