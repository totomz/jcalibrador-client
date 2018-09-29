const { spawnSync } = require('child_process');

function exec(command, args) {
    const ls = spawnSync( command, args );

    return {
        out: ls.stdout.toString(),
        err: ls.stderr.toString()
    }
}

module.exports = { exec };
