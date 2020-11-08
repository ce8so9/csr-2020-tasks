var express = require('express');
var cors = require('cors');

var app = express();
var api = require('./api')

app.use(cors());

process.on('unhandledRejection', (reason, promise) => {
    console.log('Unhandled Rejection at:', reason.stack || reason)
})


process.on('uncaughtException', function (err) {
    console.error(err.stack);
});

app.use((req, res, next) => {
    res.header('Server', 'dunno');
    res.header('X-Powered-By', 'love <3');
    res.header('Level', (9000 + Math.random() * 1000).toFixed(0));
    next();
});

//Static
app.use(express.static('dist'));

//rest
app.use('/api', api);

//Troll
app.use('/admin', function (req, res) {
    res.status(401).send();
});
app.use('/phpMyAdmin', function (req, res) {
    res.status(402).send();
});
app.use('/test.php', function (req, res) {
    res.status(403).send();
});

//Custom 404
app.get('*', function (req, res) {
    res.status(404).send('notfound.jpeg');
});

app.listen(8080, () => {
    console.log(`Listening...`)
});