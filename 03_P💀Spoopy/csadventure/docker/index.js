const express = require('express');

var app = express();

app.use(express.static('public'));

app.use((req, res, next) => {
    res.header('Server', 'dunno');
    res.header('X-Powered-By', 'love <3');
    res.header('Level', (9000 + Math.random() * 1000).toFixed(0));
    next();
});

//Troll
app.use('/admin', function (req, res) {
    res.status(401).send();
});
app.use('/phpMyAdmin', function (req, res) {
    res.status(402).send();
});
app.use('/test.php', function (req, res) {
    res.status(parseInt(Math.random() * 1000)).send();
});

//Custom 404
app.get('*', function (req, res) {
    res.status(404).send('notfound.jpeg');
});

app.listen(8080, ()=>{
    console.log("Listening...");
});