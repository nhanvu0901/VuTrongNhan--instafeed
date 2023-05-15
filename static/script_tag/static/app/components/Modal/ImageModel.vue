<template>
  <div class="instafeed-lightbox" id="1-insta-feed">
    <div class="lightbox-instagram" role="dialog" aria-labelledby="1-insta-feed" aria-modal="true">

      <div class="instafeed-post-image" style="width: 60%;height: 100%;float: left" v-if="this.type === 'IMAGE'">
        <img :src="this.image_src" style="max-width: 60% ;
  right: auto !important;">
      </div>

     <div class="instafeed-post-image" v-else-if="this.type === 'CAROUSEL_ALBUM'" style="width: 60%;float: left;height: 100%">
          <ImageCarousel :child_carousel="child_carousel"/>
    </div>

      <div class="instafeed-post-image" v-else>
         <video :src="this.image_src" style="float: left;width: 60%;height: 100%" id="feed-id" controls >

        </video>
      </div>


      <div class="description">
        <div class="instafeed-header">
          <div class="close-button" @click="this.$emit('closeModal')">
            <a style="height:25px;width:25px;display:block!important;position:relative;background: transparent;" aria-label="close button" href="#_" id="close-button-url"></a>
          </div>
          <img src="https://instafeed.nfcube.com/assets/img/logo-instagram-transparent.png" data-feed-id="insta-feed" class="profile-picture js-lazy-image js-lazy-image--handled" data-src="https://instafeed.nfcube.com/assets/img/logo-instagram-transparent.png" :alt="this.caption">
          <object class="name-section">
            <a class="fullname" :href="'https://www.instagram.com/'+this.user_name+'/'" target="_blank" rel="noopener">
                <div class="fullname instafeed-text" data-feed-id="insta-feed">{{this.user_name}}</div>
            </a>
          </object>
        </div>

        <hr style="margin: 10px;border: 0;border-bottom-color: currentcolor;border-bottom-style: none;border-bottom-width: 0px;border-bottom: 1px solid #e8e9eb;background: 0 0;max-width: 100%;width: auto;">

       <div class="box-content">
         <div class="sub-header">
           <div class="post-engagement">

           </div>
           <div class="arrows">
             <object @click="this.$emit('previousImage',index)" >
               <a style="cursor: pointer">
                 <img src="//instafeed.nfcube.com/assets/img/placeholder.gif" alt="previous image"></a>
             </object>

             <object @click="this.$emit('nextImage',index)" >
               <a style="cursor: pointer">
               <img src="//instafeed.nfcube.com/assets/img/placeholder.gif" alt="next image">
             </a>
             </object>
           </div>
         </div>
         <div class="products-tagging">

         </div><div class="tagging-message" id="tagging-17984454994934934">


       </div>

          <div class="tag-product-container">
          <div v-for="item in list_tagged_product" class="tagged-products" style="margin-bottom: 1rem;">
            <div class="tagged-products-image">
              <object>
                <a  style="cursor: pointer">
                  <img class="js-lazy-image js-lazy-image--handled" :src="item.image_src" alt="product image">
                </a>
              </object>
            </div>

            <div class="tagged-products-buttons" style="text-align: center;">
              <object class="product-title">
                <a :href="item.product_url" target="_blank">{{item.name}}</a>
                <a :href="item.product_url" target="_blank"><button class="tagged-buy-button" tabindex="-1">Shop Now</button></a></object>
            </div>

          </div>
      </div>

         <div class="caption-container"  style="margin: 20px;">
             <div v-if="this.caption !== 'false'" style="display: flex;gap: 10px;margin-bottom: 10px" class="instafeed-caption avatar">
                 <div style="font-size: 30px;">
                    <font-awesome-icon icon="fa-solid fa-circle-user" />
                 </div>
                 <div>
                     <div style="color: #000"><span style="font-weight: 600;">{{this.user_name}}</span> {{this.caption}}</div>
                     <div style="font-size: 12px;font-weight: 400">
                       {{ moment(this.date_created, "YYYYMMDD").fromNow()}}
                    </div>
                 </div>
             </div>


             <div class="comment-container" v-if="this.list_comment !== 'false'">
               <div v-for="item in list_comment" style="margin-bottom: 10px">
                    <div  style="display: flex;align-items: center;gap: 10px;" class="instafeed-caption avatar">
                       <div style="font-size: 30px;">
                          <font-awesome-icon icon="fa-solid fa-circle-user" />
                       </div>
                       <div>
                           <div style="color: #000"><span style="font-weight: 600;">{{item.comment_username}}</span> {{item.comment_text}}</div>
                           <div style="font-size: 12px;font-weight: 400">
                             {{ moment(item.comment_timestamp, "YYYYMMDD").fromNow()}}
                          </div>
                       </div>
                   </div>
               </div>
            </div>

         </div>
       </div>




      <div class="post-date">
             <span style="padding-left:8px;">{{ moment(this.date_created, "YYYYMMDD").fromNow()}}</span> • <object>
              <a :href="this.permalink" target="_blank" rel="noopener" class="follow">View on Instagram</a>
            </object>
      </div>

      </div>
    </div>
  </div>
