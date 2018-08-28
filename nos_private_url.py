#!/usr/bin/env python
# -*-coding:utf-8-*-

import time
import hmac, hashlib
import base64
from urllib import parse


def generate_signature(key, data):
    key_bytes, data_bytes = bytes(key, "utf8"), bytes(data, "utf8")
    return parse.quote_plus(base64.b64encode(bytes(hmac.new(key_bytes, data_bytes, hashlib.sha256).digest())))


def do_get_http_url(bucket, endpoint, url_path, accesskey, expires_time, sign):
    url = "https://" + bucket + "." + endpoint + str(url_path) + "?" + "NOSAccessKeyId=" + str(
        accesskey) + "&Expires=" + str(expires_time) + "&Signature=" + sign
    return  url


if __name__ == '__main__':

    url_path = "/domain/1/2/domain.txt"
    expires_time = int(time.time()) + 6000
    accesskey = "xxxx"
    secretkey = "xxxx"
    endpoint = "nos-eastchina1.126.net"
    bucket = "file201503"
    resource = "/" + bucket + "/" + parse.quote_plus(url_path[1:])
    data = "%s\n%s\n%s\n%s\n%s%s" \
           % ("GET", "", "", expires_time, "", resource)
    sign = generate_signature(secretkey, data)
    print(do_get_http_url(bucket, endpoint, url_path, accesskey, expires_time, sign))