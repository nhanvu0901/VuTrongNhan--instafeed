<template>

   <div class="card" style="">

     <div style=" font-weight: bold;
          font-size: 16px;">
       Grant Access To Instagram
     </div>
     <div class="button-container" style="display: flex;gap: 1rem;justify-content: space-between;">
       <div style="display: flex;gap: 1rem">
         <a-button  @click="RedirectUrl" type="primary" ><InstagramOutlined/> Connect with Instagram</a-button>
         <a-button type="primary"  @click="login">
             <FacebookOutlined/>
              Login with Facebook
          </a-button>
       </div>
        <a-button  @click="ReloadIstagramData" type="primary" ><InstagramOutlined/> Update Instagram Post</a-button>
     </div>


     <div v-if=" this.instagram_user_name" style="
          font-weight: bold;
          font-size: 14px;
          color:#008060;
        ">
       {{this.shopify_url}} is connected to {{this.instagram_user_name}} |
       <a style="color:grey;text-decoration:underline;" @click="this.$emit('setPopUp',!is_open_change_acc_modal)">Change account</a>
     </div>

     <div v-else="" style="
          font-weight: bold;
          font-size: 14px;
          color:#008060;
        ">
       {{this.shopify_url}} is not connected to any instagram user
       <a style="color:grey;text-decoration:underline;" @click="this.$emit('setPopUp',!is_open_change_acc_modal)">Change account</a>

     </div>

   </div>


</template>

<script>
import {InstagramOutlined, SmileOutlined} from "@ant-design/icons-vue";
import {FacebookOutlined} from "@ant-design/icons-vue";
import { notification } from 'ant-design-vue';


import axios from "axios";
import {h} from "vue";

export default {
  name: "Redirect_Instagram",
   components:{
     InstagramOutlined,
     FacebookOutlined


    },
   methods:{
     ReloadIstagramData(){
       this.$emit('setWaiting',true)
       axios.post('/update_instagram_post', {
                jsonrpc: "2.0",
                params: {
                     shopify_url:this.shopify_url,
                     instagram_user_name:this.instagram_user_name
                }
            }).then((res) => {
                 if (res.status === 200) {
                   this.$emit('update_instagram_data',JSON.parse(res.data.result))
                    this.$emit('setWaiting',false)
                    notification.open({
                      message: 'Notification',
                      description:
                        'Update Post successfully',
                      duration: 4,
                     icon: () => h(SmileOutlined, { style: 'color: #108ee9' }),
                  });
                 }
            })
     },
      RedirectUrl(){
         sessionStorage.clear()
      //"`https://api.instagram.com/oauth/authorize?client_id=${this.client_id}&redirect_uri=${this.redirect_url}&scope=user_profile,user_media&response_type=code`"
            localStorage.setItem("shop_url_instagram_shopify", this.shopify_url);
            // let a= document.createElement('a');
            //
            // a.href =`https://api.instagram.com/oauth/authorize?client_id=${this.client_id}&redirect_uri=${this.redirect_url}&scope=user_profile,user_media&response_type=code&shop_url=${this.shopify_url}`;
            // a.click();


             Object.assign(document.createElement('a'), {
                target:'_blank',
                rel: '',
                href: `https://api.instagram.com/oauth/authorize?client_id=${this.client_id}&redirect_uri=${this.redirect_url}&scope=user_profile,user_media&response_type=code&shop_url=${this.shopify_url}`,
              }).click();

         },


      login(){

        var self = this
        FB.login(

            function(response) {
              var self_self = self
          console.log(response)
          self.$emit('setWaiting',true)
          var xmlhttp = new XMLHttpRequest();

          xmlhttp.open("POST", "https://odoo.website/get_facebook_data");
          xmlhttp.setRequestHeader("Content-Type", "application/json");
          let param={
            accessToken:response.authResponse.accessToken,
            shop_url:self.shopify_url,
            instagram_user_name:self.instagram_user_name
          }
          xmlhttp.onreadystatechange = function () {
              if (xmlhttp.readyState === 4) {
                  if (xmlhttp.status === 200) {
                    if (JSON.parse(JSON.parse(xmlhttp.responseText).result)) {
                        if (JSON.parse(JSON.parse(xmlhttp.responseText).result).flag){
                          self_self.$emit('setError',JSON.parse(JSON.parse(xmlhttp.responseText).result).message,self_self.shopify_url)
                        }
                       self_self.$emit('update_instagram_data',JSON.parse(JSON.parse(xmlhttp.responseText).result))
                       self_self.$emit('setWaiting',false)
                    }
                    //self.$emit(sua du lieu cua instaram_data xong cho vao bien watch o Component Maincontent)



                  }
              }

          };
          xmlhttp.send(JSON.stringify(param))



        }, {scope: 'pages_show_list,instagram_basic,pages_read_engagement,business_management'});

      }



  },
  props:{
    client_id:String,
    redirect_url:String,
    shopify_url:String,
    instagram_user_name:String,
    is_open_change_acc_modal:Boolean
  }
}
</script>

<style scoped>
@media (min-width: 550px){
  .card {
    box-shadow: 0 0 0 1px rgba(63,63,68,.05),0 1px 3px 0 rgba(63,63,68,.15);

  }
}
@media (min-width: 550px)
.card {
    width: 100%;
    margin-left: 0;
}
a{
  cursor: pointer;
}
.card {
  display: inline-block;
  width: 100%;
  color: #1a1919;
  box-sizing: border-box;
  margin-bottom: 0;
  padding: 1.5rem;
  background-color: #fff;
  border-radius: .3rem;
  margin-top: 0.2rem;
}
.ant-btn{
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
</style>