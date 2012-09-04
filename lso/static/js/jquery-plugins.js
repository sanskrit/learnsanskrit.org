/**
 * Basic spotlight
 */

$.fn.spotlightOn = function(duration, easing, callback) {
    var $this = $(this),
        $spotlight = $('#spotlight');
    if (!$spotlight.length) {
        $spotlight = $('<div id="spotlight" />').appendTo('body');
    }

    $this.addClass('spotlighted')
    $spotlight.fadeIn(duration, easing, callback);
    return this;
};

$.fn.spotlightOff = function(duration, easing, callback) {
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
    $this.spotlightOn(duration, easing, function() {
        $(window, $this).one('click', function() {
            $this.spotlightOff(duration, easing);
        });
    });
    return this;
};

$.fn.tabs = function() {
    var $this = $(this),
        $panes = $('> section, > div', $this).hide(),
        $tabs = $('ul.tab-links li', $this);

    // If the list of tabs is not defined, cerate a new list by inspecting
    // panes and their headers.
    if (!$tabs.length) {
        $links = $('<ul class="tab-links" />');
        $panes.each(function() {
            var $pane = $(this),
                id = $pane.attr('id'),
                text = $(':header', $pane).first().hide().text(),
                $li = $('<li><a href="#' + id + '">' + text + '</a></li>');
                $li.appendTo($links);
        });
        $links.prependTo($this);
        $tabs = $('li', $links);
    }

    $panes.first().show();
    $tabs.first().addClass('active');

    $links.on('click', 'a', function(e) {
        e.preventDefault();
        var id = this.hash;
        $tabs.removeClass('active');
        $(this).closest('li').addClass('active');

        $.when($panes.fadeOut(200)).then(function() {
            $(id).fadeIn(200);
        });
    });
    return this;
};
