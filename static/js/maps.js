
                            var map,
                                infoWindow;
                            function initMap() {
                                map = new google.maps.Map(document.getElementById('map'), {
                                    mapTypeControl: false,
                                    center: {
                                        lat: -1.2986122999999998,
                                        lng: 36.7568353
                                    },
                                    zoom: 8
                                });
                                infoWindow = new google.maps.InfoWindow;
                                new AutocompleteDirectionsHandler(map);
                            }
                            if (navigator.geolocation) {
                                navigator.geolocation.getCurrentPosition(function (position) {
                                    var pos = {
                                        lat: position.coords.latitude,
                                        lng: position.coords.longitude
                                    };
                                    var marker1 = new google.maps.Marker({
                                        position: new google.maps.LatLng(pos),
                                        map: map,
                                        title: 'Current Location',
                                        icon: {
                                            url: 'http://maps.google.com/mapfiles/ms/icons/green.png'
                                        }
                                    });
                                    infoWindow.open(map);
                                    map.setCenter(pos);
                                    map.setZoom(16);
                                }, function () {
                                    handleLocationError(true, infoWindow, map.getCenter());
                                });
                            } else {
                                handleLocationError(false, infoWindow, map.getCenter());
                            }
                            function handleLocationError(browserHasGeolocation, infoWindow, pos) {
                                infoWindow.setPosition(pos);
                                infoWindow.setContent(
                                    browserHasGeolocation
                                        ? 'Error: The Geolocation service failed.'
                                        : 'Error: Your browser doesn\'t support geolocation.'
                                );
                                infoWindow.open(map);
                            }
                            /**
                              * @constructor
                             */
                            function AutocompleteDirectionsHandler(map) {
                                this.map = map;
                                this.originPlaceId = null;
                                this.destinationPlaceId = null;
                                this.travelMode = 'DRIVING';
                                var originInput = document.getElementById('origin-input');
                                var destinationInput = document.getElementById('destination-input');
                                this.directionsService = new google.maps.DirectionsService;
                                this.directionsDisplay = new google.maps.DirectionsRenderer;
                                this.directionsDisplay.setMap(map);
                                var originAutocomplete = new google.maps.places.Autocomplete(originInput, { placeIdOnly: true });
                                var destinationAutocomplete = new google.maps.places.Autocomplete(destinationInput, { placeIdOnly: true });
                                this.setupClickListener('changemode-walking', 'WALKING');
                                this.setupClickListener('changemode-transit', 'TRANSIT');
                                this.setupClickListener('changemode-driving', 'DRIVING');
                                this.setupPlaceChangedListener(originAutocomplete, 'ORIG');
                                this.setupPlaceChangedListener(destinationAutocomplete, 'DEST');
                                this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(originInput);
                                this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(destinationInput);
                            }
                            AutocompleteDirectionsHandler.prototype.setupClickListener = function (id, mode) {
                                var radioButton = document.getElementById(id);
                                var me = this;
                                radioButton.addEventListener('click', function () {
                                    me.travelMode = mode;
                                    me.route();
                                });
                            };
                            AutocompleteDirectionsHandler.prototype.setupPlaceChangedListener = function (autocomplete, mode) {
                                var me = this;
                                autocomplete.bindTo('bounds', this.map);
                                autocomplete.addListener('place_changed', function () {
                                    var place = autocomplete.getPlace();
                                    if (!place.place_id) {
                                        window.alert("Please select an option from the dropdown list.");
                                        return;
                                    }
                                    if (mode === 'ORIG') {
                                        me.originPlaceId = place.place_id;
                                    } else {
                                        me.destinationPlaceId = place.place_id;
                                    }
                                    me.route();
                                });
                            };
                            AutocompleteDirectionsHandler.prototype.route = function () {
                                if (!this.originPlaceId || !this.destinationPlaceId) {
                                    return;
                                }
                                var me = this;
                                this.directionsService.route({
                                    origin: {
                                        'placeId': this.originPlaceId
                                    },
                                    destination: {
                                        'placeId': this.destinationPlaceId
                                    },
                                    travelMode: this.travelMode
                                }, function (response, status) {
                                    if (status === 'OK') {
                                        me.directionsDisplay.setDirections(response);
                                    } else {
                                        window.alert('Directions request failed due to ' + status);
                                    }
                                });
                            };
