<template>
  <div class="Polaris-Modal-Dialog__Container_13mbo" data-polaris-layer="true" data-polaris-overlay="true">
    <div role="dialog" aria-modal="true" aria-label="Polarismodal-header10" aria-labelledby="Polarismodal-header10" tabindex="-1" class="Polaris-Modal-Dialog_n3qgo">
      <div class="Polaris-Modal-Dialog__Modal_2v9yc">
        <div class="Polaris-Box_375yx" >
          <div class="Polaris-Columns_17mx7" >
            <div class="Polaris-Inline_j8r4v" ><h2 class="Polaris-Text--root_yj4ah Polaris-Text--headingLg_yyh4u Polaris-Text--semibold_k1k0m Polaris-Text--break_32vap" id="Polarismodal-header7">Add products</h2></div>
            <button class="Polaris-Modal-CloseButton_bl13t" @click="closeTagProduct();modalProductSelect=false" aria-label="Close"><span class="Polaris-Icon_yj27d Polaris-Icon--colorBase_nqlaq Polaris-Icon--applyColor_2y25n"><span class="Polaris-Text--root_yj4ah Polaris-Text--bodySm_nvqxj Polaris-Text--regular_pjgr0 Polaris-Text--visuallyHidden_yrtt6"></span><svg viewBox="0 0 20 20" class="Polaris-Icon__Svg_375hu" focusable="false" aria-hidden="true"><path d="m11.414 10 6.293-6.293a1 1 0 1 0-1.414-1.414l-6.293 6.293-6.293-6.293a1 1 0 0 0-1.414 1.414l6.293 6.293-6.293 6.293a1 1 0 1 0 1.414 1.414l6.293-6.293 6.293 6.293a.998.998 0 0 0 1.707-.707.999.999 0 0 0-.293-.707l-6.293-6.293z"></path></svg></span></button>
          </div>
        </div>

        <div style="padding: 1rem">
           <a-input-search
              v-model:value="search_query_product"
              placeholder="Search products"
              style="width: 100%;"
              @change="searchProduct"
              size="large"
            />
        </div>


        <div style="margin-top: 1rem;flex: 1;
height: 10px;
overflow-x: hidden;
position: initial;
padding-bottom: 20px; ">
           <div v-if="is_loading_data === true" style="text-align: center">
            <a-spin size="large" />
          </div>
          <div v-else>
            <table style="width: 100%">
                <div v-for="product in product_data" class="tr-container" style="display: flex;height: 5rem;
              border-top: 2px solid #e1e3e5;padding: 0px 2rem;">
                  <tr :key="product.product_id" class="table-row" style="display: flex;gap: 2rem;
align-items: center;">
                          <td>
                            <input style="width: 1.2rem;
height: 1.2rem;" type="checkbox" :id="product.product_id"  v-model="tempSelectedProductIds" @change="tagProduct" :value="product.product_id"/>
                          </td>
                          <td><img :src="product.product_img" alt="" style="width: 3rem;height: 3rem;"></td>
                          <td>{{ product.product_name }}</td>

                       </tr>
                </div>

              </table>
          </div>
        </div>


        <div class="bottom-container" style="border-top: 2px solid rgb(225, 227, 229);
width: 100%;
display: flex;
justify-content: space-between;
padding: 1.5rem 1rem;">
            <div class="selected-num">
               {{this.tempSelectedProductIds.length}} products selected
            </div>
            <div class="button-container">
                 <a-button value="large" style="margin-right: 1rem;" @click="closeTagProduct();modalProductSelect=false">Cancel</a-button>


                 <a-button  value="large" type="primary" @click="addProduct">Add</a-button>
            </div>
        </div>

      </div>
    </div>
  </div>
  <div class="Polaris-Backdrop_1x2i2" style="z-index: 999;"></div>
</template>

