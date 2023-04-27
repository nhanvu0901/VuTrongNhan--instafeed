<template>
     <div class="insta-feed" style="display: block;
text-align: center;
clear: both;

">
          <h2>{{this.title}}</h2>
          <div style="font-size: 1.3rem;margin-bottom: 1rem;" v-if="this.showFollowers ==='Yes' && this.instagram_data.followers !== '' && this.instagram_data.followers !== false">{{this.instagram_data.followers}} FOLLOWERS</div>

<!--          <div class="insta-feed-pic" :style="{display: 'grid',gridTemplateColumns: 'auto auto',padding: '0 2rem',gap:this.spacing}">-->
          <div class="insta-feed-pic" style="position: relative;display: block;
text-align: center;
clear: both;">


              <CarouselShop :showLikes="showLikes" :layout="layout" v-if="this.layout === 'Carousel - Gallery' || this.layout ==='Carousel - Squares' || this.layout ==='Carousel - Auto' ||this.layout ==='Carousel - Active Classes'" @openImageModal="openImageModal" :RowColumnModify="RowColumnModify"/>

              <div v-else v-for="(media,index) in RowColumnModify" class="instafeed-container" :class="classLayout" :style="{margin:this.spacing,width:this.calculateWidth}" >
                  <div style="position: relative; width: 100%;" class="image-container"  :data-type="media.type" :data-id="media.media_id" :data-src="media.type === 'CAROUSEL_ALBUM' ? media.media_url.replace(/\[|\]/g,'').split(',')  :media.media_url"  :data-caption="media.caption" :data-index="index" :data-permalink="media.permalink" :data-time="media.created_date" @click="openImageModal">
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
</template>

<script>
import { Carousel, Navigation, Pagination, Slide } from 'vue3-carousel'

import 'vue3-carousel/dist/carousel.css'
import CarouselShop from "./CarouselShop.vue";
export default {
  name: "MainContentShopify",
    components: {
        CarouselShop,
      Carousel,
    Slide,
    Pagination,
    Navigation,},
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
          showLikes:'Yes',
          showFollowers:'Yes',
          numberOfFollower:'',
          calculateWidth:'29.333%',
           postToShow:'All',
          displayTagPost:'Off'
        }
    },
  watch: {
    instagram_data(newone){
      console.log(newone)
       this.media_url = newone.media_url
      console.log( this.media_url)
      this.numberOfFollower = newone.followers
    },
  },
  props:{
    instagram_data:String
  },
  mounted() {
                this.title= this.instagram_data.feed_title
                this.spacing= this.instagram_data.spacing
                this.onclickPost=this.instagram_data.on_post_click
                this.layout= this.instagram_data.layout
                this.autoLayout=this.instagram_data.configuration
                this.rows=parseInt(this.instagram_data.rows)
                this.columns=parseInt(this.instagram_data.columns)
                this.media_url=this.instagram_data.media_url
               this.showLikes=this.instagram_data.showLikes
               this.showFollowers=this.instagram_data.showFollowers
              this.postToShow=this.instagram_data.postToShow
               this.displayTagPost=this.instagram_data.displayTagPost
  },
  methods:{
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
      if(this.postToShow === "Pictures only" && this.displayTagPost ==="On"){
        this.media_url = this.instagram_data.media_url
        this.media_url = this.media_url.filter((item)=>{
          return item.type === "IMAGE" && item.num_of_tagged_product !== 0
        })
      }
     else if(this.postToShow === "Pictures only"  && this.displayTagPost ==="Off"){
      this.media_url = this.instagram_data.media_url
      this.media_url = this.media_url.filter((item)=>{
        return item.type === "IMAGE"
      })
      }
      else if(this.postToShow === "Videos only"  && this.displayTagPost ==="On"){
        this.media_url = this.instagram_data.media_url
        this.media_url = this.media_url.filter((item)=>{
          return item.type === "VIDEO" && item.num_of_tagged_product !== 0
        })
      }
      else if(this.postToShow === "Videos only" && this.displayTagPost ==="Off"){
        this.media_url = this.instagram_data.media_url
        this.media_url = this.media_url.filter((item)=>{
          return item.type === "VIDEO"
        })
      }
      else if(this.postToShow === "All" && this.displayTagPost ==="On"){
        this.media_url = this.instagram_data.media_url
        this.media_url = this.media_url.filter((item)=>{
          return item.num_of_tagged_product !== 0
        })
      }
      else{
        this.media_url = this.instagram_data.media_url
      }

      if(this.displayTagPost ==="On"){

        this.media_url = this.media_url.filter((item)=>{
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

.content{
  height: 80vh;
  box-shadow: 0 0 0 1px rgba(63,63,68,.05),0 1px 3px 0 rgba(63,63,68,.15);
}
label{
  display: block;
  color: #212b35;
  font-weight: 400;
}


@media (min-width: 550px){

    h2 {
    font-size:  3.8rem;
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

.row{
  margin-bottom: 1rem;
}
.add-flex{
  display: grid;

  grid-template-columns: auto auto;
  gap: 1rem;
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