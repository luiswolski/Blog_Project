from django.forms import ModelForm
from .models import Comment
import requests


class FormComment(ModelForm):

    def clean(self):
        raw_data = self.data
        recapcha_response = raw_data.get('g-recaptcha-response')


        recapcha_request = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': '6LdClTAjAAAAAB9f9EAEpINQZch1M0rcjmX6F6CP',
                'response': recapcha_response
            }
        )
        recapcha_result = recapcha_request.json()

        if not recapcha_result.get('success'):
            self.add_error(
                'comment',
                'Sorry Mr. Robot an error occurred'
            )



        cleaned_data = self.cleaned_data
        name = cleaned_data.get('name_comment')
        email = cleaned_data.get('email_comment')
        comment = cleaned_data.get('comment')

        if len(name) < 5:
            self.add_error(
                'name_comment',
                'Name must be have more than 5 characters'
            )


    class Meta:
        model = Comment
        fields = ('name_comment', 'email_comment', 'comment')