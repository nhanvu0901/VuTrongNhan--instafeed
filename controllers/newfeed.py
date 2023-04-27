# -*- coding: utf-8 -*-
import binascii
import os
import json
import random
import string
import time
from base64 import b64encode
import requests
import shopify
import werkzeug
from odoo import _
from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request, Response
import datetime as convertDate


class NewFeed(http.Controller):
    @http.route('/create_new_feed', type='json', auth='user', cors='*', csrf=False, save_session=False)
    def create_new_feed(self, **kwargs):
        try:
            if (kwargs):
                # TODO khi xoa het feed va tao moi thi tra ve thang moi bi rong
                widget_de_active = request.env['widget.data'].sudo().search(
                    [('id_widget', '=', kwargs.get('id_widget'))])
                if widget_de_active:
                    widget_de_active.write({
                        "is_display": False
                    })

                shopify_shop_exist = request.env['shopify.mint'].sudo().search(
                    [('shop_url', '=', kwargs.get('shopify_url'))])
                instagram_user_exist = request.env['instagram.user'].sudo().search([
                    ('user_id', '=', kwargs.get('user_id'))
                ], limit=1)
                widget_id = convertDate.datetime.now().strftime('%Y%m%d%H%M%S%f')
                list_widget_id = request.env['media.data'].get_list_media_id(instagram_user_exist)
                widget_exist = request.env['widget.data'].sudo().create({
                    "instagram_user": instagram_user_exist.id,
                    "id_widget": widget_id,
                    "shopify_shop": shopify_shop_exist.id,
                    "is_display": True,
                    "media_data": list_widget_id,

                })
                list_widget = request.env['widget.data'].get_list_widget(instagram_user_exist, shopify_shop_exist)
                choose_widget = {
                    "id_widget": widget_exist.id_widget,
                    "number": widget_exist.id
                }
                data = {
                    "choose_widget": choose_widget,
                    "list_widget": list_widget,
                    "followers":instagram_user_exist.followers
                }
                return json.dumps(data)  # TODO gui ID cua thang moi create

        except Exception as err:
            print(err)

    @http.route('/get_widget', type='json', auth='user', cors='*', csrf=False, save_session=False)
    def get_widget_data(self, **kwargs):
        try:
            if kwargs:
                shopify_shop_exist = request.env['shopify.mint'].sudo().search(
                    [('shop_url', '=', kwargs.get('shopify_url'))])
                instagram_user_exist = request.env['instagram.user'].sudo().search([
                    ('user_id', '=', kwargs.get('user_id'))], limit=1)
                widget_choosed = request.env['widget.data'].sudo().search(
                    [('id_widget', '=', kwargs.get('id_widget'))])
                if widget_choosed:
                    data = {
                        "widget": widget_choosed.set_active_widget(instagram_user_exist, shopify_shop_exist)
                    }
                    return json.dumps(data)
        except Exception as err:
            print(err)

    @http.route('/delete_feed', type='json', auth='user', cors='*', csrf=False, save_session=False)
    def delete_feed(self, **kwargs):
        try:
            if (kwargs):

                shopify_shop_exist = request.env['shopify.mint'].sudo().search(
                    [('shop_url', '=', kwargs.get('shopify_url'))])
                instagram_user_exist = request.env['instagram.user'].sudo().search([
                    ('user_id', '=', kwargs.get('user_id'))], limit=1)

                request.env['widget.data'].sudo().search(
                    ['&', ('instagram_user.id', '=', instagram_user_exist.id),
                     ('shopify_shop.id', '=', shopify_shop_exist.id),
                     ('id_widget', '=', kwargs.get('id_widget'))
                     ],
                    limit=1).unlink()  # unlink the deleted widget

                if len(instagram_user_exist.widget_data) == 0:
                    widget_data = request.env['widget.data'].get_active_widget(instagram_user_exist, shopify_shop_exist)
                else:
                    widget_data = request.env['widget.data'].search(['&', ('instagram_user.id', '=', instagram_user_exist.id),
                     ('shopify_shop.id', '=', shopify_shop_exist.id)
                     ], limit=1, order='create_date desc')
                    widget_data.write({
                        "is_display": True
                    })

                data = {
                    "widget": widget_data.get_widget_field(),
                    "followers":instagram_user_exist.followers
                }
                return json.dumps(data)


        except Exception as err:
            print(err)

    @http.route('/save_feed', type='json', auth='user', cors='*', csrf=False, save_session=False)
    def save_feed(self, **kwargs):

        if request.jsonrequest:
            shopify_shop_exist = request.env['shopify.mint'].sudo().search(
                [('shop_url', '=', request.jsonrequest.get('shopify_url'))])
            instagram_user_exist = request.env['instagram.user'].sudo().search([
                ('user_id', '=', request.jsonrequest.get('instagram_user_id'))
            ], limit=1)
            widget_exist = request.env['widget.data'].sudo().search(
                ['&', ('instagram_user.id', '=', instagram_user_exist.id),
                 ('shopify_shop.id', '=', shopify_shop_exist.id),
                 ('id_widget', '=', request.jsonrequest.get('id_widget'))
                 ],
                limit=1)


            list_widget_id = request.env['media.data'].get_list_media_id(instagram_user_exist)



            if widget_exist:
                widget_exist.write({
                    "feed_title": request.jsonrequest.get('title'),
                    "spacing": request.jsonrequest.get('spacing'),
                    "on_post_click": request.jsonrequest.get('onclickPost'),
                    "layout": request.jsonrequest.get('layout'),
                    "configuration": request.jsonrequest.get('autoLayout'),
                    "rows": request.jsonrequest.get('rows'),
                    "columns": request.jsonrequest.get('columns'),
                    "showLikes": request.jsonrequest.get('showLikes'),
                    "showFollwers": request.jsonrequest.get('showFollwers'),
                    "media_data": list_widget_id,
                    "instagram_user": instagram_user_exist.id,
                    "shopify_shop": shopify_shop_exist.id,
                    "postToShow": request.jsonrequest.get('postToShow'),
                    "displayTagPost": request.jsonrequest.get('displayTagPost'),
                    "is_display": True,
                })

            return Response('success', 200)
