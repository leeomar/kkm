/*********************************** GoogleMapCreator Class **********************************/

var GoogleMapCreator = new Class({
	
	Implements:	[Options, Events],
	
	options: {
		size: {
			width:	'100%',
			height:	'100%'
		},
		backgroundColor: '#ccc',
		center: {
			lat: 7.6,
			lng: -74
		},
		disableDefaultUI: false,
		disableDoubleClickZoom: true,
		draggable: true,
		draggableCursor: 'cursor',
		draggingCursor: 'cursor',
		keyboardShortcuts: true,
		mapTypeControl: true,
		mapTypeId: 'ROADMAP',
		navigationControl: true,
		scaleControl: true,
		scrollwheel: true,
		streetViewControl: true,
		zoom: 6
	},
	
	initialize: function (mapContainer, options) {
		this.mapContainer = mapContainer;
		this.setOptions(options);
		this.mapConfig();
		this.createMap();
		this.addListeners();
	},
	
	mapConfig: function () {
		this.mapOptions = {
			backgroundColor : this.options.backgroundColor,
			center: this.createLatLng(this.options.center.lat, this.options.center.lng),
			disableDefaultUI: this.options.disableDefaultUI,
			disableDoubleClickZoom: this.options.disableDoubleClickZoom,
			draggable: this.options.draggable,
			draggableCursor: this.options.draggableCursor,
			draggingCursor: this.options.draggingCursor,
			keyboardShortcuts: this.options.keyboardShortcuts,
			mapTypeId: this.options.mapTypeId.toLowerCase(),
			navigationControl: this.options.navigationControl,
			scaleControl: this.options.scaleControl,
			scrollwheel: this.options.scrollwheel,
			streetViewControl: this.options.streetViewControl,
			zoom: this.options.zoom
		};
		
	},
		
	createMap: function() {
		this.mapContainer.setStyles({
			width:	this.options.size.width,
			height:	this.options.size.height
		});
		this.mapObj = new google.maps.Map(this.mapContainer, this.mapOptions);
	},
	
	
	/**************************************************************
							API BASE CLASSES
	**************************************************************/
	
	//LatLng API Class
	createLatLng: function(latitude, longitude) {
		var latLng = new google.maps.LatLng(latitude, longitude);
		return latLng;
	},
	
	//LatLng API Class Method
	getLatitude: function(latLng) {
		latLng = [latLng, this.getCenter()].pick();
		var lat = latLng.lat();
		return lat;
	},
	
	//LatLng API Class Method
	getLongitude: function(latLng) {
		latLng = [latLng, this.getCenter()].pick();
		var lng = latLng.lng();
		return lng;
	},
	
	//LatLngBounds API Class
	createLatLngBounds: function(SWLatLng, NELatLng) {
		var LatLngBounds = new google.maps.LatLngBounds(SWLatLng, NELatLng);
		return LatLngBounds;
	},
	
	//LatLngBounds API Class Method
	getBoundsCenter: function(bounds) {
		var center = bounds.getCenter();
		return center;
	},
	
	/**************************************************************
					MAP CLASS (Google Maps API Class)
	**************************************************************/
	
	/*------------------------- METHODS -------------------------*/
	
	setCenter: function(latLng) {
		var center = [latLng, this.getCenter()].pick();
		this.mapObj.setCenter(latLng);
	},
	
	getCenter: function() {
		var center = this.mapObj.getCenter();
		return center;
	},
	
	setZoom: function(zoomLevel) {
		// Google API will convert IT downwards to the nearest integer.
		zoomLevel = [zoomLevel, this.getZoom()].pick();
		this.mapObj.setZoom(zoomLevel);
	},
	
	getZoom: function() {
		var zoomLevel = this.mapObj.getZoom();
		return zoomLevel;
	},
		
	setMapType: function(mapType) {
		mapType = [mapType.toLowerCase(), this.getMapType].pick();
		this.mapObj.setMaypTypeId(mapType);
	},
	
	getMapType: function() {
		var mapType = this.mapObj.getMapTypeId();
		return mapType;
	},
	
	fitBounds: function(LatLngBounds) {
		LatLngBounds = [LatLngBounds, this.getBounds].pick();
		this.mapObj.fitBounds(LatLngBounds);
	},
	
	getBounds: function() {
			var bounds = this.mapObj.getBounds();
			return bounds;
	},
	
	panBy: function(x,y) {
		x = [x, 0].pick();
		y = [y, 0].pick();
		this.mapObj.panBy(x,y);
	},
		
	panTo: function(latLng) {
		latLng = [latLng, this.getCenter()].pick();
		this.mapObj.panTo(latLng);
	},
	
	panToBounds: function(latLngBounds) {
		latLngBounds = [latLngBounds, this.getBounds()].pick();
		this.mapObj.panToBounds(latLngBounds);
	},
	
	setStreetView: function(streetViewPanorama) {
		streetViewPanorama = [streetViewPanorama, this.getStreetView()].pick();
		this.mapObj.setStreetView(streetViewPanorama);
	},
	
	getStreetView: function() {
		var streetView = this.mapObj.getStreetView();
		return streetView;
	},
	
	getDiv: function() {
		var mapDiv = this.mapObj.getdiv();
		return mapDiv;
	},
	
	setMapOptions: function(mapOptions) {
		mapOptions = [mapOptions, this.mapOptions].pick();
		this.mapObj.setOptions(mapOptions);
	},
	
	getMap: function() {
		return this.mapObj;
	},
	
	/**************************************************************
						ADDING	LISTENERS for MAP EVENTS
	**************************************************************/
	
	addListeners: function() {
		
		/*
		Connects Google listeners with MooTools class events,
		each one is described later in next section of this code (MAP CLASS->Events).
		*/
		
		google.maps.event.addListener(this.mapObj,'bounds_changed', function() {
			this.boundsChanged();
		}.bind(this));
		
		google.maps.event.addListener(this.mapObj,'center_changed', function() {
			this.centerChanged();
		}.bind(this));
		
		google.maps.event.addListener(this.mapObj,'click', function(event) {
			this.click(event.latLng);
		}.bind(this));
		
		google.maps.event.addListener(this.mapObj,'dblclick', function(event) {
			this.dblClick(event.latLng);
		}.bind(this));
		
		google.maps.event.addListener(this.mapObj,'drag', function() {
			this.drag();
		}.bind(this));
		
		google.maps.event.addListener(this.mapObj,'dragend', function() {
			this.dragEnd();
		}.bind(this));
		
		google.maps.event.addListener(this.mapObj,'dragstart', function() {
			this.dragStart();
		}.bind(this));
		
		google.maps.event.addListener(this.mapObj,'idle', function() {
			this.idle();
		}.bind(this));
		
		google.maps.event.addListener(this.mapObj,'maptypeid_changed', function() {
			this.mapTypeChanged();
		}.bind(this));
		
		google.maps.event.addListener(this.mapObj,'mousemove', function(event) {
			this.mouseMove(event.latLng);
		}.bind(this));
		
		google.maps.event.addListener(this.mapObj,'mouseout', function(event) {
			this.mouseOut(event.latLng);
		}.bind(this));
		
		google.maps.event.addListener(this.mapObj,'mouseover', function(event) {
			this.mouseOver(event.latLng);
		}.bind(this));
		
		google.maps.event.addListener(this.mapObj,'projection_changed', function() {
			this.projectionChanged();
		}.bind(this));
		
		google.maps.event.addListener(this.mapObj,'resize', function() {
			this.resize();
		}.bind(this));
		
		google.maps.event.addListener(this.mapObj,'rightclick', function(event) {
			this.rightClick(event.latLng);
		}.bind(this));
		
		google.maps.event.addListener(this.mapObj,'tilesloaded', function() {
			this.tilesLoaded();
		}.bind(this));
		
		google.maps.event.addListener(this.mapObj,'zoom_changed', function() {
			this.zoomChanged();
		}.bind(this));
		
	},
	
	/*------------------------- EVENTS -------------------------*/
	
	/* BoundsChanged:
		This event is fired when the viewport bounds have changed.
	*/
	boundsChanged: function() {
		this.fireEvent('boundsChanged');
	},
	
	/* CenterChanged:
		This event is fired when the map center property changes.
	*/
	centerChanged: function() {
		this.fireEvent('centerChanged');
	},
		
	/* Click:
		This event is fired when the user clicks on the map (but not when they click on a marker or infowindow).
	*/
	click: function(location) {
		this.fireEvent('click', location);
	},
	
	/* DoubleClick:
		This event is fired when the user double-clicks on the map. Note that the click event will also fire, right before this one.
	*/
	dblClick: function(location) {
		this.fireEvent('dblClick', location);
	},
	
	/* Drag:
		This event is repeatedly fired while the user drags the map.
	*/
	drag: function() {
		this.fireEvent('drag');
	},
	
	/* DragEnd:
		This event is fired when the user stops dragging the map.
	*/
	dragEnd: function() {
		this.fireEvent('dragEnd');
	},
	
	/* DragStart:
		This event is fired when the user starts dragging the map.
	*/
	dragStart: function() {
		this.fireEvent('dragStart');
	},
	
	/* Idle:
		This event is fired when the map becomes idle after panning or zooming.
	*/
	idle: function() {
		this.fireEvent('idle');
	},
	
	/* MapTypeChanged:
		This event is fired when the mapTypeId property changes.
	*/
	mapTypeChanged: function() {
		this.fireEvent('mapTypeChanged');
	},
	
	/* MouseMove:
		This event is fired whenever the user's mouse moves over the map container.
	*/
	mouseMove: function(location) {
		this.fireEvent('mouseMove', location);
	},
	
	/* MouseOut:
		This event is fired when the user's mouse exits the map container.
	*/
	mouseOut: function(location) {
		this.fireEvent('mouseOut', location);
	},
	
	/* MouseOver:
		This event is fired when the user's mouse enters the map container.
	*/
	mouseOver: function(location) {
		this.fireEvent('mouseOver', location);
	},
	
	/* ProjectionChanged:
		This event is fired when the projection has changed.
	*/
	projectionChanged: function() {
		this.fireEvent('projectionChanged');
	},
	
	/* Resize:
		Developers should trigger this event on the map when the div changes size: google.maps.event.trigger(map, 'resize').
	*/
	resize: function() {
		this.fireEvent('resize');
	},
	
	/* RightClick:
		This event is fired when the DOM contextmenu event is fired on the map container.
	*/
	rightClick: function(location) {
		this.fireEvent('rightClick', location);
	},
	
	/* TilesLoaded:
		This event is fired when the visible tiles have finished loading.
	*/
	tilesLoaded: function() {
		this.fireEvent('tilesLoaded');
	},
	
	/* ZoomChanged:
		This event is fired when the map zoom property changes.
	*/
	zoomChanged: function() {
		this.fireEvent('zoomChanged');
	},	
	
	/**************************************************************
					MARKER CLASS (Google Maps API Class)
	**************************************************************/
	
	/*------------------------- METHODS -------------------------*/
	
	createMarker: function(markerOptions) {
		var marker = new GoogleMapMarker(markerOptions);
		marker.setMap(this.mapObj);
		return marker;
	},
	
	// Possible to define a different Marker Event (action) than 'click'
	// to trigger the opening of the infoWindow. See GoogleMapMarker Class>>EVENTS (ln 724).
	createInfoMarker: function(markerOptions, infoWindowOptions, action) {
		action = [action, 'click'].pick();
		var marker = new GoogleMapMarker(markerOptions);
		var infoWindow = new GoogleMapInfoWindow(infoWindowOptions);
		marker.addEvent(action, function() {
			infoWindow.open(this.mapObj, marker.markerObj);
		}.bind(this));
		marker.setMap(this.mapObj);
		return marker;
	},
	
	createCircle: function(circleOptions) {
		var circle = new GoogleMapCircle(circleOptions);
		circle.setMap(this.mapObj);
		return circle;
	},
	
	createRectangle: function(rectangleOptions) {
		var rectangle = new GoogleMapRectangle(rectangleOptions);
		rectangle.setMap(this.mapObj);
		return rectangle;
	},
	
	/*	
		Creates a PolyLine on the map.
		Coordinates is an array of [lat,lng]
		e.g, coordinates: [[lat,lng], [lat2, lng2], [lat3,lng3],...so on]
	*/
	createPolyLine: function(coordinates, polyLineOptions) {
		var polyLine = new GoogleMapPolyLine(polyLineOptions);
		polyLine.setMap(this.mapObj);
		if(coordinates && (typeOf(coordinates) == 'array') ) {
			coordinates.each(function(latLng) {
				var lat = latLng[0];
				var lng = latLng[1];
				latLng = new google.maps.LatLng(lat, lng);
				polyLine.addLine(latLng);
			}, this);
		};
		return polyLine;
	}
	
});

