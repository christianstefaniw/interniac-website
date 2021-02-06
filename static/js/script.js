(function($) {
  $.fn.visible = function(partial) {

      var $t            = $(this),
          $w            = $(window),
          viewTop       = $w.scrollTop(),
          viewBottom    = viewTop + $w.height(),
          _top          = $t.offset().top,
          _bottom       = _top + $t.height(),
          compareTop    = partial === true ? _bottom : _top,
          compareBottom = partial === true ? _top : _bottom;

    return ((compareBottom <= viewBottom) && (compareTop >= viewTop));

  };

})(jQuery);

var win = $(window);

var allSlideUp = $(".slider-up");
var allSlidesRight = $(".slider-right")

win.scroll(function(event) {

  allSlideUp.each(function(i, el) {
    var el = $(el);
    if (el.visible(true)) {
      el.addClass("slide-up");
    }
  });

  allSlidesRight.each(function(i, el) {
    var el = $(el);
    if (el.visible(true)) {

      el.addClass("slide-right");
    }
  });

});

