
<template>
<!--  <Authorization/>-->
  <div class="example" v-if="is_waiting">
     <a-spin size="large" />
  </div>



  <Error v-if="is_error" :error_text="error_text" :back_url="back_url"/>

  <Loading v-if="is_loading"/>

  <div v-if="this.is_error === false && this.is_loading === false" class="main-container" style="display: flex;
    flex-direction: column;
    align-items: baseline;
    overflow-y: scroll;
  ">
       <Redirect_Instagram  @setError="setError" @setWaiting="setWaiting" @update_instagram_data="update_instagram_data" :is_open_change_acc_modal="is_open_change_acc_modal" @setPopUp="setPopUp"  :client_id="client_id" :redirect_url="redirect_url" :shopify_url="shopify_url" :instagram_user_name="instagram_user_name"/>
       <div  v-if="is_open_change_acc_modal">
         <ChangeAccModal :is_open_change_acc_modal="is_open_change_acc_modal" @setPopUp="setPopUp" class="active"/>
      </div>

      <div v-if="is_open_image_modal">
        <ImageModel :type="type" :watch_list="watch_list" :media_id="media_id" :permalink="permalink" @openTagProduct="openTagProduct" @previousImage="previousImage" @nextImage="nextImage" :index="index" :instagram_data="instagram_data" :image_src="image_src" :user_name="instagram_user_name" :caption="caption" :date_created="date_created" @closeModal="closeModal"/>
      </div>

      <div style="width: 100%">
      <MainContent @update_instagram_data="update_instagram_data" @setError="setError" @paidFeature="paidFeature" @setWaiting="setWaiting" :instagram_data="instagram_data" @openImageModal="openImageModal"/>
      </div>

      <div v-if="is_open_tag_product">
       <TagProduct @update_instagram_data="update_instagram_data" :instagram_data="instagram_data"  @closeTagProduct="closeTagProduct" :media_id="media_id" @watch_list_product="watch_list_product"/>
      </div>

   </div>

</template>

<script>


import axios from "axios";