/*********************************** /GoogleMapCreator Class **********************************/

/************************************ GoogleMapMarker Class ***********************************/

var GoogleMapMarker = new Class({
	
	Implements: [Options, Events],
	
	options: {
		clickable: true,
		cursor: '',
		draggable: false,
		flat: false,
		icon: '',
		map: null, 
		center: {
			lat: 7.6,
			lng: -74
		},
		shadow: '',
		shape: {},
		title: 'Marker Title',
		visible: true,
		//zIndex: number
	},
	
	initialize: function(options) {
		this.setOptions(options);
		this.createMarker();
		this.addListeners();
	},	
	
	createMarker: function() {
		var location = new google.maps.LatLng(this.options.center.lat, this.options.center.lng);		
		this.markerObj = new google.maps.Marker({
			clickable: this.options.clickable,
			cursor: this.options.cursor,
			draggable: this.options.draggable,
			flat: this.options.flat,
			icon: this.options.icon,
			position: location,
			map: this.options.map,
			shadow: this.options.shadow,
			title: this.options.title,
			visible: this.options.visible,
			zIndex: this.options.zIndex
		});
	},
	
	/*------------------------- METHODS -------------------------*/
	
	getClickable: function() {
		var clickable = this.markerObj.getClickable();
		return clickable;
	},
	
	getCursor: function() {
		var cursor = this.markerObj.getCursor();
		return cursor;
	},
	
	getDraggable: function() {
		var draggable = this.markerObj.getDraggable();
		return draggable;
	},
	
	getFlat: function() {
		var flat = this.markerObj.getFlat();
		return flat;
	},
	
	getIcon: function() {
		var icon = this.markerObj.getIcon();
		return icon;
	},
	
	getMap: function() {
		var map = this.markerObj.getMap();
		return map;
	},
	
	getPosition: function() {
		var position = this.markerObj.getPosition();
		return position;
	},
	
	getShadow: function() {
		var shadow = this.markerObj.getShadow();
		return shadow;
	},
	
	getShape: function() {
		var shape = this.markerObj.getShape();
		return shape;
	},
	
	getTitle: function() {
		var title = this.markerObj.getTitle();
		return title;
	},
	
	getVisible: function() {
		var visible = this.markerObj.getVisible();
		return visible;
	},
	
	getZIndex: function() {
		var zindex = this.markerObj.getZIndex();
		return zindex;
	},
	
	setClickable: function(clickable) {
		clickable = [clickable, this.getClickable()].pick();
		this.markerObj.setClickable(clickable);
	},
	
	setCursor: function(cursorUrl) {
		cursorUrl = [cursorUrl, this.getCursor()].pick();
		this.markerObj.setCursor(cursorUrl);
	},
	
	setDraggable: function(draggable) {
		draggable = [draggable, this.getDraggable()].pick();
		this.markerObj.setDraggable(draggable)
	},
	
	setFlat: function(flat) {
		flat = [flat, this.getFlat()].pick();
		this.markerObj.setFlat(flat);
	},
	
	setIcon: function(iconUrl) {
		icon = [icon, this.getIcon()].pick();
		this.markerObj.setIcon(iconUrl);
	},
	
	setMap: function(map) {
		map = [map, this.getMap()].pick();
		this.markerObj.setMap(map);
	},
	
	configOptions: function(markerOptions) {
		this.markerObj.setOptions(markerOptions);
	},
	
	setPosition: function(position) {
		position = [position, this.getPosition()].pick();
		this.markerObj.setPosition(position);
	},
	
	setShadow: function(shadowUrl) {
		shadowUrl = [shadowUrl, this.getShadow()].pick();
		this.markerObj.setShadow();
	},
	
	setShape: function(shape) {
		shape = [shape, this.getShape()].pick();
		this.markerObj.setShape(shape);
	},
	
	setTitle: function(title) {
		title = [title, this.getTitle()].pick();
		this.markerObj.setTitle(title);
	},
	
	setVisible: function(visible) {
		visible = [visible, this.getVisible()].pick();
		this.markerObj.setVisible();
	},
	
	setZIndex: function(zindex) {
		zindex = [zindex, this.getZIndex()].pick();
		this.markerObj.setZIndex(zindex);
	},
	
	/**************************************************************
						ADDING	LISTENERS for MARKER EVENTS
	**************************************************************/
	
	addListeners: function() {
		
		/*
		Connects Google Marker listeners with MooTools class events,
		each one is described later in next section of this code (MARKER CLASS->Events).
		*/
		
		google.maps.event.addListener(this.markerObj,'click', function() {
			this.click();
		}.bind(this));
		
		google.maps.event.addListener(this.markerObj,'clickable_changed', function() {
			this.clickableChanged();
		}.bind(this));
		
		google.maps.event.addListener(this.markerObj,'cursor_changed', function() {
			this.cursorChanged();
		}.bind(this));
		
		google.maps.event.addListener(this.markerObj,'dblclick', function() {
			this.dblClick();
		}.bind(this));
		
		google.maps.event.addListener(this.markerObj,'drag', function(event) {
			this.drag(event.latLng);
		}.bind(this));
		
		google.maps.event.addListener(this.markerObj,'dragend', function(event) {
			this.dragEnd(event.latLng);
		}.bind(this));
		
		google.maps.event.addListener(this.markerObj,'draggable_changed', function() {
			this.draggableChanged();
		}.bind(this));
		
		google.maps.event.addListener(this.markerObj,'dragstart', function(event) {
			this.dragStart(event.latLng);
		}.bind(this));
		
		google.maps.event.addListener(this.markerObj,'flat_changed', function() {
			this.flatChanged();
		}.bind(this));
		
		google.maps.event.addListener(this.markerObj,'icon_changed', function() {
			this.iconChanged();
		}.bind(this));
		
		google.maps.event.addListener(this.markerObj,'mousedown', function() {
			this.mouseDown();
		}.bind(this));
		
		google.maps.event.addListener(this.markerObj,'mouseout', function() {
			this.mouseOut();
		}.bind(this));
		
		google.maps.event.addListener(this.markerObj,'mouseover', function() {
			this.mouseOver();
		}.bind(this));
		
		google.maps.event.addListener(this.markerObj,'mouseup', function() {
			this.mouseUp();
		}.bind(this));
		
		google.maps.event.addListener(this.markerObj,'position_changed', function() {
			this.positionChanged();
		}.bind(this));
		
		google.maps.event.addListener(this.markerObj,'rightclick', function() {
			this.rightClick();
		}.bind(this));
		
		google.maps.event.addListener(this.markerObj,'shadow_changed', function() {
			this.shadowChanged();
		}.bind(this));
		
		google.maps.event.addListener(this.markerObj,'shape_changed', function() {
			this.shapeChanged();
		}.bind(this));
		
		google.maps.event.addListener(this.markerObj,'title_changed', function() {
			this.titleChanged();
		}.bind(this));
		
		google.maps.event.addListener(this.markerObj,'visible_changed', function() {
			this.visibleChanged();
		}.bind(this));
		
		google.maps.event.addListener(this.markerObj,'zindex_changed', function() {
			this.zIndexChanged();
		}.bind(this));
		
	},
	
	/*------------------------- EVENTS -------------------------*/
	
	/* Click:
		This event is fired when the marker icon was clicked.
	*/
	click: function() {
		this.fireEvent('click');
	},
	
	/* ClickableChanged:
		This event is fired when the marker's clickable property changes.
	*/
	clickableChanged: function() {
		this.fireEvent('clickableChanged');
	},
	
	/* CursorChanged:
		This event is fired when the marker's cursor property changes.
	*/
	cursorChanged: function() {
		this.fireEvent('cursorChanged');
	},
	
	/* DoubleClick:
		This event is fired when the marker icon was double clicked.
	*/
	dblClick: function() {
		this.fireEvent('dblClick');
	},
	
	/* Drag:
		This event is repeatedly fired while the user drags the marker.
	*/
	drag: function(location) {
		this.fireEvent('drag', location);
	},
	
	/* DragEnd:
		This event is fired when the user stops dragging the marker.
	*/
	dragEnd: function(location) {
		this.fireEvent('dragEnd', location);
	},
	
	/* DraggableChanged:
		This event is fired when the marker's draggable property changes.
	*/
	draggableChanged: function() {
		this.fireEvent('draggableChanged');
	},
	
	/* DragStart:
		This event is fired when the user starts dragging the marker.
	*/
	dragStart: function() {
		this.fireEvent('dragStart');
	},
	
	/* FlatChanged:
		This event is fired when the marker's flat property changes.
	*/
	flatChanged: function() {
		this.fireEvent('flatChanged');
	},
	
	/* IconChanged:
		This event is fired when the marker icon property changes.
	*/
	iconChanged: function() {
		this.fireEvent('iconChanged');
	},
	
	/* MouseDown:
		This event is fired when the DOM mousedown event is fired on the marker icon.
	*/
	mouseDown: function() {
		this.fireEvent('mouseDown');
	},
	
	/* MouseOut:
		This event is fired when the mouse leaves the area of the marker icon.
	*/
	mouseOut: function() {
		this.fireEvent('mouseOut');
	},
	
	/* MouseOver:
		This event is fired when the mouse enters the area of the marker icon.
	*/
	mouseOver: function() {
		this.fireEvent('mouseOver');
	},
	
	/* MouseUp:
		This event is fired for the DOM mouseup on the marker.
	*/
	mouseUp: function() {
		this.fireEvent('mouseUp');
	},
	
	/* PositionChanged:
		This event is fired when the marker position property changes.
	*/
	positionChanged: function() {
		this.fireEvent('positionChanged');
	},
	
	/* RightClick:
		This event is fired when the marker is right clicked on.
	*/
	rightClick: function() {
		this.fireEvent('rightClick');
	},
	
	/* ShadowChanged:
		This event is fired when the marker's shadow property changes.
	*/
	shadowChanged: function() {
		this.fireEvent('shadowChanged');
	},
	
	/* ShapeChanged:
		This event is fired when the marker's shape property changes.
	*/
	shapeChanged: function() {
		this.fireEvent('shapeChanged');
	},
	
	/* TitleChanged:
		This event is fired when the marker title property changes.
	*/
	titleChanged: function() {
		this.fireEvent('titleChanged');
	},
	
	/* VisibleChanged:
		This event is fired when the marker's visible property changes.
	*/
	visibleChanged: function() {
		this.fireEvent('visibleChanged');
	},
	
	/* ZIndexChanged:
		This event is fired when the marker's zIndex property changes.
	*/
	zIndexChanged: function() {
		this.fireEvent('zIndexChanged');
	},

});

