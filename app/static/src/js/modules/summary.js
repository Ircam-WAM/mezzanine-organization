var Summary = function() {

    this.$summary = $('[data-summary]');
    this.$content = $('[data-summary-content]');

    //
    // Init
    //
    this.init();

};

Summary.prototype.init = function() {

    var that = this,
        $template;

    if(that.$summary.length == 1 && that.$content.length == 1) {

        $template = that.$summary.find('li:first-child');
        that.$content.find('h2').each(function(idx) {

            var $element = $(this),
                $template_clone = $template.clone();
            $template_clone.find('a').text($element.text());
            $template_clone.find('a').attr('href', '#section-' + idx);
            $template_clone.removeClass('hide');
            that.$summary.append($template_clone);

            $element.attr('id', "section-" + idx);

        });

        $template.remove();

    }

};

module.exports = Summary;
