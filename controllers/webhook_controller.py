from odoo import http
from odoo.http import request, Response


class WebhookController(http.Controller):
    @http.route("/webhook/<string:topic>/<string:shopify_id>", auth="public", type="json", csrf=False, cors="*", save_session=False)
    def webhook_order_create(self, topic, shopify_id):
        try:
            if 'app' in topic:
                print(request.jsonrequest)
                shopify_shop = request.env['shopify.mint'].sudo().search([
                    ('shop_id', '=', request.jsonrequest.get('id'))
                ], limit=1)
                try:
                    if shopify_shop:

                        if shopify_shop.is_delete == False:
                            shopify_shop.write({
                                "is_delete":True
                            })
                        if shopify_shop.instagram_data != '':
                            instagram_data = request.env['instagram.user'].sudo().search([
                            ('user_id', '=', shopify_shop.instagram_data.user_id)
                        ], limit=1)
                            instagram_data.unlink()


                except Exception as err:
                    print(err)
            return Response("success", status=200)
        except Exception as err:
            print(err)