/************************************ /GoogleMapMarker Class ***********************************/


/************************************ GoogleMapInfoWindow Class ***********************************/

var GoogleMapInfoWindow = new Class({
	
	Implements: [Options, Events],
	
	options: {
		content: 'Content',
		disableAutoPan: false,
		//maxWidth: number,
		pixelOffset: new google.maps.Size(10,10),
		center: {
			lat: 7.6,
			lng: -74
		}
		//zIndex: number
	},
	
	initialize: function(options) {
		this.setOptions(options);
		this.createInfoWindow();
		this.addListeners();
	},
	
	createInfoWindow: function() {
		var location = new google.maps.LatLng(this.options.center.lat, this.options.center.lng);
		this.infoWindowObj = new google.maps.InfoWindow({
			content: this.options.content,
			disableAutoPan: this.options.disableAutoPan,
			maxWidth: this.options.maxWidth,
			pixelOffset: this.options.pixelOffset,
			position: location,
			zIndex: this.options.zIndex	
		});
	},
		
	/*------------------------- METHODS -------------------------*/
	
	close: function() {
		this.infoWindowObj.close();
	},
	
	getContent: function() {
		var content = this.infoWindowObj.getContent();
		return content;
	},
	
	getPosition: function() {
		var position = this.infoWindowObj.getPosition();
		return position;
	},
	
	getZIndex: function() {
		var zindex = this.infoWindowObj.getZIndex();
		return zindex;
	},
	
	//MVC object is usually a marker.
	open: function(map, MVCObject) {
		this.infoWindowObj.open(map, MVCObject);
	},
	
	setContent: function(content) {
		content = [content, this.getContent()].pick();
		this.infoWindowObj.setContent(content);
	},
	
	configOptions: function(infoWindowOptions) {
		this.infoWindowObj.setOptions(infoWindowOptions);
	},
	
	setPosition: function(position) {
		position = [position, this.getPosition()].pick();
		this.infoWindowObj.setPosition(position);
	},
	
	setZIndex: function(zindex) {
		zindex = [zindex, this.getZIndex()].pick();
		this.infoWindowObj.setZIndex(zindex);
	},

	
	/**************************************************************
				ADDING	LISTENERS for INFOWINDOW EVENTS
	**************************************************************/
	
	addListeners: function() {
		
		/*
		Connects Google InfoWindow listeners with MooTools class events,
		each one is described later in next section of this code (INFOWINDOW CLASS->Events).
		*/
		
		google.maps.event.addListener(this.infoWindowObj,'closeclick', function() {
			this.closeClick();
		}.bind(this));
		
		google.maps.event.addListener(this.infoWindowObj,'content_changed', function() {
			this.contentChanged();
		}.bind(this));
		
		google.maps.event.addListener(this.infoWindowObj,'domready', function() {
			this.domReady();
		}.bind(this));
		
		google.maps.event.addListener(this.infoWindowObj,'position_changed', function() {
			this.positionChanged();
		}.bind(this));
		
		google.maps.event.addListener(this.infoWindowObj,'zindex_changed', function() {
			this.ZIndexChanged();
		}.bind(this));
		
	},
	/*------------------------- EVENTS -------------------------*/
	
	/* CloseClick:
		This event is fired when the close button was clicked.
	*/
	closeClick: function() {
		this.fireEvent('closeClick');
	},
	
	/* ContentChanged:
		This event is fired when the content property changes.
	*/
	contentChanged: function() {
		this.fireEvent('contentChanged');
	},
	
	/* DOMReady:
		This event is fired when the <div> containing the InfoWindow's content is attached to the DOM.
		You may wish to monitor this event if you are building out your info window content dynamically.
	*/
	domReady: function() {
		this.fireEvent('domReady');
	},
	
	/* PositionChanged:
		This event is fired when the position property changes.
	*/
	positionChanged: function() {
		this.fireEvent('positionChanged');
	},
	
	/* ZIndexChanged:
		This event is fired when the InfoWindow's zIndex changes.
	*/
	ZIndexChanged: function() {
		this.fireEvent('ZIndexChanged');
	}	

});

