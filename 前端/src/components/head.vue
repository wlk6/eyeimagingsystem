<template>
  <div>
     <div class="eimheader">
      <div class="home-btn" @click="goindex"></div>

      <img src="@/assets/loginimg/login/logo.png" alt="">
      <p>眼科疾病智能诊断系统</p>
    </div>

    <img class="sci-wheel" src="@/assets/loginimg/login/sci.gif" alt="">
  </div>
</template>

<script>
export default {
name: 'Head',
methods: {
  goindex() {
    if(this.$store.state.role=='doctor')
    this.$router.push('/info')
  }
}
}
</script>

<style>
 .eimheader{
        width: 100%; height: 100px; line-height: 100px;
        padding: 0px 40px;
        background:rgba(0,0,0,0.3);
      }
      .eimheader img{
        float: left;
        margin: 10px 10px;
        width: 100px;
      }
      .eimheader p{
        float: left;
        font-size: 30px; color: white;
        letter-spacing: 3px;
      }
      .eimheader .home-btn {
        float: left;
        margin-top: 20px;
        width: 74px;
        height: 74px;
        border: 1px solid #102262;
        border-radius: 5px;
        background: url(@/assets/loginimg/login/icon.png) no-repeat center center;
        background-size: 45% 45%;
        cursor: pointer;
      }
</style>