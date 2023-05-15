<template>
  <div style="

    ">

    <div style="background-color: #ffffff;
    height: auto; " class="content card five" >

      <form id="instafeed-form"  style="display:inline;">
    <div class="row">
      <label><b>Feed Title</b></label>
      <input type="text" v-model="title" maxlength="255" placeholder="Leave empty if you don't want a title">
    </div>
    <div class="row add-flex">
      <div class="column four">
        <label><b>Post Spacing</b></label>
        <select v-model="spacing" id="space">
          <option value="0">No spacing</option>
          <option value="1px">Small</option>
          <option value="5px">Medium</option>
          <option value="10px">Large</option>
        </select>
      </div>
      <div class="column eight">
        <label><b>On post click</b></label>
        <select v-model="onclickPost" id="onclick">
          <option >Open popup / show product</option>
          <option >Go to Instagram</option>

        </select>
      </div>
    </div>

    <div class="row add-flex">
      <div class="column six">
        <label><b>Layout</b></label>
        <select v-model="layout" id="layout">
          <option >Grid - Squares</option>
          <option >Grid - Tiles</option>
          <option >Carousel - Squares</option>
          <option >Carousel - Auto</option>
          <option >Carousel - Active Classes</option>
          <option >Carousel - Gallery</option>
        </select>
      </div>
      <div class="column six">
        <label><b>Configuration</b><span style="position:relative;font-size:11px;text-transform: none;font-weight:normal;float:right;" class="tip" data-hover="'Auto' lets Instafeed decide the optimal picture size for each device"><font-awesome-icon icon="fa-solid fa-eye" /></span></label>
        <select v-model="autoLayout" id="auto-layout">
          <option>Auto</option>
          <option>Manual</option>
        </select>
      </div>
    </div>

    <div class="row add-flex">
      <div class="column one-half">
        <label id="label-number-rows"><b>Rows</b></label>
        <input type="number" v-model="rows" min="0" max="60" id="rows" placeholder="number of rows">
      </div>
      <div class="column one-half">
        <label id="label-number-columns"><b>Columns</b></label>

        <div v-if="this.autoLayout === 'Auto'">
            <input  disabled="disabled" type="number" v-model="columns" min="0" max="8" id="columns" placeholder="number of columns">
        </div>
        <div v-else>
            <input   type="number" v-model="columns" min="0" max="8" id="columns" placeholder="number of columns">
        </div>

      </div>
    </div>



    <div class="row paid-feature" style="">
        <div class="column one-half">
          <label><b>Show Likes</b> <span class="paid-label"></span> <span style="position:relative;font-size:11px;text-transform: none;font-weight:normal;float:right;" class="tip" data-hover="Likes are only available when you connect your account with Facebook"><font-awesome-icon icon="fa-solid fa-eye" /> </span></label>

          <select disabled="disabled" v-if="this.followers === '' || this.followers === false || this.followers === undefined" id="likes" v-model="showLikes">
            <option>No</option>
            <option>Yes</option>
          </select>

          <select v-else id="likes" v-model="showLikes">
            <option>No</option>
            <option>Yes</option>
          </select>


        </div>
        <div class="column one-half" style="margin-top: 10px;">
          <label><b>Show Followers</b> <span class="paid-label"></span> <span style="position:relative;font-size:11px;text-transform: none;font-weight:normal;float:right;" class="tip" data-hover="Followers are only available when you set a title and connect your account with Facebook"><font-awesome-icon icon="fa-solid fa-eye" /> </span></label>

          <select disabled="disabled" v-if="this.followers === '' || this.followers === false || this.followers === undefined" id="show-followers" v-model="showFollowers">
            <option>No</option>
            <option>Yes</option>
          </select>

          <select v-else id="show-followers"  v-model="showFollowers">
            <option>No</option>
            <option>Yes</option>
          </select>

        </div>

      </div>

        <div class="column twelve" >
          <label><b>Posts to show <span class="paid-label"></span><span class="tip" style="position:relative;font-size:11px;text-transform: none;font-weight:normal;float:right;"  data-hover="Choose the type of post you want to show"><font-awesome-icon icon="fa-solid fa-eye" /> </span></b></label>
          <select id="content" v-model="postToShow">
            <option>All</option>
            <option>Pictures only</option>
            <option>Videos only</option>
          </select>
        </div>

        <div class="column twelve">
          <label><b>Automatic Product Feed <span class="paid-label"></span> <span  style="color:#7cb342;font-size:8px;font-weight:bold;">NEW!</span> <span class="tip" style="position:relative;font-size:11px;text-transform: none;font-weight:normal;float:right;" data-hover="When 'On', add this feed to a product page and it will only display tagged posts"><font-awesome-icon icon="fa-solid fa-eye" /></span></b></label>
          <select id="product-feed-filter" v-model="displayTagPost">
              <option>Off</option>
              <option>On</option>
          </select>
        </div>


        <div class="column twelve">
          <label><b>Filter By HashTags <span class="paid-label"></span> <span class="tip" style="position:relative;font-size:11px;text-transform: none;font-weight:normal;float:right;" data-hover="List of hashtags separated by commas. #myshop,#sale"><font-awesome-icon icon="fa-solid fa-eye" /></span></b></label>
          <input type="text" id="filter" placeholder="Leave empty to show all posts">
        </div>


      <button id="publish" class="btn primary" style="width:100%;margin-top: 1rem" v-on:click="showConfirm"  >Save feed</button>




  </form>




    </div>
    <div style="background-color: #ffffff;height: auto;margin-left: 2%;" class="content card seven">
      <CreateNewFeed @setWaiting="setWaiting" :instagram_data="instagram_data" @updatetFeed="updatetFeed" @setError="this.$emit('setError')" :list_widget="list_widget" :user_id="user_id"  @createNewFeed="showConfirmCreateNewFeed" />
      <label><b>Preview</b></label>
      <hr style="margin: 0;
        border-width: 0;
          border-top-width: 0px;
        border-collapse: collapse;
        border-top: .1rem solid #dfe4e8;">

      <div class="insta-feed" style="display: block;