</template>

<script>
import moment from 'moment'
import ImageCarousel from "./ImageCarousel.vue";
export default {
  name: "ImageModel",
    components: {ImageCarousel},
    created: function () {
    this.moment = moment;
   },
   props:{
    shopify_url:'',
    watch_list:'',
   image_src:String,
    user_name:String,
   caption:String,
     index:String,
     instagram_data:String,
     date_created:String,
     permalink:String,
     post_id:String,
      type:String,
       selected_product:Array,
       list_comment_post:Array

  },
   data() {
    return {
      list_tagged_product :[],
      list_comment:[],
      child_carousel:[]
    }
  },
  mounted() {

// console.log(this.media_id)
      if(this.type === 'CAROUSEL_ALBUM'){
            this.child_carousel = this.image_src.replace(/\[|\]/g,'').split("'").filter(e => typeof e === 'string' && e !== ', ' && e !== '')
      }
      let media_active = this.instagram_data.media_url.find((item) => item.post_id === this.post_id)
      console.log(media_active)
      this.list_tagged_product = this.selected_product
      this.list_comment = this.list_comment_post


          //
          //  var self = this
          // var xmlhttp = new XMLHttpRequest();
          //
          //
          // xmlhttp.open("POST", "https://odoo.website/get_product_list");
          // xmlhttp.setRequestHeader("Content-Type", "application/json");
          // let param = {
          //   shopify_url: '',
          //    media_id : this.media_id,
          // }
          // xmlhttp.onreadystatechange = function () {
          //   if (xmlhttp.readyState === 4) {
          //     if (xmlhttp.status === 200) {
          //
          //
          //       console.log(JSON.parse(JSON.parse(xmlhttp.responseText).result))
          //       self.list_tagged_product = JSON.parse(JSON.parse(xmlhttp.responseText).result)
          //       sessionStorage.setItem("selected#"+self.media_id,JSON.stringify(JSON.parse(JSON.parse(xmlhttp.responseText).result)));
          //     }
          //   }
          //
          // };
          // xmlhttp.send(JSON.stringify(param))

  },
  methods:{
    tagProduct(){
       this.$emit('openTagProduct')
    }
  },
  watch: {
    watch_list(newone){
       this.list_tagged_product = newone
    },
    post_id(newone){
     if(this.type === 'CAROUSEL_ALBUM'){
          this.child_carousel = this.image_src.replace(/\[|\]/g,'').split("'").filter(e => typeof e === 'string' && e !== ', ' && e !== '')
      }
      let media_active = this.instagram_data.media_url.find((item) => item.post_id === newone)
      console.log(media_active)

    },
    selected_product(newone){
        this.list_tagged_product = newone
    },
    list_comment_post(newone){
        this.list_comment = newone
    }

    // whenever question changes, this function will run
   // media_id(newOne){
   //   console.log(this.media_id)
   //   var self = this
   //        var xmlhttp = new XMLHttpRequest();
   //
   //        xmlhttp.open("POST", "https://odoo.website/get_product_list");
   //        xmlhttp.setRequestHeader("Content-Type", "application/json");
   //        let param = {
   //          shopify_url: '',
   //           media_id : newOne,
   //        }
   //        xmlhttp.onreadystatechange = function () {
   //          if (xmlhttp.readyState === 4) {
   //            if (xmlhttp.status === 200) {
   //
   //
   //               self.list_tagged_product = JSON.parse(JSON.parse(xmlhttp.responseText).result)
   //              sessionStorage.setItem("selected#"+self.media_id,JSON.stringify(JSON.parse(JSON.parse(xmlhttp.responseText).result)));
   //            }
   //          }
   //
   //        };
   //        xmlhttp.send(JSON.stringify(param))
   //
   // },
  },
}
</script>

