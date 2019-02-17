from crispy_forms.helper import FormHelper
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_show_errors = False
        self.helper.error_text_inline = False
        self.helper.form_class = 'form-horizontal'

        for fieldname in ['password1', ]:
            self.fields[fieldname].help_text = None

        for fieldname in ['password2', ]:
                    self.fields[fieldname].help_text = None

        self.helper.label_class = 'col-lg-6 col-md-6 col-sm-6 text-lg-left'
        self.helper.field_class = 'col-lg-6 col-md-6 col-sm-6'
