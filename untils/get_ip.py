import urllib.request
import json
def get_ip(request):
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return ip

def ip_belong(ip):
    #ip = get_ip(request)
    if ip:
        url = "http://ip.taobao.com/service/getIpInfo.php?ip="
        data = urllib.request.urlopen(url+ip).read()
        data_dict = json.loads(data)
        print(data_dict["data"]["region"])
        return data_dict["data"]["region"]
    else:
        return '未知'