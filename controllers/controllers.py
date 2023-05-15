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
_logger = logging.getLogger(__name__)

CURRENCY_SYMBOLS_LIST = {
    "AFN": "؋",
    "ARS": "$",
    "AWG": "ƒ",
    "AUD": "$",
    "AZN": "₼",
    "BSD": "$",
    "BBD": "$",
    "BYN": "Br",
    "BZD": "BZ$",
    "BMD": "$",
    "BOB": "$b",
    "BGN": "лв",
    "BRL": "R$",
    "BND": "$",
    "KHR": "៛",
    "CAD": "$",
    "KYD": "$",
    "CLP": "$",
    "CNY": "¥",
    "COP": "$",
    "CRC": "₡",
    "HRK": "kn",
    "CUP": "₱",
    "CZK": "Kč",
    "DKK": "kr",
    "DOP": "RD$",
    "XCD": "$",
    "EGP": "£",
    "SVC": "$",
    "EUR": "€",
    "FKP": "£",
    "FJD": "$",
    "GHS": "¢",
    "GIP": "£",
    "GTQ": "Q",
    "GGP": "£",
    "GYD": "$",
    "HNL": "L",
    "HKD": "$",
    "HUF": "Ft",
    "IDR": "Rp",
    "IRR": "﷼",
    "IMP": "£",
    "ILS": "₪",
    "JMD": "J$",
    "JPY": "¥",
    "JEP": "£",
    "KZT": "лв",
    "KPW": "₩",
    "KRW": "₩",
    "KGS": "лв",
    "LAK": "₭",
    "LBP": "£",
    "LRD": "$",
    "MKD": "ден",
    "MYR": "RM",
    "MUR": "₨",
    "MXN": "$",
    "NAD": "$",
    "NPR": "₨",
    "ANG": "ƒ",
    "NZD": "$",
    "NIO": "C$",
    "NGN": "₦",
    "NOK": "kr",
    "OMR": "﷼",
    "PKR": "₨",
    "PHP": "₱",
    "PLN": "zł",
    "QAR": "﷼",
    "RUB": "₽",
    "SHP": "£",
    "SAR": "﷼",
    "SCR": "₨",
    "SGD": "$",
    "SBD": "$",
    "SOS": "S",
    "ZAR": "R",
    "LKR": "₨",
    "SEK": "kr",
    "SRD": "$",
    "SYP": "£",
    "TWD": "NT$",
    "THB": "฿",
    "TTD": "TT$",
    "TRY": "₺",
    "TVD": "$",
    "UAH": "₴",
    "GBP": "£",
    "USD": "$",
    "UYU": "$U",
    "UZS": "лв",
    "VEF": "Bs",
    "VND": "₫",
    "YER": "﷼",
    "ZWD": "Z$"
}
class ShopifyMint(http.Controller):

    @http.route('/products_search', type='json', auth='user', cors='*', csrf=False, save_session=False)
    def products_search(self, **kw):
        if request.jsonrequest:

            # if(request.jsonrequest['media_id'])
            current_user = request.env.user.id
            shopify_exist = request.env['shopify.store'].sudo().search([('admin', '=', current_user)], limit=1)
            shopify_exist.initShopifySession()
            limit = 10
            if shopify_exist:
                if 'limit' in kw:
                    limit = kw['limit']
                # data_shopify = shopify.Product.find()
                client = shopify.GraphQL()


                search_query = kw['query']
                query = '{products(first: %d, query: "title:%s* AND status:ACTIVE") {edges {node {id title handle totalVariants onlineStorePreviewUrl status priceRangeV2 { minVariantPrice { amount currencyCode } maxVariantPrice { amount currencyCode } } images(first: 1) {edges { node {originalSrc}}}}}}}' % (
                    limit, search_query)
                # query = """
                # {
                #             products(first: 20) {
                #                 edges {
                #                     node {
                #                         id
                #                         title
                #                          variants(first: 10) {
                #                           edges {
                #         			node {
                #         			   price
                #         			   inventoryQuantity
                #                         	   compareAtPrice
                #
                #
                #         			}
                #         		    }
                #                          }
                #                          images(first:1){
                # 		            edges{
                # 		                node{ url }
                # 		            }
                # 		        }
                #                     }
                #                 }
                #             }
                #         }
                # """
                query_result = client.execute(query)
                query_result = json.loads(query_result)
                product_options = []
                if query_result['data']['products']['edges']:
                    for product in query_result['data']['products']['edges']:
                        data = product['node']
                        if not data['images']['edges']:
                            data['images']['edges'].append(
                                {'node': {
                                    'originalSrc': 'https://apps.nestscale.com/omnichat/static/img/no_image.png'}})
                        product_options.append({
                            'id': data['id'],
                            'name': data['title'],
                            'handle': data['handle'],
                            'image_src': data['images']['edges'][0]['node']['originalSrc'],
                            'variant_num': data['totalVariants'],
                            'product_url': data['onlineStorePreviewUrl'],
                            'price_range': self.get_price_range(
                                data['priceRangeV2']['minVariantPrice']['amount'],
                                data['priceRangeV2']['minVariantPrice']['currencyCode'],
                                data['priceRangeV2']['maxVariantPrice']['amount'],
                                data['priceRangeV2']['maxVariantPrice']['currencyCode'])
                        })
                    shopify.ShopifyResource.clear_session()
                return {
                    'code': 0,
                    'product_options': product_options,
                }
            else:
                return {
                    'code': -1,
                    'error': 'Store not found.'
                }

    def get_price_range(self, min_price_amount, min_price_currency_code, max_price_amount,
                        max_price_currency_code):
        if float(min_price_amount) < float(max_price_amount):
            return self.format_currency(min_price_amount,
                                        min_price_currency_code) + ' - ' + self.format_currency(
                max_price_amount, max_price_currency_code)
        elif float(min_price_amount) == float(max_price_amount):
            return self.format_currency(min_price_amount, min_price_currency_code)
        else:
            return ''

    def format_currency(self, amount, currency_code):
        if CURRENCY_SYMBOLS_LIST.get(currency_code):
            return CURRENCY_SYMBOLS_LIST.get(currency_code) + amount
        else:
            return amount + ' ' + currency_code







            # products = json.loads(query_result)['data']['products']['edges']
            # for product in products:
            #     item = {
            #         "product_id": product['node'].get('id').split('/')[len(product['node'].get('id').split('/')) - 1],
            #         "product_img": product['node'].get("images").get('edges')[0].get('node').get('url') if len(product['node'].get("images").get('edges')) !=0 else '',
            #         "product_name": product['node'].get("title"),
            #         # "product_price": product['node'].get('variants').get("edges")[0].get("node").get("price"),
            #         # "product_compare_at_price": product['node'].get('variants').get("edges")[0].get("node").get(
            #         #     "compareAtPrice"),
            #         # "quantity": product['node'].get('variants').get("edges")[0].get("node").get("inventoryQuantity"),
            #         # "currency": currency
            #     }
            #     product_exist = request.env['product.data'].sudo().search([('product_id', '=',
            #                                                                 product['node'].get('id').split('/')[len(
            #                                                                     product['node'].get('id').split(
            #                                                                         '/')) - 1])], limit=1)
            #     if product_exist:
            #         product_exist.write(item)
            #     else:
            #         request.env['product.data'].sudo().create(item)
            #     list_product.append(item)
            # widget_exist = request.env['widget.data'].sudo().search(
            #     ['&', ('admin', '=', current_user),
            #      ('is_display', '=', True)])
            # get_product = {
            #     "list_product": list_product,
            #     "product_list": widget_exist.media_data.get_post_product_tag() if widget_exist.media_data.selected_posts_global.selected_product else ''
            # }



    @http.route('/get_product_list', type='json', auth='none', cors='*', csrf=False, save_session=False)
    def get_product_list(self):

        media_exist = request.env['post.private'].sudo().search([('post_id', '=', request.jsonrequest['post_id'])],
                                                              limit=1)
        list_product = media_exist.get_list_tag_product()
        list_comment = media_exist.get_list_comment()

        data = {
            "list_product": list_product,
            "list_comment": list_comment,
        }
        return json.dumps(data)

    @http.route('/tag_product', methods=['POST'], type='json', auth='user')
    def tag_product(self, **kw):
        try:
            print(kw)
            current_user = request.env.user.id
            shopify_app_exist = request.env['shopify.store'].sudo().search(
                ['&', ('admin', '=', current_user), ('is_delete', '=', False)], limit=1)

            if shopify_app_exist:
                hotspot_private = request.env['hotspot.private'].sudo()
                if 'products' in kw:
                    products = kw['products']
                    product_ids = []
                    for product in products:
                        product_ids.append(product['id'])
                    if kw.get('post_id'):

                        post_id = kw['post_id']
                        media_exist = request.env['post.private'].sudo().search(
                            [('post_id', '=', post_id)],
                            limit=1)
                        hotspots = hotspot_private.search([('post', '=', media_exist.id)])
                        remain_hotspot_ids = []
                        for hotspot in hotspots:
                            if hotspot.shopify_product_id not in product_ids:
                                hotspot.status = False
                            else:
                                hotspot.status = True
                                remain_hotspot_ids.append(hotspot.shopify_product_id)
                        for item in products:
                            if item['id'] not in remain_hotspot_ids:
                                print(item)
                                hotspot_private.create({
                                    'name': item['name'],
                                    'admin': current_user,
                                    'post': media_exist.id,
                                    'shopify_product_id': item['id'],
                                    'shopify_product_handle': item['handle'],
                                    'shopify_product_img_src': item['image_src'],
                                     'shopify_product_variant_num': item['variant_num'],
                                    'shopify_product_product_url': item['product_url'],
                                    'shopify_product_price_range': item['price_range'],
                                    'status': True,
                                })
                        return {
                            'code': 0,
                            'products': products
                        }
                    else:
                        return {
                            'code': -1,
                            'error': 'Post ID not found.'
                        }
                else:
                    return {
                        'code': -1,
                        'error': 'Product list not found.'
                    }
            else:
                return {
                    'code': -1,
                    'error': 'Shop not found.'
                }
        except Exception as e:
            _logger.error(e)
            return {
                'code': -1,
                'error': 'Something went wrong. Please contact the customer support'
            }




    # @http.route('/set_tag_product', type='json', auth='user', cors='*', csrf=False, save_session=False)
    # def set_tag_product(self, **kwargs):
    #     print(kwargs)
    #     list_product = []
    #     list_product_id = []
    #     if request.jsonrequest:
    #         media_exist = request.env['post.private'].sudo().search([('media_id', '=', request.jsonrequest['media_id'])],
    #                                                               limit=1)
    #         if len(media_exist.hotspot) <= len(request.jsonrequest['selected_product']):
    #             for item in request.jsonrequest['selected_product']:
    #                 product = request.env['hotspot.private'].sudo().search([('shopify_product_id', '=', item.get('id'))], limit=1)
    #                 if product:
    #                     list_product.append(product.id)
    #             for i in list_product:
    #                 product = (4, i)  # link to an existing record
    #                 list_product_id.append(product)
    #             media_exist.sudo().write({
    #                 "selected_product": list_product_id
    #             })
    #         else:
    #
    #             list_product_id_arr = []
    #
    #             for item in request.jsonrequest['selected_product']:
    #                 list_product_id_arr.append(item.get('id'))
    #                 product = request.env['hotspot.private'].sudo().search([('shopify_product_id', '=', item.get('id'))],
    #                                                                     limit=1)
    #                 if product:
    #                     list_product.append(product.id)
    #
    #             for item in media_exist.selected_product:
    #                 if item.product_id not in list_product_id_arr:
    #
    #                     product = request.env['hotspot.private'].sudo().search([('shopify_product_id', '=', item.id)],
    #                                                                         limit=1)
    #                     if product:
    #                         # list_product.append(product.id)
    #
    #                         list_product_id.append((3, product.id))
    #
    #             for i in list_product:
    #                 product = (4, i)  # link to an existing record
    #                 list_product_id.append(product)
    #
    #             media_exist.sudo().write({
    #                 "selected_product": list_product_id
    #             })
    #
    #     return Response('success', 200)

    @http.route('/update_instagram_post', type='json', auth='user', cors='*', csrf=False, save_session=False)
    def update_instagram_post(self, **kwargs):
        try:
            if (kwargs):
                current_user = request.env.user.id
                shop_url = kwargs.get('shopify_url')
                instagram_user_name = kwargs.get('instagram_user_name')
                instagram_user_exist = request.env['instagram.user'].sudo().search(
                    ['&', ('admin', '=', current_user), ('user_name', '=', instagram_user_name)], limit=1)
                instagram_user_exist.fetch_instagram_media()

                data = instagram_user_exist.get_instagram_data_model()
                # TODO sua phan cap nhat nay cap nhat like voi follow nx

                return json.dumps(data)


        except Exception as err:
            print(err)
