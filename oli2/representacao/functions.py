import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


def render_pdf_view(request, template_src, context_dict):
    template_path = template_src
    context = context_dict
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)

    if pisa_status.err:
       return HttpResponse('Houve problemas para gerar o pdf <pre>' + html + '</pre>')
    return response


def link_callback(uri, rel):
     result = finders.find(uri)

     if result:
          if not isinstance(result, (list, tuple)):
               result = [result]

          result = list(os.path.realpath(path) for path in result)
          path = result[0]
     else:
          sUrl = settings.STATIC_URL
          sRoot = settings.STATIC_ROOT
          mUrl = settings.MEDIA_URL
          mRoot = settings.MEDIA_ROOT

          if uri.startswith(mUrl):
               path = os.path.join(mRoot, uri.replace(mUrl, ""))
          elif uri.startswith(sUrl):
               path = os.path.join(sRoot, uri.replace(sUrl, ""))
          else:
               return uri

     if not os.path.isfile(path):
          raise Exception('media URI must start with %s or %s' % (sUrl, mUrl))
     return path

