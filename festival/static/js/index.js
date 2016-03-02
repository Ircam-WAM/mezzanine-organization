$(function() {
    // Masonry
    var $grid = $('.artist__list');

    $grid.imagesLoaded( function(){
        $grid.masonry({
          itemSelector: '.artist__item',
          percentPosition: true,
          columnWidth: '.artist__sizer'
        });
    });
});