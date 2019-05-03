const express = require('express');
const app = express();
const Node = require('./node.model');
var path = require('path');
var mysql = require('mysql');
const fs = require('fs');

var con = mysql.createConnection({
  host: "localhost",
  user: "UIUC",
  password: "UIUC_492",
  database: "SOLANA"
});

function pullData(req,res, next) {
    con.query("SELECT longitude, latitude, map_depth, node_size FROM NODES_TEST_CLUSTER",
    function (err, result, fields) {
      if (err) {
        return next(err);
        // throw err;
      }
      const features = [];
      result.forEach(res => {
        console.log(res);
        const newRes = {};
        newRes.type = 'Feature';
        newRes.properties = {};
        newRes.geometry = {};
        newRes.geometry.type = "Point";
        newRes.geometry.coordinates = [];
        newRes.geometry.coordinates.push(res.latitude);
        newRes.geometry.coordinates.push(res.longitude);
        newRes.geometry.depth = res.map_depth;
        newRes.geometry.radius = res.node_size;
        features.push(newRes);
      });
    const final = {levels: [{type: 'FeatureCollection', features}]};
    fs.writeFileSync('./public/d.json', JSON.stringify(final));
    });
    next();

};


app.use('/', pullData, express.static(path.join(__dirname, 'public')));


app.get('/newNode', async function (req, res) {
  const node = await Node.create({
    ip_addr: 258,
    longitude: 38.4,
    latitude: 25.6,
    city:'champaign',
    region:'latea',
    country:'US',
    ping_time:888,
    slot_height:250,
    transaction_count:24,
    stake_weight:23.4,
  });
  res.json(node);
});

app.use(function(req, res, next) {
  return next(new Error('not found'));
});

app.use(function(req, res, next, err) {
  res.json(err.message);
});

app.listen(8000, function(){
  console.log("listening on port." + 8000);
})
