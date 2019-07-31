import datetime
import hmac, hashlib
import base64
import requests
import json


def generate_signature(access_key,secret_key,http_verb,content_md5,content_type,gmt_date,canonicalized_resource):
    data = http_verb+"\n"+content_md5+"\n"+content_type+"\n"+gmt_date+"\n"+canonicalized_resource
    secret_key_bytes, data_bytes = bytes(secret_key, "utf8"), bytes(data, "utf8")
    signature =	str(base64.b64encode(hmac.new(secret_key_bytes, data_bytes, hashlib.sha256).digest()),"utf-8")
    return  "NCDN " + access_key + ":" +signature


def create_cdn_domain(access_key,secret_key):

    api_url = "http://ncdn-eastchina1.126.net/domain/"
    http_verb = "POST"  # 根据具体的接口要求填写，例如创建 CDN 这里是需要传 POST 
    GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
    gmt_date = datetime.datetime.utcnow().strftime(GMT_FORMAT)  # 当前 GMT 时间
    canonicalized_resource = "/domain/"  # 参考构建CanonicalizedResource的方法，创建加速域名，资源为/domain
    content_md5 = ""  # 非必填，如为空用""替代
    content_type = "application/json"
    auth_headers = generate_signature(access_key, secret_key, http_verb, content_md5,content_type, gmt_date, canonicalized_resource)


    headers = {
        "Content-Type":"application/json",
        "Date":gmt_date,
        "Authorization":auth_headers
    }
    body = {
    "domain-name": "www.awen.me",
    "service-type": "web",
    "service-areas": "mainland",
    "comment": "ceshi",
    "origin-type": "ip",
    "origin-ips": [
        "1.1.1.1"
    ],
    "cache-behaviors": [
        {
            "path-pattern": "/*.jpg",
            "ignore-cache-control": True,
            "cache-ttl": 604800
        }
    ],
    "logging": {
        "enabled": True,
        "bucket": "aaas",
        "prefix": "log_"
    },
    "ssl": {
        "enabled": True,
        "origin-protocol": "https",
        "redirect-https": True,
        "use-for-sni": True,
        "cert-order-id": "7e117850-5068-4166-96bf-8c4ca7f97067"
        }
    }
    response = requests.post(api_url,headers=headers,data=json.dumps(body))

    print(response.url)
    print(response.status_code)
    print(response.json())



if __name__ == '__main__':

    access_key = "xxxx"  # https://c.163yun.com/dashboard#/m/account/accesskey/ 获取
    secret_key = "xxxxx"  # https://c.163yun.com/dashboard#/m/account/accesskey/ 获取
    create_cdn_domain()



