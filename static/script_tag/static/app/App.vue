
<template>
  <MainContentShopify @paidFeature="paidFeature" v-if="instagram_data !== ''" :instagram_data="instagram_data" @setWaiting="setWaiting" @openImageModal="openImageModal"/>
  <div v-if="is_open_image_modal">
      <ImageModel :type="type" :shopify_url="shopify_url" :watch_list="watch_list" :media_id="media_id" :permalink="permalink" @openTagProduct="openTagProduct" @previousImage="previousImage" @nextImage="nextImage" :index="index" :instagram_data="instagram_data" :image_src="image_src" :user_name="instagram_user_name" :caption="caption" :date_created="date_created" @closeModal="closeModal"/>
    </div>

</template>

<script>

import MainContentShopify from "./components/MainContentShopify.vue";
import ImageModel from "./components/Modal/ImageModel.vue";
export default {
    name: "App",
    components:{
      MainContentShopify,
      ImageModel


    },
    data() {
          return {
          widget_id: null,
          instagram_data:'',
          shopify_url:'',
          client_id:'',
          redirect_url:'',
          instagram_user_name:'',
          is_open_change_acc_modal:false,
          is_open_image_modal:false,
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
  methods:{
    paidFeature(postToShow,displayTagPost){
      this.postToShow =postToShow
      this.displayTagPost = displayTagPost
    },
   setWaiting(flag){
      this.$emit('setWaiting',flag)
    },
    watch_list_product(data){
      this.watch_list =data
    },
    closeTagProduct(){
      this.is_open_tag_product = false
    },
    openTagProduct(){
      this.is_open_tag_product = true

    },
   closeModal(){this.is_open_image_modal = false},
   setPopUp(flag){
     this.is_open_change_acc_modal = flag
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
         console.log(this.media_id)
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
      this.widget_id = this.$.attrs.data.widget_id




     this.shopify_url = Shopify.shop

    var xmlhttp = new XMLHttpRequest();
    var self = this
    xmlhttp.open("POST", "https://odoo.website/get_data_to_store");
    xmlhttp.setRequestHeader("Content-Type", "application/json");
    let param={

      shop_url:Shopify.shop,
      widget_id:this.widget_id
    }
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4) {
            if (xmlhttp.status == 200) {

                console.log(JSON.parse(JSON.parse(xmlhttp.responseText).result))
                if(JSON.parse(JSON.parse(xmlhttp.responseText).result) !== ''){
                    self.instagram_data=JSON.parse(JSON.parse(xmlhttp.responseText).result)
                    self.instagram_user_name =self.instagram_data.instagram_user
                }
                else{
                    self.instagram_data=''
                }
            }
        }
    };
    xmlhttp.send(JSON.stringify(param))

    }

}

</script>
<style>
#app{


}
body{

}
</style>