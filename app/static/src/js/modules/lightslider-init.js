var LightSliderInit = function() {

    //
    // Init
    //
    this.init();

};

LightSliderInit.prototype.init = function() {

    var that = this;

    $('[data-slider-page]').lightSlider({
        autoWidth: true,
        item: 4,
        pager: false,
        responsive: [
            {
                breakpoint: 752,
                settings: {
                    autoWidth: false,
                    item: 1
                }
            }
        ]
    });

};

module.exports = LightSliderInit;