<style scoped>
a{
  cursor: pointer;
}
.tagged-products-image {
  text-align: center;
  font-weight: initial;
}
.tagged-products a {
  color: #000 !important;
  font-size: 14px !important;
}
.lightbox-instagram a:visited {
  font-weight: initial;
}
.tagged-products {
  margin: 40px auto;
  width: 90%;
}
.tagged-products-image {
  width: 100%;
  text-align: center;
}
a {
  border: none !important;
  position: static;
  display: inline;
  padding: 0;
  z-index: 999999;
  color: transparent;
  text-decoration: none !important;
}
img {
  max-width: none;
  object-fit: cover;
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  margin: 0 auto;
  width: 100%;
  height: 100%;
  border-radius: 0;
  transform: initial;
  display: initial;
  opacity: 1;
}
.tagged-products img {
  position: relative !important;
  object-fit: contain !important;
  height: 120px !important;
  width: 120px !important;
}
.tagged-products-image {
  width: 100%;
  text-align: center;
}
.product-title {
  color: #000 !important;
  font-size: 14px !important;
}
.tagged-buy-button {
  color: #fff !important;
  border: 0px !important;
  background-color: #008060 !important;
  border-radius: 2px !important;
}

.tagged-buy-button {
      height: auto;
    background: 0 0;
    background-color: rgba(0, 0, 0, 0);
    border: 1px solid #ccc;
    margin: 5px auto 7px;
    cursor: pointer;
    display: block;
    box-shadow: none;
    outline: 0;
    font-size: 1.3rem !important;
    line-height: 1.6 !important;
    text-transform: uppercase !important;
    letter-spacing: .15rem !important;
    font-weight: 700 !important;
    padding: 1rem 2.75rem !important;
    text-align: center;
    width: 150px !important;
}





