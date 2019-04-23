from django.views.generic import View
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from .forms import SearchForm
from django.shortcuts import render
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
import django_excel as excel

@login_required
def home(request):
    form = SearchForm()
    return render(request, 'candidate/home.html' , {'searchform': form})

@method_decorator(login_required, name='dispatch')
class Application(View):

    get_type = ''
    # application post reqeust tells server to prepare document for download
    def post(self, request):
        #tokenize the ids 
        ids =  request.POST['data'].split()

        data = dict()
        data['ids'] = ids

        #TODO: validate each id

        #Check if the POST request is Ajax
        if request.is_ajax():
            #TODO prepare the application data
            # data = []
            # for each id in ids:
                #doc = OceanParkApplications.get_document_as_dict(id)
                # if doc is not None:
                    #data.append(OceanParkApplications.get_document_as_dict(id))

            #TODO store the document in session        
            request.session['documents'] = data

            #if len(doc) > 0
            #TODO prepare the response according to different get type
            if request.POST['get_type'] == 'SPREADSHEET':
                return JsonResponse({'url': reverse('download-spreadsheet') , 'app_len': len(data) } )
            elif request.POST['get_type'] == 'FORM':
                return JsonResponse({'url': reverse('download-form') , 'app_len': len(data)} )
            else:
                return HttpResponseBadRequest('No such get type')
            #else:
            #    return JsonResponse( { 'url': '', 'app_len': 0 } )
        else:
            return HttpResponseBadRequest()
            


    # the application get request download the prepared form 
    def get(self, request, *args, **kwargs):

        documents = request.session.get('documents')
        # print(documents)

        if documents is not None:
            if self.get_type == 'SPREADSHEET':
                # import collections

                # result = collections.defaultdict(list)

                # for d in documents:
                #     for k, v in d.items():
                #         result[k].append(v)
                result = documents
                return excel.make_response_from_dict(result, "xls")

            elif self.get_type == 'FORM':
                return render(request, 'candidate/forms.html' , {'documents': documents} )
            else:
                return HttpResponseBadRequest('No Such Get Type')
            
            # del request.session['documents']
        else:
            return HttpResponse('No Documents Prepared')

        
