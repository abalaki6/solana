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

app.get('/d.json', function (req, res){
  con.query("SELECT longitude, latitude, map_depth, node_size FROM NODES_TEST_CLUSTER",
  function (err, result, fields) {
    if (err) {
      return next(err);
    }
    const all_features_on_level_zero = [];
    const all_features_on_level_one = [];
    const all_features_on_level_two = [];
    const all_features_on_level_three = [];
    const all_features_on_level_four = [];

    result.forEach(res => {
      // console.log(res);
      const newRes = {};
      newRes.type = 'Feature';
      newRes.properties = {};
      newRes.geometry = {};
      newRes.geometry.type = "Point";
      newRes.geometry.coordinates = [];
      newRes.geometry.coordinates.push(res.latitude);
      newRes.geometry.coordinates.push(res.longitude);
      newRes.node_size = res.node_size;
      if(res.map_depth==0){
        all_features_on_level_zero.push(newRes);
      }
      if(res.map_depth==1){
        all_features_on_level_one.push(newRes);
      }
      if(res.map_depth==2){
        all_features_on_level_two.push(newRes);
      }
      if(res.map_depth==3){
        all_features_on_level_three.push(newRes);
      }
      if(res.map_depth==4){
        all_features_on_level_four.push(newRes);
      }
    }
    );
  const final = {
    levels: [
      {
	      type: 'FeatureCollection', features: all_features_on_level_zero
      },
      {
	      type: 'FeatureCollection', features: all_features_on_level_one
      },
      {
	      type: 'FeatureCollection', features: all_features_on_level_two
      },
      {
	      type: 'FeatureCollection', features: all_features_on_level_three
      },
      {
	      type: 'FeatureCollection', features: all_features_on_level_four
      }
    ]
  };
  res.json(final)
});
})

app.use('/', express.static(path.join(__dirname, 'public')));

app.use(function(req, res, next) {
  return next(new Error('not found'));
});

app.use(function(req, res, next, err) {
  res.json(err.message);
});

app.listen(80, function(){
})
