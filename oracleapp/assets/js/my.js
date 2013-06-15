{% load url from future %} {# required for django-1.5 forwards-compatibility #}

$(document).ready(function() {
    $('.search-form').on("submit", processForm);

    var thread = null;
    
    $('.search-box').keyup(function() {
        clearTimeout(thread);
        var $this = $(this); 
        thread = setTimeout(function(){ajax_query()}, 0.25);
    });
});

var processForm = function (e) {
    if (e.preventDefault) e.preventDefault();

    ajax_query();

    return false;
};

var ajax_query = function (){
    $.ajax({
        data: $('.search-form').serialize(),
        type: 'get',
        url: '{% url "search" %}',
        success: function(response) {
            $('.results-list').html(response);
        }
    });
};

/*var overlaps = (function () {
    function getPositions( elem ) {
        var pos, width, height;
        pos = $( elem ).position();
        width = $( elem ).width();
        height = $( elem ).height();
        return [ [ pos.left, pos.left + width ], [ pos.top, pos.top + height ] ];
    }

    function comparePositions( p1, p2 ) {
        var r1, r2;
        r1 = p1[0] < p2[0] ? p1 : p2;
        r2 = p1[0] < p2[0] ? p2 : p1;
        return r1[1] > r2[0] || r1[0] === r2[0];
    }

    return function ( a, b ) {
        var pos1 = getPositions( a ),
            pos2 = getPositions( b );
        return comparePositions( pos1[0], pos2[0] ) && comparePositions( pos1[1], pos2[1] );
    };
})();

var kill_overlaps = function() {
    $spans = $('span');
    for(var i = 0; i < $spans.size(); i++) {
        for(var j = 0; j < $spans.size(); j++) {
            if ($spans[i]!=$spans[j] && overlaps($spans[i], $spans[j])) {
                $($spans[i]).hide()
                $($spans[j]).hide()
                console.log("killed elements "+$($spans[i]).text()+" and "+$($spans[j]).text());
            }
        }
    }
};*/