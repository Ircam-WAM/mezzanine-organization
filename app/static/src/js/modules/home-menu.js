var HomeMenu = function() {

    //
    // Init
    //
    this.init();

};

HomeMenu.prototype.init = function() {

    var that = this,
        $elements = $('.home__menu a');

    $elements.hover(function() {
        $elements.removeClass('active');
        $(this).addClass('active');
    }, function() {
        $elements.removeClass('active');
        $($elements.get(0)).addClass('active');
    });

};

module.exports = HomeMenu;
