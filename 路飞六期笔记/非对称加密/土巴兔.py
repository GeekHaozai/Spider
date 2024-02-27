from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64
from urllib.parse import quote_plus

puc_key_str = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDhNhuAr4UjFv+cj99PbAQWWx9HX+3jSRThJqJdXkWUMFMTRay8EYRtPFIiwiOUU4gCh4ePMxiuZJWUBHe1waOkXEFcKg17luhVqECsO+EOLhxa3yHoXA5HcSKlG85hNV3G4uQCr+C8SOE0vCGTnMdnEGmUnG1AGGe44YKy6XR4VwIDAQAB"
public_key = RSA.importKey(base64.b64decode(puc_key_str))
rsa = PKCS1_v1_5.new(key=public_key)
enc_str = rsa.encrypt("123456".encode())
b64_en_str = base64.b64encode(enc_str).decode()
print(quote_plus(b64_en_str))