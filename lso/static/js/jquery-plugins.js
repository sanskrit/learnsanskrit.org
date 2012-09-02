/**
 * Basic spotlight
 */

$.fn.spotlightIn = function(duration, easing, callback) {
    var $this = $(this),
        $spotlight = $('#spotlight');
    if (!$spotlight.length) {
        $spotlight = $('<div id="spotlight" />').appendTo('body');
    }

    $this.addClass('spotlighted')
    $spotlight.fadeIn(duration, easing, callback);
    return this;
};

$.fn.spotlightOut = function(duration, easing, callback) {
    var $this = $(this),
        $spotlight = $('#spotlight');

    $spotlight.fadeOut(duration, easing, function() {
        $this.removeClass('spotlighted');
        var fn = callback || easing || duration;
        if ($.isFunction(fn)) {
            fn();
        }
    });
    return this;
};

$.fn.spotlight = function(duration, easing) {
    var $this = $(this);
    $this.spotlightIn(duration, easing, function() {
        $(window, $this).one('click', function() {
            $this.spotlightOut(duration, easing);
        });
    });
};
