<template>
  <div class="row paid-feature" style="display: flex">
    <div class="column six" style="display: flex;gap: 10px">
      <a id="new-feed" class="button secondary" @click="this.$emit('createNewFeed')">Create new feed</a>
      <a id="delete-feed" class="tip button secondary"  data-hover="Delete this Feed" @click="showConfirmDeleteFeed"><font-awesome-icon style="position:static;" icon="fa-solid fa-trash" /></a>
    </div>

    <div class="column six" style="text-align:right;">
      <select id="feeds" v-model="selected" @change="onChange()">
        <option v-for="(item,index) in this.list_widget" :value="item">WIDGET #{{item.number}}</option>
      </select>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import {Modal, notification} from 'ant-design-vue';
import {ExclamationCircleOutlined} from '@ant-design/icons-vue';
import { SmileOutlined } from '@ant-design/icons-vue';
import { ExclamationOutlined} from "@ant-design/icons-vue";
import { createVNode, h } from 'vue';
export default {
    name: "CreateNewFeed",
    props:{

   user_id:String,
   list_widget:Array,
instagram_data:''
  },
    data() {
      return {
        selected:String,
      }
    },
    watch: {
      instagram_data(newone){
           if(newone.id_widget !== false || newone.number !== false){
               this.selected = newone.choose_widget
           }
      },

    },
    mounted() {
      this.selected = this.instagram_data.choose_widget
    },
    methods:{
      onChange(){
       this.$emit('setWaiting',true)
       let queryString = window.location.search
          let urlParams = new URLSearchParams(queryString)
            axios.post('/get_widget', {
                  jsonrpc: "2.0",
                  params: {
                       shopify_url:urlParams.get('shop_url'),
                      id_widget:this.selected.id_widget,//TODO gui id cua thang dang hoat dong
                      user_id:this.user_id
                  }
              }).then((res) => {

                   if (res.status === 200) {
                      let widget =  JSON.parse(res.data.result).widget
                      let followers = widget.followers
                     this.$emit('updatetFeed',widget,widget.title,widget.spacing,widget.onclickPost,widget.layout,widget.autoLayout,widget.rows,widget.columns,widget.showLikes,widget.showFollwers,
    widget.postToShow,widget.displayTagPost,followers)

                       this.$emit('setWaiting',false)
                   }
              })
      },
      showConfirmDeleteFeed(){
        var self = this
       Modal.confirm({
        title: 'Do you want to delete feed',
        icon: createVNode(ExclamationCircleOutlined),

        content: createVNode('div', { style: 'color:red;' }, 'This feed will be delete in your database'),
        onOk() {

              setTimeout( self.deleteFeed(), 200);

        },
        onCancel() {

        },
        class: 'test',
      });
   },
        deleteFeed(){
          if(this.list_widget.length > 1){
              let queryString = window.location.search
              let urlParams = new URLSearchParams(queryString)
                axios.post('/delete_feed', {
                      jsonrpc: "2.0",
                      params: {
                           shopify_url:urlParams.get('shop_url'),
                          id_widget:this.instagram_data.choose_widget.id_widget,//TODO gui id cua thang dang hoat dong
                          user_id:this.user_id
                      }
                  }).then((res) => {

                       if (res.status === 200) {
                          let widget =  JSON.parse(res.data.result).widget
                         this.$emit('updatetFeed',widget,widget.title,widget.spacing,widget.onclickPost,widget.layout,widget.autoLayout,widget.rows,widget.columns,widget.showLikes,widget.showFollwers,
    widget.postToShow,widget.displayTagPost,widget.followers)
                       }
                  })
          }
          else{
              notification.open({
              message: 'Notification !!',
              description:
                'No feed to delete',
              duration: 4,
              icon: () => h(ExclamationOutlined, { style: 'color: red' }),
            });
          }
        }
    },
}
</script>

<style scoped>
@media (min-width: 550px){
      .column.six {
      width: 49%;
  }
}
.button.secondary {
    fill: #637381;
    color: #212b36;
    background: -webkit-linear-gradient(top,#fff,#f9fafb);
    background: linear-gradient(180deg,#fff,#f9fafb);
    border: 1px solid #c4cdd5;
    box-shadow: 0 1px 0 0 rgb(22 29 37 / 5%);
}
.button {

    min-width: 3.6rem;
    padding: 0.7rem 1.6rem;
}
a {
    text-decoration: none;
    cursor: pointer;
    color: #007ace;
    -webkit-transition: color .24s cubic-bezier(.64,0,.35,1);
    transition: color .24s cubic-bezier(.64,0,.35,1);
}

select {
    padding-right: 3.2rem;

    background-size: 21px 21px;
    background-repeat: no-repeat;
    background-position: right 0.7rem top 0.7rem;
    box-shadow: 0 0 0 1px transparent, 0 1px 0 0 rgb(22 29 37 / 5%);
}
select {
    position: relative;
    padding: 0.5rem 1rem;
    background-color: #fff;
    border: 0.1rem solid #c4cdd5;
    border-radius: 0.3rem;
    color: #31373d;
    box-sizing: border-box;
    display: block;
    width: 100%;

    line-height: 2.4rem;
    min-width: 7.5rem;
    vertical-align: baseline;
    height: auto;
    margin: 0;
    max-width: 100%;
    font-family: -apple-system,blinkmacsystemfont,san francisco,roboto,segoe ui,helvetica neue,sans-serif;
    box-shadow: 0 0 0 1px transparent, 0 1px 0 0 rgb(22 29 37 / 5%);

}
</style>