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

    // hide submit button if browser has javascript support and can react to onchange event
    $('#language_selector_form').change(function() { this.submit(); });
    $('#language_selector_form input').hide();

});