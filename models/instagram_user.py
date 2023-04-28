import shopify
import time
from odoo import models, fields, api
from odoo.http import request
from odoo.tools.safe_eval import datetime
import binascii
import os
import json
import random
import string
import time
from base64 import b64encode
import requests

from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request, Response

import datetime as convertDate
from ..static.instagram_auth.InstagramAPI import InstagramAPI

class Instagram_User(models.Model):
    _name = 'instagram.user'
    _description = 'Instagram User'

    shopify_shop = fields.Many2one('shopify.mint', 'Shopify Shop', ondelete='cascade')

    ins_access_token = fields.Char()
    # cdn_tag = fields.Char()

    user_id = fields.Char(string="User ID")
    user_name = fields.Char(string="User name")
    media_url = fields.Char(string="Media URl")
    code = fields.Char(string="Code")
    media = fields.One2many('media.data', 'instagram_user')
    widget_data = fields.One2many('widget.data', 'instagram_user')
    followers = fields.Char('Followers', default='')
    facebook_access_token = fields.Char()

    def get_instagram_data_model(self, shop_url):
        try:
            if self.shopify_shop.shop_url == shop_url:
                list_media = request.env['media.data'].get_list_media(self)

                widget_exist = self.env['widget.data'].get_active_widget(self, self.shopify_shop)

                list_widget = self.env['widget.data'].get_list_widget(self, self.shopify_shop)
                choose_widget = {
                    "id_widget": widget_exist.id_widget,
                    "number": widget_exist.id
                }
                data = {
                    "followers": self.followers,
                    "user_name": self.user_name,
                    "user_id": self.user_id,
                    "media_url": list_media,

                    "choose_widget": choose_widget,

                    "is_display": widget_exist.is_display,

                    "title": widget_exist.feed_title,
                    "spacing": widget_exist.spacing,
                    "onclickPost": widget_exist.on_post_click,
                    "layout": widget_exist.layout,
                    "autoLayout": widget_exist.configuration,
                    "rows": widget_exist.rows,
                    "columns": widget_exist.columns,
                    "showLikes": widget_exist.showLikes,
                    "showFollwers": widget_exist.showFollwers,
                    "postToShow": widget_exist.postToShow,
                    "displayTagPost": widget_exist.displayTagPost,
                    "list_widget": list_widget
                }
                return data
        except Exception as err:
            print(err)

    def update_like_follow(self):
        instagram = InstagramAPI(request)
        response_instagram_data = instagram.get_like_comment(self.user_id,self.facebook_access_token)

        if response_instagram_data.ok:
            self.write({
                "followers": json.loads(response_instagram_data.text).get('followers_count')
            })
            for data in json.loads(response_instagram_data.text).get('media').get('data'):
                media_exist = request.env['media.data'].sudo().search(
                    [('media_id', '=', data.get('id'))], limit=1)
                if data.get('comments'):
                    # unlink the all old comment
                    request.env['media.comment'].sudo().search(
                        [
                            ('media.id', '=', media_exist.id)
                        ],
                    ).unlink()

                    for comment in data.get('comments').get('data'):
                        comment_created = request.env['media.comment'].sudo().create({
                            "comment_id": comment['id'],
                            "comment_text": comment['text'],
                            "comment_timestamp": comment['timestamp'],
                            "comment_username": comment['username'],
                            "media": media_exist.id
                        })
                if media_exist:
                    media_exist.write({
                        "media_like": data.get('like_count'),

                        "count_comment": data.get('comments_count')
                    })

    def update_instagram_media(self):
        if self:
            instagram = InstagramAPI(request)
            response_media = instagram.get_instagram_media(self.ins_access_token)
            try:
                if response_media.ok:
                    data_media = json.loads(response_media.text)
                    list_media_url = []
                    for data in data_media.get('data'):
                        response_url = instagram.get_details_instagram_media(data, self.ins_access_token)
                        media_exist = request.env['media.data'].sudo().search(
                            [('media_id', '=', json.loads(response_url.text).get('id'))], limit=1)
                        self.save_media(media_exist, response_url)

            except Exception as err:
                print(err)

        if self.followers != '' and self.followers != False:
            self.update_like_follow()

    def save_media(self, media_exist, response_url):
        instagram = InstagramAPI(request)
        if media_exist:
            media_exist.write({
                "media_id": json.loads(response_url.text).get('id'),
                "type": json.loads(response_url.text).get('media_type'),
                "caption": json.loads(response_url.text).get('caption'),
                "permalink": json.loads(response_url.text).get('permalink'),
                "instagram_user": self.id,
                "created_date": json.loads(response_url.text).get('timestamp'),
                "media_like": ''
            })
            if json.loads(response_url.text).get('media_type') == 'CAROUSEL_ALBUM':

                # call the children
                data_child_image = instagram.get_child_media_details(json.loads(response_url.text).get(
                        'id'),self.ins_access_token)
                child_url = data_child_image.get('child_url')
                child_thumbnail_url =data_child_image.get('child_thumbnail_url')

                media_exist.write({
                    "media_url": child_url,
                    "thumbnail_url": child_thumbnail_url if len(child_thumbnail_url) != 0  else '',
                })
            else:
                media_exist.write({
                    "media_url": json.loads(response_url.text).get('media_url'),
                    "thumbnail_url": json.loads(response_url.text).get('thumbnail_url'),
                })

        else:
            media_exist = request.env['media.data'].create({
                "media_id": json.loads(response_url.text).get('id'),
                "type": json.loads(response_url.text).get('media_type'),
                "caption": json.loads(response_url.text).get('caption'),
                "permalink": json.loads(response_url.text).get('permalink'),
                "instagram_user": self.id,
                "created_date": json.loads(response_url.text).get('timestamp'),
                "media_like": ''
            })
            if json.loads(response_url.text).get('media_type') == 'CAROUSEL_ALBUM':
                data_child_image = instagram.get_child_media_details(json.loads(response_url.text).get(
                    'id'), self.ins_access_token)
                child_url = data_child_image.get('child_url')
                child_thumbnail_url = data_child_image.get('child_thumbnail_url')

                media_exist.write({
                    "media_url": child_url,
                    "thumbnail_url": child_thumbnail_url if len(child_thumbnail_url) != 0 else '',
                })

            else:
                media_exist.write({
                    "media_url": json.loads(response_url.text).get('media_url'),
                    "thumbnail_url": json.loads(response_url.text).get('thumbnail_url'),
                })

    def refresh_long_live_tk(self):
        instagram = InstagramAPI(request)
        for instagram_user in self.env['instagram.user'].sudo().search([]):
            response_refresh_tk = instagram.refresh_token(instagram_user.ins_access_token)
            if response_refresh_tk.ok:
                print(json.loads(response_refresh_tk.text))
                instagram_user.write({
                    "ins_access_token": json.loads(response_refresh_tk.text).get('access_token')
                })

    def cr_update_instagram_media(self):
        for instagram_user in self.env['instagram.user'].sudo().search([]):
            instagram_user.update_instagram_media()
