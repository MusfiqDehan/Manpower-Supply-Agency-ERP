from django.contrib import admin
from agent_management_app.models import AgentInfo, AgentDocument, AgentAccount, AgentTransaction
# Register your models here.


@admin.register(AgentInfo)
@admin.register(AgentAccount)
@admin.register(AgentDocument)
@admin.register(AgentTransaction)


class AgentAdmin(admin.ModelAdmin):
    pass

