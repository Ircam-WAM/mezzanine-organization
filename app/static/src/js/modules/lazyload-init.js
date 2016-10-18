var LazyLoadInit = function() {

    //
    // Init
    //
    this.init();

};

LazyLoadInit.prototype.init = function() {

    var that = this;

    $("img.lazyload").lazyload({
        effect : "fadeIn"
    });

};

module.exports = LazyLoadInit;
