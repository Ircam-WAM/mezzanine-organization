var ProfilSelector = function() {

    this.$element = null;
    this.$elementMobile = null;

    //
    // Init
    //
    this.init();

};

ProfilSelector.prototype.init = function() {

    var that = this;

    that.$element = $('#ProfilSelector');
    that.$element.find('li:first-child a').click(function(e) {

        if ($(this).hasClass('unclickable')) {
            e.preventDefault();
        }
        that.$element.toggleClass('open');
        if(that.$element.hasClass('open')) {
            that.$element.one('mouseleave', function() {
                that.$element.removeClass('open');
            })
        }

    });


    that.$elementMobile = $('#ProfilSelectorMobile');
    that.$elementMobile.find('a').click(function(e) {

        e.preventDefault();
        return false;

    });

};


module.exports = ProfilSelector;
