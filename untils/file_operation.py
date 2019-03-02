from  django.http import HttpResponse,FileResponse
from django.utils.encoding import escape_uri_path

def download(path,filename):
    try:
        file = open(path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = "attachment;filename*=utf-8''{0}".format(escape_uri_path(filename))
        return response
    except Exception as e:
        return HttpResponse('提取文件失败！')