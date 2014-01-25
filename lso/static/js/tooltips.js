/**
 * An extremely lightweight tooltip plugin.
 */
$.tooltips = function(selector, scope) {
    // Bind to titled elements if no selector provided
    selector = selector || '[title]';
    // Bind to page if no scope provided
    scope = scope || 'body';
    // Offset from cursor
    var offset = 5;

    $(scope).on({
        mouseover: function() {
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
                .show();
            $this.data('tooltip', $tt);
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
            $(this).data('tooltip').hide().remove();
        }
    }, selector);
};
