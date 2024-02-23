var window = this;
var jsencrypt = require('jsencrypt');

var publickeystr = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDhNhuAr4UjFv+cj99PbAQWWx9H \
X+3jSRThJqJdXkWUMFMTRay8EYRtPFIiwiOUU4gCh4ePMxiuZJWUBHe1waOkXEFc \
Kg17luhVqECsO+EOLhxa3yHoXA5HcSKlG85hNV3G4uQCr+C8SOE0vCGTnMdnEGmU \
nG1AGGe44YKy6XR4VwIDAQAB";

var jmq = new jsencrypt();
jmq.setPublicKey(publickeystr);

var jm = function(txt) {
    var nestr = jmq.encrypt(txt);
    return nestr;
}
console.log(jm("12345"));