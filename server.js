const command = require("./command");

const app = require('express')();
const bodyParser = require('body-parser');

app.use(bodyParser.json()); // for parsing application/json
app.use(bodyParser.urlencoded({ extended: true })); // for parsing application/x-www-form-urlencodeds

app.post('/run', function (req, res) {
    const out = command.exec(req.body.command, req.body.args);
    res.send(out);
});

app.listen(3000, function () {
    console.log('Example app listening on port 3000!');
});

// const res = command.exec('docker', ['run', 'backtrader/test', '_verbose=False']);
//
// console.log( `stderr: ${res.err}` );
// console.log( `stdout: ${res.out}` );