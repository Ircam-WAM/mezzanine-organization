$(function() {

    /**
     * Masonry
     * @author Philippe Barbosa
     */
    var $grid = $('.msry__container');
    $grid.imagesLoaded(function() {
        $grid.masonry({
            itemSelector: '.msry__item',
            percentPosition: true,
            columnWidth: '.msry__sizer'
        });
        $grid.addClass('is-ready');
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

        rtl: false,
        adaptiveHeight: false,

        vertical: false,
        verticalHeight: 500,
        vThumbWidth: 100,

        thumbItem: 10,
        pager: true,
        gallery: false,
        galleryMargin: 5,
        thumbMargin: 5,
        currentPagerPosition: 'middle',

        enableTouch: true,
        enableDrag: false,
        freeMove: false,
        swipeThreshold: 40,

        responsive: [],

        onBeforeStart: function(el) {},
        onSliderLoad: function(el) {
            $(".hero__slider").addClass('is-ready');
        },
        onBeforeSlide: function(el) {},
        onAfterSlide: function(el) {
            // el.find('.container').fadeIn();
        },
        onBeforeNextSlide: function(el) {},
        onBeforePrevSlide: function(el) {}
    });

    /**
     * Close message
     */

    var notification = $('#js-notificationContainer');

    $('.js-notificationClose').on('click', function(event) {
        notification.addClass('notification__remove');

        setTimeout(function() {
            notification.remove();
        }, 4000);
    });

    /**
     * Instafeed
     * @author Philippe Barbosa
     */

    var t = new Instafeed({
        get: 'tagged',
        tagName: 'manifeste16',
        userId: 1343260619,
        accessToken: "2985811.467ede5.2d850141659d4a5fab04f28187e580cd",
        sortBy: "most-recent",
        limit: 8,
        template: '<div class="box-item-25"> <a href="{{link}}" target="_blank"> <img src="{{image}}" alt="{{caption}}"></a></div>',
        error: function() {
            $(".instagram").remove()
        }
    });

    $("#instafeed").length && t.run();

    /**
     * Tabs
     */

   var zeTab = $('#tabs');

   if (zeTab.length) {
    var myTabs = tabs({
        el: '#tabs',
        tabNavigationLinks: '.c-tabs-nav__link',
        tabContentContainers: '.c-tab'
    });

    myTabs.init();
   }


    /**
     * Audio player
     */

     if ($('#audio').length) {
        function init_player() {
            var audio;
            var playlist;
            var tracks;
            var current;

            current = 0;
            audio = $('#audio');
            playlist = $('#playlist');
            tracks = playlist.find('li a');
            len = tracks.length - 1;
            audio[0].volume = .90;
            //    audio[0].play();
            playlist.find('a').click(function(e) {
                e.preventDefault();
                link = $(this);
                current = link.parent().index();
                run_player(link, audio[0]);
                linkTitle = link.text();
                $('.audio__title').html(linkTitle);
            });
            audio[0].addEventListener('ended', function(e) {
                current++;
                if (current == len) {
                    current = 0;
                    link = playlist.find('a')[0];
                } else {
                    link = playlist.find('a')[current];
                }
                run_player($(link), audio[0]);
            });
        }

        function run_player(link, player) {
            $(player).find('#primarysrc').attr('src', link.attr('href'));
            $(player).find('#secondarysrc').attr('src', link.attr('data-altsrc'));
            par = link.parent();
            par.addClass('active').siblings().removeClass('active');
            player.load();
            player.play();
        }

        init_player();
     }




});
