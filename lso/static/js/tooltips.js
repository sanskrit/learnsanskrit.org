/**
 * An extremely lightweight tooltip plugin.
 */
$.tooltips = function(selector, scope) {
    // Bind to titled elements if no selector provided
    selector = selector || '[title]';
    // Bind to page if no scope provided
    scope = scope || 'body';
    // Speed for fading in and out
    var fadeSpeed = 100,
    // Offset from cursor
        offset = 5;

    $(scope).on({
        mouseover: function() {
            console.log('over');
            var $this = $(this),
                title = $this.data('title');

            // Remove `title` so that the browser doesn't create its own
            // tooltip, but keep the attribute itself so that it will still
            // match e.g. a [title] selector.
            if (!title) {
                title = $this.attr('title');
                $this.data('title', title);
                $this.attr('title', '');
            }

            // Each matched element has access to its own tooltip. This
            // provides reasonable behavior in the (rare) case that two
            // tooltips are active at once.
            var $tt = $('<div class="tt" />').html(title)
                .hide()
                .appendTo('body')
                .fadeIn(fadeSpeed);
            $this.data('tooltip', $tt);
            console.log($tt);
        },
        mousemove: function(e) {
            var $tt = $(this).data('tooltip'),
                el = $tt[0],
                rect = el.getBoundingClientRect();

            var top = e.pageY + offset,
                left = e.pageX + offset;

            var xOverlap = left + rect.width - $(window).width();
            var yOverlap = top + rect.height - $(window).height();
            if (xOverlap > 0) {
                left = e.pageX - rect.width - offset;
            }
            if (yOverlap > 0) {
                top = e.pageY - rect.height - offset;
            }

            $tt.css({ top: top, left: left });
        },
        mouseout: function() {
            $(this).data('tooltip').fadeOut(fadeSpeed, function() {
                // $(this).remove();
            });
        }
    }, selector);
};