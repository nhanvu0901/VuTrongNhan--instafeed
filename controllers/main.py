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
import logging
import traceback

_logger = logging.getLogger(__name__)
from ..static.instagram_auth.InstagramAPI import  InstagramAPI

class MainController(http.Controller):

    @http.route('/shopify_mint/main', auth='user', type="http", website=True)
    def main(self, **kw):
        response ={"error":''}
        client_id = request.env['ir.config_parameter'].sudo().get_param('shopify_mint.meta_client_id')
        redirect_url = request.env['ir.config_parameter'].sudo().get_param('shopify_mint.meta_redirect_url')
        current_user = request.env.user
        data_transfer = {
            "flag": json.dumps(""),
            "data": json.dumps("")
        }
        shopify_app_exist = request.env['shopify.mint'].sudo().search(
            ['&', ('user', '=', current_user.id), ('is_delete', '=', False)], limit=1)
        shop_url = shopify_app_exist.shop_url
        if current_user and shopify_app_exist:
            if "code" in kw:
                response = self.update_instagram_user(kw["code"], shop_url)
                if response.get("error") !='':
                    data_transfer['flag'] = json.dumps(response.get("error"))
            if response.get("error")=='':
                instagram_user_exist = request.env['instagram.user'].sudo().search([
                    ('admin', '=', current_user.id)
                ], limit=1)
                data = self.get_instagram_user_data(instagram_user_exist, client_id, shop_url, redirect_url)
                data_transfer['data'] = json.dumps(data)
        else:
            data_transfer['flag'] = json.dumps({"error":"Not user"})
        return request.render("shopify_mint.shopify_mint_template", data_transfer)


    def update_instagram_user(self, code, shop_url):

        instagram = InstagramAPI(request)
        response = instagram.get_access_token(code)
        current_user = request.env.user.id
        if response.ok:
            data = response.json()

            access_token = data.get('access_token')
            user_id = str(data.get('user_id'))

            data_username = instagram.get_instagram_user_name(user_id, access_token)
            if data_username:

                instagram_user_exist = request.env['instagram.user'].sudo().search([
                    ('user_name', '=', data_username)
                ], limit=1)

                shopify_shop_exist = request.env['shopify.mint'].sudo().search([
                    ('shop_url', '=', shop_url)
                ], limit=1)
                # exchange for the long live access token
                long_live_access_tk = instagram.get_long_live_token(access_token)

                # check thang moi dang nhap ins
                if not instagram_user_exist and shopify_shop_exist:
                    instagram_user_exist_system = request.env['instagram.user'].sudo().search([
                        ('admin', '=', current_user)
                    ], limit=1)

                    instagram_user_exist = request.env['instagram.user'].create({

                        "ins_access_token": long_live_access_tk,
                        "user_id": user_id,
                        "user_name": data_username,
                        "admin":current_user,
                        "platform":"instagram"

                        # "code": code
                    })
                    # shopify_shop_exist.write({
                    #     "instagram_data": instagram_user_exist.id
                    # })
                    # Xoa thang hien tai neu co

                    if shopify_shop_exist and instagram_user_exist_system:

                        # shopify_shop_exist.write({
                        #     "instagram_data": (3, instagram_user_exist_system.id)
                        # })
                        #
                        # shopify_shop_exist.write({
                        #     "instagram_data": instagram_user_exist.id
                        # })

                        for media in instagram_user_exist_system.media:
                            media.unlink()
                        for widget in instagram_user_exist_system.widget_data:
                            widget.unlink()

                        instagram_user_exist_system.unlink()
                elif instagram_user_exist and shopify_shop_exist:
                    if instagram_user_exist.admin == shopify_shop_exist.user:  # if the instagram already use by 1 shop
                        instagram_user_exist.write({
                            # "shopify_shop": shopify_shop_exist.id,
                            "ins_access_token": long_live_access_tk,
                            "user_id": user_id,
                            "user_name": data_username,

                        })
                    else:
                        return {"error":"Instagram user already been used"}
                else:
                    return {"error":"Shop not exist"}




                # TODO viet nut reload va cronjob
                instagram_user_exist.update_instagram_media()
                return {"error":""}
        else:
            return Response('fail', 404)

    def get_instagram_user_data(self, instagram_user_exist, client_id, shopify_url, redirect_url):
        if instagram_user_exist:

            instagram_data = instagram_user_exist.get_instagram_data_model()
        else:
            instagram_data = ""
        data = {
            "client_id": client_id,
            "user_name": instagram_user_exist.user_name,
            "redirect_url": redirect_url + '?shop_url=' + shopify_url,
            "instagram_data": instagram_data,
            "shopify_url": shopify_url
        }
        return data



