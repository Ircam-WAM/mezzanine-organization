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
            styles: [
                {
                    "featureType": "all",
                    "elementType": "labels",
                    "stylers": [
                        {
                            "gamma": 0.26
                        },
                        {
                            "visibility": "off"
                        }
                    ]
                },
                {
                    "featureType": "administrative.province",
                    "elementType": "all",
                    "stylers": [
                        {
                            "visibility": "on"
                        },
                        {
                            "lightness": -50
                        }
                    ]
                },
                {
                    "featureType": "administrative.province",
                    "elementType": "labels.text",
                    "stylers": [
                        {
                            "lightness": 20
                        }
                    ]
                },
                {
                    "featureType": "administrative.province",
                    "elementType": "labels.text.stroke",
                    "stylers": [
                        {
                            "visibility": "off"
                        }
                    ]
                },
                {
                    "featureType": "poi",
                    "elementType": "all",
                    "stylers": [
                        {
                            "visibility": "off"
                        }
                    ]
                },
                {
                    "featureType": "road",
                    "elementType": "all",
                    "stylers": [
                        {
                            "hue": "#ffffff"
                        }
                    ]
                },
                {
                    "featureType": "road",
                    "elementType": "labels.text.stroke",
                    "stylers": [
                        {
                            "visibility": "off"
                        }
                    ]
                },
                {
                    "featureType": "road.highway",
                    "elementType": "geometry",
                    "stylers": [
                        {
                            "lightness": 50
                        },
                        {
                            "hue": "#ffffff"
                        }
                    ]
                },
                {
                    "featureType": "road.arterial",
                    "elementType": "geometry",
                    "stylers": [
                        {
                            "lightness": 20
                        }
                    ]
                },
                {
                    "featureType": "road.arterial",
                    "elementType": "geometry.fill",
                    "stylers": [
                        {
                            "color": "#f26662"
                        }
                    ]
                },
                {
                    "featureType": "road.arterial",
                    "elementType": "labels.text",
                    "stylers": [
                        {
                            "visibility": "on"
                        }
                    ]
                },
                {
                    "featureType": "transit",
                    "elementType": "all",
                    "stylers": [
                        {
                            "visibility": "off"
                        }
                    ]
                }
            ]
        });

        google.maps.event.addListenerOnce(that.map, 'projection_changed', function() {
            that.initMarkers();

            var bounds = new google.maps.LatLngBounds();
            for (var i = 0; i < that.markers.length; i++) {
                bounds.extend(that.markers[i].marker.getPosition());
            }
            that.map.fitBounds(bounds);

        });

        google.maps.event.addListener(that.map, 'zoom_changed', function() {
            //if (that.map.getZoom() < 3) that.map.setZoom(3);
        });

        google.maps.event.addListener(that.map, "click", function(event) {
            that.markers.forEach(function(m, i) {
                m.info.close();
            });
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
            content: '<div class="map-infowindow"><div class="map-infowindow__image"><img src="' + $(this).attr('data-marker-image') + '" /></div><div class="map-infowindow__content"><div class="map-infowindow__title">' + $(this).find('[data-marker-title]').text() + '</div><div class="map-infowindow__subtitle">' + $(this).find('[data-marker-subtitle]').text() + '</div><p>' + $(this).find('[data-marker-description]').html() + '</p></div></div>'
        });

        google.maps.event.addListener(info, 'domready', function() {

            // Reference to the DIV which receives the contents of the infowindow using jQuery
            var iwOuter = $('.gm-style-iw');

            /* The DIV we want to change is above the .gm-style-iw DIV.
            * So, we use jQuery and create a iwBackground variable,
            * and took advantage of the existing reference to .gm-style-iw for the previous DIV with .prev().
            */
            var iwBackground = iwOuter.prev();

            iwOuter.prev().css({'display' : 'none'});
            iwOuter.next().css({'top' : '100px'});

            // Remove the background shadow DIV
            iwBackground.children(':nth-child(2)').css({'display' : 'none'});

            // Remove the white background DIV
            iwBackground.children(':nth-child(4)').css({'display' : 'none'});

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
