var StickyKitInit = function() {

    //
    // Init
    //
    this.init();

};

StickyKitInit.prototype.init = function() {

    var that = this,
        options = {},
        data;

    $('[data-sticky]').each(function(i) {

        data = $(this).data();
        if(data.stickyOffset) {
            options.offset_top = data.stickyOffset;
        }
        if(data.stickyParent) {
            options.parent = '.' + data.stickyParent;
        }
        $(this).stick_in_parent(options);

    });

};

module.exports = StickyKitInit;
