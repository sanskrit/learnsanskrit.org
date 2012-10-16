$(function() {
    $('div.tabs').tabs();
});

$(document).on('click', 'a[href*="#"]', function(e) {
    e.preventDefault();
    var $this = $(this);
    $('html, body').stop().animate({
        scrollTop: $($this.attr('href')).position().top
    }, 500);
});
