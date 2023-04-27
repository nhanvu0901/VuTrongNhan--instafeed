import base64
import json
import logging
import re
import time
import traceback
from datetime import datetime
from io import BytesIO
from urllib.parse import urlencode

_logger = logging.getLogger(__name__)

import requests

class InstagramAPI(object):
    CLIENT_ID = None
    CLIENT_SECRET = None
    AUTH_CODE = None
    ACCESS_TOKEN = None
    REFRESH_TOKEN = None
    REDIRECT_URL =None


    def __init__(self, social=None, params=None, ):
        if social is not None:
            self.SOCIAL = social
            self.CLIENT_ID = social.env['ir.config_parameter'].sudo().get_param('shopify_mint.meta_client_id')
            self.CLIENT_SECRET = social.env['ir.config_parameter'].sudo().get_param('shopify_mint.meta_client_secret')
            self.REDIRECT_URL =  social.env['ir.config_parameter'].sudo().get_param('shopify_mint.meta_redirect_url')
    def get_access_token(self, code):
        PATH ='https://api.instagram.com/oauth/access_token'
        data = {
             'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'redirect_uri': self.REDIRECT_URL,
            'code': code
        }
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(PATH, data=data, headers=headers)

        return response
    def get_instagram_user_name(self,user_id,access_token):
        response_username = requests.get(
            'https://graph.instagram.com/' + user_id + '?fields=id,username&access_token=' + access_token)
        data_username = json.loads(response_username.text).get("username")
        return data_username

    def get_instagram_media(self,ins_access_token):
        response_media = requests.get(
            'https://graph.instagram.com/me/media?fields=id&access_token=' + ins_access_token)
        return response_media

    def get_details_instagram_media(self,data,ins_access_token):
        response_url = requests.get('https://graph.instagram.com/' + data.get(
            'id') + '?fields=id,media_type,media_url,username,timestamp,caption,permalink,thumbnail_url&access_token=' + ins_access_token)
        return response_url