<script>
import { notification } from 'ant-design-vue';
import {ExclamationOutlined, SmileOutlined} from '@ant-design/icons-vue';
import { createVNode, defineComponent, h } from 'vue';
import _ from 'lodash';
import axios from "axios";
export default {
  name: "TagProduct",
  data() {
    return {
      product_data: [],
      is_loading_data: false,
      search_query_product: null,

      modalProductSelect:false,
       tempSelectedProductIds: [],
            tempSelectedProduct: [],
    }
  },

  computed: {

    },
    props: {
     media_id:String,
     watch_list:[],
      instagram_data:String,
      modalProductSelectApp:Boolean
    },
    methods:{
      closeTagProduct(){
          this.$emit('closeTagProduct')
      },
      searchProduct(){
          this.getProductLink()
      },
      tagProduct: function (event) {//lay thong tin thang dc tag push vao array
            console.log(event)
            var product_id = event.target.value
            if (event.target.checked) {
                if (this.product_data.filter(i => i.product_id === product_id).length > 0) {
                    var product = this.product_data.filter(i => i.product_id === product_id)[0]
                    this.tempSelectedProduct.push(product)
                }
            } else {
                this.tempSelectedProduct = this.tempSelectedProduct.filter(i => i.product_id !== product_id)
            }
        },
      addProduct: function () {
            var self = this

            axios.post('/tag_product', {
                jsonrpc: "2.0",
                params: {

                    products: this.tempSelectedProduct,
                    post_id: this.media_id
                }
            }).then(function (response) {
                var data = response.data.result
                console.log(data)
                if (data.code === 0) {
                    //TODO self.post.products = data.products cap nhat lai product da dc select o cai modal ngoai
                    var shop_url_storage_selected = sessionStorage.getItem("selected#"+self.media_id);
                    if(shop_url_storage_selected !== null){
                       self.$emit('watch_list_product',self.selected)
                       sessionStorage.setItem("selected#"+self.media_id,JSON.stringify(self.selected));
                        let index_item = 0
                        for (let i = 0; i < self.instagram_data.media_url.length; i++) {
                          if(self.instagram_data.media_url[i].media_id === self.media_id){
                             index_item =i
                             break
                           }
                        }
                         self.instagram_data.media_url[index_item].num_of_tagged_product =  self.selected.length;
                         self.$emit('update_instagram_data',self.instagram_data)
                    }
                    self.$emit('closeTagProduct')
                    notification.open({
                    message: 'Product(s) tagged',
                    description:
                      'Successfully!!',
                    duration: 4,
                     icon: () => h(SmileOutlined, { style: 'color: #108ee9' }),
                  });
                } else if (data.code === -1) {

                    notification.open({
                    message: data.error,
                    description:
                      '',
                    duration: 4,
                     icon: () => h(SmileOutlined, { style: 'color: #108ee9' }),
                  });
                }
                // self.isLoadingTagProduct = false;
                self.modalProductSelect = false;
            }).catch(function (error) {
                // self.isLoadingTagProduct = false;
                self.modalProductSelect = false;
                notification.open({
                    message: error,
                    description:
                      '',
                    duration: 4,
                     icon: () => h(SmileOutlined, { style: 'color: #108ee9' }),
                  });
                console.log(error);
            });
        },
      // saveTagProduct(){
      //   console.log(this.selected_product)
      //   var self = this
      //   var xmlhttp = new XMLHttpRequest();
      //   let queryString = window.location.search
      //   let urlParams = new URLSearchParams(queryString)
      //   this.shopify_url = urlParams.get('shop_url')
      //   xmlhttp.open("POST", "https://odoo.website/set_tag_product");
      //   xmlhttp.setRequestHeader("Content-Type", "application/json");
      //   let param = {
      //     shopify_url: urlParams.get('shop_url'),
      //     media_id : this.media_id,
      //     selected_product:this.selected
      //   }
      //   xmlhttp.onreadystatechange = function () {
      //     if (xmlhttp.readyState === 4) {
      //       if (xmlhttp.status === 200) {
      //         console.log((JSON.parse(xmlhttp.responseText).result))
      //         if(JSON.parse(xmlhttp.responseText).result.includes("200")){
      //           //check xem trong session ds selected cua thang media_id chua co roi thi update
      //           var shop_url_storage_selected = sessionStorage.getItem("selected#"+self.media_id);
      //           if(shop_url_storage_selected !== null){
      //              self.$emit('watch_list_product',self.selected)
      //              sessionStorage.setItem("selected#"+self.media_id,JSON.stringify(self.selected));
      //               let index_item = 0
      //               for (let i = 0; i < self.instagram_data.media_url.length; i++) {
      //                 if(self.instagram_data.media_url[i].media_id === self.media_id){
      //                    index_item =i
      //                   break
      //                  }
      //               }
      //                self.instagram_data.media_url[index_item].num_of_tagged_product =  self.selected.length;
      //                self.$emit('update_instagram_data',self.instagram_data)
      //           }
      //           self.$emit('closeTagProduct')
      //            this.modalProductSelect = false
      //           notification.open({
      //           message: 'Notification !!',
      //           description:
      //             'No feed to delete',
      //           duration: 4,
      //           icon: () => h(ExclamationOutlined, { style: 'color: red' }),
      //         });
      //         }
      //       }
      //     }
      //   };
      //   xmlhttp.send(JSON.stringify(param))
      // },
        getProductLink: _.debounce(
            function () {
                  var self = this
                   this.is_loading_data = true
                  var search_query_product = this.search_query_product
                  if (!this.search_query_product) {
                      search_query_product = ' '
                  }
                  var shop_url_storage_product_list =JSON.parse(sessionStorage.getItem("product_data"));

                  if(shop_url_storage_product_list !== null ){
                      this.product_data =shop_url_storage_product_list
                      this.is_loading_data = false
                }
                else{
                    axios.post('/products_search', {
                        jsonrpc: "2.0",
                        params: {
                            query: search_query_product,
                            limit: 20,
                        }
                    }).then(function (response) {
                        var data = response.data.result
                        if (data.code === 0) {
                            self.product_data = data.product_options
                           sessionStorage.setItem("product_data",JSON.stringify(data.product_options));
                        } else if (data.code === -1) {
                            notification.open({
                                message: data.error,
                                description:
                                  'No feed to delete',
                                duration: 4,
                                icon: () => h(ExclamationOutlined, { style: 'color: red' }),
                              });
                        }
                        self.is_loading_data = false;
                    }).catch(function (error) {
                        self.is_loading_data = false;
                        notification.open({
                            message:  error.message,
                            description:
                              'No feed to delete',
                            duration: 4,
                            icon: () => h(ExclamationOutlined, { style: 'color: red' }),
                          });

                    });
                }

            }, 500
        ),
    },
    mounted() {
     this.modalProductSelect = this.modalProductSelectApp
      var shop_url_storage_selected = sessionStorage.getItem("selected#"+this.media_id);


      this.tempSelectedProduct = []
      this.tempSelectedProductIds = []
        if(JSON.parse(shop_url_storage_selected).length  !== 0){
             for (let item of JSON.parse(shop_url_storage_selected)) {
              this.tempSelectedProductIds.push(item.id)
              this.tempSelectedProduct.push({
                  'product_id': item.id,
                  'product_name': item.name,
                  'handle': item.handle,
                  'product_img': item.img_src,
                  'variant_num': item.variant_num,
                  'product_url': item.product_url
              })
          }
        }

     // var shop_url_storage_product_list = sessionStorage.getItem("product_data");
     // var shop_url_storage_selected = sessionStorage.getItem("selected#"+this.media_id);
     //
     //  if(shop_url_storage_selected !== "undefined"){
     //    this.selected =JSON.parse(shop_url_storage_selected)
     //  }
     //  if(shop_url_storage_product_list !== null ){
     //    this.product_data =JSON.parse(shop_url_storage_product_list)
     //    this.is_loading_data = false
     // }
     // else {
     //       var self = this
     //      var xmlhttp = new XMLHttpRequest();
     //
     //      xmlhttp.open("POST", "https://odoo.website/get_product");
     //      xmlhttp.setRequestHeader("Content-Type", "application/json");
     //      let param = {
     //
     //         media_id : this.media_id,
     //      }
     //      xmlhttp.onreadystatechange = function () {
     //        if (xmlhttp.readyState === 4) {
     //          if (xmlhttp.status === 200) {
     //            self.product_data = JSON.parse(JSON.parse(xmlhttp.responseText).result)['list_product']
     //            if(JSON.parse(JSON.parse(xmlhttp.responseText).result)['product_list'] !== null || JSON.parse(JSON.parse(xmlhttp.responseText).result)['product_list'].length !== 0 ){
     //              // self.selected = JSON.parse(JSON.parse(xmlhttp.responseText).result)['product_list']
     //              //luu lai tren session
     //              sessionStorage.setItem("product_data",JSON.stringify(JSON.parse(JSON.parse(xmlhttp.responseText).result)['list_product']));
     //              self.is_loading_data = false
     //            }
     //          }
     //        }
     //      };
     //      xmlhttp.send(JSON.stringify(param))
     // }
    },
    watch: {

        modalProductSelect: function (newone) {
            if (newone === true) {
                this.getProductLink()

            } else {
              console.log(false)
            }
        },

    },
}
</script>