import Error from "./components/Error.vue";
import Loading from "./components/Loading.vue";
import { notification } from 'ant-design-vue';
import Redirect_Instagram from "./components/Redirect_Instagram.vue";
import ChangeAccModal from "./components/Modal/ChangeAccModal.vue";
import MainContent from "./components/MainContent.vue";
import ImageModel from "./components/Modal/ImageModel.vue";
import TagProduct from "./components/Modal/TagProduct.vue";
window.global_media_data = [];
window.global_postToShow = "All"
window.global_displayTagPost = "Off"
export default {
    name: "App",
    components:{
        TagProduct,
        ImageModel,
        MainContent,
        ChangeAccModal,
        Redirect_Instagram,

      Error,
      Loading

    },
    data() {
          return {
              currentTab: '',
              tabs: ['App','Error','Loading'],

              shopify_url:'',
              code:'',
              user_id:'',
              error_text:'',
              instagram_data:'',
              is_waiting:false,
              back_url:'',
              is_error:false,
              is_loading:false,
              is_open_change_acc_modal:false,
              is_open_image_modal:false,
              client_id:'',
              redirect_url:'',
              instagram_user_name:'',

              //MainContent
              image_src:'',
              index:0,
              caption:'',
              is_open_tag_product:false,
              date_created:'',
              permalink:'',
              media_id:'',
              watch_list:'',
              type:'',
              postToShow:'',
              displayTagPost:''

          }
      },
    watch: {
        instagram_data(newone) {

            this.instagram_data = newone
        },
    },
  methods:{
      closeModal(){this.is_open_image_modal = false},
      closeTagProduct(){
        this.is_open_tag_product = false
      },
      openTagProduct(){
        this.is_open_tag_product = true
      },
      watch_list_product(data){
        this.watch_list =data
      },
      paidFeature(postToShow,displayTagPost){
      this.postToShow =postToShow
      this.displayTagPost = displayTagPost
    },
      setPopUp(flag){
       this.is_open_change_acc_modal = flag
     },
      update_instagram_data(data){

        this.instagram_data = data
      },
      setWaiting(flag){
        this.is_waiting = flag
      },
      setError(text,shop){
        var state = {authorize_url:'https://odoo.website/shopify_mint/main?shop_url='+this.shopify_url};
        this.is_error = true
        this.error_text = text
        this.back_url = 'https://odoo.website/shopify_mint/main?shop_url='+shop
        history.pushState('https://odoo.website/shopify_mint/error', '', 'https://odoo.website/shopify_mint/error');
      },
      openImageModal(type,src,index,caption,date,permalink,id){
      this.media_id = id
       this.image_src = src
        this.index = index
       this.caption = caption
       this.is_open_image_modal = true
      this.date_created = date
      this.permalink = permalink
      this.type = type
      },
      setImage(previous_media,index){


       this.index =index
       this.image_src = previous_media.media_url
        this.caption = previous_media.caption
        this.media_id = previous_media.media_id
        this.type = previous_media.type
      },
      previousImage(index){

      let index_num = parseInt(index)-1
      while(index_num < this.instagram_data.media_url.length){
        let previous_media = null
        if(index_num  === -1){
          previous_media = this.instagram_data.media_url[this.instagram_data.media_url.length-1]
          index_num = this.instagram_data.media_url.length-1
        }
        else{
          previous_media = this.instagram_data.media_url[index_num]
        }
        //check dk con lai neu ko duoc thi i--
        if(this.postToShow === "Pictures only" && this.displayTagPost ==="On"){
          if(previous_media.type ==="IMAGE" && previous_media.num_of_tagged_product !==0){
            this.setImage(previous_media,index_num)
            break;
          }
          else{
            --index_num;
          }
        }
        else if(this.postToShow === "Pictures only"  && this.displayTagPost ==="Off"){
           if(previous_media.type ==="IMAGE"){
            this.setImage(previous_media,index_num)
            break;
          }
          else{
            --index_num;
          }
        }
        else if(this.postToShow === "Videos only"  && this.displayTagPost ==="On"){
          if(previous_media.type ==="VIDEO" && previous_media.num_of_tagged_product !== 0){
            this.setImage(previous_media,index_num)
            break;
          }
          else{
            --index_num;
          }
        }
        else if(this.postToShow === "Videos only" && this.displayTagPost ==="Off"){
          if(previous_media.type ==="VIDEO"){
            this.setImage(previous_media,index_num)
            break;
          }
          else{
            --index_num;
          }
        }
        else if(this.postToShow === "All" && this.displayTagPost ==="On"){
          if(previous_media.num_of_tagged_product !== 0){
            this.setImage(previous_media,index_num)
            break;
          }
          else{
            --index_num;
          }
        }
        else{
          this.setImage(previous_media,index_num)
            break;
        }

      }


    },
    nextImage(index){


      let index_num = parseInt(index)+1
      while(index_num > -1){
        let previous_media = null
        if(index_num  === this.instagram_data.media_url.length){
          previous_media = this.instagram_data.media_url[0]
          index_num = 0
        }
        else{
          previous_media = this.instagram_data.media_url[index_num]
        }
        //check dk con lai neu ko duoc thi i--
        if(this.postToShow === "Pictures only" && this.displayTagPost ==="On"){
          if(previous_media.type ==="IMAGE" && previous_media.num_of_tagged_product !==0){
            this.setImage(previous_media,index_num)
            break;
          }
          else{
            ++index_num;
          }
        }
        else if(this.postToShow === "Pictures only"  && this.displayTagPost ==="Off"){
           if(previous_media.type ==="IMAGE"){
            this.setImage(previous_media,index_num)
            break;
          }
          else{
            ++index_num;
          }
        }
        else if(this.postToShow === "Videos only"  && this.displayTagPost ==="On"){
          if(previous_media.type ==="VIDEO" && previous_media.num_of_tagged_product !== 0){
            this.setImage(previous_media,index_num)
            break;
          }
          else{
            ++index_num;
          }
        }
        else if(this.postToShow === "Videos only" && this.displayTagPost ==="Off"){
          if(previous_media.type ==="VIDEO"){
            this.setImage(previous_media,index_num)
            break;
          }
          else{
            ++index_num;
          }
        }
        else if(this.postToShow === "All" && this.displayTagPost ==="On"){
          if(previous_media.num_of_tagged_product !== 0){
            this.setImage(previous_media,index_num)
            break;
          }
          else{
            ++index_num;
          }
        }
        else{
          this.setImage(previous_media,index_num)
          break;
        }

      }
    },
  },
    mounted() {
       this.is_loading = true
      if(window.global_flag === true){
              let queryString = window.location.search
             let urlParams = new URLSearchParams(queryString)
             this.shopify_url = urlParams.get('shop_url')
             //viet ham check xem co ton tai database dua tren ten shop
            // ham goi den trang van co shop_url de ma neu no co
            // ko can nhieu param nua
            if(urlParams.get('shop_url')){

               axios.post('/check_instagram_user_data_exist', {
                jsonrpc: "2.0",
                params: {
                     shopify_url:urlParams.get('shop_url')
                }
            }).then((res) => {

                 if (res.status === 200) {

                     if(JSON.parse(res.data.result) !== ''){
                         let result = JSON.parse(res.data.result)
                         this.instagram_data = result.instagram_data
                         this.client_id = result.client_id
                         this.redirect_url = result.redirect_url
                         this.instagram_user_name = this.instagram_data.user_name
                         console.log(this.instagram_data)
                         var state = {authorize_url:'https://odoo.website/shopify_mint/main?shop_url='+this.shopify_url};

                         history.pushState(state, '', 'https://odoo.website/shopify_mint/main?shop_url='+this.shopify_url);

                     }
                 this.is_loading = false
                 }

            })
           }


            if(window.global_code !== '' && window.global_code !== undefined) {

                this.code = window.global_code
                var shop_url_storage = localStorage.getItem("shop_url_instagram_shopify");
                this.shopify_url = shop_url_storage


                axios.post('/get_instagram_data', {
                    jsonrpc: "2.0",
                    params: {
                        shop_url: shop_url_storage,
                        code: this.code
                    }
                }).then((res) => {

                    if (res.status === 200) {

                        if (JSON.parse(res.data.result) !== '' || JSON.parse(res.data.result) !== undefined) {

                            if (JSON.parse(res.data.result) === 'Instagram user already been used') {
                                this.setError('Instagram user already been used', localStorage.getItem("shop_url_instagram_shopify"))
                            } else if (JSON.parse(res.data.result) === 'Shop not exist') {
                                this.setError('Shop not exist', localStorage.getItem("shop_url_instagram_shopify"))
                            } else {

                                var state = {authorize_url: 'https://odoo.website/shopify_mint/main?shop_url=' + localStorage.getItem("shop_url_instagram_shopify")};
                                history.pushState(state, '', 'https://odoo.website/shopify_mint/main?shop_url=' + localStorage.getItem("shop_url_instagram_shopify"));
                                let result = JSON.parse(res.data.result)
                                this.instagram_data = result.instagram_data
                                this.client_id = result.client_id
                                this.redirect_url = result.redirect_url
                                this.redirect_url = result.redirect_url
                                this.instagram_user_name = this.instagram_data.user_name

                                localStorage.removeItem("shop_url_instagram_shopify");
                                this.is_loading = false
                            }

                        } else {
                            this.setError('Code is not verify')
                        }


                    }

                })


            }



      }
      else{
        this.setError("Not user")
      }


    }

}

</script>
<style>
#app{
min-height: 100vh;
background-color: #f4f6f8;
font-family: -apple-system,blinkmacsystemfont,san francisco,roboto,segoe ui,helvetica neue,sans-serif;

}
.example {
  width: 100%;
  height: 100%;
  position: fixed;
  text-align: center;
  background: rgb(0 0 0 / 60%);
  border-radius: 4px;
  margin-bottom: 20px;
  padding: 30px 50px;

  z-index: 9999999999999999;
  display: flex;
  justify-content: center;
  align-items: center;
}
.main-container{
      width: 100%;
      gap: 1rem;
      padding:0 2rem;
    }
</style>