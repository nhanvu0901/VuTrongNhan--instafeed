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



    @http.route('/get_product', type='json', auth='user', cors='*', csrf=False, save_session=False)
    def get_product(self, **kwargs):
        if request.jsonrequest:

            # if(request.jsonrequest['media_id'])
            current_user = request.env.user.id
            media_exist = request.env['media.data'].sudo().search([('admin', '=', current_user)],
                                                                  limit=1)


            shop_url = request.jsonrequest['shopify_url']
            shopify_exist = request.env['shopify.mint'].sudo().search([('shop_url', '=', shop_url)], limit=1)
            shopify_exist.initShopifySession()
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
            for product in products:
                item = {
                    "product_id": product['node'].get('id').split('/')[len(product['node'].get('id').split('/')) - 1],
                    "product_img": product['node'].get("images").get('edges')[0].get('node').get('url') if len(product['node'].get("images").get('edges')) !=0 else '',
                    "product_name": product['node'].get("title"),
                    # "product_price": product['node'].get('variants').get("edges")[0].get("node").get("price"),
                    # "product_compare_at_price": product['node'].get('variants').get("edges")[0].get("node").get(
                    #     "compareAtPrice"),
                    # "quantity": product['node'].get('variants').get("edges")[0].get("node").get("inventoryQuantity"),
                    # "currency": currency
                }
                product_exist = request.env['product.data'].sudo().search([('product_id', '=',
                                                                            product['node'].get('id').split('/')[len(
                                                                                product['node'].get('id').split(
                                                                                    '/')) - 1])], limit=1)
                if product_exist:
                    product_exist.write(item)
                else:
                    request.env['product.data'].sudo().create(item)
                list_product.append(item)
            widget_exist = request.env['widget.data'].sudo().search(
                ['&', ('admin', '=', current_user),
                 ('is_display', '=', True)])
            get_product = {
                "list_product": list_product,
                "product_list": widget_exist.media_data.get_post_product_tag() if widget_exist.media_data.selected_posts_global.selected_product else ''
            }

            return json.dumps(get_product)

    @http.route('/get_product_list', type='json', auth='none', cors='*', csrf=False, save_session=False)
    def get_product_list(self):

        media_exist = request.env['post.global'].sudo().search([('media_id', '=', request.jsonrequest['media_id'])],
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
            media_exist = request.env['post.global'].sudo().search([('media_id', '=', request.jsonrequest['media_id'])],
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
                current_user = request.env.user.id
                shop_url = kwargs.get('shopify_url')
                instagram_user_name = kwargs.get('instagram_user_name')
                instagram_user_exist = request.env['instagram.user'].sudo().search(
                    ['&', ('admin', '=', current_user), ('user_name', '=', instagram_user_name)], limit=1)
                instagram_user_exist.update_instagram_media()

                data = instagram_user_exist.get_instagram_data_model()
                # TODO sua phan cap nhat nay cap nhat like voi follow nx

                return json.dumps(data)


        except Exception as err:
            print(err)