/************************************ /GoogleMapInfoWindow Class ***********************************/

/************************************ GoogleMapCircle Class ***********************************/

var GoogleMapCircle = new Class({
	
	Implements: [Options, Events],
	
	options: {
		clickable: true,
		center: {
			lat: 7.6,
			lng: -74
		},
		fillColor: '#000000',
		fillOpacity: 0.3,
		map: null,
		radius: 100000,
		strokeColor: '#000000',
		strokeOpacity: 0.8,
		strokeWeight: 2
		//zIndex: number
	},
	
	initialize: function(options) {
		this.setOptions(options);
		this.createCircle();
		this.addListeners();
	},
	
	createCircle: function() {
		var location = new google.maps.LatLng(this.options.center.lat, this.options.center.lng);
		this.circleObj = new google.maps.Circle({
			center: location,
			clickable: this.options.clickable,
			fillColor: this.options.fillColor,
			fillOpacity: this.options.fillOpacity,
			map: this.options.map,
			radius: this.options.radius,
			strokeColor: this.options.strokeColor,
			strokeOpacity: this.options.strokeOpacity,
			strokeWeight: this.options.strokeWeight,
			zIndex: this.options.zIndex
		});
	},
		
	/*------------------------- METHODS -------------------------*/
	
	getBounds: function() {
		var bounds = this.circleObj.getBounds();
		return bounds;
	},
	
	getCenter: function() {
		var center = this.circleObj.getCenter();
		return center;
	},
	
	getMap: function() {
		var map = this.circleObj.getMap();
		return map;
	},
	
	getRadius: function() {
		var radius = this.circleObj.getRadius();
		return radius;
	},
	
	setCenter: function(center) {
		center = [center, this.getCenter()].pick();
		this.circleObj.setCenter(center);
	},
	
	setMap: function(map) {
		map = [map, this.getMap()].pick();
		this.circleObj.setMap(map);
	},
	
	configOptions: function(circleOptions) {
		this.circleObj.setOptions(circleOptions);
	},
	
	setRadius: function(radius) {
		radius = [radius, this.getRadius()].pick();
		this.circleObj.setRadius(radius);
	},
	
	/**************************************************************
				ADDING	LISTENERS for CIRCLE EVENTS
	**************************************************************/
	
	addListeners: function() {
		
		/*
		Connects Google Circle listeners with MooTools class events,
		each one is described later in next section of this code (CIRCLE CLASS->Events).
		*/
		
		google.maps.event.addListener(this.circleObj,'click', function(event) {
			this.click(event.latLng);
		}.bind(this));
		
		google.maps.event.addListener(this.circleObj,'dblclick', function(event) {
			this.dblClick(event.latLng);
		}.bind(this));
		
		google.maps.event.addListener(this.circleObj,'mousedown', function(event) {
			this.mouseDown(event.latLng);
		}.bind(this));
		
		google.maps.event.addListener(this.circleObj,'mousemove', function(event) {
			this.mouseMove(event.latLng);
		}.bind(this));
		
		google.maps.event.addListener(this.circleObj,'mouseout', function(event) {
			this.mouseOut(event.latLng);
		}.bind(this));
		
		google.maps.event.addListener(this.circleObj,'mouseover', function(event) {
			this.mouseOver(event.latLng);
		}.bind(this));
		
		google.maps.event.addListener(this.circleObj,'mouseUp', function(event) {
			this.mouseUp(event.latLng);
		}.bind(this));
		
		google.maps.event.addListener(this.circleObj,'rightclick', function(event) {
			this.rightClick(event.latLng);
		}.bind(this));
		
		
	},
	
	/*------------------------- EVENTS -------------------------*/
	
	/* Click:
		This event is fired when the DOM click event is fired on the Circle.
	*/
	click: function(location) {
		this.fireEvent('click', location);
	},
	
	/* DoubleClick:
		This event is fired when the DOM dblclick event is fired on the Circle.
	*/
	dblClick: function(location) {
		this.fireEvent('dblClick', location);
	},
	
	/* MouseDown:
		This event is fired when the DOM mousedown event is fired on the Circle.
	*/
	mouseDown: function(location) {
		this.fireEvent('mouseDown', location);
	},
	
	/* MouseMove:
		This event is fired when the DOM mousemove event is fired on the Circle.
	*/
	mouseMove: function(location) {
		this.fireEvent('mouseMove', location);
	},
	
	/* MouseOut:
		This event is fired on Circle mouseout.
	*/
	mouseOut: function(location) {
		this.fireEvent('mouseOut', location);
	},
	
	/* MouseOver:
		This event is fired on Circle mouseover.
	*/
	mouseOver: function(location) {
		this.fireEvent('mouseOver', location);
	},
	
	/* MouseUp:
		This event is fired when the DOM mouseup event is fired on the Circle.
	*/
	mouseUp: function(location) {
		this.fireEvent('mouseUp', location);
	},
	
	/* RightClick:
		This event is fired when the Circle is right-clicked on.
	*/
	rightClick: function(location) {
		this.fireEvent('rightClick', location);
	}
	
});