text-align: center;
clear: both;

">
          <h2>{{this.title}}</h2>
          <div style="font-size: 1.3rem;margin-bottom: 1rem;" v-if="this.showFollowers ==='Yes' && this.followers !== '' && this.followers !== false && this.followers !== undefined    ">{{this.followers}} FOLLOWERS</div>

<!--          <div class="insta-feed-pic" :style="{display: 'grid',gridTemplateColumns: 'auto auto',padding: '0 2rem',gap:this.spacing}">-->
          <div class="insta-feed-pic" style="position: relative;display: block;
text-align: center;
clear: both;">


              <CarouselShop :showLikes="showLikes" :layout="layout" v-if="this.layout === 'Carousel - Gallery' || this.layout ==='Carousel - Squares' || this.layout ==='Carousel - Auto' ||this.layout ==='Carousel - Active Classes'" @openImageModal="openImageModal" :RowColumnModify="RowColumnModify"/>

              <div v-else v-for="(media,index) in RowColumnModify" class="instafeed-container" :class="classLayout" :style="{margin:this.spacing,width:this.calculateWidth}" >
                  <div style="position: relative; width: 100%;" class="image-container"  :data-type="media.type" :data-id="media.post_id" :data-src="media.type === 'CAROUSEL_ALBUM' ? media.media_url.replace(/\[|\]/g,'').split(',')  :media.media_url"  :data-caption="media.caption" :data-index="index" :data-permalink="media.permalink" :data-time="media.created_date" @click="openImageModal">
                       <img v-if="media.type !== 'CAROUSEL_ALBUM'" class="js-lazy-image js-lazy-image--handled" :src="media.type ==='VIDEO' ? media.thumbnail_url : media.media_url"    alt="Instagram post with the caption: ...">
                       <img v-else :src="media.thumbnail_url !== '' ? media.thumbnail_url.replace(/\[|\]/g,'').split(',')[0].replace(/'/g, ''): media.media_url.replace(/\[|\]/g,'').split(',')[0].replace(/'/g, '')">
                        <div style="width:99%;height:99%;" class="instafeed-overlay instafeed-video">

                            <div v-if="media.type ==='VIDEO'">
                                <font-awesome-icon class="icon-big" icon="fa-solid fa-play" />
                            </div>
                            <div v-else>
                                <font-awesome-icon class="icon-big" icon="fa-brands fa-instagram" />
                            </div>



                          <div style="display:flex;gap: 1rem;z-index: 100;opacity: 1;position: absolute;font-size: 17px;color: #fff;bottom: 0;right: 0;" class="show-like" v-if="this.showLikes === 'Yes' && media.media_like !== false && media.media_like !==''">
                                 <div>
                                      <font-awesome-icon icon="fa-solid fa-heart" />
                                      {{media.media_like}}
                                 </div>
                                 <div>
                                      <font-awesome-icon icon="fa-solid fa-comment" />
                                       {{media.media_count}}
                                 </div>
                          </div>

                        </div>
                  </div>

              </div>


          </div>





      </div>
      <em style="margin-top: 15px;" id="tip-product-tagging"><i><b>Tip:</b> Click on a post to start tagging products</i></em>

    </div>
  </div>
