var EventForm = function() {

    var that = this;

    this.$form = $('#jsEventsForm');
    this.$homeform = $('#jsEventsHomeForm');
    this.$container = $('#jsEventsContainer');
    this.req = null;

    this.queryDict = {}
    location.search.substr(1).split("&").forEach(function(item) {that.queryDict[item.split("=")[0]] = item.split("=")[1]});

    //
    // Init
    //
    if(this.$form.length > 0) {
        this.init();
    }

    if(this.$homeform.length > 0) {
        $('input[type="radio"][disabled]', that.$homeform).each(function(idx) {
            $(this).parents('li').addClass('disabled');
        });

        $('input[type="radio"]', that.$homeform).on('change', function() {
            that.$homeform.submit();
        });
    }

};

EventForm.prototype.init = function() {

    var that = this;

    that.$form.on('submit', function(e) {
        e.preventDefault();

        var data = that.$form.serialize();

        if(that.req) that.req.abort();
        that.req = $.get(that.$form.attr('action'), data, function(res) {
            that.$container.html(res);

            // reload Lazyload
            window['LazyLoadInit'].init();
        });

        return false;
    });

    $('#id_event_day_filter li').each(function(idx) {
        if( $('input', $(this)).prop('checked') ) {
            $($('#id_event_day_filter li')[idx]).addClass('active');
        }
    });

    if(!that.queryDict['event_categories_filter[]']) {
        $('#id_event_categories_filter input').prop("checked", true);
        $('#id_event_categories_filter li').addClass('active');
    }
    if(!that.queryDict['id_event_locations_filter[]']) {
        $('#id_event_locations_filter input').prop("checked", true);
        $('#id_event_locations_filter li').addClass('active');
    }

    $('input[type="radio"][disabled]', that.$form).each(function(idx) {
        $(this).parents('li').addClass('disabled');
    });

    $('input[type="radio"]', that.$form).on('change', function() {
        that.$form.submit();

        $('#id_event_day_filter li').removeClass('active');
        $(this).parents('li').addClass('active');
    });

    $('input[type="checkbox"]', that.$form).on('change', function() {
        that.$form.submit();

        if($(this).prop('checked')) {
            $(this).parents('li').addClass('active');
        } else {
            $(this).parents('li').removeClass('active');
        }

    });

};

module.exports = EventForm;
