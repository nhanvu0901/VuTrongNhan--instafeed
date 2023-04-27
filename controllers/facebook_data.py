import binascii
import os
import json
import random
import string
from base64 import b64encode
import requests
import shopify
import werkzeug
from odoo import _
from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request, Response


class Facebook_data(http.Controller):
    @http.route('/get_facebook_data', type='json', auth='none', cors='*', csrf=False, save_session=False)
    def get_data_to_store(self, **kwargs):
        print(request.jsonrequest)
        shopify_shop_exist = request.env['shopify.mint'].sudo().search(
            [('shop_url', '=', request.jsonrequest.get('shop_url'))])
        instagram_user_exist = request.env['instagram.user'].sudo().search([
            ('user_name', '=', request.jsonrequest.get('instagram_user_name'))
        ], limit=1)

        response_page = requests.get(
            'https://graph.facebook.com/v16.0/me/accounts?access_token=' + request.jsonrequest['accessToken'])
        # TODO luu access_token cua facebook
        if response_page.ok:
            if len(json.loads(response_page.text).get('data')) == 1:
                page_id = json.loads(response_page.text).get('data')[0].get('id')
                response_instagram = requests.get(
                    'https://graph.facebook.com/v16.0/' + page_id + '?fields=instagram_business_account&access_token=' +
                    request.jsonrequest['accessToken'])
                instagram_user_exist.write({
                    "facebook_access_token": request.jsonrequest['accessToken']
                })
                if response_instagram:
                    try:
                        instagram_id = json.loads(response_instagram.text).get('instagram_business_account').get('id')
                        if instagram_id != instagram_user_exist.user_id:
                            return json.dumps(
                                {"message": "Instagtam user not valid",
                                 "flag": True})
                    except Exception:
                        return json.dumps(
                            {"message": "Shop not match with instagram account or not instagram for business",
                             "flag": True})

                    if instagram_user_exist:
                        response_instagram_data = requests.get(
                            'https://graph.facebook.com/v16.0/' + instagram_id + '?fields=followers_count,media{like_count,comments_count,comments{text,username,timestamp}}&access_token=' +
                            request.jsonrequest['accessToken'])
                        if response_instagram_data:
                            instagram_user_exist.write({
                                "followers": json.loads(response_instagram_data.text).get('followers_count')
                            })
                            for data in json.loads(response_instagram_data.text).get('media').get('data'):
                                media_exist = request.env['media.data'].sudo().search(
                                    [('media_id', '=', data.get('id'))], limit=1)

                                if data.get('comments'):
                                    # TODO unlink the all old comment
                                    request.env['media.comment'].sudo().search(
                                        [
                                            ('media.id', '=', media_exist.id)
                                        ],
                                    ).unlink()  # unlink the deleted widget
                                    # TODO get the new comment
                                    for comment in data.get('comments').get('data'):
                                        comment_created = request.env['media.comment'].sudo().create({
                                            "comment_id": comment['id'],
                                            "comment_text": comment['text'],
                                            "comment_timestamp": comment['timestamp'],
                                            "comment_username": comment['username'],
                                            "media":media_exist.id
                                        })

                                if media_exist:
                                    media_exist.write({
                                        "media_like": data.get('like_count'),
                                        "count_comment": data.get('comments_count')
                                    })

                            data = instagram_user_exist.get_instagram_data_model(
                                instagram_user_exist.shopify_shop.shop_url)
                            return json.dumps(data)
                    else:
                        return json.dumps({"message": "Choose instagram account that link to the shop", "flag": True})
            else:
                return json.dumps({"message": "Choose 1 shop that link instagram account to the store", "flag": True})

        return "Hello"
