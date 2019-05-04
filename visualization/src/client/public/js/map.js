function Datamap() {
    this.$container = $("#container");
    this.instance = new Datamaps({
        scope: 'world',
        element: this.$container.get(0),
        projection: 'mercator',
        geographyConfig: {
            popupOnHover: false,
            highlightOnHover: false,
            borderWidth: 0.1,
        },
        fills: {
            defaultFill: 'grey',
            s1: '#f7fbff',
            s2: '#deebf7',
            s3: '#c6dbef',
            s4: '#9ecae1',
            s5: '#9ecae1',
            s6: '#4292c6',
            s7: '#2171b5',
            s8: '#08519c',
            s9: '#08306b'
        },
        done: this._handleMapReady.bind(this),
        bubblesConfig: {
            borderWidth: 1,
            borderOpacity: 0.5,
            borderColor: 'black',
        },
    });

}

Datamaps.prototype.update_level = function (level) {
    for (let i = 0; i < this.levels.length; i++) {
        if (level == this.levels[i]) {
            if (i == this.current_level) {
                return;
            }
            console.log("update level to " + i);
            this.current_level = i;
            return this._set_level(i);
        }
    }
}

Datamaps.prototype._set_level = function (level) {
    try {
        json = this.responce.responseJSON;
        return create_bubles(json.levels[level], 1);
    }
    catch{

    }
}


Datamap.prototype._handleMapReady = function (datamap) {
    datamap.levels = new Array(0, 20, 40, 70);
    datamap.current_level = -1;

    this.zoom = new Zoom({
        $container: this.$container,
        datamap: datamap
    });


    this.get_fillKey = function (val) {
        return 's' + (1 + Math.floor(d3.interpolate(0, 8)(val)));
    }
}

datamap = new Datamap();


datamap.instance.responce = $.getJSON("d.json", function () {
})
    .done(function (data) {
        create_bubles(data.levels[0]);
    })
    .fail(function () {
        console.log("Failed to load json");
    });

function create_bubles(d, max_radius = 20) {
    $("#container").find("svg").find("g.bubbles").empty()
    features = d.features;
    bubbles = new Array(features.length);
    for (let i = 0; i < bubbles.length; i++) {
        xy = features[i].geometry.coordinates;
        // rad = Math.ceil(max_radius * Math.random());
        // console.log(rad);
        number_of_nodes = features[i].node_size;
        //rad = max_radius * 5> number_of_nodes ? max_radius : Math.sqrt(number_of_nodes) / 5;
        rad = Math.min(Math.sqrt(number_of_nodes) * 2, 20); 
	key = rad / 20;
        key = datamap.get_fillKey(key);
        bubbles[i] = {
            radius: rad,
            fillKey: key,
            latitude: xy[1],
            longitude: xy[0],
            number_of_nodes: number_of_nodes
        };
    }
    datamap.instance.bubbles(
        bubbles,
        {
            popupTemplate: function (geo, data) {
                return '<div class="hoverinfo"> Number of nodes: ' + data.number_of_nodes;
            }
        }
    );
}
