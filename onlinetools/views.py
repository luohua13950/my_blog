from django.shortcuts import render
from blog.models import Post,Users,Category,Tag
from django.contrib.auth.views import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from PyPDF2 import PdfFileReader,PdfFileWriter,PdfFileMerger
import os
from untils import file_operation
from PyPDF2 import PdfFileWriter, PdfFileReader
# Create your views here.
PATH = "/home/luohua/upload/"
def split_pdf(request):
    msg = ''
    try:
        user_prof = Users.objects.get(user=request.user)
    except Exception as e:
        user_prof = ''
    if request.method == "POST":
        files = request.FILES.get('pdf',None)
        start_page = int(request.POST.get('startpdf',0))
        end_page = int(request.POST.get('endpdf',0))

        if start_page >0 or end_page >0:
        #path = os.path.join(PATH, files.name)
            if files.name.endswith('pdf'):
                path = os.path.join('upload',files.name)
                final_name = files.name + "output.pdf"
                final_path = os.path.join('upload', final_name)

                with open(path, 'wb+') as f:
                    for chunk in files.chunks():
                        f.write(chunk)
                #response = file_operation.download(path)
                output = PdfFileWriter()
                pdf_file = PdfFileReader(open(path, "rb"),strict=False)#将严格查询关闭
                pdf_pages_len = pdf_file.getNumPages()
                end_page = end_page if end_page <pdf_pages_len else pdf_pages_len
                print(pdf_pages_len,end_page)
                if end_page - start_page>0:
                    for i in range(start_page-1,end_page):
                        output.addPage(pdf_file.getPage(i))
                    if end_page != pdf_pages_len:
                        output.addPage(pdf_file.getPage(end_page))
                elif end_page == start_page:
                    output.addPage(pdf_file.getPage(end_page))
                # elif end_page == pdf_pages_len or start_page == end_page:
                #     for i in range(start_page,end_page):
                #         output.addPage(pdf_file.getPage(i))

                else:
                    msg= "你输入的页码存在问题，请重新输入！"
                outputStream = open(final_path, "wb")
                output.write(outputStream)
                response = file_operation.download(final_path,final_name)
                return response
            else:
                msg = '输入的文件为非PDF格式，请重新选择！'
        else:
            msg='起始页码和结束页码必须为正整数'
    return render(request,"onlinetools/splitpdf.html",{"msg":msg,"user_prof":user_prof})


