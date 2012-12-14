/**
 * An extremely lightweight tooltip plugin.
 */
$.tooltips = function(selector, scope) {
    // Bind to page if no scope provided
    scope = scope || 'body';
    // Bind to titled elements if no selector provided
    selector = selector || '[title]';
    var fadeSpeed = 100;

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
            // toolselector are active at once.
            var $tt = $('<div class="tt" />').html(title)
                .hide()
                .appendTo('body')
                .fadeIn(fadeSpeed);
            $this.data('tooltip', $tt);
        },
        mousemove: function(e) {
            $(this).data('tooltip').css({
                top: e.pageY + 6,
                left: e.pageX + 6
            });
        },
        mouseout: function() {
            $(this).data('tooltip').fadeOut(fadeSpeed, function() {
                $(this).remove();
            });
        }
    }, selector);
};