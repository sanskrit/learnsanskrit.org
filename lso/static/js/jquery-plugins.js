/**
 * Pin any matching element when the window is scrolled beyond its
 * starting point.
 */
$.fn.pin = function() {
    var $this = $(this),
        $window = $(window);

    if (!$this.data('y')) {
        var offset = $this.offset();
        $this.data({
            y: offset.top,
            height: $this.height()
        });
    }

    var pinFn = function() {
        var objY = $this.data('y'),
            objHeight = $this.data('h'),
            y = $window.scrollTop();

        if (y > objY) {
            $this.addClass('pinned');
        } else {
            $this.removeClass('pinned');
        }
    };

    pinFn();
    $window.scroll(pinFn);
    return this;
};

/**
 * Transliterate all text in the matched elements.
 */
$.fn.sanscript = function(from, to) {
    this.each(function() {
        var $this = $(this),
            text = $this.html();
        $this.html(Sanscript.t(text, from, to, { skip_sgml: true }));
    });
};

/**
 * Basic spotlight
 */

$.fn.spotlightOn = function(duration, easing, callback) {
    var $this = $(this),
        $spotlight = $('#spotlight');
    if (!$spotlight.length) {
        $spotlight = $('<div id="spotlight" />').appendTo('body');
    }

    $this.addClass('spotlighted');
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
        $links = $('ul.tab-links'),
        $tabs = $('li', $links);

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
        e.stopPropagation();
        var id = this.hash,
            $li = $(this).closest('li'),
            active = 'active';
        if ($li.hasClass(active)) {
            return;
        } else {
            $tabs.removeClass(active);
        }
        $li.addClass(active);

        $.when($panes.fadeOut(200)).then(function() {
            $(id).fadeIn(200);
        });
    });
    return this;
};
