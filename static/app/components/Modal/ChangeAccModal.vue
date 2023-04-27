<template>
  <div class="instafeed-lightbox" id="change-account-modal" >
     <div class="lightbox-instagram" style="text-align: justify;
color: black;
border-radius: 15px;
padding: 50px 26px 0px;
height: 375px;
right: 0px;
left: 0px;
margin: 0px auto;
width: 640px;">
          <a style="position:absolute;cursor:pointer;top:7px;right:16px;color:#666;font-weight:bold;font-size:18px;" id="rate-us-banner-close" @click="this.$emit('setPopUp',!is_open_change_acc_modal)">X</a>
          <h3><b>CHANGE THE INSTAGRAM ACCOUNT CONNECTED</b></h3>
          Follow the steps below on your computer and not mobile.<br><br>
          1 - Go to <a href="https://www.instagram.com/" target="_blank">www.instagram.com</a> in your desktop browser and log out.<br><br>
          2 - <b>Important:</b> Login to <a href="https://www.instagram.com/" target="_blank">www.instagram.com</a> with the Instagram username you want to show in your feed. This is <b>not your personal or shared username</b>, you need to log in using the username (account name) of the account that you want to show. If you don't have the password for that username use the <a href="https://www.instagram.com/accounts/password/reset/" target="_blank">recover password option</a><br><br>
          Go back to Instafeed and connect your Instagram account again.
    </div>
  </div>
</template>

<script>
export default {
  name: "ChangeAccModal",
  props:{


   is_open_change_acc_modal:Boolean

  },
}
</script>

<style scoped>
.instafeed-lightbox {

  position: fixed !important;
  font-size: 15px;
  z-index: 99999;
  width: 100%;
  height: 100%;
  text-align: center;
  top: 0;
  left: 0;
  background: rgba(0,0,0,.8);
}
.instafeed-lightbox .lightbox-instagram {
  height: 80%;
  width: 70%;
  background-color: #fff;
  position: absolute;
  top: 10%;
  left: 15%;
}
</style>