$(function() {

    /**
     * Masonry
     * @author Philippe Barbosa
     */
    var $grid = $('.artist__list');
    $grid.imagesLoaded( function(){
        $grid.masonry({
          itemSelector: '.artist__item',
          percentPosition: true,
          columnWidth: '.artist__sizer'
        });
    });

    /**
     * Rsponsive menu
     * @author Philippe Barbosa
     */

    var toggleButton = $('.menu__toggle'),
        navigation = $('.navigation');

        toggleButton.on('click', function(event) {
            event.preventDefault();
            $(this).toggleClass('toggled');
            navigation.slideToggle();
        });
});