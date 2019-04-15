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

    this.instance.bubbles([
        {
            radius: 1,
            fillKey: 'LARGE',
            latitude: 73.482,
            longitude: 54.5854,
            number_of_nodes: 50
        }
    ], {
            popupTemplate: function (geo, data) {
                return '<div class="hoverinfo">' + data.number_of_nodes;
            }
        });
}

Datamap.prototype._handleMapReady = function (datamap) {
    this.zoom = new Zoom({
        $container: this.$container,
        datamap: datamap
    });

    this.get_fillKey = function (val) {
        return 's' + Math.floor(d3.interpolate(0, 9)(val));
    }
}

datamap = new Datamap();


$.getJSON("d.json", function () {
})
    .done(function (data) {
        create_bubles(data)
    })
    .fail(function () {
        console.log("Failed to load json");
    });

function create_bubles(d) {
    features = d.features
    bubbles = new Array(features.length)
    for (let i = 0; i < bubbles.length; i++) {
        xy = features[i].geometry.coordinates

        rad = Math.ceil(20 * Math.random());
        key = rad / 20;
        key = datamap.get_fillKey(key);
        bubbles[i] = {
            radius: rad + 2,
            fillKey: key,
            latitude: xy[1],
            longitude: xy[0],
            number_of_nodes: rad * rad
        }
    }
    datamap.instance.bubbles(
        bubbles,
        {
            popupTemplate: function (geo, data) {
                return '<div class="hoverinfo"> density:' + data.number_of_nodes;
            }
        }
    );
}

// $("#container").find("svg").find("g.bubbles").empty()
