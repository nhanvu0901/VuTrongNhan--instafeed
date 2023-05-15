<template>
 <Carousel v-if="this.layout ==='Carousel - Squares'">
    <Slide v-for="(media,index) in this.RowColumnModify" :key="media">
      <div style="position: relative; width: 80%;height: 80%;" class="image-container"  :data-type="media.type" :data-id="media.post_id" :data-src="media.media_url"  :data-caption="media.caption" :data-index="index" :data-permalink="media.permalink" :data-time="media.created_date" @click="openImageModal">
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




    </Slide>

    <template #addons>
      <Navigation />
      <Pagination />
    </template>
  </Carousel>


  <Carousel :autoplay="2000" :wrap-around="true" v-else-if="this.layout ==='Carousel - Auto'">
    <Slide v-for="(media,index) in this.RowColumnModify" :key="media">
      <div style="position: relative; width: 80%;height: 80%;" class="image-container"  :data-type="media.type" :data-id="media.post_id" :data-src="media.media_url"  :data-caption="media.caption" :data-index="index" :data-permalink="media.permalink" :data-time="media.created_date" @click="openImageModal">
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

    </Slide>

    <template #addons>
      <Navigation />
      <Pagination />
    </template>
  </Carousel>

   <Carousel itemsToShow="3.95" :wrapAround="true" :transition="500" v-else-if="this.layout ==='Carousel - Active Classes'">
    <Slide v-for="(media,index) in this.RowColumnModify" :key="media">
      <div style="position: relative; width: 80%;height: 80%;" class="image-container"  :data-type="media.type" :data-id="media.post_id" :data-src="media.media_url"  :data-caption="media.caption" :data-index="index" :data-permalink="media.permalink" :data-time="media.created_date" @click="openImageModal">
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

    </Slide>

    <template #addons>
      <Navigation />
      <Pagination />
    </template>
  </Carousel>


   <div v-else-if="this.layout ==='Carousel - Gallery'">
        <Carousel id="gallery" :items-to-show="1" :wrap-around="false" v-model="currentSlide" >
            <Slide v-for="(media,index) in this.RowColumnModify" :key="media">
             <div style="position: relative; width: 80%;height: 80%;" class="image-container"  :data-type="media.type" :data-id="media.post_id" :data-src="media.media_url"  :data-caption="media.caption" :data-index="index" :data-permalink="media.permalink" :data-time="media.created_date" @click="openImageModal">
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

            </Slide>

            <template #addons>
              <Navigation />
              <Pagination />
            </template>
          </Carousel>


       <Carousel
        id="thumbnails"
        :items-to-show="4"
        :wrap-around="true"
        v-model="currentSlide"
        ref="carousel"
      >
        <Slide v-for="(media,index) in this.RowColumnModify" :key="media">
              <div @click="slideTo(index)" style="position: relative; width: 80%;height: 80%;" class="image-container"  :data-type="media.type" :data-id="media.post_id" :data-src="media.media_url"  :data-caption="media.caption" :data-index="index" :data-permalink="media.permalink" :data-time="media.created_date">
                   <img v-if="media.type !== 'CAROUSEL_ALBUM'" class="js-lazy-image js-lazy-image--handled" :src="media.type ==='VIDEO' ? media.thumbnail_url : media.media_url"    alt="Instagram post with the caption: ...">
                  <img v-else :src="media.thumbnail_url !== '' ? media.thumbnail_url.replace(/\[|\]/g,'').split(',')[0].replace(/'/g, ''): media.media_url.replace(/\[|\]/g,'').split(',')[0].replace(/'/g, '')">
                </div>

            </Slide>
      </Carousel>


   </div>

</template>

<script>
import { Carousel, Navigation, Pagination, Slide } from 'vue3-carousel'

import 'vue3-carousel/dist/carousel.css'
export default {
  name: "CarouselShop",
    data() {
        return {

            currentSlide: 0,
        }
  },


  props:{
   // media_url:Array,
   //  showLikes:String,
   //  postToShow:String,
   //  displayTagPost:String
      layout:String,
      RowColumnModify:Function,
      showLikes:String
  },
   components: {
      Carousel,
    Slide,
    Pagination,
    Navigation,},

    mounted() {

    },
    methods:{
    openImageModal(event){
      this.$emit('openImageModal',event)
    },
    slideTo(val) {
          this.currentSlide = val
        },



},

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
.postToShow:hover:before {
    border: solid;
    border-color: #333 transparent;
    border-width: 0.6rem 0.6rem 0;
    content: "";
    left: 38.7%;
    transform: translateX(-50%);
    position: absolute;
    z-index: 99;
    bottom: 10%;
}
.postToShow:hover:after {
    background-color: #333;
    border-radius: 0.3rem;
    bottom: 11%;
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
.tagProduct:hover:before {
    border: solid;
    border-color: #333 transparent;
    border-width: 0.6rem 0.6rem 0;
    content: "";
    left: 38.7%;
    transform: translateX(-50%);
    position: absolute;
    z-index: 99;
    bottom: 0%;
}
.tagProduct:hover:after {
        background-color: #333;
    border-radius: 0.3rem;
    bottom: 1%;
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
.config:hover:before {
        border: solid;
    border-color: #333 transparent;
    border-width: 0.6rem 0.6rem 0;
    content: "";
    left: 38.7%;
    transform: translateX(-50%);
    position: absolute;
    z-index: 99;
    bottom: 54%;
}
.config:hover:after {
          background-color: #333;
    border-radius: 0.3rem;
    bottom: 55%;
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
.like:hover:before {
    border: solid;
    border-color: #333 transparent;
    border-width: 0.6rem 0.6rem 0;
    content: "";
    left: 38.7%;
    transform: translateX(-50%);
    position: absolute;
    z-index: 99;
  bottom: 31%;
}
.like:hover:after {
          background-color: #333;
    border-radius: 0.3rem;
        bottom: 32%;
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
.follow:hover:before {
    border: solid;
    border-color: #333 transparent;
    border-width: 0.6rem 0.6rem 0;
    content: "";
    left: 38.7%;
    transform: translateX(-50%);
    position: absolute;
    z-index: 99;
        bottom: 21%;
}
.follow:hover:after {
          background-color: #333;
    border-radius: 0.3rem;
    bottom: 22%;
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
@media (min-width: 550px){
  .card {
    box-shadow: 0 0 0 1px rgba(63,63,68,.05),0 1px 3px 0 rgba(63,63,68,.15);

  }
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