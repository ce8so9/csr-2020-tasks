class Utility {
    require(resource) {
        return new Promise((res, rej)=>{
            try {
                var module = require(resource);
                return res(module); 
            } catch(ex) {
                return rej(ex);
            }
        });
    }
    isRunningOnWindows() {
        return process.platform.indexOf('win' === 0);
    }
    getUrlHost(url) {
        try{
            return new URL(url).hostname;
        } catch(ex){
            return null;
        }
    }
}

LEGACY_UTILS = new Utility();

module.exports = LEGACY_UTILS;