</template>

<script>
import { notification } from 'ant-design-vue';
import {ExclamationCircleOutlined} from '@ant-design/icons-vue';
import { SmileOutlined } from '@ant-design/icons-vue';
import { ExclamationOutlined} from "@ant-design/icons-vue";
import { createVNode, h } from 'vue';
import { Modal } from 'ant-design-vue';

import { Carousel, Navigation, Pagination, Slide } from 'vue3-carousel'

import 'vue3-carousel/dist/carousel.css'
import CarouselShop from "./CarouselShop.vue";
import CreateNewFeed from "./CreateNewFeed.vue";
import axios from "axios";



export default {
  name: "MainContent",
  components: {
      CreateNewFeed,
      CarouselShop,
      Carousel,
    Slide,
    Pagination,
    Navigation,},
   props:{
   instagram_data:String
  },

  watch: {
    instagram_data(newone){

        this.media_url = newone.media_url
        this.title= newone.title
        this.spacing= newone.spacing
        this.onclickPost=newone.onclickPost
        this.layout= newone.layout
        this.autoLayout=newone.autoLayout
        this.rows=parseInt(newone.rows)
        this.columns=parseInt(newone.columns)
        this.showLikes=newone.showLikes
        this.showFollwers=newone.showFollwers
        this.followers = newone.followers
        this.postToShow=newone.postToShow
        this.displayTagPost = newone.displayTagPost
        this.choose_widget = newone.choose_widget
        this.user_id = newone.user_id
        this.list_widget = newone.list_widget
    },
      choose_widget(newone){
        this.choose_widget= newone
      },
       postToShow(newon){
        this.postToShow = newon

      },
      displayTagPost(newon){
        this.displayTagPost = newon
      },


  },

  data() {
        return {
         media_url :[],
          title: "Leave empty if you don't want a title",
          spacing: 0,
          onclickPost: 'Open popup / show product',
          layout: 'Grid - Squares',
          autoLayout: 'Auto',
          rows: 0,
          columns: 0,
          showLikes:'No',
          showFollowers:'No',
          followers:'',
          calculateWidth:'29.333%',
          postToShow:'All',
          displayTagPost:'Off',
          choose_widget:{},
          user_id:'',
          list_widget:[]

        }
    },
   mounted() {
    console.log(this.instagram_data)
    if(this.instagram_data !== ''){
        this.title= this.instagram_data.title
        this.spacing= this.instagram_data.spacing
        this.onclickPost=this.instagram_data.onclickPost
        this.layout= this.instagram_data.layout
        this.autoLayout=this.instagram_data.autoLayout
        this.rows=parseInt(this.instagram_data.rows)
        this.columns=parseInt(this.instagram_data.columns)
        this.showLikes=this.instagram_data.showLikes
        this.showFollwers=this.instagram_data.showFollwers
        this.followers = this.instagram_data.followers
        this.postToShow=this.instagram_data.postToShow
        this.displayTagPost = this.instagram_data.displayTagPost
        this.choose_widget = this.instagram_data.choose_widget,
        this.user_id = this.instagram_data.user_id,
        this.list_widget = this.instagram_data.list_widget

    }


   },
   methods: {
    setWaiting(flag){
      this.$emit('setWaiting',flag)
    },
    updatetFeed(res,title,spacing,onclickPost,layout,autoLayout,rows,columns,showLikes,showFollwers,
    postToShow,displayTagPost,followers,media_data){
        this.choose_widget = res.choose_widget
       this.list_widget = res.list_widget
        let data= {
            //TODO widget id cap nhat them
          title:title,
          spacing: spacing,
          onclickPost:onclickPost,
          layout:layout,
          autoLayout:autoLayout,
          rows:rows,
          columns:columns,
          showLikes:showLikes,
          showFollwers:showFollwers,

          postToShow:postToShow,
          displayTagPost : displayTagPost,
          followers:followers ,
          media_url:media_data,
          user_id:this.instagram_data.user_id,
          user_name:this.instagram_data.user_name,
          choose_widget: res.choose_widget,
          list_widget:res.list_widget
      }
       this.$emit('update_instagram_data',data)

    },
    createNewFeed(){
        if(this.instagram_data === ''){
            notification.open({
              message: 'Notification !!',
              description:
                'No instagram user , cannot create new feed',
              duration: 4,
              icon: () => h(ExclamationOutlined, { style: 'color: red' }),
            });
        }
        else{
          let queryString = window.location.search
          let urlParams = new URLSearchParams(queryString)
            this.$emit('setWaiting',true)
          axios.post('/create_new_feed', {
                  jsonrpc: "2.0",
                  params: {
                       shopify_url:urlParams.get('shop_url'),
                      hashed_id:this.instagram_data.choose_widget.hashed_id,//TODO gui id cua thang dang hoat dong
                      user_id:this.instagram_data.user_id


                  }
              }).then((res) => {

                   if (res.status === 200) {
                    let followers =  JSON.parse(res.data.result).followers
                    this.updatetFeed(JSON.parse(res.data.result),"Create new feed",0,'Open popup / show product','Grid - Squares','Auto',
                    "0","0","No","No","All","Off",followers)
                        this.$emit('setWaiting',false)

                   }
              })
          }




    },
   saveFeed(){

     this.$emit('setWaiting',true)
     if(this.instagram_data === ''){
       notification.open({
          message: 'Notification !!',
          description:
            'No instagram user ,cannot save feed',
          duration: 4,
          icon: () => h(ExclamationOutlined, { style: 'color: red' }),
        });
       this.$emit('setWaiting',false)
     }
     else{
       let queryString = window.location.search
       let urlParams = new URLSearchParams(queryString)
       var self = this
      var xmlhttp = new XMLHttpRequest();
      this.shopify_url = urlParams.get('shop_url')
      xmlhttp.open("POST", "https://odoo.website/save_feed");
      xmlhttp.setRequestHeader("Content-Type", "application/json");
      let param={
        shopify_url:urlParams.get('shop_url'),
            // media_url :this.media_url,
            title: this.title,
            spacing: this.spacing,
            onclickPost: this.onclickPost,
            layout: this.layout,
            autoLayout: this.autoLayout,
            rows: this.rows,
            columns: this.columns,
            instagram_user_id:this.instagram_data.user_id,
            showLikes:this.showLikes,
            showFollwers:this.showFollowers,
            postToShow:this.postToShow,
            displayTagPost: this.displayTagPost,
            hashed_id:this.choose_widget.hashed_id
      }
      xmlhttp.onreadystatechange = function () {
          if (xmlhttp.readyState === 4) {
              if (xmlhttp.status === 200) {
                self.$emit('setWaiting',false)

                 notification.open({
                  message: 'Notification !!',
                  description:
                    'Your widget have been saved to database',
                  duration: 4,
                   icon: () => h(SmileOutlined, { style: 'color: #108ee9' }),
                });
              }
          }

      };
      xmlhttp.send(JSON.stringify(param))

     }



   },
   showConfirmCreateNewFeed(){
        var self = this
       Modal.confirm({
        title: 'Do you want to create new feed',
        icon: createVNode(ExclamationCircleOutlined),

        content: createVNode('div', { style: 'color:red;' }, 'This feed will be created in your database'),
        onOk() {
              setTimeout( self.createNewFeed(), 200);
        },
        onCancel() {

        },
        class: 'test',
      });
   },
   showConfirm(e){ var self = this
     e.preventDefault()
     Modal.confirm({
      title: 'Do you want to save this feed',
      icon: createVNode(ExclamationCircleOutlined),

      content: createVNode('div', { style: 'color:red;' }, 'This feed will be saved in your database'),
      onOk() {

            setTimeout( self.saveFeed(), 6000);
      },
      onCancel() {

      },
      class: 'test',
    });
  },

   openImageModal(event) {
     if(this.onclickPost ==="Open popup / show product"){
       event.preventDefault();
      const type = event.currentTarget.getAttribute("data-type");
      const src = event.currentTarget.getAttribute("data-src");
       const index =event.currentTarget.getAttribute("data-index");
        const caption =event.currentTarget.getAttribute("data-caption");
        const date =event.currentTarget.getAttribute("data-time");
         const permalink = event.currentTarget.getAttribute("data-permalink");
         const id = event.currentTarget.getAttribute("data-id")
       this.$emit('openImageModal',type,src,index,caption,date,permalink,id)
     }
     else if(this.onclickPost ==="Go to Instagram"){
       const permalink = event.currentTarget.getAttribute("data-permalink")
        let a= document.createElement('a');
        a.target= '_blank';
        a.href =permalink
        a.click();
     }
     else{
       console.log("Do Nothing")
     }


    },

  },
  computed: {
    classLayout() {
      return {
        square: this.layout ==='Grid - Squares',
        tiles: this.layout ==='Grid - Tiles'
      }
    },


    RowColumnModify(){

      this.$emit("paidFeature",this.postToShow,this.displayTagPost)
      if(this.instagram_data.media_url !== null && this.instagram_data.media_url !== undefined){
          if(this.postToShow === "Pictures only" && this.displayTagPost ==="On"){

           let mapping_array =this.instagram_data.media_url.filter((item)=>{
            return item.type === "IMAGE" && item.num_of_tagged_product !== 0
          })
            return mapping_array
        }
       else if(this.postToShow === "Pictures only"  && this.displayTagPost ==="Off"){

        let mapping_array = this.instagram_data.media_url.filter((item)=>{
          return item.type === "IMAGE"
        })
            return mapping_array
        }
        else if(this.postToShow === "Videos only"  && this.displayTagPost ==="On"){

          this.media_url = this.instagram_data.media_url.filter((item)=>{
            return item.type === "VIDEO" && item.num_of_tagged_product !== 0
          })
        }
        else if(this.postToShow === "Videos only" && this.displayTagPost ==="Off"){

          this.media_url = this.instagram_data.media_url.filter((item)=>{
            return item.type === "VIDEO"
          })
        }
        else if(this.postToShow === "All" && this.displayTagPost ==="On"){

          this.media_url = this.instagram_data.media_url.filter((item)=>{
            return item.num_of_tagged_product !== 0
          })
        }
        else{
          this.media_url = this.instagram_data.media_url
        }

        if(this.displayTagPost ==="On"){

          this.media_url = this.instagram_data.media_url.filter((item)=>{
            return item.num_of_tagged_product !== 0
          })
        }

         if(this.instagram_data !==''){
               if(this.autoLayout === 'Auto'){

               this.calculateWidth = '29.333%'
                   if(this.rows === 0){
                     let mapping_array=  this.media_url.filter((item,index)=>{
                       return index ===0 ;
                     })

                     return  mapping_array;
                   }
                   else if(this.rows === 1){
                   let mapping_array=  this.media_url.filter((item,index)=>{
                       return index  <=2  ;
                     })

                     return  mapping_array;
                   }
                   else {
                     let mapping_array=  this.media_url.filter((item,index)=>{
                       return index < this.rows *3  ;
                     })
                     return  mapping_array;
                   }
             }


             else{
               if(this.rows === 0){
                 this.calculateWidth = '29.333%'
                  let mapping_array=  this.media_url.filter((item,index)=>{
                     return index ===0 ;
                   })

                   return  mapping_array;
               }
               else if(this.columns ===0){
                 return null
               }
               else if(this.rows !== 0 && this.columns !== 0){
                  this.calculateWidth = '29.333%'
                if(this.rows === this.columns){

                    if(this.rows === 1){
                       let mapping_array=  this.media_url.filter((item,index)=>{
                           return index ===0 ;
                         })

                         return  mapping_array;
                    }
                    else{
                       let mapping_array=  this.media_url.filter((item,index)=>{
                       return index  <= this.rows +this.columns -1;
                       })

                      let parentDiv = document.getElementsByClassName("insta-feed-pic");
                      let parentDivWidth = parentDiv['0'].offsetWidth;
                      this.calculateWidth = (90 / this.rows).toString()+"%"
                      return  mapping_array;
                    }
                  }

                  else if(this.rows ===1 && this.columns !== 1){
                      let mapping_array=  this.media_url.filter((item,index)=>{
                       return index  < this.columns ;
                       })

                      let parentDiv = document.getElementsByClassName("insta-feed-pic");
                      let parentDivWidth = parentDiv['0'].offsetWidth;
                      this.calculateWidth = (parentDivWidth / this.columns).toString()
                      return  mapping_array;
                  }

                  else if(this.columns ===1 && this.rows !== 1){
                      let mapping_array=  this.media_url.filter((item,index)=>{
                       return index  < this.rows ;
                       })

                      let parentDiv = document.getElementsByClassName("insta-feed-pic");

                      this.calculateWidth = "55%"
                      return  mapping_array;
                  }

                  else {
                      let mapping_array=  this.media_url.filter((item,index)=>{
                       return index  <= this.columns ;
                       })

                      let parentDiv = document.getElementsByClassName("insta-feed-pic");
                      let parentDivWidth = parentDiv['0'].offsetWidth;
                      this.calculateWidth = (90 / this.columns).toString()+"%"
                      return  mapping_array;
                  }


               }
             }
         }
      }



    },

  }
}
</script>

