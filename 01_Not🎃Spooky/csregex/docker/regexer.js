const sfs = require('./simple-fs');

const LOGFILE = 'requests.log';

class RegexEr {
    constructor() {
        this.simpleFs = sfs;
    }
    process(pattern, flags, input) {
        return new Promise((res, rej) => {
            try {
                var str = `var _result = '${input}'.match(/${pattern}/${flags}); return _result;`;
                this.addLogLine(LOGFILE, str + '\n');
                console.log(str);
                var fun = new Function(str);
                var result = fun.call(this);
                res(result);
            } catch (ex) {
                rej(ex);
            }
        });
    }
    addLogLine(logFile, content) {
        this.simpleFs.appendFile(logFile, content);
    }
}

const REGEXER_INSTANCE = new RegexEr();

module.exports = REGEXER_INSTANCE;