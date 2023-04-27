<template>
  <div class="image-carousel-container" >
      <div v-if="typeof(this.array_child[current_child_image]) === 'string'">
          <video v-if="this.array_child[current_child_image].includes('mp4')" :src="this.array_child[current_child_image]" style="float: left;height: 100%;width: 100%" id="feed-id" controls ></video>
          <img v-else :src="this.array_child[current_child_image]">
      </div>


      <div class="arrows">
         <object @click="preChildImage">
           <a>
             <img src="//instafeed.nfcube.com/assets/img/placeholder.gif" alt="previous image">
           </a>
         </object>

         <object @click="nextChildImage">
           <a >
           <img src="//instafeed.nfcube.com/assets/img/placeholder.gif" alt="next image">
         </a>
         </object>
      </div>
  </div>
</template>

<script>
export default {
    name: "ImageCarousel",
    props:{
   child_carousel:Array,

  },
   data() {
      return {
        current_child_image:0,
        array_child:[]
      }
  },
    watch:{
        child_carousel(newone){
            this.array_child = newone
        }
    },
    mounted() {
        this.array_child =  this.child_carousel

    },
    methods:{
      nextChildImage(){
        //TH cai cuoi cung thi ve cai dau
          if(this.current_child_image +1 === this.child_carousel.length){
              this.current_child_image =0
          }
          else{
              ++this.current_child_image
          }
      },
       preChildImage(){
          //Th cai nay la cai dau
          if(this.current_child_image === 0){
              this.current_child_image = this.child_carousel.length -1
          }
          else{
              --this.current_child_image
          }
       }
   }
}
</script>

<style scoped>
.image-carousel-container{
 position: relative;
}
img{
  object-fit: cover;

  margin: 0 auto;
  width: 100%;
  height: 100%;
  border-radius: 0;
  transform: initial;
  display: initial;
  opacity: 1;
}
.arrows {
  display: flex;
  justify-content: space-between;
  width: 100%;
  margin: 0 auto;
    position: absolute;
    top: 37vh;

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
</style>