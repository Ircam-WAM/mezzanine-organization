var LightSliderHomeInit = function() {

    //
    // Init
    //
    this.init();

};

LightSliderHomeInit.prototype.init = function() {

    var that = this;

    $('[data-slider-home]').lightSlider({
        item: 1,
        slideMargin: 0,
        pager: false,
        loop: true,
        auto: true,
        pauseOnHover: true,
        pause: 5000,
        onAfterSlide: function(slider) {
            var $pages = slider.find('li.slider-home__slide.lslide');
            $pages.removeClass('active');
            $($pages[slider.getCurrentSlideCount()-1]).addClass('active');
            var $next = $($pages[slider.getCurrentSlideCount()-1]).next('li.slider-home__slide.lslide').find('figure img');
            var $img_src = $next.attr('data-original');
            var $next = $next.attr('src', $img_src);
        },
        onSliderLoad: function(slider) {
            var $pages = slider.parents('.slider-home').find('.slider-home__pager li');
            $pages.each(function(idx) {
                var that = $(this);
                that.click(function(e) {
                    e.preventDefault();
                    $pages.removeClass('active');
                    that.addClass('active');
                    slider.goToSlide(idx+1);
                    return false;
                });

            });
        }
    });

};

module.exports = LightSliderHomeInit;
