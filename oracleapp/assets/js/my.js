var query_num = 0

$(document).ready(function() {
    // focus on search bar & prevent enter from submitting
    $('.search-textarea').focus();
    $('.search-box').keydown(function (e) {
        if (e.which == 13){e.preventDefault();}
    });
    
    $('.search-box').keyup( function(e) {
        if($('.search-textarea').val() != ""){
            get_results()
        } else {
            $('.results-list').empty()
        }
    });
});


var get_results = function(){
    $.ajax({
        data: $('.search-form').serialize()+"&qn="+(query_num+=1),
        type: 'get',
        url: '/search/',
        success: function(response) {
            $('.results-list').html(response);
            fadeOpacity();

            $('.result-item').on("click tap", function(){
                expand($(this));
            });  
        } 
    });
};

var expand = function($elem) {
    if($elem.data("expanded")==1) {
        $elem.html($elem.data('old_html'));
        $elem.css("opacity", $elem.data("opacity"));  // restore original opacity
        $elem.data("expanded",0);
    } else {
        $elem.data('old_html', $elem.html());
        $elem.data("opacity", $elem.css("opacity")); // store current opacity
        $elem.css("opacity", "1");  //  make the result opaque

        $elem.data("expanded",1);
        
        fill_detail($elem);
    }
}

var fill_detail = function($elem) {
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
