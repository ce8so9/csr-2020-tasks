var express = require('express');
var router = express.Router();
var RegexEr = require('./regexer')

router.get('/regex/:pattern/:flags/:input', (req, res) => {
    var params = {
        pattern: req.params.pattern,
        input: req.params.input,
        flags: req.params.flags
    };
    try {
        params.pattern = Buffer.from(req.params.pattern, 'base64').toString();
        params.input = Buffer.from(req.params.input, 'base64').toString().replace(/\n/gm, "").trim();
        params.flags = Buffer.from(req.params.flags, 'base64').toString();
        RegexEr.process(params.pattern, params.flags, params.input)
            .then((result) => res.status(200).send({result: result}))
            .catch((err) => res.status(400).send({ error: err.message }));

    } catch (ex) {
        console.error(ex);
        res.status(400).send(JSON.stringify(ex));
    }

});

module.exports = router;