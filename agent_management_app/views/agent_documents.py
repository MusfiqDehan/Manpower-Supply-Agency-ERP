from django.shortcuts import render
from agent_management_app.forms import AgentDocumentSubmitForm
from agent_management_app.models import AgentDocument
from visa_management_app.models import Visa
from django.contrib.auth.decorators import login_required

from django.template.loader import render_to_string
from django.http import JsonResponse


#create passenger document
def save_document_form(request, form, document, agent_id, template_name):
    
    data = dict()
    
    if request.method == 'POST':
        
        if form.is_valid():
          
            form.save()
            
            data['form_is_valid'] = True
            
            
            agent_document_list = AgentDocument.objects.filter(agent__id=agent_id).order_by('document_name')
            
            data['html_agent_document_list'] = render_to_string('agent_management/agent_documents/agent_document_list.html', {
                'agent_document_list': agent_document_list, 
                'user': request.user,
           })
        
        else:
       
            data['form_is_valid'] = False

    context = {
        'form': form,
        'agent_id': agent_id,
        'document': document,
        'user': request.user,
        
        }
    
    data['html_form'] = render_to_string(template_name, context, request= request)
    return JsonResponse(data)



# Document Add/Create
@login_required
def agent_document_add(request,agent_id):
    
    if request.method == 'POST':  
        form = AgentDocumentSubmitForm(request.POST, request.FILES)
    else:
        agent_id = agent_id
        form = AgentDocumentSubmitForm()
    document = None
    return save_document_form(request, form, document, agent_id,'agent_management/agent_documents/add_document.html')



@login_required
def agent_document_edit(request, pk):
    
    document = AgentDocument.objects.get(id=pk)
    agent_id = document.agent.id  
        
    if request.method == 'POST':        
        
        form = AgentDocumentSubmitForm(request.POST , request.FILES, instance=document)
        
    else:
        
         
        form = AgentDocumentSubmitForm( instance=document)
    
    return save_document_form(request, form, document,agent_id, 'agent_management/agent_documents/edit_document.html') 
  
# delete account document 
def save_document_delete_form(request, document, template_name):
    
    data = dict()
    
    object = document
    agent_delete_id =document.agent.id
    
    if request.method == 'POST':
        
        object.delete()
        
        data['form_is_valid'] = True
          
        agent_document_list = AgentDocument.objects.filter(agent__id=agent_delete_id).order_by('document_name')
            
        data['html_agent_document_list'] = render_to_string('agent_management/agent_documents/agent_document_list.html', {
            'agent_document_list': agent_document_list, 
            'user': request.user,
        })
    
    else:
        data['form_is_valid'] = False


    context = {
        'document': document,
        'user': request.user,
        }
    
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


  

@login_required
def agent_document_delete(request, pk):
    
    document = AgentDocument.objects.get(id=pk)
    
    
    return save_document_delete_form(request, document, 'agent_management/agent_documents/delete_document.html')