/************************************ /GoogleMapCircle Class ***********************************/

/************************************ GoogleMapRectangle Class ***********************************/

var GoogleMapRectangle = new Class({
	
	Implements: [Options, Events],
	
	options: {
		bounds: null,
		clickable: true,
		fillColor: '#000000',
		fillOpacity: 0.3,
		map: null,
		strokeColor: '#000000',
		strokeOpacity: 0.8,
		strokeWeight: 2
		//zindex: number
	},
	
	initialize: function(options) {
		this.setOptions(options);
		this.createRectangle();
		this.addListeners();
	},
	
	createRectangle: function() {
		var location = new google.maps.LatLngBounds(new google.maps.LatLng(11.04,-75.75), new google.maps.LatLng(10.9,-74.8));
		this.rectangleObj = new google.maps.Rectangle({
			bounds: [this.options.bounds, location].pick(),
			clickable: this.options.clickable,
			fillColor: this.options.fillColor,
			fillOpacity: this.options.fillOpacity,
			map: this.options.map,
			strokeColor: this.options.strokeColor,
			strokeOpacity: this.options.strokeOpacity,
			strokeWeight: this.options.strokeWeight,
			zIndex: this.options.zIndex
		});
	},
		
	/*------------------------- METHODS -------------------------*/
	
	getBounds: function() {
		var bounds = this.rectangleObj.getBounds();
		return bounds;
	},
	
	getMap: function() {
		var map = this.rectangleObj.getMap();
		return map;
	},
	
	setBounds: function(bounds) {
		bounds = [bounds, this.getBounds()].pick();
		this.rectangleObj.setBounds(bounds);
	},
	
	setMap: function(map) {
		map = [map, this.getMap()].pick();
		this.rectangleObj.setMap(map);
	},
	
	configOptions: function(rectangleOptions) {
		this.rectangleObj.setOptions(rectangleOptions);
	},

	
	/**************************************************************
				ADDING	LISTENERS for RECTANGLE EVENTS
	**************************************************************/
	
	addListeners: function() {
		
		/*
		Connects Google Rectangle listeners with MooTools class events,
		each one is described later in next section of this code (RECTANGLE CLASS->Events).
		*/
		
		google.maps.event.addListener(this.rectangleObj,'click', function(event) {
			this.click(event.latLng);
		}.bind(this));
		
		google.maps.event.addListener(this.rectangleObj,'dblclick', function(event) {
			this.dblClick(event.latLng);
		}.bind(this));
		
		google.maps.event.addListener(this.rectangleObj,'mousedown', function(event) {
			this.mouseDown(event.latLng);
		}.bind(this));
		
		google.maps.event.addListener(this.rectangleObj,'mousemove', function(event) {
			this.mouseMove(event.latLng);
		}.bind(this));
		
		google.maps.event.addListener(this.rectangleObj,'mouseout', function(event) {
			this.mouseOut(event.latLng);
		}.bind(this));
		
		google.maps.event.addListener(this.rectangleObj,'mouseover', function(event) {
			this.mouseOver(event.latLng);
		}.bind(this));
		
		google.maps.event.addListener(this.rectangleObj,'mouseUp', function(event) {
			this.mouseUp(event.latLng);
		}.bind(this));
		
		google.maps.event.addListener(this.rectangleObj,'rightclick', function(event) {
			this.rightClick(event.latLng);
		}.bind(this));
		
		
	},
	
	/*------------------------- EVENTS -------------------------*/
	
	/* Click:
		This event is fired when the DOM click event is fired on the Rectangle.
	*/
	click: function(location) {
		this.fireEvent('click', location);
	},
	
	/* DoubleClick:
		This event is fired when the DOM dblclick event is fired on the Rectangle.
	*/
	dblClick: function(location) {
		this.fireEvent('dblClick', location);
	},
	
	/* MouseDown:
		This event is fired when the DOM mousedown event is fired on the Rectangle.
	*/
	mouseDown: function(location) {
		this.fireEvent('mouseDown', location);
	},
	
	/* MouseMove:
		This event is fired when the DOM mousemove event is fired on the Rectangle.
	*/
	mouseMove: function(location) {
		this.fireEvent('mouseMove', location);
	},
	
	/* MouseOut:
		This event is fired on Rectangle mouseout.
	*/
	mouseOut: function(location) {
		this.fireEvent('mouseOut', location);
	},
	
	/* MouseOver:
		This event is fired on Rectangle mouseover.
	*/
	mouseOver: function(location) {
		this.fireEvent('mouseOver', location);
	},
	
	/* MouseUp:
		This event is fired when the DOM mouseup event is fired on the Rectangle.
	*/
	mouseUp: function(location) {
		this.fireEvent('mouseUp', location);
	},
	
	/* RightClick:
		This event is fired when the Rectangle is right-clicked on.
	*/
	rightClick: function(location) {
		this.fireEvent('rightClick', location);
	}
	
	
});

