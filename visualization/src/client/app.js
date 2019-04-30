const express = require("express");
const app = express();
const Node = require('./node.model');

app.get('/', async function (req,res){
  const cars = await Node.findOne({where:{ip_addr:'258'}});
  res.json(cars);
});

app.get('/newNode', async function (req, res) {
  console.log(req.body);
  const node = await Node.create({
    ip_addr: 258,
    longtitude: 38.4,
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

app.listen(8080, function(){
  console.log("listening on port." + 8080);
})
