var Summary = function() {

    this.$summary = $('[data-summary]');
    this.$content = $('[data-summary-content]');
    this.$links = [];

    //
    // Init
    //
    this.init();

};

Summary.prototype.init = function() {

    var that = this,
        $template, sectionCount = 0;

    if(that.$summary.length == 1 && that.$content.length > 0) {

        $template = that.$summary.find('li:first-child');
        that.$content.each(function(idx) {

            $(this).find('h2:not(.page-box__title)').each(function(idx) {

                var $element = $(this),
                    $template_clone = $template.clone();

                $template_clone.find('a').text($element.text());
                $template_clone.find('a').attr('href', '#section-' + sectionCount);
                $template_clone.removeClass('hide');

                that.$links.push($template_clone.find('a'));

                that.$summary.append($template_clone);

                $element.attr('id', "section-" + sectionCount);
                sectionCount++;

            });

        });

        $template.remove();

        // Scrollspy
        $(document).on("scroll", that.onScroll.bind(that));

    }

};

Summary.prototype.onScroll = function(e) {

    var scrollPos = $(document).scrollTop(),
        that = this,
        currentTitle, minDiff = 9999999999999;

    that.$links.forEach(function (elem) {
        var currLink = elem;
        var refElement = $(elem.attr("href"));
        var diff = refElement.offset().top - scrollPos;
        if(diff < minDiff && diff > 0) {
            minDiff = diff;
            currentTitle = refElement;
        }
        if (refElement.position().top <= scrollPos) {
            that.$links.forEach(function (elem) {
                elem.removeClass('active');
            });
            currLink.addClass("active");
        }
        else{
            currLink.removeClass("active");
        }
    });

    that.$links.forEach(function (elem) {
        elem.removeClass('active');
    });

    if(currentTitle) {
        $('[href="#' + currentTitle.attr('id') + '"]').addClass('active');
    }

};

module.exports = Summary;
