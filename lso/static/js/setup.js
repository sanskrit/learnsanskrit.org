$(function() {
    $('div.tabs').tabs();
    $.cookie.defaults.expires = 365;
    $.cookie.json = true;
    $.tooltips('[title]', 'body');
});

$(document).on('click', 'a[href*="#"]', function(e) {
    e.preventDefault();
    var $this = $(this);
    $('html, body').stop().animate({
        scrollTop: $($this.attr('href')).position().top
    }, 500);
});
