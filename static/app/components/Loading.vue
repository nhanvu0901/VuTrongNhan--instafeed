<template>
  <div class="main-container" style="display: flex;
  flex-direction: column;
  align-items: baseline;
  gap: 2rem;

">


      <div style="width:40%;height: 100px" class="is-loading"></div>

        <div style="width: 100%; height: 90vh">
          <div style="
              height: 100%;
              display: grid;
              grid-template-columns: 40% 55%;
              gap: 1rem;
            " >
            <div class="is-loading"></div>
            <div class="is-loading"></div>
          </div>
        </div>

  </div>
</template>

<script>
export default {
  name: "Loading"
}
</script>

<style scoped>
.main-container{
      width: 100%;
      padding-top:1rem;
      padding-left: 1rem;
}
.is-loading{
   background: #eee;
	 background: linear-gradient(110deg, #ececec 8%, #f5f5f5 18%, #ececec 33%);
	 border-radius: 5px;
	 background-size: 200% 100%;
	 animation: 1.5s shine linear infinite;
}
 @keyframes shine {
	 to {
		 background-position-x: -200%;
	}
}
</style>