.post-date a {
  color: grey;
  font-size: 11px;
}
.post-date {
  color: grey;
  font-size: 11px;
  border-top: 1px solid #eee;
  padding-top: 3px;
  width: 100%;
  height: 30px;
  line-height: 27px;
}
.instafeed-lightbox {

  position: fixed ;
  font-size: 15px;
  z-index: 999;
  width: 100%;
  height: 100%;
  text-align: center;
  top: 0;
  left: 0;
  background: rgba(0,0,0,.8);
}
.instafeed-lightbox:target {
  outline: 0;
  display: block ;
}
.lightbox-instagram {
  height: 80%;
  width: 70%;
  background-color: #fff;
  position: fixed;
  top: 10%;
  left: 15%;
    overflow: hidden;
}
img{

  object-fit: cover;
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  margin: 0 auto;
  width: 100%;
  height: 100%;
  border-radius: 0;
  transform: initial;
  display: initial;
  opacity: 1;
}
.description {
  position: absolute;
  display: flex;
  flex-direction: column;
  height: 100%;
  right: 0;
  width: 40%;
  text-align: left;
  color: #000;
  text-decoration: none;
  box-sizing: content-box;
  padding: 0;
}
.instafeed-header {
  height: 58px !important;
  position: relative !important;
  transform: none;
  margin: 0;
  padding: 0;
  text-align: inherit;
  opacity: 1;
  background: 0 0;
}
.close-button {
  background-image: url(data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHdpZHRoPScyMCcgaGVpZ2h0PScyMCcgY2xhc3M9J2ljb24nPjxwYXRoIGZpbGw9JyM5Mzk1OTgnIGQ9J00xNS44OSAxNC42OTZsLTQuNzM0LTQuNzM0IDQuNzE3LTQuNzE3Yy40LS40LjM3LTEuMDg1LS4wMy0xLjQ4NXMtMS4wODUtLjQzLTEuNDg1LS4wM0w5LjY0MSA4LjQ0NyA0Ljk3IDMuNzc2Yy0uNC0uNC0xLjA4NS0uMzctMS40ODUuMDNzLS40MyAxLjA4NS0uMDMgMS40ODVsNC42NzEgNC42NzEtNC42ODggNC42ODhjLS40LjQtLjM3IDEuMDg1LjAzIDEuNDg1czEuMDg1LjQzIDEuNDg1LjAzbDQuNjg4LTQuNjg3IDQuNzM0IDQuNzM0Yy40LjQgMS4wODUuMzcgMS40ODUtLjAzcy40My0xLjA4NS4wMy0xLjQ4NXonLz48L3N2Zz4=);
  position: absolute;
  right: 0;
  background-repeat: no-repeat;
  width: 20px;
  height: 20px;
  margin: 14px;
}
.profile-picture {
  height: 45px !important;
  width: 45px !important;
  border-radius: 50% !important;
  margin: 12px !important;
  border: 1px solid #eee;
}
.name-section {
  position: absolute;
  top: 24px;
  left: 65px;
}
.instafeed-post-image img {


}
.fullname {
  color: #000;
  font-weight: 600;
  line-height: 23px;
  font-size: 17px;
}
.box-content {
  flex: 1;
  height: 10px;
  overflow-x: hidden;
  position: initial;
  padding-bottom: 20px;
}
.sub-header {
  height: 32px;
  color: grey;
  position: relative;
}
.post-engagement {
  position: absolute !important;
  margin: auto !important;
  left: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
  top: 0 !important;
  display: flex;
  justify-content: center;
  align-items: center;
  text-transform: uppercase;
}
.arrows {
  display: flex;
  justify-content: space-between;
  width: 96%;
  margin: 0 auto;
}
insta-feed a {
  border: none !important;
  position: static;
  display: inline;
  padding: 0;
  z-index: 999;
  color: transparent;
  text-decoration: none !important;
}
.products-tagging {
  margin-top: 15px;
  font-size: 14px;
  text-align: center;
}
.tagging-message {
  width: 90%;
  color: grey;
  margin: 0 auto;
  text-align: center;
}
.instafeed-caption {
  word-wrap: break-word;
  white-space: pre-wrap;
  clear: both;
  color: #666;
  width: 90%;
  margin: 20px auto 0;
}
.arrows a {
  display: inline-block !important;
  height: 32px;
}
a:hover{
  opacity: 1 !important;
}
.arrows object:first-child img {
  background-image: url(data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHZpZXdCb3g9JzAgMCA0NzcuMTc1IDQ3Ny4xNzUnIHdpZHRoPSc1MTInIGhlaWdodD0nNTEyJz48cGF0aCBkPSdNMTQ1LjE4OCAyMzguNTc1bDIxNS41LTIxNS41YzUuMy01LjMgNS4zLTEzLjggMC0xOS4xcy0xMy44LTUuMy0xOS4xIDBsLTIyNS4xIDIyNS4xYy01LjMgNS4zLTUuMyAxMy44IDAgMTkuMWwyMjUuMSAyMjVjMi42IDIuNiA2LjEgNCA5LjUgNHM2LjktMS4zIDkuNS00YzUuMy01LjMgNS4zLTEzLjggMC0xOS4xbC0yMTUuNC0yMTUuNXonIGZpbGw9J2JsYWNrJy8+PC9zdmc+);
}
.arrows object:nth-child(2) img {
  background-image: url(data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHZpZXdCb3g9JzAgMCA0NzcuMTc1IDQ3Ny4xNzUnIHdpZHRoPSc1MTInIGhlaWdodD0nNTEyJz48cGF0aCBkPSdNMzYwLjczMSAyMjkuMDc1bC0yMjUuMS0yMjUuMWMtNS4zLTUuMy0xMy44LTUuMy0xOS4xIDBzLTUuMyAxMy44IDAgMTkuMWwyMTUuNSAyMTUuNS0yMTUuNSAyMTUuNWMtNS4zIDUuMy01LjMgMTMuOCAwIDE5LjEgMi42IDIuNiA2LjEgNCA5LjUgNCAzLjQgMCA2LjktMS4zIDkuNS00bDIyNS4xLTIyNS4xYzUuMy01LjIgNS4zLTEzLjguMS0xOXonIGZpbGw9J2JsYWNrJy8+PC9zdmc+);
}
.arrows img {
  position: relative !important;
  width: 32px !important;
  object-position: 99999px 99999px;
  background: 50%/50% no-repeat;

}
.arrows a:hover, .slider-arrow:hover {
  background-color: #eee;
}
.arrows a:hover, .instafeed-shopify .slider-arrow:hover {
  background-color: #eee;
}
.btn.primary, .button {
  border-radius: 4px;
  background: rgb(0 128 96);
  border: .1rem solid transparent;
  box-shadow: inset 0 1px 0 0 transparent, 0 1px 0 0 rgb(22 29 37 / 5%), 0 0 0 0 transparent;
  font-weight: 400;
  margin: 3px;
  padding: .7rem 1.6rem;
  color: #fff;
  fill: #fff;
}
.btn.primary:hover, .button:hover {
  background: rgb(0 110 82);
}
</style>