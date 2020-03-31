from django import forms  
from katana.wapps.equinix.models import equinixgroups, equinixops, equinixtransponder
class equinixgroupsForm(forms.ModelForm):  
    class Meta:  
        model = equinixgroups
        fields = "__all__"  
       
class equinixtransponderForum(forms.ModelForm):
    class Meta:
        model = equinixtransponder
        fields = "__all__"
    
class equinixopsForum(forms.ModelForm):
    class Meta:
        model = equinixops
        fields = "__all__"