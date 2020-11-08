const fs = require('fs');
const LEGACY_UTILS = require('./leftover')

class SimpleFs {
    static exists(path) {
        return new Promise((res, rej) => {
            fs.stat(path, (err, stats) => {
                if (err) return rej(err);
                if (!stats.isFile()) return rej('Not a file');
                return res();
            });
        });
    }

    static readFile(path) {
        return new Promise((res, rej) => {
            if (!fs.existsSync(path)) return rej('File not found');
            fs.readFile(path, { encoding: 'utf-8' }, (err, data) => {
                if (err) return rej(err);
                return res(data);
            });
        });
    }

    static readFileSync(path) {
        if (!fs.existsSync(path)) return rej('File not found');
        try {
            return fs.readFileSync(path, { encoding: 'utf-8' });
        } catch (ex) {
            return false;
        }
    }

    static writeFile(path, contents) {
        return new Promise((res, rej) => {
            if (fs.existsSync(path)) return rej('File already exists');
            fs.writeFile(path, contents, { encoding: 'utf-8' }, (err) => {
                if (err) return rej(err);
                return res();
            })
        });
    }

    static writeFileSync(path, contents) {
        if (fs.existsSync(path)) return rej('File already exists');
        try {
            fs.writeFileSync(path, contents, { encoding: 'utf-8' });
            return true;
        } catch (ex) {
            return false;
        }
    }

    static appendFile(path, contents) {
        return new Promise((res, rej) => {
            if (!fs.existsSync(path)) return rej('File not found');
            fs.appendFile(path, contents, { encoding: 'utf-8' }, (err) => {
                if (err) return rej(err);
                return res();
            });
        });
    }

    static appendFileSync(path, contents) {
        if (!fs.existsSync(path)) return rej('File not found');
        try {
            fs.appendFileSync(path, contents, { encoding: 'utf-8' });
            return true;
        } catch (ex) {
            return false;
        }
    }
}

module.exports = SimpleFs;