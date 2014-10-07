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

var ajax_query = function(){
    $.ajax({
        data: $('.search-form').serialize(),
        type: 'get',
        url: '/search/',
        success: function(response) {
            $('.results-list').html(response);
            fadeOpacity();
            $('.result-item').on("click tap", function(){
                swap_content($(this));
                console.log("test")
            });
        }
    });
};

var swap_content = function($elem) {
    if($elem.data("expanded")==1) {
        $elem.html($elem.data('old_html'));
        $elem.css("opacity", $elem.data("opacity"));  // restore original opacity
        $elem.data("expanded",0);
    } else {
        $elem.data('old_html', $elem.html());
        // Store the current opacity and make the result opaque
        $elem.data("opacity", $elem.css("opacity"));
        $elem.css("opacity", "1");

        $elem.data("expanded",1);
        
        ajax_detail($elem);
    }
}

var ajax_detail = function($elem) {
    $id = $elem.attr("id")
    $.ajax({
        type: 'get',
        url: '/info/'+$id,
        success: function(response) {
            $elem.html(response);
        }
    });
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