<style scoped>
.ant-btn-primary{
   background: #008060;color:#fff;
  border: #008060;
}
.ant-btn-primary:hover{
 background:  rgb(0 110 82);
}
.ant-btn-primary:active {
  background:  rgb(0 110 82);
}
 .ant-btn-primary:focus {
  background:  rgb(0 110 82);
}
.tr-container:hover{
  background: #f6f6f7;
}
.Polaris-Modal-CloseButton_bl13t::after {
    border-radius: var(--p-border-radius-1);
    bottom: -.0625rem;
    box-shadow: 0 0 0 -.0625rem var(--p-focused);
    content: "";
    display: block;
    left: -.0625rem;
    pointer-events: none;
    position: absolute;
    right: -.0625rem;
    top: -.0625rem;
    transition: box-shadow var(--p-duration-100) var(--p-ease);
    z-index: 1;
}
.Polaris-Modal-CloseButton_bl13t:hover {
  background: var(--p-surface-hovered);
}
.Polaris-Text--bodySm_nvqxj {
  font-size: var(--p-font-size-75);
  line-height: var(--p-font-line-height-1);
}
.Polaris-Text--regular_pjgr0 {
  font-weight: var(--p-font-weight-regular);
}
.Polaris-Text--visuallyHidden_yrtt6 {
  border: 0 !important;
  clip-path: inset(50%) !important;
  height: .0625rem !important;
  margin: 0 !important;
  overflow: hidden !important;
  padding: 0 !important;
  position: absolute !important;
  top: 0;
  white-space: nowrap !important;
  width: .0625rem !important;
}
.Polaris-Icon__Img_375hq, .Polaris-Icon__Svg_375hu {
  display: block;
  max-height: 100%;
  max-width: 100%;
  position: relative;
  width: 100%;
}
.Polaris-Icon_yj27d {
  display: block;
height: 1.25rem;
margin: auto;
max-height: 100%;
max-width: 100%;
width: 1.25rem;
}
.Polaris-Modal-CloseButton_bl13t {
  -webkit-appearance: none;
  appearance: none;
  background: none;
  border: none;
  border-radius: var(--p-border-radius-2);
  color: inherit;
  cursor: pointer;
  font-size: inherit;
  line-height: inherit;
  margin: 0;
  margin-left: var(--p-space-5);
  margin-right: calc(var(--p-space-2)*-1);
  padding: 0;
  position: relative;
}
.Polaris-Text--root_yj4ah{
  box-sizing: border-box;
color: rgb(32, 34, 35);
color-scheme: light;
font-family: -apple-system, BlinkMacSystemFont, "San Francisco", "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
font-size: 20px;
font-weight: 600;
letter-spacing: normal;
line-height: 24px;
margin-bottom: 0px;
margin-left: 0px;
margin-right: 0px;
margin-top: 0px;
overflow-wrap: break-word;
pointer-events: auto;
text-align: start;
text-rendering: optimizelegibility;
text-transform: none
}
.Polaris-Inline_j8r4v{
  align-items: center;
box-sizing: border-box;
color: rgb(32, 34, 35);
color-scheme: light;
display: flex;
flex-wrap: wrap;
font-family: -apple-system, BlinkMacSystemFont, "San Francisco", "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
font-size: 29px;
font-weight: 400;
justify-content: start;
letter-spacing: normal;
line-height: 20px;
pointer-events: auto;
text-rendering: optimizelegibility;
text-transform: none
}
.Polaris-Columns_17mx7{
  box-sizing: border-box;
color: rgb(32, 34, 35);
color-scheme: light;
display: grid;
font-family: -apple-system, BlinkMacSystemFont, "San Francisco", "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
font-size: 29px;
font-weight: 400;
grid-template-columns: 516px 48px;
letter-spacing: normal;
line-height: 20px;
pointer-events: auto;
text-rendering: optimizelegibility;
text-transform: none
}
.Polaris-Box_375yx{
  border-bottom: 2px solid #e1e3e5;
  background-color: rgba(0, 0, 0, 0);
  border-block-end-width: 1px;
  border-block-start-width: 0px;
  border-end-end-radius: 0px;
  border-end-start-radius: 0px;
  border-inline-end-width: 0px;
  border-inline-start-width: 0px;
  border-start-end-radius: 0px;
  border-start-start-radius: 0px;
  box-shadow: none;
  box-sizing: border-box;
  color: rgb(32, 34, 35);
  color-scheme: light;
  font-family: -apple-system, BlinkMacSystemFont, "San Francisco", "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
  font-size: 29px;
  font-weight: 400;
  inset-block-end: auto;
  inset-block-start: auto;
  inset-inline-end: auto;
  inset-inline-start: auto;
  letter-spacing: normal;
  line-height: 20px;
  max-width: none;
  min-height: auto;
  min-width: auto;
  overflow-x: visible;
  overflow-y: visible;
  padding-block-end: 16px;
  padding-block-start: 16px;
  padding-inline-end: 20px;
  padding-inline-start: 20px;
  pointer-events: auto;
  text-rendering: optimizelegibility;
  text-transform: none;
  width: 620px;
}
.Polaris-Backdrop_1x2i2 {
  animation: var(--p-keyframes-fade-in) var(--p-duration-200) 1 forwards;
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
  background: var(--p-backdrop);
  width: 100vw;
  height: 100vh;
  bottom: 0;
  display: block;
  left: 0;
  position: fixed;
  right: 0;
  top: 0;
  will-change: opacity;
  z-index: var(--p-z-index-10);
}
.Polaris-Modal-Dialog__Container_13mbo {
  bottom: 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  left: 0;
  pointer-events: none;
  position: fixed;
  right: 0;
  top: 0;
  z-index:1000;
}
  @media (min-width: 48em){
    .Polaris-Modal-Dialog__Container_13mbo {
      justify-content: center;
    }
    .Polaris-Modal-Dialog__Modal_2v9yc {
        border-radius: 4px;
        margin: 0 auto;
        max-width: 38.75rem;
        position: relative;
      }
    .Polaris-Text--headingLg_yyh4u {
      font-size: var(--p-font-size-300);
      line-height: var(--p-font-line-height-3);
    }
  }
