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
from ..static.instagram_auth.InstagramAPI import InstagramAPI

class Facebook_data(http.Controller):
    @http.route('/get_facebook_data', type='json', auth='none', cors='*', csrf=False, save_session=False)
    def get_data_to_store(self, **kwargs):
        print(request.jsonrequest)

        instagram_user_exist = request.env['instagram.user'].sudo().search([
            ('user_name', '=', request.jsonrequest.get('instagram_user_name'))
        ], limit=1)
        instagram = InstagramAPI(request)

        get_instagram_id = instagram.get_instagram_user_id(request.jsonrequest['accessToken'],instagram_user_exist)
        if get_instagram_id.get('status') == "error":
            return json.dumps(get_instagram_id)
        else:
            instagram_id = get_instagram_id.get("message")
            if instagram_user_exist:
                instagram_user_exist.write({
                    "facebook_access_token": request.jsonrequest['accessToken']
                })
                response_instagram_data = instagram.get_like_comment(instagram_id,request.jsonrequest['accessToken'])

                if response_instagram_data:
                    instagram_user_exist.write({
                        "followers": json.loads(response_instagram_data.text).get('followers_count'),
                        "url_image":json.loads(response_instagram_data.text).get('profile_picture_url')

                    })
                    for data in json.loads(response_instagram_data.text).get('media').get('data'):
                        media_exist = request.env['post.private'].sudo().search(
                            [('post_id', '=', data.get('id'))], limit=1)

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

                    data = instagram_user_exist.get_instagram_data_model()
                    return json.dumps(data)
            else:
                return json.dumps({"message": "Choose instagram account that link to the shop", "flag": True})


        return "Hello"
