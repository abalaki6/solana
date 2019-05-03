const express = require('express');
const app = express();
const Node = require('./node.model');
var path = require('path');
var mysql = require('mysql');

app.use(express.static(path.join(__dirname, 'public')));


app.get('/', function (req,res){
  res.sendFile('index.html');
});


var con = mysql.createConnection({
  host: "localhost",
  user: "UIUC",
  password: "UIUC_492",
  database: "SOLANA"
});


con.connect(function(err) {
  if (err) throw err;
  con.query("SELECT longitude, latitude, map_depth, node_size FROM NODES_TEST_CLUSTER", function (err, result, fields) {
    if (err) throw err;
    console.log(result);
  });
});



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
