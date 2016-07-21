var StickyKitInit = function() {

    this.elements = [];

    //
    // Init
    //
    this.init();

};

StickyKitInit.prototype.init = function() {

    var that = this,
        options = {},
        data, element, $element;

    $('[data-sticky]').each(function(i) {

        $element = $(this);
        data = $(this).data();

        if(data.stickyOffset) {
            options.offset_top = data.stickyOffset;
        }
        if(data.stickyParent) {
            options.parent = '.' + data.stickyParent;
        }

        element = {
            $element: $(this),
            options: options,
            data: $(this).data(),
            attached: false
        };
        that.elements.push(element);
        that.attach(element);

    });

    $(window).resize(that.windowResize.bind(that));

};

StickyKitInit.prototype.windowResize = function(e) {

    var that = this,
        windowWidth = $(window).width();

    for(var i=0; i<that.elements.length; i++) {

        if(that.elements[i].data.stickyDetachAt) {

            if(windowWidth > that.elements[i].data.stickyDetachAt && !that.elements[i].attached) {
                that.attach(that.elements[i]);
            }

            if(windowWidth <= that.elements[i].data.stickyDetachAt && that.elements[i].attached) {
                that.detach(that.elements[i]);
            }

        }

    }

};

StickyKitInit.prototype.attach = function(element) {

    var that = this;

    if(element.data.stickyDetachAt) {

        var $window = $(window);

        //
        // Attach if window width is larger
        //
        if($window.width() > element.data.stickyDetachAt) {

            element.$element.stick_in_parent(element.options);
            element.attached = true;

        }

    } else {

        element.$element.stick_in_parent(element.options);
        element.attached = true;

    }

};

StickyKitInit.prototype.detach = function(element) {

    element.$element.trigger("sticky_kit:detach");
    element.attached = false;

};

module.exports = StickyKitInit;
