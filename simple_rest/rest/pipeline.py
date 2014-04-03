# -*- coding: utf-8 -*-
import datetime
import requests
import re
from time import mktime, strptime
from django.shortcuts import redirect
from social.pipeline.partial import partial
from simple_rest.rest.models import CustomUser

@partial
def require_email(strategy, details, user=None, is_new=False, *args, **kwargs):
    if user and user.email:
        return
    elif is_new and not details.get('email'):
        if strategy.session_get('saved_email'):
            details['email'] = strategy.session_pop('saved_email')
        else:
            return redirect('require_email')
            
   
def get_gender_age(strategy, details, response, user=None, *args, **kwargs):
    """Update user details using data from provider."""
    
    if user:
        # Just created the user?        
        if 1: #kwargs['is_new']:
            if strategy.backend.__class__.__name__ == 'FacebookOAuth2':                
                if 'gender' in response:
                    details['gender'] = response['gender'] 
                if 'birthday' in response and re.search(r'^\d+\/\d+\/\d+$', response['birthday']):
                    details['birthdate'] = datetime.datetime.fromtimestamp(mktime(strptime(response['birthday'], '%m/%d/%Y')))               
            
            if strategy.backend.__class__.__name__ == 'VKOAuth2':
                if 'access_token' in response and 'user_id' in response:
                    api_response = requests.post('https://api.vk.com/method/users.get', data={'uids': str(response['user_id']), 'fields': 'sex,bdate', 'access_token': response['access_token']})
                    res_json = api_response.json()['response']
                    
                    if len(res_json) > 0:
                        res_json = res_json[0]
                        sex = res_json['sex']
                        if sex and sex == 1: 
                            details['gender'] = 'female'
                        elif sex == 2:
                            details['gender'] = 'male'
                            
                        bdate = res_json['bdate']
                        if bdate and re.search(r'^\d+\.\d+\.\d+$', bdate):
                            details['birthdate'] = datetime.datetime.fromtimestamp(mktime(strptime(bdate, '%d.%m.%Y')))