/************************************ /GoogleMapRectangle Class ***********************************/

/************************************ GoogleMapPolyLine Class ***********************************/

var GoogleMapPolyLine = new Class({
	
	Implements: [Options, Events],
	
	options: {
		clickable: true,
		geodesic: true,
		map: null,
		path: [], // Empty path.
		strokeColor: '#000000',
		strokeOpacity: 0.8,
		strokeWeight: 2,
		//zindex: number
	},
	
	initialize: function(options) {
		this.setOptions(options);
		this.createPolyLine();
		this.addListeners();
	},
	
	createPolyLine: function() {
		this.polyLineObj = new google.maps.Polyline({
			clickable: this.options.clickable,
			geodesic: this.options.geodesic,
			map: this.options.map,
			path: this.options.path,
			strokeColor: this.options.strokeColor,
			strokeOpacity: this.options.strokeOpacity,
			strokeWeight: this.options.strokeWeight,
			zIndex: this.options.zIndex
		});
	},
		
	/*------------------------- METHODS -------------------------*/
	
	getMap: function() {
		var map = this.polyLineObj.getMap();
		return map;
	},
	
	// Retrieves the first path.
	getPath: function() {
		var path = this.polyLineObj.getPath();
		return path;
	},
	
	setMap: function(map) {
		var map = [map, this.getMap()].pick();
		this.polyLineObj.setMap(map);
	},
	
	configOptions: function(polyLineOptions) {
		this.polyLineObj.setOptions(polyLineOptions);
	},
	
	// Sets the first path.
	setPath: function(path) {
		path = [path, this.getPath()].pick();
		this.polyLineObj.setPath(path);
	},
	
	// Adds one element to the end of the array and returns the new length of the array.
	addLine: function(latLng) {
		var path = this.getPath();
		var length = path.push(latLng);
		this.setPath(path);
		return length;
	},
	
	// Inserts an element at the specified index.
	insertLineAt: function(index, latLng) {
		var path = this.getPath();
		path.insertAt(index, latLng); 
		this.setPath(path);
	},
	
	// Removes the last element of the array and returns that element.
	removeLastLine: function() {
		var path = this.getPath();
		var poppedLine = path.pop();
		this.setPath(path);
		return poppedLine;
	},
	
	// Returns the number of elements in this array.
	getLength: function() {
		var path = this.getPath();
		var length = path.getLength();
		return length;
	},
	
	// Removes an element from the specified index.
	removetLineAt: function(index) {
		var path = this.getPath();
		path.removeAt(index); 
		this.setPath(path);
	},
	
	// Sets an element at the specified index.
	setLineAt: function(index, latLng) {
		path = this.getPath();
		path.setAt(index, latLng);
		this.setPath(path);
	},
	
	// Get an element at the specified index.
	getLineAt: function(index) {
		path = this.getPath();
		var line = path.getAt(index);
		return line;
	},
	
	/**************************************************************
				ADDING	LISTENERS for POLYLINE EVENTS
	**************************************************************/
	
	addListeners: function() {
		
		/*
		Connects Google PolyLine listeners with MooTools class events,
		each one is described later in next section of this code (POLYLINE CLASS->Events).
		*/
		
		google.maps.event.addListener(this.polyLineObj,'click', function(event) {
			this.click(event.latLng);
		}.bind(this));
		
		google.maps.event.addListener(this.polyLineObj,'dblclick', function(event) {
			this.dblClick(event.latLng);
		}.bind(this));
		
		google.maps.event.addListener(this.polyLineObj,'mousedown', function(event) {
			this.mouseDown(event.latLng);
		}.bind(this));
		
		google.maps.event.addListener(this.polyLineObj,'mousemove', function(event) {
			this.mouseMove(event.latLng);
		}.bind(this));
		
		google.maps.event.addListener(this.polyLineObj,'mouseout', function(event) {
			this.mouseOut(event.latLng);
		}.bind(this));
		
		google.maps.event.addListener(this.polyLineObj,'mouseover', function(event) {
			this.mouseOver(event.latLng);
		}.bind(this));
		
		google.maps.event.addListener(this.polyLineObj,'mouseUp', function(event) {
			this.mouseUp(event.latLng);
		}.bind(this));
		
		google.maps.event.addListener(this.polyLineObj,'rightclick', function(event) {
			this.rightClick(event.latLng);
		}.bind(this));
				
		
	},
	
	/*------------------------- EVENTS -------------------------*/
	
	/* Click:
		This event is fired when the DOM click event is fired on the PolyLine.
	*/
	click: function(location) {
		this.fireEvent('click', location);
	},
	
	/* DoubleClick:
		This event is fired when the DOM dblclick event is fired on the PolyLine.
	*/
	dblClick: function(location) {
		this.fireEvent('dblClick', location);
	},
	
	/* MouseDown:
		This event is fired when the DOM mousedown event is fired on the PolyLine.
	*/
	mouseDown: function(location) {
		this.fireEvent('mouseDown', location);
	},
	
	/* MouseMove:
		This event is fired when the DOM mousemove event is fired on the PolyLine.
	*/
	mouseMove: function(location) {
		this.fireEvent('mouseMove', location);
	},
	
	/* MouseOut:
		This event is fired on PolyLine mouseout.
	*/
	mouseOut: function(location) {
		this.fireEvent('mouseOut', location);
	},
	
	/* MouseOver:
		This event is fired on PolyLine mouseover.
	*/
	mouseOver: function(location) {
		this.fireEvent('mouseOver', location);
	},
	
	/* MouseUp:
		This event is fired when the DOM mouseup event is fired on the PolyLine.
	*/
	mouseUp: function(location) {
		this.fireEvent('mouseUp', location);
	},
	
	/* RightClick:
		This event is fired when the PolyLine is right-clicked on.
	*/
	rightClick: function(location) {
		this.fireEvent('rightClick', location);
	}
	
	
});

