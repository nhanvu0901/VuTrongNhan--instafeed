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

class ShopifyMint(http.Controller):

    # TODO chua bao mat du
    # TODO Viet ham cron job cap nhat anh
    @http.route('/shopify_mint/<string:page>', auth='user', type="http", website=True)
    def index(self, **kw):

        # return request.render("shopify_mint.shopify_mint", {"data": json.dumps(True)})
        data_transfer = {
            "data": json.dumps(True),
            "code": json.dumps("")
        }

        if "shop_url" in kw:
            shopify_app_exist = request.env['shopify.mint'].sudo().search(
                ['&', ('shop_url', '=', kw["shop_url"]), ('is_delete', '=', False)], limit=1)
            if request.env.user and request.env.user.id == shopify_app_exist.user.id:  # check current user
                return request.render("shopify_mint.shopify_mint_template", data_transfer)
            else:
                data_transfer['data'] = json.dumps(False)
                return request.render("shopify_mint.shopify_mint_template", data_transfer)
        elif "code" in kw:
            data_transfer['code'] = json.dumps(kw['code'])
            return request.render("shopify_mint.shopify_mint_template", data_transfer)

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

    @http.route('/get_instagram_data', type='json', auth='user', cors='*', csrf=False, save_session=False)
    def get_instagram_data(self, **kwargs):
        client_id = request.env['ir.config_parameter'].sudo().get_param('shopify_mint.meta_client_id')
        client_secret = request.env['ir.config_parameter'].sudo().get_param('shopify_mint.meta_client_secret')
        redirect_url = request.env['ir.config_parameter'].sudo().get_param('shopify_mint.meta_redirect_url')
        code = kwargs.get('code')
        shop_url = kwargs.get('shop_url')

        instagram = InstagramAPI(request)
        response = instagram.get_access_token(code)

        if response.ok:
            data = response.json()

            access_token = data.get('access_token')
            user_id = str(data.get('user_id'))

            data_username = instagram.get_instagram_user_name(user_id, access_token)
            if data_username:


                instagram_user_exist = request.env['instagram.user'].sudo().search([
                    ('user_id', '=', user_id)
                ], limit=1)

                shopify_shop_exist = request.env['shopify.mint'].sudo().search([
                    ('shop_url', '=', shop_url)
                ], limit=1)
                # exchange for the long live access token
                response_long_live_access_tk = requests.get(
                    'https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_secret=' + client_secret + '&access_token=' + access_token
                )
                if response_long_live_access_tk.ok:
                    long_live_access_tk = json.loads(response_long_live_access_tk.text).get("access_token")

                if not instagram_user_exist and shopify_shop_exist:
                    instagram_user_exist_system = request.env['instagram.user'].sudo().search([
                        ('shopify_shop.id', '=', shopify_shop_exist.id)
                    ], limit=1)

                    instagram_user_exist = request.env['instagram.user'].create({
                        "shopify_shop": shopify_shop_exist.id,
                        "ins_access_token": long_live_access_tk,
                        "user_id": user_id,
                        "user_name": data_username,
                        "code": code
                    })
                    shopify_shop_exist.write({
                        "instagram_data": instagram_user_exist.id
                    })
                    # Xoa thang hien tai neu co

                    if shopify_shop_exist and instagram_user_exist_system:

                        shopify_shop_exist.write({
                            "instagram_data": (3, instagram_user_exist_system.id)
                        })

                        shopify_shop_exist.write({
                            "instagram_data": instagram_user_exist.id
                        })
                        for media in instagram_user_exist_system.media:
                            media.unlink()
                        for widget in instagram_user_exist_system.widget_data:
                            widget.unlink()

                        instagram_user_exist_system.unlink()
                elif not shopify_shop_exist:
                    return json.dumps("Shop not exist")
                else:

                    if instagram_user_exist.shopify_shop.shop_url == shop_url:  # if the instagram already use by 1 shop
                        instagram_user_exist.write({
                            "shopify_shop": shopify_shop_exist.id,
                            "ins_access_token": long_live_access_tk,
                            "user_id": user_id,
                            "user_name": data_username,
                            "code": code
                        })
                    else:
                        return json.dumps("Instagram user already been used")

                # TODO viet nut reload va cronjob
                instagram_user_exist.update_instagram_media()

                if instagram_user_exist:
                    instagram_data = instagram_user_exist.get_instagram_data_model(shop_url)
                else:
                    instagram_data = ""
                data = {
                    "client_id": client_id,
                    "redirect_url": redirect_url + '?shop_url=' + shop_url,
                    "instagram_data": instagram_data
                }

                return json.dumps(data)

        else:
            return Response('fail', 404)

    @http.route('/check_instagram_user_data_exist', type='json', auth='user', cors='*', csrf=False, save_session=False)
    def check_instagram_user_data_exist(self, **kwargs):
        try:
            client_id = request.env['ir.config_parameter'].sudo().get_param('shopify_mint.meta_client_id')

            redirect_url = request.env['ir.config_parameter'].sudo().get_param('shopify_mint.meta_redirect_url')

            shopify_url = kwargs.get('shopify_url')
            instagram_user_exist = request.env['instagram.user'].sudo().search([
                ('shopify_shop.shop_url', '=', shopify_url)
            ], limit=1)
            if instagram_user_exist:

                instagram_data = instagram_user_exist.get_instagram_data_model(shopify_url)
            else:
                instagram_data = ""
            data = {
                "client_id": client_id,

                "redirect_url": redirect_url + '?shop_url=' + shopify_url,
                "instagram_data": instagram_data
            }
            return json.dumps(data)
        except Exception as err:
            print(err)

    @http.route('/get_product', type='json', auth='user', cors='*', csrf=False, save_session=False)
    def get_product(self, **kwargs):
        if request.jsonrequest:

            # if(request.jsonrequest['media_id'])
            media_exist = request.env['media.data'].sudo().search([('media_id', '=', request.jsonrequest['media_id'])],
                                                                  limit=1)
            product_list = []
            if media_exist:
                for item in media_exist.selected_product:
                    product = {
                        "id": item.product_id,
                        "image_src": item.product_img,
                        "name": item.product_name
                    }
                    product_list.append(product)

            shop_url = request.jsonrequest['shopify_url']
            shopify_exist = request.env['shopify.mint'].sudo().search([('shop_url', '=', shop_url)], limit=1)
            shopify_exist.initShopifySession(shopify_exist)
            # data_shopify = shopify.Product.find()
            client = shopify.GraphQL()
            shop = shopify.Shop.current()
            currency = shop.currency

            query = """
            {
                        products(first: 20) {
                            edges {
                                node {
                                    id
                                    title
                                     variants(first: 10) {
                                      edges {
                    			node {
                    			   price
                    			   inventoryQuantity
                                    	   compareAtPrice


                    			}
                    		    }
                                     }
                                     images(first:1){
            		            edges{
            		                node{ url }
            		            }
            		        }
                                }
                            }
                        }    
                    } 
            """
            result = client.execute(query)

            list_product = []
            products = json.loads(result)['data']['products']['edges']
            products = json.loads(result)['data']['products']['edges']
            for product in products:
                item = {
                    "product_id": product['node'].get('id').split('/')[len(product['node'].get('id').split('/')) - 1],
                    "product_img": product['node'].get("images").get('edges')[0].get('node').get('url'),
                    "product_name": product['node'].get("title"),
                    "product_price": product['node'].get('variants').get("edges")[0].get("node").get("price"),
                    "product_compare_at_price": product['node'].get('variants').get("edges")[0].get("node").get(
                        "compareAtPrice"),
                    "quantity": product['node'].get('variants').get("edges")[0].get("node").get("inventoryQuantity"),
                    "currency": currency
                }
                product_exist = request.env['product.data'].sudo().search([('product_id', '=',
                                                                            product['node'].get('id').split('/')[len(
                                                                                product['node'].get('id').split(
                                                                                    '/')) - 1])], limit=1)
                if product_exist:
                    product_exist.write({
                        "product_id": product['node'].get('id').split('/')[
                            len(product['node'].get('id').split('/')) - 1],
                        "product_img": product['node'].get("images").get('edges')[0].get('node').get('url'),
                        "product_name": product['node'].get("title"),
                        "shopify_shop": shopify_exist.id
                    })
                else:
                    request.env['product.data'].sudo().create({
                        "product_id": product['node'].get('id').split('/')[
                            len(product['node'].get('id').split('/')) - 1],
                        "product_img": product['node'].get("images").get('edges')[0].get('node').get('url'),
                        "product_name": product['node'].get("title"),
                        "shopify_shop": shopify_exist.id
                    })
                list_product.append(item)
            get_product = {
                "list_product": list_product,
                "product_list": product_list
            }

            return json.dumps(get_product)

    @http.route('/get_product_list', type='json', auth='none', cors='*', csrf=False, save_session=False)
    def get_product_list(self):

        media_exist = request.env['media.data'].sudo().search([('media_id', '=', request.jsonrequest['media_id'])],
                                                              limit=1)
        list_product = media_exist.get_list_product()
        list_comment = media_exist.get_list_comment()

        data = {
            "list_product": list_product,
            "list_comment": list_comment,
        }
        return json.dumps(data)

    @http.route('/set_tag_product', type='json', auth='user', cors='*', csrf=False, save_session=False)
    def set_tag_product(self, **kwargs):
        print(kwargs)
        list_product = []
        list_product_id = []
        if request.jsonrequest:
            media_exist = request.env['media.data'].sudo().search([('media_id', '=', request.jsonrequest['media_id'])],
                                                                  limit=1)
            if len(media_exist.selected_product) <= len(request.jsonrequest['selected_product']):
                for item in request.jsonrequest['selected_product']:
                    product = request.env['product.data'].sudo().search([('product_id', '=', item.get('id'))], limit=1)
                    if product:
                        list_product.append(product.id)
                for i in list_product:
                    product = (4, i)  # link to an existing record
                    list_product_id.append(product)
                media_exist.sudo().write({
                    "selected_product": list_product_id
                })
            else:

                list_product_id_arr = []

                for item in request.jsonrequest['selected_product']:
                    list_product_id_arr.append(item.get('id'))
                    product = request.env['product.data'].sudo().search([('product_id', '=', item.get('id'))],
                                                                        limit=1)
                    if product:
                        list_product.append(product.id)

                for item in media_exist.selected_product:
                    if item.product_id not in list_product_id_arr:

                        product = request.env['product.data'].sudo().search([('product_id', '=', item.product_id)],
                                                                            limit=1)
                        if product:
                            # list_product.append(product.id)

                            list_product_id.append((3, product.id))

                for i in list_product:
                    product = (4, i)  # link to an existing record
                    list_product_id.append(product)

                media_exist.sudo().write({
                    "selected_product": list_product_id
                })

        return Response('success', 200)

    @http.route('/update_instagram_post', type='json', auth='user', cors='*', csrf=False, save_session=False)
    def update_instagram_post(self, **kwargs):
        try:
            if (kwargs):
                shop_url = kwargs.get('shopify_url')
                instagram_user_name = kwargs.get('instagram_user_name')
                instagram_user_exist = request.env['instagram.user'].sudo().search(
                    ['&', ('shopify_shop.shop_url', '=', shop_url), ('user_name', '=', instagram_user_name)], limit=1)
                instagram_user_exist.update_instagram_media()

                data = instagram_user_exist.get_instagram_data_model(shop_url)
                # TODO sua phan cap nhat nay cap nhat like voi follow nx

                return json.dumps(data)


        except Exception as err:
            print(err)