<style scoped>

.carousel__item {

  width: 100%;
  background-color: var(--vc-clr-primary);
  color: var(--vc-clr-white);
  font-size: 20px;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.carousel__slide {
  padding: 10px;
}

.carousel__prev,
.carousel__next {
  box-sizing: content-box;
  border: 5px solid white;
}
.icon-big{
  z-index:100;opacity: 1;font-size: 40px;position: absolute;top: 50%;left: 50%;transform: translate(-50%, -50%);color: #fff;
}




.twelve{
  margin-top: 10px;
}
em {
    font-style: normal;
    color: #707070;
}
i {
    font-style: italic;
}
b, strong {
    font-weight: 700;
}




.tip:hover:before {
    border: solid;
    border-color: #333 transparent;
    border-width: 0.6rem 0.6rem 0;
    content: "";
    left: 38.7%;
    transform: translateX(-50%);
    position: absolute;
    z-index: 99;
        bottom: 1em;
}
.tip:hover:after {
          background-color: #333;
    border-radius: 0.3rem;
    bottom: 1rem;
    color: #fff;
    content: attr(data-hover);
    font-size: 0.8rem;
    line-height: 2rem;
    left: 37%;
    transform: translateX(-50%);
    padding: 0.5rem 1.5rem;
    position: absolute;
    z-index: 98;
    width: auto;
    white-space: nowrap;
    text-align: left;
}
input[type=email]:disabled, input[type=number]:disabled, input[type=search]:disabled, input[type=text]:disabled, input[type=tel]:disabled, input[type=url]:disabled, input[type=password]:disabled, textarea:disabled, select:disabled {
    cursor: not-allowed;
    background-color: #f4f6f8;
    border: .1rem solid #dfe4e8;
    color: #c4cdd5;
}
.instafeed-container, .instafeed-shopify .instafeed-container {
  display: inline-block;

  position: relative;
  vertical-align: top;
  padding: 0;


  color: #fff;
}
.tiles{
  padding-top: 35%;
}
.square{
  height: 33%;
}
.image-container:after{
   content: "";
  display: block;
  padding-bottom: 100%;
}
.card{
  float:left
}
.content{
  height: 80vh;
  box-shadow: 0 0 0 1px rgba(63,63,68,.05),0 1px 3px 0 rgba(63,63,68,.15);
}
label{
  display: block;
  color: #212b35;
  font-weight: 400;
}
.card {
  display: inline-block;
  width: 100%;
  color: #1a1919;
  box-sizing: border-box;
  margin-top: 0.2rem;
  padding: 1.5rem;
  background-color: #fff;
  border-radius: .3rem;
}
@media (min-width: 550px){
  .card {
    box-shadow: 0 0 0 1px rgba(63,63,68,.05),0 1px 3px 0 rgba(63,63,68,.15);

  }
    .five{
        width: 40.8333333333%;
    }
    .seven{
        width: 57.1666666667%;
    }
}

@media (min-width: 550px){
    .card {
  box-shadow: 0 0 0 1px rgba(63,63,68,.05),0 1px 3px 0 rgba(63,63,68,.15);
  margin-bottom: 2rem;
  }
    h2 {
    font-size:  1.8rem;
    line-height: 3.6rem;
  }
}
h2 {
  margin-bottom: 30px;
}
label {
  display: block;
  color: #212b35;
  font-weight: 400;
}
input[type="email"], input[type="number"], input[type="search"], input[type="text"], input[type="tel"], input[type="url"], input[type="password"], textarea, select {
  position: relative;
  padding: 0.5rem 1rem;
  background-color: #fff;
  border: .1rem solid #c4cdd5;
  border-radius: .3rem;
  color: #31373d;
  box-sizing: border-box;
  display: block;
  width: 100%;
  font-size: 14px;
  line-height: 2.4rem;
  min-width: 7.5rem;
  vertical-align: baseline;
  height: auto;
  margin: 0;
  max-width: 100%;
  font-family: -apple-system,blinkmacsystemfont,san francisco,roboto,segoe ui,helvetica neue,sans-serif;
  box-shadow: 0 0 0 1px transparent,0 1px 0 0 rgba(22,29,37,.05);
  box-sizing: border-box;
  -webkit-transition: box-shadow .2s cubic-bezier(.64,0,.35,1);
  transition: box-shadow .2s cubic-bezier(.64,0,.35,1);
}
.row{
  margin-bottom: 1rem;
}
.add-flex{
  display: grid;

  grid-template-columns: auto auto;
  gap: 1rem;
}
.btn.primary, button {
  border-radius: 4px;
  background:#008060;
  border: .1rem solid transparent;
  box-shadow: inset 0 1px 0 0 transparent, 0 1px 0 0 rgb(22 29 37 / 5%), 0 0 0 0 transparent;
  font-weight: 400;
  margin: 3px;
  padding: .7rem 1.6rem;
  cursor: pointer;
  color: #fff;
  transition: ease-in-out 250ms;
}
.primary:hover{
  background: rgb(0 110 82);
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

  object-position: 50% 50%;
}

.instafeed-overlay {
  opacity: 0;
  position: absolute;
  display: block;
  background-color: transparent;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  width: 100%;
  height: 100%;
  margin: 0 auto;
  transition: .2s linear;
}
.instafeed-overlay:hover{
  opacity: 1;
}

.instafeed-overlay:after{
  content: ' ';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: #000;
  opacity: .5;
}
.icon{
  z-index:100;opacity: 1;font-size: 18px;position: absolute;top: 50%;left: 50%;transform: translate(-50%, -50%);color: #fff;
}
h1, h2, h3, h4, h5, h6 {
  margin-top: 0;
  margin-bottom: 2rem;
  font-weight: 400;
}
</style>