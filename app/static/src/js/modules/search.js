var Search = function() {

    this.$element = $('#searchBtn');
    this.$search = $('#search');
    this.$searchInput = this.$search.find('input[type="text"]');

    //
    // Init
    //
    this.init();

};

Search.prototype.init = function() {

    var that = this;

    that.$element = $('#searchBtn');
    that.$search = $('#search');


    that.$element.click(function(e) {

        e.preventDefault();

        that.$searchInput.focus();

        return false;

    });


};

module.exports = Search;
