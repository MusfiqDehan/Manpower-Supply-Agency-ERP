from django import forms
from agent_management_app.models import AgentInfo, AgentDocument, AgentAccount,AgentTransaction,AgentAccount


class AgentInfoSubmitForm(forms.ModelForm):
    class Meta:
        model = AgentInfo
        
        fields = '__all__'
        
        
class AgentDocumentSubmitForm(forms.ModelForm):
    class Meta:
        model = AgentDocument
        
        fields = '__all__'
        
class AgentAccountForm(forms.ModelForm):
    class Meta:
        model = AgentAccount
        
        fields = '__all__'



class AgentAccountForm(forms.ModelForm):
    class Meta:
        model=AgentAccount
        fields='__all__'
    

# Agent Acccount Management
class AgentTransactionForm(forms.ModelForm):
    class Meta:
        model=AgentTransaction
        fields='__all__'
        
         
# MiddlemanTransactionEditForm
class AgentAccuntTransactionEditForm(forms.ModelForm):
    class Meta:
        model = AgentTransaction
        fields = '__all__'


# MiddlemanTransactionEditForm
class AgentTransactionEditForm(forms.ModelForm):
    class Meta:
        model = AgentTransaction
        fields = '__all__'