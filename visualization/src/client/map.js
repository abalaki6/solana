function Datamap() {
    this.$container = $("#container");
    this.instance = new Datamaps({
        scope: 'world',
        element: this.$container.get(0),
        projection: 'mercator',
        geographyConfig: {
            popupOnHover: false,
            highlightOnHover: false
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


bubbles = new Array(50)

for (let i = 0; i < bubbles.length; i++) {
    rad = Math.ceil(30 * Math.random());
    key = rad / 30;
    key = datamap.get_fillKey(key);
    lat = Math.random() * 120 - 60;
    long = Math.random() * 120 - 60;
    bubbles[i] = {
        radius: rad,
        fillKey: key,
        latitude: lat,
        longitude: long,
        number_of_nodes: rad
    }
}

datamap.instance.bubbles(
    bubbles,
    {
        popupTemplate: function (geo, data) {
            return '<div class="hoverinfo">' + data.number_of_nodes;
        }
    }
);
