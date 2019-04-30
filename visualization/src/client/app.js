var express = require('express');
var app = express();
var path = require('path');

app.use(express.static(path.join(__dirname, 'public')));

// viewed at http://localhost:8080
app.get('/', function (req, res) {
    res.sendFile('index.html');
});

app.listen(80);
