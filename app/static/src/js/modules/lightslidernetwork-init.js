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
    that.slider = $('[data-slider-network]').lightSlider({
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
    });

    //
    // Init map
    //
    if($('#network-map').length > 0) {

        that.map = new google.maps.Map(document.getElementById('network-map'), {
            zoom: 4,
            center: {lat: -25.363, lng: 131.044},
            styles: [{"featureType":"water","elementType":"geometry","stylers":[{"color":"#e9e9e9"},{"lightness":17}]},{"featureType":"landscape","elementType":"geometry","stylers":[{"color":"#f5f5f5"},{"lightness":20}]},{"featureType":"road.highway","elementType":"geometry.fill","stylers":[{"color":"#ffffff"},{"lightness":17}]},{"featureType":"road.highway","elementType":"geometry.stroke","stylers":[{"color":"#ffffff"},{"lightness":29},{"weight":0.2}]},{"featureType":"road.arterial","elementType":"geometry","stylers":[{"color":"#ffffff"},{"lightness":18}]},{"featureType":"road.local","elementType":"geometry","stylers":[{"color":"#ffffff"},{"lightness":16}]},{"featureType":"poi","elementType":"geometry","stylers":[{"color":"#f5f5f5"},{"lightness":21}]},{"featureType":"poi.park","elementType":"geometry","stylers":[{"color":"#dedede"},{"lightness":21}]},{"elementType":"labels.text.stroke","stylers":[{"visibility":"on"},{"color":"#ffffff"},{"lightness":16}]},{"elementType":"labels.text.fill","stylers":[{"saturation":36},{"color":"#333333"},{"lightness":40}]},{"elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"transit","elementType":"geometry","stylers":[{"color":"#f2f2f2"},{"lightness":19}]},{"featureType":"administrative","elementType":"geometry.fill","stylers":[{"color":"#fefefe"},{"lightness":20}]},{"featureType":"administrative","elementType":"geometry.stroke","stylers":[{"color":"#fefefe"},{"lightness":17},{"weight":1.2}]}]
        });

        google.maps.event.addListenerOnce(that.map, 'projection_changed', function() {
            that.initMarkers();
        });

    }

};

LightSliderNetworkInit.prototype.initMarkers = function() {

    var that = this;

    $('[data-marker-idx]').each(function(idx) {

        that.markers.push({
            'lat': parseFloat($(this).attr('data-marker-lat').replace(',', '.')),
            'lng': parseFloat($(this).attr('data-marker-lng').replace(',', '.')),
            'elem': $(this),
            'marker': new google.maps.Marker({
                position: {lat: parseFloat($(this).attr('data-marker-lat').replace(',', '.')), lng: parseFloat($(this).attr('data-marker-lng').replace(',', '.'))},
                map: that.map,
                icon: "/static/img/map-marker.png"
            })
        });

    });

    console.log(that.markers);
    that.markers.forEach(function(m, i) {

        m.marker.addListener('mouseover', function(e) {

            this.setIcon("/static/img/map-marker-hover.png");

            var target = that.markers[i].elem[0];

            var idx = target.getAttribute('data-marker-idx');
            var lat = that.markers[idx].lat;
            var lng = that.markers[idx].lng;

            that.slider.goToSlide(Math.floor(i/4));

            setTimeout(function() {
                var x = target.offsetLeft + (target.offsetWidth * .5);

                var buttonPos = target.getBoundingClientRect();
                var x = (buttonPos.left + (buttonPos.width * .5)) - document.getElementById('network-map').getBoundingClientRect().left;

                var fakeLatLng = that.point2LatLng({x: x, y: document.getElementById('network-map').getBoundingClientRect().height}, that.map);

                that.drawLine(fakeLatLng, new google.maps.LatLng(that.markers[idx].lat, that.markers[idx].lng));
            }, 250);

        });

        m.marker.addListener('mouseout', function(e) {

            clearInterval(that.animationInterval);
            this.setIcon("/static/img/map-marker.png");

            if (that.currentLine) {
                that.currentLine.setMap(null);
            }

        });

        m.elem[0].addEventListener('mouseover', function(e) {

            var idx = e.currentTarget.getAttribute('data-marker-idx');
            var lat = that.markers[idx].lat;
            var lng = that.markers[idx].lng;

            that.markers[idx].marker.setIcon("/static/img/map-marker-hover.png");

            that.map.panTo({lat: lat, lng: lng});

            var x = e.currentTarget.offsetLeft + (e.currentTarget.offsetWidth * .5);

            var buttonPos = e.currentTarget.getBoundingClientRect();
            var x = (buttonPos.left + (buttonPos.width * .5)) - document.getElementById('network-map').getBoundingClientRect().left;

            var fakeLatLng = that.point2LatLng({x: x, y: document.getElementById('network-map').getBoundingClientRect().height}, that.map);

            that.drawLine(fakeLatLng, new google.maps.LatLng(that.markers[idx].lat, that.markers[idx].lng));

        });

        m.elem[0].addEventListener('mouseout', function(e) {

            var idx = e.currentTarget.getAttribute('data-marker-idx');
            that.markers[idx].marker.setIcon("/static/img/map-marker.png");

            clearInterval(that.animationInterval);

            if (that.currentLine) {
                that.currentLine.setMap(null);
            }

        });

    });

};

LightSliderNetworkInit.prototype.drawLine = function(start, end) {

    var that = this;

    if (that.currentLine) {
        that.currentLine.setMap(null);
    }

    that.currentLine = new google.maps.Polyline({
        path: [
            start,
            start
        ],
        strokeColor: 'red',
        strokeOpacity: 1.0,
        strokeWeight: 1,
        geodesic: false,
        map: that.map
    });

    var step = 0;
    var numSteps = 25;
    var timePerStep = 5;

    that.animationInterval = setInterval(function() {

        step += 1;

        if (step > numSteps) {
            clearInterval(that.animationInterval);
        } else {
            var currentPosLatLng = google.maps.geometry.spherical.interpolate(start, end, step / numSteps);
            that.currentLine.setPath([start, currentPosLatLng]);
        }

    }, timePerStep);

};

LightSliderNetworkInit.prototype.point2LatLng = function(point, map) {

    var that = this;
    var topRight = that.map.getProjection().fromLatLngToPoint(that.map.getBounds().getNorthEast());
    var bottomLeft = that.map.getProjection().fromLatLngToPoint(that.map.getBounds().getSouthWest());
    var scale = Math.pow(2, that.map.getZoom());
    var worldPoint = new google.maps.Point(point.x / scale + bottomLeft.x, point.y / scale + topRight.y);
    return that.map.getProjection().fromPointToLatLng(worldPoint);

};

module.exports = LightSliderNetworkInit;
