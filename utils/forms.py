from django import forms
from django.forms.util import ErrorList

class BootstrapForm(forms.Form):
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=None,
                 empty_permitted=False):
        super(BootstrapForm, self).__init__(data, files, auto_id, prefix, initial,
                                            error_class, label_suffix, empty_permitted)
        
        for name, field in self.fields:
            field.widget.attrs.update({'class':'form-control'})

    def as_bootstrap(self):
        "Retorna div no padrao bootstrap"
        html = '''<div class="form-group">
        %(label)s
        %(field)s%(help_text)s
        </div>'''
        
        return self._html_output(
            normal_row = html,
            error_row = '%s',
            row_ender = '</div>',
            help_text_html = ' <span class="help-block">%s</span>',
            errors_on_separate_row = True)
            

class BootstrapModelForm(forms.ModelForm):
    
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=None,
                 empty_permitted=False, instance=None):

        super(BootstrapModelForm, self).__init__(data, files, auto_id, prefix, initial,
                                            error_class, label_suffix, empty_permitted, instance)
        
        for name, field in self.fields.items():
            if isinstance(self.fields[name].widget, forms.TextInput):
                self.fields[name].widget.attrs.update({'class':'form-control'})
            if isinstance(self.fields[name].widget, forms.DateInput):
                self.fields[name].widget.attrs.update({'class':self.fields[name].widget.attrs['class'] + ' date'})
            #self.fields[name] = field
                                            
                                
    def as_bootstrap(self):
        "Retorna div no padrao bootstrap"
        html = '''<div class="form-group">
        %(label)s
        %(field)s%(help_text)s
        </div>'''
        
        return self._html_output(
            normal_row = html,
            error_row = '%s',
            row_ender = '</div>',
            help_text_html = ' <span class="help-block">%s</span>',
            errors_on_separate_row = True)
