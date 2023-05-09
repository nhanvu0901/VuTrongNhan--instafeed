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
                    [('hashed_id', '=', kwargs.get('hashed_id'))])
                if widget_de_active:
                    widget_de_active.write({
                        "is_display": False
                    })


                instagram_user_exist = request.env['instagram.user'].sudo().search([
                    ('user_id', '=', kwargs.get('user_id'))
                ], limit=1)



                widget_exist = request.env['widget.data'].create_action()
                list_widget = request.env['widget.data'].get_list_widget()
                choose_widget = {
                    "hashed_id": widget_exist.hashed_id,
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

                instagram_user_exist = request.env['instagram.user'].sudo().search([
                    ('user_id', '=', kwargs.get('user_id'))], limit=1)
                widget_choosed = request.env['widget.data'].sudo().search(
                    [('hashed_id', '=', kwargs.get('hashed_id'))])
                if widget_choosed:

                    data = {
                        "widget": widget_choosed.set_active_widget(),
                        "followers": instagram_user_exist.followers
                    }
                    return json.dumps(data)
        except Exception as err:
            print(err)

    @http.route('/delete_feed', type='json', auth='user', cors='*', csrf=False, save_session=False)
    def delete_feed(self, **kwargs):
        try:
            if (kwargs):

                current_user = request.env.user.id
                instagram_user_exist = request.env['instagram.user'].sudo().search([
                    ('user_id', '=', kwargs.get('user_id'))], limit=1)

                request.env['widget.data'].sudo().search(
                    ['&',('admin', '=',current_user),
                     ('hashed_id', '=', kwargs.get('hashed_id'))
                     ],
                    limit=1).unlink()  # unlink the deleted widget
                widget_data_exist = request.env['widget.data'].sudo().search(
                    [('admin', '=', current_user)])
                if len(widget_data_exist) == 0:
                    widget_data = request.env['widget.data'].get_active_widget()
                else:
                    widget_data = request.env['widget.data'].search([('admin', '=',current_user)
                     ], limit=1, order='create_date desc')
                    widget_data.write({
                        "is_display": True
                    })

                data = {
                    "widget": widget_data.get_widgets() if widget_data != '' else '',
                    "followers":instagram_user_exist.followers
                }
                return json.dumps(data)


        except Exception as err:
            print(err)

    @http.route('/save_feed', type='json', auth='user', cors='*', csrf=False, save_session=False)
    def save_feed(self, **kwargs):

        if request.jsonrequest:
            current_user = request.env.user.id

            widget_exist = request.env['widget.data'].sudo().search(
                ['&', ('admin','=',current_user),

                 ('hashed_id', '=', request.jsonrequest.get('hashed_id'))
                 ],
                limit=1)


            list_widget_id = request.env['media.source'].get_list_media_id()



            if widget_exist:
                widget_exist.widget_config.write({
                    "feed_title": request.jsonrequest.get('title'),
                    "spacing": request.jsonrequest.get('spacing'),
                    "on_post_click": request.jsonrequest.get('onclickPost'),
                    "layout": request.jsonrequest.get('layout'),
                    "configuration": request.jsonrequest.get('autoLayout'),
                    "rows": request.jsonrequest.get('rows'),
                    "columns": request.jsonrequest.get('columns'),
                    "showLikes": request.jsonrequest.get('showLikes'),
                    "showFollwers": request.jsonrequest.get('showFollwers'),
                    "postToShow": request.jsonrequest.get('postToShow'),
                    "displayTagPost": request.jsonrequest.get('displayTagPost'),
                })
                widget_exist.write({

                    "media_data": list_widget_id,

                    "is_display": True,

                })

            return Response('success', 200)
