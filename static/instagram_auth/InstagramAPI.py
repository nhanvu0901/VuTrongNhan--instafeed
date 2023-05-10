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
from odoo.http import request, Response

class InstagramAPI(object):
    CLIENT_ID = None
    CLIENT_SECRET = None
    AUTH_CODE = None
    ACCESS_TOKEN = None
    REFRESH_TOKEN = None
    REDIRECT_URL = None

    def __init__(self, social=None, params=None, ):
        if social is not None:
            self.SOCIAL = social
            self.CLIENT_ID = social.env['ir.config_parameter'].sudo().get_param('shopify_mint.meta_client_id')
            self.CLIENT_SECRET = social.env['ir.config_parameter'].sudo().get_param('shopify_mint.meta_client_secret')
            self.REDIRECT_URL = social.env['ir.config_parameter'].sudo().get_param('shopify_mint.meta_redirect_url')

    def get_access_token(self, code):
        PATH = 'https://api.instagram.com/oauth/access_token'
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

    def get_instagram_user_name(self, user_id, access_token):
        response_username = requests.get(
            'https://graph.instagram.com/' + user_id + '?fields=id,username&access_token=' + access_token)
        data_username = json.loads(response_username.text).get("username")
        return data_username

    def get_instagram_media(self, ins_access_token):
        response_media = requests.get(
            'https://graph.instagram.com/me/media?fields=id&access_token=' + ins_access_token)
        return response_media

    def get_details_instagram_media(self, data, ins_access_token):
        response_url = requests.get('https://graph.instagram.com/' + data.get(
            'id') + '?fields=id,media_type,media_url,username,timestamp,caption,permalink,thumbnail_url&access_token=' + ins_access_token)
        return response_url

    def get_like_comment(self, user_id, facebook_access_token):
        response_instagram_data = requests.get(
            'https://graph.facebook.com/v16.0/' + user_id + '?fields=followers_count,media{like_count,comments_count,comments{text,username,timestamp}}&access_token=' +
            facebook_access_token)
        return response_instagram_data

    def get_child_media_details(self, media_id, ins_access_token):
        child_url = []
        child_thumbnail_url = []
        try:
            response_children = requests.get(
                'https://graph.instagram.com/' + media_id + '/children?fields=id,media_type,media_url,permalink,thumbnail_url&access_token=' + ins_access_token)
            if response_children.ok:
                for item in json.loads(response_children.text).get('data'):
                    child_url.append(item.get('media_url'))
                    if item.get('thumbnail_url'):
                        child_thumbnail_url.append(item.get('thumbnail_url'))
                data = {
                    "child_url": child_url,
                    "child_thumbnail_url": child_thumbnail_url
                }
                return data
        except Exception as e:
            _logger.error(traceback.format_exc())

    def refresh_long_live_token(self, ins_access_token):
        response_refresh_tk = requests.get(
            'https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token=' + ins_access_token)
        return response_refresh_tk

    def get_long_live_token(self, access_token):
        response_long_live_access_tk = requests.get(
            'https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_secret=' + self.CLIENT_SECRET + '&access_token=' + access_token)
        try:
            if response_long_live_access_tk.ok:
                long_live_access_tk = json.loads(response_long_live_access_tk.text).get("access_token")
                return long_live_access_tk
        except Exception as e:
            _logger.error(traceback.format_exc())

    def get_instagram_user_id(self,accessToken,instagram_user_exist):
        response_page = requests.get(
            'https://graph.facebook.com/v16.0/me/accounts?access_token=' + accessToken)
        if response_page.ok:
            if len(json.loads(response_page.text).get('data')) == 1:
                page_id = json.loads(response_page.text).get('data')[0].get('id')
                response_instagram = requests.get(
                    'https://graph.facebook.com/v16.0/' + page_id + '?fields=instagram_business_account&access_token=' +
                    accessToken)
                try:
                    instagram_id = json.loads(response_instagram.text).get('instagram_business_account').get('id')
                    if instagram_id != instagram_user_exist.user_id:
                        return {"message": "Instagtam user not valid",
                             "status": "error"}
                    else:
                        return {"message": instagram_id,
                             "status": "success"}
                except Exception:
                    return {"message": "Shop not match with instagram account or not instagram for business",
                            "status": "error"}

            else:
                return {"message": "Choose 1 shop that link instagram account to the store",   "status": "error"}



