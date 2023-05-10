import binascii
import os
import json
import random
import string
from base64 import b64encode
import requests
import shopify
import werkzeug

from ..static.instagram_auth.InstagramAPI import InstagramAPI
from odoo import _
from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request, Response

class Frontend(http.Controller):
    @http.route('/get_data_to_store', type='json', auth='none', cors='*', csrf=False, save_session=False)
    def get_data_to_store(self, **kwargs):
        print(request.jsonrequest)

        shopify_shop_exist = request.env['shopify.mint'].sudo().search(
            [('shop_url', '=', request.jsonrequest.get('shop_url'))])
        instagram_user = request.env['instagram.user'].sudo().search(
            [('admin', '=',shopify_shop_exist.user.id )])
        if shopify_shop_exist:
            if request.jsonrequest.get('hashed_id') != '':
                widget_exist = request.env['widget.data'].sudo().search(
                    [
                        ('hashed_id', '=', request.jsonrequest.get('hashed_id'))])
                list_media = []
                if widget_exist:
                    for item in widget_exist.media_data.selected_posts_global:
                        list_product = item.get_list_tag_product()
                        list_comment = item.get_list_comment()
                        media_data = {
                            "type": item.type,
                            "caption": item.caption,
                            "permalink": item.permalink,
                            "thumbnail_url": item.thumbnail_url,
                            "created_date": item.created_date,
                            "selected_product": list_product,
                            'media_url': item.media_url,
                            "media_id": item.media_id,
                            "media_like": item.media_like,
                            "num_of_tagged_product": len(item.hotspot),
                            "list_comment": list_comment,
                            "media_count": item.count_comment,

                        }
                        list_media.append(media_data)
                    widget_data = {
                        "feed_title": widget_exist.widget_config.feed_title,
                        "spacing": widget_exist.widget_config.spacing,
                        "on_post_click": widget_exist.widget_config.on_post_click,
                        "layout": widget_exist.widget_config.layout,
                        "configuration": widget_exist.widget_config.configuration,
                        "rows": widget_exist.widget_config.rows,
                        "columns": widget_exist.widget_config.columns,
                        "instagram_user": instagram_user.user_name,
                        "media_url": list_media,
                        "showLikes": widget_exist.widget_config.showLikes,
                        "showFollowers": widget_exist.widget_config.showFollwers,
                        "followers": instagram_user.followers,
                        "postToShow": widget_exist.widget_config.postToShow,
                        "displayTagPost": widget_exist.widget_config.displayTagPost,
                    }

                    return json.dumps(widget_data)