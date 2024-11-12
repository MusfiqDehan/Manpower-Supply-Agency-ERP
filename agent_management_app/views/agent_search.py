from agent_management_app.models import AgentInfo
from django.contrib.auth.decorators import login_required

from django.template.loader import render_to_string
from django.http import JsonResponse

@login_required
def agent_search(request):
    data=dict()
    search_value=request.GET.get('search_value')
  
    agent_search_list=(AgentInfo.objects.filter(agent_id__icontains=search_value) 
                       | AgentInfo.objects.filter(full_name__icontains=search_value) 
                       | AgentInfo.objects.filter(phone_number__icontains=search_value))
    context={'agent_list':agent_search_list, 'user': request.user,}
    data['search_list']=render_to_string('agent_management/agent/agent_list.html',context)
    return JsonResponse(data)