/************************************ /GoogleMaPolyLine Class ***********************************/


/************************************ WIDGETS ***********************************/


/************************************ DistanceWidget ***********************************/
var DistanceWidget = new Class({
	
	Extends: google.maps.MVCObject,
	Implements: [Options, Events],
	
	options: {
		
	},
	
	initialize: function(map, options) {
		this.set('map', map);
		this.position = map.getCenter();
		this.setOptions(options);
		this.constructWidget();
		this.addListeners();
	},
	
	constructWidget: function() {
		var marker = new google.maps.Marker({
			draggable: true,
			title: 'Move me!'
		});
		
		// Bind the marker map property to the DistanceWidget map property.
		marker.bindTo('map', this);
		
		// Bind the marker position property to the DistanceWidget position property.
		marker.bindTo('position', this);
		
		// Create a new radius widget.
		var radiusWidget = new RadiusWidget();
		
		// Bind the radiusWidget map to the DistanceWidget map.
		radiusWidget.bindTo('map', this);
		
		// Bind the radiusWidget center to the DistanceWidget position.
		radiusWidget.bindTo('center', this, 'position');
		
		// Bind to the radiusWidgets distance property
		this.bindTo('distance', radiusWidget);

		// Bind to the radiusWidgets bounds property
		this.bindTo('bounds', radiusWidget);
	},
	
	addListeners: function() {
		
		google.maps.event.addListener(this, 'distance_changed', function() {
		  displayInfo(this);
		}.bind(this));

		google.maps.event.addListener(this, 'position_changed', function() {
		  displayInfo(this);
		}.bind(this));
	}
	
});

