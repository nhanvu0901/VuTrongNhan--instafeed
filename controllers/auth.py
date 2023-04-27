
# -*- coding: utf-8 -*-
import binascii
import os
import json

import traceback
import time

import requests
import shopify
import werkzeug
from odoo import _
from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request, Response
import datetime as convertDate
import logging
_logger = logging.getLogger(__name__)


class Auth(http.Controller):
    @http.route('/return_instagram_api', auth='user', website=True, method=['GET'], csrf=False)
    def return_api_instagram(self, **kwargs):

        if 'code' in kwargs:
            web_base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            redirectUrl = web_base_url + '/shopify_mint'
            return werkzeug.utils.redirect(redirectUrl + "/authorization?code=%s" % kwargs['code'])

    @http.route('/shopify_mint_authenticate', auth='user', website=True, method=['GET'], csrf=False)
    def setup(self, **kw):
        if 'shop' in kw:
            sp_api_key = request.env['ir.config_parameter'].sudo().get_param(
                'shopify_mint.sp_api_key_shopify_mint')
            sp_api_secret_key = request.env['ir.config_parameter'].sudo().get_param(
                'shopify_mint.sp_api_secret_key_shopify_mint')
            shop_url = kw['shop']

            api_version = request.env['ir.config_parameter'].sudo().get_param(
                'shopify_mint.api_version_shopify_mint')
            redirect_url = request.env['ir.config_parameter'].sudo().get_param(
                'shopify_mint.redirect_url_shopify_mint')

            shopify.Session.setup(api_key=sp_api_key, secret=sp_api_secret_key)

            state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
            redirect_uri = redirect_url
            scopes = ['read_products', "read_customers", "write_customers", "read_third_party_fulfillment_orders",
                      "write_third_party_fulfillment_orders", "read_orders", "write_orders", "write_products",
                      "write_draft_orders", "read_draft_orders", "write_script_tags", "read_script_tags",
                      "read_shipping", "read_themes", "write_themes", "read_price_rules"]

            newSession = shopify.Session(shop_url, api_version)
            auth_url = newSession.create_permission_url(scopes, redirect_uri, state)

            return werkzeug.utils.redirect(auth_url)
        return "Hello , world"

    @http.route('/shopify_mint_redirect', type='http', auth='user')
    def redirect(self, **kw):
        if 'shop' not in request.params:
            raise Exception('Missing shop url parameter')

        sp_api_key = request.env['ir.config_parameter'].sudo().get_param(
            'shopify_mint.sp_api_key_shopify_mint')
        sp_api_secret_key = request.env['ir.config_parameter'].sudo().get_param(
            'shopify_mint.sp_api_secret_key_shopify_mint')
        api_version = request.env['ir.config_parameter'].sudo().get_param(
            'shopify_mint.api_version_shopify_mint')
        script_tag = request.env['ir.config_parameter'].sudo().get_param('shopify_mint.cdn_tag_shopify_mint')
        shop_url = kw['shop']
        try:
            shopify.Session.setup(
                api_key=sp_api_key,
                secret=sp_api_secret_key)
            shopify_session = shopify.Session(shop_url, api_version)
            access_token = shopify_session.request_token(kw)
            shopify.ShopifyResource.activate_session(shopify_session)

            shop = shopify.Shop.current()

            domain = shop.domain

            shopify_app_enviroment = request.env['shopify.mint']
            shopify_app_exist = request.env['shopify.mint'].sudo().search([('shop_url', '=', shop_url)], limit=1)

            if access_token:
                existing_webhooks = shopify.Webhook.find()
                for webhook in existing_webhooks:
                    print(webhook.id, webhook.topic)
                    shopify.Webhook.find(webhook.id).destroy()

                print("*******************")
                ngrok_url = 'https://c884-116-97-240-10.ap.ngrok.io'

                webhook_products_create = shopify.Webhook()
                webhook_products_create.topic = "app/uninstalled"
                webhook_products_create.address = ngrok_url + "/webhook/app_uninstalled/" + str(shop.id)
                webhook_products_create.format = "json"
                webhook_products_create.save()
                print(f"{webhook_products_create.id}: {webhook_products_create.topic}")

            current_user = request.env.user
            if shopify_app_exist:
                shopify_app_exist.write({
                    "shop_url": domain,
                    "sp_access_token": access_token,
                    "email": shop.email,
                    "shop_name": shop.name,
                    "shop_id": shop.id,
                    "user": current_user.id,
                    "currency": shop.currency,
                    "script_tag": script_tag,
                    "is_update_script_tag": True,
                    "is_delete": False
                })
            else:

                shopify_app_exist = shopify_app_enviroment.create({
                    "shop_url": domain,
                    "sp_access_token": access_token,
                    "email": shop.email,
                    "shop_name": shop.name,
                    "shop_id": shop.id,
                    "user": current_user.id,
                    "currency": shop.currency,
                    "script_tag": script_tag,
                    "is_update_script_tag": True,
                    "is_delete": False

                })
            web_base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            web_base = web_base_url.replace("http", "https")

            scripTag = shopify.ScriptTag.find()
            if not scripTag:
                shopify.ScriptTag.create({
                    "event": "onload",
                    "src": web_base + "/shopify_mint/static/script_tag/static/js/" + "index.js" + "?v=" + str(
                        time.time())
                })
            else:
                for script in scripTag:
                    if "index.js" in script.src:
                        script.destroy()

                shopify.ScriptTag.create({
                    "event": "onload",
                    "src": web_base + "/shopify_mint/static/script_tag/js/" + "index.js" + "?v=" + str(time.time())
                })

            redirectUrl = web_base_url + '/shopify_mint'
            return werkzeug.utils.redirect(redirectUrl + "/authorization?shop_url=%s" % (shop.domain))

        except Exception as e:
            _logger.error(traceback.format_exc())
            return e.__class__.__name__ + ': ' + str(e) + ' .Please try again!'