$(function() {

    /**
     * Masonry
     * @author Philippe Barbosa
     */
    var $grid = $('.msry__container');
    $grid.imagesLoaded( function(){
        $grid.masonry({
          itemSelector: '.msry__item',
          percentPosition: true,
          columnWidth: '.msry__sizer'
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

    /**
     * Lightslider
     */
    $("#lightSlider").lightSlider({
        item: 1,
        autoWidth: false,
        slideMove: 1, // slidemove will be 1 if loop is true
        slideMargin: 10,

        addClass: '',
        mode: "fade",
        useCSS: true,
        cssEasing: 'ease', //'cubic-bezier(0.25, 0, 0.25, 1)',//
        easing: 'linear', //'for jquery animation',////

        speed: 800, //ms'
        auto: true,
        loop: true,
        slideEndAnimation: true,
        pause: 8000,

        keyPress: true,
        controls: true,
        prevHtml: '',
        nextHtml: '',

        rtl:false,
        adaptiveHeight:false,

        vertical:false,
        verticalHeight:500,
        vThumbWidth:100,

        thumbItem:10,
        pager: true,
        gallery: false,
        galleryMargin: 5,
        thumbMargin: 5,
        currentPagerPosition: 'middle',

        enableTouch:true,
        enableDrag:false,
        freeMove:false,
        swipeThreshold: 40,

        responsive : [],

        onBeforeStart: function (el) {},
        onSliderLoad: function (el) {},
        onBeforeSlide: function (el) {},
        onAfterSlide: function (el) {
            // el.find('.container').fadeIn();
        },
        onBeforeNextSlide: function (el) {},
        onBeforePrevSlide: function (el) {}
    });

    /**
     * Close message
     */

     var notification = $('#js-notificationContainer');

     $('.js-notificationClose').on('click', function(event) {
        notification.addClass('notification__remove');

        setTimeout(function () {
            notification.remove();
        }, 4000);
     });

    /**
     * Instafeed
     * @author Philippe Barbosa
     */

    // Ircam user ID : 1343260619
    // Client ID eeed5acba6ce490798253ce5c09a1852
    // Client secret ef3f37ce39c54db1b5145de40fb56c68

    var t = new Instafeed({
        get: "user",
        userId: 1343260619,
        accessToken: "2985811.467ede5.2d850141659d4a5fab04f28187e580cd",
        resolution: "standard_resolution",
        sortBy: "most-recent",
        limit: 8,
        template: '<div class="box-item-25"> <a href="{{link}}" target="_blank"> <img src="{{image}}" alt="{{caption}}"></a></div>',
        error: function() {
            $(".instagram").remove()
        }
    });

    $("#instafeed").length && t.run();

    /**
     *
     */

     var myTabs = tabs({
        el: '#tabs',
        tabNavigationLinks: '.c-tabs-nav__link',
        tabContentContainers: '.c-tab'
     });

     myTabs.init();

});