/************************************ RadiusWidget ***********************************/
var RadiusWidget = new Class({
	
	Extends: google.maps.MVCObject,
	Implements: [Options, Events],
	
	options: {
		
	},
	
	initialize: function(options) {
		this.setOptions(options);
		this.constructWidget();
		this.addSizer_();
	},
	
	constructWidget: function() {
		var circle = new google.maps.Circle({
			strokeWeight: 2
		});
		
		// Set the distance property value, default to 50km.
		this.set('distance', 50);
		
		// Bind the RadiusWidget bounds property to the circle bounds property.
		this.bindTo('bounds', circle);
		
		// Bind the circle center to the RadiusWidget center property.
		circle.bindTo('center', this);
		
		// Bind the circle map to the RadiusWidget map.
		circle.bindTo('map', this);
		
		// Bind the circle radius property to the RadiusWidget radius property.
		circle.bindTo('radius', this);
	},
	
	// Add the sizer marker to the map.
	addSizer_: function() {
		var sizerMarker = new google.maps.Marker({
			draggable: true,
			title: 'Drag me!'
		});
		
		sizerMarker.bindTo('map', this);
		sizerMarker.bindTo('position', this, 'sizerMarker_position');
		
		// Add Drag event to the sizerMarker.
		google.maps.event.addListener(sizerMarker, 'drag', function() {
			// Set the circle distance (radius).
			this.setDistance();
		}.bind(this));
	},
		
	/*	Update the center of the circle and position the sizer back on the line.
		'Position' is bound to the DistanceWidget so this is expected to change when
		the position of the distance widget is changed.
	*/
	center_changed: function() {
		var bounds = this.get('bounds');
		
		// Bounds might not always be set so check that it exists first.
		if(bounds) {
			var lng = bounds.getNorthEast().lng();
			
			// Put the sizer at center, right on the circle.
			var position = new google.maps.LatLng(this.get('center').lat(), lng);
			this.set('sizerMarker_position', position);
		}
	},
	
	// Update the radius when the distance has changed.
	distance_changed: function() {
		this.set('radius', this.get('distance') * 1000);
	},
	
	// Set the distance of the circle based on the position of the sizer.
	setDistance: function() {
		// As the sizer is being dragged, its position changes.  Because the
		// RadiusWidget's sizer_position is bound to the sizer's position, it will
		// change as well.
		
		var pos = this.get('sizerMarker_position');
		var center = this.get('center');
		var distance = this.distanceBetweenPoints_(center, pos);
		
		// Set the distance property for any objects that are bound to it.
		this.set('distance', distance);
	},
	
	
	/**
	 * Calculates the distance between two latlng locations in km.
	 * @see http://www.movable-type.co.uk/scripts/latlong.html
	 *
	 * @param {google.maps.LatLng} p1 The first lat lng point.
	 * @param {google.maps.LatLng} p2 The second lat lng point.
	 * @return {number} The distance between the two points in km.
	 * @private
	*/
	distanceBetweenPoints_: function(p1, p2) {
	  if (!p1 || !p2) {
		return 0;
	  }

	  var R = 6371; // Radius of the Earth in km
	  var dLat = (p2.lat() - p1.lat()) * Math.PI / 180;
	  var dLon = (p2.lng() - p1.lng()) * Math.PI / 180;
	  var a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
		Math.cos(p1.lat() * Math.PI / 180) * Math.cos(p2.lat() * Math.PI / 180) *
		Math.sin(dLon / 2) * Math.sin(dLon / 2);
	  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
	  var d = R * c;
	  return d;
	}
	
});

/************************************ /WIDGETS ***********************************/

/* FUNCTIONS*/

function displayInfo(widget) {
  var info = document.getElementById('info');
  info.innerHTML = 'Position: ' + widget.get('position') + ', distance: ' +
    widget.get('distance');
}

/* /FUNCTIONS */

/*********************************** DOMREADY FUNCTION *********************************
 Description: Do stuff when the document has loaded but images have not yet.
 ***************************************************************************************/

window.addEvent('domready', function() {
		
	/*----------------------------------------------------
		GLOBAL VARIABLES
	----------------------------------------------------*/
	
	var body = $(document.body);
	
	/*----------------------------------------------------
		GLOBAL EFFECTS
	----------------------------------------------------*/
	
	$('wrapper').setStyle('height', (body.getSize().y - 80));
	
	var map = new GoogleMapCreator($('map_canvas'), {
		streetViewControl: false
	});
		
	map.addEvents({	
		click: function(pos) {
			alert('Map clicked at: ' + pos);
		},
		rightClick: function(pos) {
			alert('Map right clicked at: ' + pos);
		}
	});
		
	var b = map.createMarker({
		center: {
			lat: 8,
			lng: -70,
		},
		draggable: true,
		title: 'Draggable Marker'
	}).addEvents({
		click: function() {
			alert('Marker clicked!');
		},
		dragEnd: function(pos) {
			alert('You\'ve just thrown this marker at ' + pos)
		}
	});
	
	var c = map.createInfoMarker({
		center: {
			lat: 7,
			lng: -72
		},
		title: 'InfoMarker'
	},
	{
		content: "This is the infoWindow content"
	});
		
	var distanceWidget = new DistanceWidget(map.mapObj);
	var polyLine = map.createPolyLine([[9,-75],[9,-79],[8,-79]]);
	
	var btn = $('actionBtn');
	btn.addEvent('click', function() {
		// do testing action.
		
	});
	
	
});
/******************************** END of DOMREADY FUNCTION *****************************/
/***************************************************************************************/

/*********************************** LOAD FUNCTION *************************************
 Description: Do stuff when the document has loaded along with images and other stuff.
 ***************************************************************************************/

window.addEvent('load', function(){ 
  // do stuff when the document has loaded along with images and other stuff 
});

/********************************** END of LOAD FUNCTION *******************************/
/***************************************************************************************/