.Polaris-Modal-Dialog__Modal_2v9yc {
  background: #fff;
  bottom: 0;
  box-shadow: 0 1.625rem 5rem #0003,0 0 0.0625rem #0003;
  display: flex;
  flex-direction: column;
  left: 0;
  max-height: calc(100vh - 3.75rem);
  pointer-events: auto;
  position: fixed;
  right: 0;
  width: 100%;
  top: 2rem;
}
.Polaris-Text--break_32vap {
  overflow-wrap: break-word;
}
.Polaris-Text--semibold_k1k0m {
  font-weight: var(--p-font-weight-semibold);
}
</style>

<style>
  :root{
  --p-breakpoints-xs: 0rem;
  --p-breakpoints-sm: 30.625rem;
  --p-breakpoints-md: 48rem;
  --p-breakpoints-lg: 65rem;
  --p-breakpoints-xl: 90rem;
  --p-color-bg-inverse: #1f2124;
  --p-color-bg-inset-strong: #616a75;
  --p-color-bg-inverse-hover: #616a75;
  --p-color-bg-inverse-active: #87909b;
  --p-color-bg-strong-hover: #caced3;
  --p-color-bg-strong-active: #caced3;
  --p-color-bg-strong: #dde0e4;
  --p-color-bg-subdued-active: #dde0e4;
  --p-color-bg-disabled: #e8eaed;
  --p-color-bg-interactive-disabled: #e8eaed;
  --p-color-bg-app: #f1f2f4;
  --p-color-bg-app-active: #dde0e4;
  --p-color-bg-app-hover: #e8eaed;
  --p-color-bg-app-selected: #e8eaed;
  --p-color-bg-active: #e8eaed;
  --p-color-bg-subdued-hover: #e8eaed;
  --p-color-bg-inset: #f1f2f4;
  --p-color-bg-hover: #f1f2f4;
  --p-color-bg-subdued: #f9fafb;
  --p-color-bg-input: #fff;
  --p-color-bg: #fff;
  --p-color-bg-primary-active: #0c3b2f;
  --p-color-bg-primary-hover: #125443;
  --p-color-bg-primary: #008060;
  --p-color-bg-success-strong: #16a679;
  --p-color-bg-success: #a1edd0;
  --p-color-bg-primary-subdued-active: #c0f2dd;
  --p-color-bg-success-subdued-active: #c0f2dd;
  --p-color-bg-success-subdued: #e0f8ee;
  --p-color-bg-primary-subdued-hover: #e0f8ee;
  --p-color-bg-success-subdued-hover: #f0fdf8;
  --p-color-bg-primary-subdued: #f0fdf8;
  --p-color-bg-primary-subdued-selected: #f0fdf8;
  --p-color-bg-critical-strong-active: #731807;
  --p-color-bg-critical-strong-hover: #9f200a;
  --p-color-bg-critical-strong: #c5280c;
  --p-color-bg-critical-subdued-active: #fbc5bc;
  --p-color-bg-critical: #fbc5bc;
  --p-color-bg-critical-subdued: #fde2dd;
  --p-color-bg-critical-subdued-hover: #fef3f1;
  --p-color-bg-caution-strong: #d89b0d;
  --p-color-bg-caution: #f8d990;
  --p-color-bg-caution-subdued-active: #fae5b2;
  --p-color-bg-caution-subdued: #fcf0d4;
  --p-color-bg-caution-subdued-hover: #fef8ec;
  --p-color-bg-info-strong: #2aacbb;
  --p-color-bg-info-subdued-active: #b8e9ef;
  --p-color-bg-info: #b8e9ef;
  --p-color-bg-info-subdued: #def5f7;
  --p-color-bg-info-subdued-hover: #eefafb;
  --p-color-bg-interactive-active: #0e356c;
  --p-color-bg-interactive-hover: #144995;
  --p-color-bg-interactive: #2463bc;
  --p-color-bg-interactive-subdued-active: #bbd4f7;
  --p-color-bg-interactive-subdued-hover: #e8f0fd;
  --p-color-bg-interactive-subdued: #f0f5fd;
  --p-color-bg-interactive-selected: #f0f5fd;
  --p-color-bg-warning: #fac9a8;
  --p-color-bg-magic-strong: #7945e3;
  --p-color-bg-magic-hover: #e2d6fa;
  --p-color-bg-magic: #ece3fd;
  --p-color-bg-magic-subdued-hover: #ece3fd;
  --p-color-bg-magic-subdued: #f2edfd;
  --p-color-border-input-hover: #616a75;
  --p-color-border-inverse: #616a75;
  --p-color-border-strong-hover: #87909b;
  --p-color-border-input: #abb1ba;
  --p-color-border-hover: #abb1ba;
  --p-color-border-strong: #abb1ba;
  --p-color-border: #caced3;
  --p-color-border-disabled: #dde0e4;
  --p-color-border-subdued: #dde0e4;
  --p-color-border-interactive-disabled: #dde0e4;
  --p-color-border-primary: #008060;
  --p-color-border-success: #16a679;
  --p-color-border-success-subdued: #c0f2dd;
  --p-color-border-critical-active: #430e04;
  --p-color-border-critical-hover: #731807;
  --p-color-border-critical: #c5280c;
  --p-color-border-critical-subdued: #fbc5bc;
  --p-color-border-caution: #d89b0d;
  --p-color-border-caution-subdued: #fae5b2;
  --p-color-border-info: #3bc3d3;
  --p-color-border-info-subdued: #b8e9ef;
  --p-color-border-interactive-active: #0e356c;
  --p-color-border-interactive-hover: #144995;
  --p-color-border-interactive: #3e7dd5;
  --p-color-border-interactive-focus: #3e7dd5;
  --p-color-border-interactive-subdued: #bbd4f7;
  --p-color-border-magic-strong: #7945e3;
  --p-color-border-magic: #ad8bf1;
  --p-color-icon-hover: #1f2124;
  --p-color-icon: #616a75;
  --p-color-icon-active: #1f2124;
  --p-color-icon-subdued: #87909b;
  --p-color-icon-disabled: #abb1ba;
  --p-color-icon-interactive-disabled: #abb1ba;
  --p-color-icon-inverse: #dde0e4;
  --p-color-icon-on-color: #fff;
  --p-color-icon-primary: #008060;
  --p-color-icon-success: #16a679;
  --p-color-icon-critical: #c5280c;
  --p-color-icon-caution: #b77e0b;
  --p-color-icon-info: #16a679;
  --p-color-icon-warning: #f27522;
  --p-color-icon-interactive-active: #0e356c;
  --p-color-icon-interactive-hover: #144995;
  --p-color-icon-interactive: #2463bc;
  --p-color-icon-interactive-inverse: #6699e1;
  --p-color-icon-magic: #5a24cd;
  --p-color-text: #1f2124;
  --p-color-text-subdued: #616a75;
  --p-color-text-disabled: #87909b;
  --p-color-text-interactive-disabled: #87909b;
  --p-color-text-inverse-subdued: #abb1ba;
  --p-color-text-inverse: #f1f2f4;
  --p-color-text-on-color: #fff;
  --p-color-text-success-strong: #0c3b2f;
  --p-color-text-success: #008060;
  --p-color-text-primary: #008060;
  --p-color-text-primary-hover: #125443;
  --p-color-text-critical-strong: #430e04;
  --p-color-text-critical-active: #731807;
  --p-color-text-critical: #c5280c;
  --p-color-text-caution-strong: #4d2e05;
  --p-color-text-caution: #875c08;
  --p-color-text-info-strong: #104147;
  --p-color-text-info: #20828d;
  --p-color-text-warning-strong: #4d2405;
  --p-color-text-interactive-active: #0e356c;
  --p-color-text-interactive-hover: #144995;
  --p-color-text-interactive: #2463bc;
  --p-color-text-interactive-inverse: #6699e1;
  --p-color-text-magic-strong: #310d78;
  --p-color-text-magic: #5a24cd;
  --p-background: #f6f6f7;
  --p-background-hovered: #f1f2f3;
  --p-background-pressed: #edeeef;
  --p-background-selected: #edeeef;
  --p-surface: #fff;
  --p-surface-dark: #202123;
  --p-surface-neutral: #e4e5e7;
  --p-surface-neutral-hovered: #dbdddf;
  --p-surface-neutral-pressed: #c9ccd0;
  --p-surface-neutral-disabled: #f1f2f3;
  --p-surface-neutral-subdued: #f6f6f7;
  --p-surface-neutral-subdued-dark: #44474a;
  --p-surface-subdued: #fafbfb;
  --p-surface-disabled: #fafbfb;
  --p-surface-hovered: #f6f6f7;
  --p-surface-hovered-dark: #2f3133;
  --p-surface-pressed: #f1f2f3;
  --p-surface-pressed-dark: #3e4043;
  --p-surface-depressed: #edeeef;
  --p-surface-search-field: #f1f2f3;
  --p-surface-search-field-dark: #2f3133;
  --p-backdrop: #00000080;
  --p-overlay: #ffffff80;
  --p-shadow-color-picker: #00000080;
  --p-shadow-color-picker-dragger: #212b3652;
  --p-hint-from-direct-light: #00000026;
  --p-border: #8c9196;
  --p-border-on-dark: #505356;
  --p-border-neutral-subdued: #babfc3;
  --p-border-hovered: #999ea4;
  --p-border-disabled: #d2d5d8;
  --p-border-subdued: #c9cccf;
  --p-border-depressed: #575959;
  --p-border-shadow: #aeb4b9;
  --p-border-shadow-subdued: #babfc4;
  --p-divider: #e1e3e5;
  --p-divider-dark: #454749;
  --p-icon: #5c5f62;
  --p-icon-on-dark: #a6acb2;
  --p-icon-hovered: #1a1c1d;
  --p-icon-pressed: #44474a;
  --p-icon-disabled: #babec3;
  --p-icon-subdued: #8c9196;
  --p-text: #202223;
  --p-text-on-dark: #e3e5e7;
  --p-text-disabled: #8c9196;
  --p-text-subdued: #6d7175;
  --p-text-subdued-on-dark: #999fa4;
  --p-interactive: #2c6ecb;
  --p-interactive-on-dark: #36a3ff;
  --p-interactive-disabled: #bdc1cc;
  --p-interactive-hovered: #1f5199;
  --p-interactive-pressed: #103262;
  --p-interactive-pressed-on-dark: #88bcff;
  --p-focused: #458fff;
  --p-surface-selected: #f2f7fe;
  --p-surface-selected-hovered: #edf4fe;
  --p-surface-selected-pressed: #e5effd;
  --p-icon-on-interactive: #fff;
  --p-text-on-interactive: #fff;
  --p-action-secondary: #fff;
  --p-action-secondary-disabled: #fff;
  --p-action-secondary-hovered: #f6f6f7;
  --p-action-secondary-hovered-dark: #54575b;
  --p-action-secondary-pressed: #f1f2f3;
  --p-action-secondary-pressed-dark: #606467;
  --p-action-secondary-depressed: #6d7175;
  --p-action-primary: #008060;
  --p-action-primary-disabled: #f1f1f1;
  --p-action-primary-hovered: #006e52;
  --p-action-primary-pressed: #005e46;
  --p-action-primary-depressed: #003d2c;
  --p-icon-on-primary: #fff;
  --p-text-on-primary: #fff;
  --p-text-primary: #007b5c;
  --p-text-primary-hovered: #006c50;
  --p-text-primary-pressed: #005c44;
  --p-surface-primary-selected: #f1f8f5;
  --p-surface-primary-selected-hovered: #b3d0c3;
  --p-surface-primary-selected-pressed: #a2bcb0;
  --p-border-critical: #fd5749;
  --p-border-critical-subdued: #e0b3b2;
  --p-border-critical-disabled: #ffa7a3;
  --p-icon-critical: #d72c0d;
  --p-surface-critical: #fed3d1;
  --p-surface-critical-subdued: #fff4f4;
  --p-surface-critical-subdued-hovered: #fff0f0;
  --p-surface-critical-subdued-pressed: #ffe9e8;
  --p-surface-critical-subdued-depressed: #febcb9;
  --p-text-critical: #d72c0d;
  --p-action-critical: #d82c0d;
  --p-action-critical-disabled: #f1f1f1;
  --p-action-critical-hovered: #bc2200;
  --p-action-critical-pressed: #a21b00;
  --p-action-critical-depressed: #6c0f00;
  --p-icon-on-critical: #fff;
  --p-text-on-critical: #fff;
  --p-interactive-critical: #d82c0d;
  --p-interactive-critical-disabled: #fd938d;
  --p-interactive-critical-hovered: #cd290c;
  --p-interactive-critical-pressed: #670f03;
  --p-border-warning: #b98900;
  --p-border-warning-subdued: #e1b878;
  --p-icon-warning: #b98900;
  --p-surface-warning: #ffd79d;
  --p-surface-warning-subdued: #fff5ea;
  --p-surface-warning-subdued-hovered: #fff2e2;
  --p-surface-warning-subdued-pressed: #ffebd3;
  --p-text-warning: #916a00;
  --p-border-highlight: #449da7;
  --p-border-highlight-subdued: #98c6cd;
  --p-icon-highlight: #00a0ac;
  --p-surface-highlight: #a4e8f2;
  --p-surface-highlight-subdued: #ebf9fc;
  --p-surface-highlight-subdued-hovered: #e4f7fa;
  --p-surface-highlight-subdued-pressed: #d5f3f8;
  --p-text-highlight: #347c84;
  --p-border-success: #00a47c;
  --p-border-success-subdued: #95c9b4;
  --p-icon-success: #007f5f;
  --p-surface-success: #aee9d1;
  --p-surface-success-subdued: #f1f8f5;
  --p-surface-success-subdued-hovered: #ecf6f1;
  --p-surface-success-subdued-pressed: #e2f1ea;
  --p-text-success: #008060;
  --p-icon-attention: #8a6116;
  --p-surface-attention: #ffea8a;
  --p-decorative-one-icon: #7e5700;
  --p-decorative-one-surface: #ffc96b;
  --p-decorative-one-text: #3d2800;
  --p-decorative-two-icon: #af294e;
  --p-decorative-two-surface: #ffc4b0;
  --p-decorative-two-text: #490b1c;
  --p-decorative-three-icon: #006d41;
  --p-decorative-three-surface: #92e6b5;
  --p-decorative-three-text: #002f19;
  --p-decorative-four-icon: #006a68;
  --p-decorative-four-surface: #91e0d6;
  --p-decorative-four-text: #002d2d;
  --p-decorative-five-icon: #ae2b4c;
  --p-decorative-five-surface: #fdc9d0;
  --p-decorative-five-text: #4f0e1f;
  --p-shadow-transparent: 0 0 0 0 #0000;
  --p-shadow-faint: 0 0.0625rem 0 0 #161d250d;
  --p-shadow-base: 0 0 0 0.0625rem #3f3f440d,0 0.0625rem 0.1875rem 0 #3f3f4426;
  --p-shadow-deep: 0 0 0 0.0625rem #062c521a,0 0.125rem 1rem #212b3614;
  --p-shadow-button: 0 0.0625rem 0 #0000000d;
  --p-shadow-top-bar: 0 0.125rem 0.125rem -0.0625rem #00000026;
  --p-shadow-card: 0 0 0.3125rem #1718180d,0 0.0625rem 0.125rem #00000026;
  --p-shadow-popover: 0 0.1875rem 0.375rem -0.1875rem #17181814,0 0.5rem 1.25rem -0.25rem #1718181f;
  --p-shadow-layer: 0 1.9375rem 2.5625rem 0 #202a3533,0 0.125rem 1rem 0 #202a3614;
  --p-shadow-modal: 0 1.625rem 5rem #0003,0 0 0.0625rem #0003;
  --p-shadows-inset-button: inset 0 -0.0625rem 0 #0003;
  --p-shadows-inset-button-pressed: inset 0 0.0625rem 0 #00000026;
  --p-font-family-sans: -apple-system,BlinkMacSystemFont,"San Francisco","Segoe UI",Roboto,"Helvetica Neue",sans-serif;
  --p-font-family-mono: ui-monospace,SFMono-Regular,"SF Mono",Consolas,"Liberation Mono",Menlo,monospace;
  --p-font-size-75: 0.75rem;
  --p-font-size-100: 0.875rem;
  --p-font-size-200: 1rem;
  --p-font-size-300: 1.25rem;
  --p-font-size-400: 1.5rem;
  --p-font-size-500: 1.75rem;
  --p-font-size-600: 2rem;
  --p-font-size-700: 2.5rem;
  --p-font-weight-regular: 400;
  --p-font-weight-medium: 500;
  --p-font-weight-semibold: 600;
  --p-font-weight-bold: 700;
  --p-font-line-height-1: 1rem;
  --p-font-line-height-2: 1.25rem;
  --p-font-line-height-3: 1.5rem;
  --p-font-line-height-4: 1.75rem;
  --p-font-line-height-5: 2rem;
  --p-font-line-height-6: 2.5rem;
  --p-font-line-height-7: 3rem;
  --p-override-loading-z-index: 514;
  --p-choice-size: 1.25rem;
  --p-icon-size-small: 0.5rem;
  --p-icon-size-medium: 1.25rem;
  --p-choice-margin: 0.0625rem;
  --p-control-border-width: 0.125rem;
  --p-banner-border-default: inset 0 0.0625rem 0 0 var(--p-border-neutral-subdued),inset 0 0 0 0.0625rem var(--p-border-neutral-subdued);
  --p-banner-border-success: inset 0 0.0625rem 0 0 var(--p-border-success-subdued),inset 0 0 0 0.0625rem var(--p-border-success-subdued);
  --p-banner-border-highlight: inset 0 0.0625rem 0 0 var(--p-border-highlight-subdued),inset 0 0 0 0.0625rem var(--p-border-highlight-subdued);
  --p-banner-border-warning: inset 0 0.0625rem 0 0 var(--p-border-warning-subdued),inset 0 0 0 0.0625rem var(--p-border-warning-subdued);
  --p-banner-border-critical: inset 0 0.0625rem 0 0 var(--p-border-critical-subdued),inset 0 0 0 0.0625rem var(--p-border-critical-subdued);
  --p-thin-border-subdued: 0.0625rem solid var(--p-border-subdued);
  --p-text-field-spinner-offset: 0.125rem;
  --p-text-field-focus-ring-offset: -0.25rem;
  --p-button-group-item-spacing: -0.0625rem;
  --p-range-slider-thumb-size-base: 1rem;
  --p-range-slider-thumb-size-active: 1.5rem;
  --p-frame-offset: 0rem;
  --p-duration-0: 0ms;
  --p-duration-50: 50ms;
  --p-duration-100: 100ms;
  --p-duration-150: 150ms;
  --p-duration-200: 200ms;
  --p-duration-250: 250ms;
  --p-duration-300: 300ms;
  --p-duration-350: 350ms;
  --p-duration-400: 400ms;
  --p-duration-450: 450ms;
  --p-duration-500: 500ms;
  --p-duration-5000: 5000ms;
  --p-ease: cubic-bezier(0.25,0.1,0.25,1);
  --p-ease-in: cubic-bezier(0.42,0,1,1);
  --p-ease-out: cubic-bezier(0,0,0.58,1);
  --p-ease-in-out: cubic-bezier(0.42,0,0.58,1);
  --p-linear: cubic-bezier(0,0,1,1);
  --p-keyframes-bounce: p-keyframes-bounce;
  --p-keyframes-fade-in: p-keyframes-fade-in;
  --p-keyframes-pulse: p-keyframes-pulse;
  --p-keyframes-spin: p-keyframes-spin;
  --p-border-radius-05: 0.125rem;
  --p-border-radius-1: 0.25rem;
  --p-border-radius-2: 0.5rem;
  --p-border-radius-3: 0.75rem;
  --p-border-radius-4: 1rem;
  --p-border-radius-5: 1.25rem;
  --p-border-radius-6: 1.875rem;
  --p-border-radius-full: 624.9375rem;
  --p-border-radius-base: 0.1875rem;
  --p-border-radius-large: 0.375rem;
  --p-border-radius-half: 50%;
  --p-border-width-1: 0.0625rem;
  --p-border-width-2: 0.125rem;
  --p-border-width-3: 0.1875rem;
  --p-border-width-4: 0.25rem;
  --p-border-width-5: 0.3125rem;
  --p-border-base: var(--p-border-width-1) solid var(--p-border-subdued);
  --p-border-dark: var(--p-border-width-1) solid var(--p-border);
  --p-border-transparent: var(--p-border-width-1) solid #0000;
  --p-border-divider: var(--p-border-width-1) solid var(--p-divider);
  --p-border-divider-on-dark: var(--p-border-width-1) solid var(--p-divider-dark);
  --p-space-0: 0;
  --p-space-025: 0.0625rem;
  --p-space-05: 0.125rem;
  --p-space-1: 0.25rem;
  --p-space-2: 0.5rem;
  --p-space-3: 0.75rem;
  --p-space-4: 1rem;
  --p-space-5: 1.25rem;
  --p-space-6: 1.5rem;
  --p-space-8: 2rem;
  --p-space-10: 2.5rem;
  --p-space-12: 3rem;
  --p-space-16: 4rem;
  --p-space-20: 5rem;
  --p-space-24: 6rem;
  --p-space-28: 7rem;
  --p-space-32: 8rem;
  --p-z-index-1: 100;
  --p-z-index-2: 400;
  --p-z-index-3: 510;
  --p-z-index-4: 512;
  --p-z-index-5: 513;
  --p-z-index-6: 514;
  --p-z-index-7: 515;
  --p-z-index-8: 516;
  --p-z-index-9: 517;
  --p-z-index-10: 518;
  --p-z-index-11: 519;
  --p-z-index-12: 520;
  --p-z-1: 100;
  --p-z-2: 400;
  --p-z-3: 510;
  --p-z-4: 512;
  --p-z-5: 513;
  --p-z-6: 514;
  --p-z-7: 515;
  --p-z-8: 516;
  --p-z-9: 517;
  --p-z-10: 518;
  --p-z-11: 519;
  --p-z-12: 520;
  color-scheme: light;
}
</style>