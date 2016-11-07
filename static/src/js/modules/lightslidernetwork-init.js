var LightSliderNetworkInit = function() {

    this.slider = null;
    this.map = null;
    this.markers = [];
    this.currentLine = null;
    this.animationInterval = null;

    //
    // Init
    //
    this.init();

};

LightSliderNetworkInit.prototype.init = function() {

    var that = this;

    //
    // Slider init
    //
    /*that.slider = $('[data-slider-network]').lightSlider({
        item: 4,
        slideMargin: 10,
        pager: false,
        controls: false,
        loop: false,
        adaptiveHeight: true,
        onSliderLoad: function(elem) {
            elem.parents('.slider-network').find('.lSPrev').click(function(e) {
                elem.goToPrevSlide();
            });
            elem.parents('.slider-network').find('.lSNext').click(function(e) {
                elem.goToNextSlide();
            });
        },
        onBeforeSlide: function(elem) {
            if (that.currentLine) {
                that.currentLine.setMap(null);
            }
        }
    });*/

    //
    // Init map
    //
    if($('#network-map').length > 0) {

        that.map = new google.maps.Map(document.getElementById('network-map'), {
            zoom: 3,
            center: {lat: 48.85982, lng: 2.351402},
            styles: [{"featureType":"water","elementType":"geometry","stylers":[{"color":"#e9e9e9"},{"lightness":17}]},{"featureType":"landscape","elementType":"geometry","stylers":[{"color":"#f5f5f5"},{"lightness":20}]},{"featureType":"road.highway","elementType":"geometry.fill","stylers":[{"color":"#ffffff"},{"lightness":17}]},{"featureType":"road.highway","elementType":"geometry.stroke","stylers":[{"color":"#ffffff"},{"lightness":29},{"weight":0.2}]},{"featureType":"road.arterial","elementType":"geometry","stylers":[{"color":"#ffffff"},{"lightness":18}]},{"featureType":"road.local","elementType":"geometry","stylers":[{"color":"#ffffff"},{"lightness":16}]},{"featureType":"poi","elementType":"geometry","stylers":[{"color":"#f5f5f5"},{"lightness":21}]},{"featureType":"poi.park","elementType":"geometry","stylers":[{"color":"#dedede"},{"lightness":21}]},{"elementType":"labels.text.stroke","stylers":[{"visibility":"on"},{"color":"#ffffff"},{"lightness":16}]},{"elementType":"labels.text.fill","stylers":[{"saturation":36},{"color":"#333333"},{"lightness":40}]},{"elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"transit","elementType":"geometry","stylers":[{"color":"#f2f2f2"},{"lightness":19}]},{"featureType":"administrative","elementType":"geometry.fill","stylers":[{"color":"#fefefe"},{"lightness":20}]},{"featureType":"administrative","elementType":"geometry.stroke","stylers":[{"color":"#fefefe"},{"lightness":17},{"weight":1.2}]}]
        });

        google.maps.event.addListenerOnce(that.map, 'projection_changed', function() {
            that.initMarkers();
        });

        google.maps.event.addListener(that.map, 'zoom_changed', function() {
            if (that.map.getZoom() < 3) that.map.setZoom(3);
        });

    }

};

LightSliderNetworkInit.prototype.initMarkers = function() {

    var that = this;

    $('[data-marker-idx]').each(function(idx) {

        var obj = {
            'lat': parseFloat($(this).attr('data-marker-lat').replace(',', '.')),
            'lng': parseFloat($(this).attr('data-marker-lng').replace(',', '.')),
            'elem': $(this),
            'marker': new google.maps.Marker({
                position: {lat: parseFloat($(this).attr('data-marker-lat').replace(',', '.')), lng: parseFloat($(this).attr('data-marker-lng').replace(',', '.'))},
                map: that.map,
                icon: "/static/img/map-marker-" + $(this).attr('data-marker-color') + ".png"
            })
        };

        var info = new google.maps.InfoWindow({
            content: '<div class="map-infowindow"><div class="map-infowindow__image"><a href="' + $(this).attr('data-marker-url') + '" target="_blank"><img src="' + $(this).attr('data-marker-image') + '" /></a></div><div class="map-infowindow__content"><div class="map-infowindow__title">' + $(this).find('[data-marker-title]').text() + '</div><div class="map-infowindow__subtitle">' + $(this).find('[data-marker-subtitle]').text() + '</div></div></div>'
        });

        obj.info = info;

        obj.marker.addListener('click', function() {
            that.markers.forEach(function(m, i) {
                m.info.close();
            });
            info.open(that.map, obj.marker);
        });

        that.markers.push(obj);

    });

};

module.exports = LightSliderNetworkInit;
