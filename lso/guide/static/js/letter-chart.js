(function($) {
    var clearTD = function($container) {
        $('td', $container).removeClass('hover-row hover-col');
    };

    $.fn.tableHover = function() {
        $(this).on('mouseover mouseout', 'td, th', function(e) {
            var $cell = $(this),
                $table = $cell.closest('table');

            if (e.type == 'mouseover') {
                var cellIndex = $cell.index(),
                    counter = -1, // exclusive limit
                    diff = 0,
                    $row = $cell.closest('tr'),
                    $point = null,
                    $points = $('thead th', $table);

                clearTD($table);
                $('td', $row).addClass('hover-row');

                // Find corresponding <th>
                $points.each(function() {
                    $point = $(this);
                    diff = parseInt($point.attr('colspan')) || 1;
                    if (counter + diff >= cellIndex) {
                        return false; // break
                    } else {
                        counter += diff;
                    }
                });

                // Find all "children" of <th>
                $('td', $table).each(function() {
                    var $td = $(this),
                        tdIndex = $td.index();
                    if (tdIndex > counter && tdIndex <= counter + diff) {
                        $td.addClass('hover-col');
                    }
                });
            } else {
                if ($(e.currentTarget).closest('table')[0] !== $table[0]) {
                    clearTD($table);
                }
            }
        }).on('mouseleave', function(e) {
            clearTD($(this));
        });
    }
}(window.jQuery));

$(function() {
    $('table.letter-chart').tableHover();
});
