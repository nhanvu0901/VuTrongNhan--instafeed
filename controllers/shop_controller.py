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

class Frontend(http.Controller):
    @http.route('/get_data_to_store', type='json', auth='none', cors='*', csrf=False, save_session=False)
    def get_data_to_store(self, **kwargs):
        print(request.jsonrequest)
        shopify_shop_exist = request.env['shopify.mint'].sudo().search(
            [('shop_url', '=', request.jsonrequest.get('shop_url'))])
        if request.jsonrequest.get('widget_id') != '':
            widget_exist = request.env['widget.data'].sudo().search(
                ['&',
                 ('shopify_shop.id', '=', shopify_shop_exist.id),
                 ('id', '=', request.jsonrequest.get('widget_id'))])
            list_media = []
            if widget_exist:
                for item in widget_exist.media_data:
                    list_product = []
                    for product in item.selected_product:
                        product_data = {
                            "product_id": product.product_id,
                            "product_img": product.product_img,
                            "product_name": product.product_name,
                        }
                        list_product.append(product_data)
                    list_comment = item.get_list_comment()
                    media_data = {
                        "type": item.type,
                        "caption": item.caption,
                        "permalink": item.permalink,
                        "thumbnail_url": item.thumbnail_url,
                        "created_date": item.created_date,
                        "selected_product": list_product,
                        'media_url':item.media_url,
                        "media_id":item.media_id,
                        "media_like": item.media_like,
                        "num_of_tagged_product": len(item.selected_product),
                        "list_comment":list_comment,
                        "media_count": item.count_comment,

                    }
                    list_media.append(media_data)
                widget_data = {
                    "feed_title": widget_exist.feed_title,
                    "spacing": widget_exist.spacing,
                    "on_post_click": widget_exist.on_post_click,
                    "layout": widget_exist.layout,
                    "configuration": widget_exist.configuration,
                    "rows": widget_exist.rows,
                    "columns": widget_exist.columns,
                    "instagram_user": widget_exist.instagram_user.user_name,
                    "media_url": list_media,
                    "showLikes": widget_exist.showLikes,
                    "showFollowers": widget_exist.showFollwers,
                    "followers":widget_exist.instagram_user.followers,
                    "postToShow": widget_exist.postToShow,
                    "displayTagPost": widget_exist.displayTagPost,
                }
                return json.dumps(widget_data)
