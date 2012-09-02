/**
 * Basic spotlight
 */

$.fn.spotlightIn = function(callback) {
    var $this = $(this),
        $spotlight = $('#spotlight');
    if (!$spotlight.length) {
        $spotlight = $('<div id="spotlight" />').appendTo('body');
    }

    $this.addClass('spotlighted')
    $spotlight.fadeIn(callback);
    return this;
};

$.fn.spotlightOut = function(callback) {
    var $this = $(this),
        $spotlight = $('#spotlight');

    $spotlight.fadeOut(function() {
        $this.removeClass('spotlighted');
        if ($.isFunction(callback)) {
            callback();
        }
    });
    return this;
};

$.fn.spotlight = function() {
    var $this = $(this);
    $this.spotlightIn(function() {
        $(window).one('click', function() {
            $this.spotlightOut();
        });
    });
};
