<template>
  <div>
    <Head></Head>
    <div class="content-container">
      <header>
        <div class="header-inner">
          <div class="logo">
            <a href="javascript:void(0)" style="cursor:default">
              <span v-if="currentIndex === 0">密码修改审核列表</span>
              <span v-else>信息审核列表</span>
              <img src="@/assets/img/icon-next.png" alt="next" />
            </a>
          </div>
          <div class="header-headline">
            <p style="font-size: 18px;color:white" v-if="currentIndex === 0">信息审核列表</p>
            <p style="font-size: 18px;color:white" v-else>密码修改审核列表</p>
          </div>
        </div>
      </header>
      <nav id="nav">
        <button id="prev" class="nav-item" @click="rotate(-1)">
          <img src="@/assets/img/icon-prev.png" alt="prev" />
        </button>
        <button class="nav-item right" @click="rotate(1)" id="next">
          <img src="@/assets/img/icon-next.png" alt="next" />
        </button>
      </nav>
      <section class="coidea-3d-carousel">
        <div class="stage">
          <div class="item" style="background-color:transparent;">
            <table1></table1>
          </div>
          <div class="item" style="background-color:transparent;">
            <table2></table2>
          </div>
        </div>
      </section>
    </div>
    <liuxing></liuxing>
  </div>
</template>

<script>
import liuxing from '../../components/liuxing.vue'
import table1 from '../../components/table3.vue'
import table2 from '../../components/table2.vue'
import { TweenMax, TimelineMax, Circ } from 'gsap'

export default {
  components: { table1, table2, liuxing },
  data() {
    return {
      carousel: null,
      boxes: null,
      stage: null,
      angle: 180, // 两个轮播项的角度为 180 度
      isRotating: false,
      currentIndex: 0, // 当前显示的轮播项索引
    }
  },
  mounted() {
    this.initCarousel()
  },
  methods: {
    initCarousel() {
      this.carousel = document.querySelector('.coidea-3d-carousel')
      this.boxes = document.querySelectorAll('.item')
      this.stage = document.querySelector('.stage')

      if (!this.carousel || !this.stage) {
        console.error('Carousel or stage element not found')
        return
      }

      TweenMax.set(this.stage, {
        perspective: "86vw",
        transformStyle: "preserve-3d"
      })

      this.boxes.forEach((box, index) => {
        TweenMax.set(box, { rotationY: index * this.angle })
        box.dataset.rotationY = index * this.angle
      })
    },

    rotate(direction) {
      if (this.isRotating) return
      this.isRotating = true

      const timeline = new TimelineMax()
      const rotationStep = direction * this.angle

      timeline
        .to(this.boxes, 0.5, {
          width: "80%",
          height: "80%",
          top: "10%",
          left: "10%",
          ease: Circ.easeOut
        })
        .to(this.boxes, 1, {
          rotationY: (index, element) => {
            const currentAngle = parseInt(element.dataset.rotationY)
            const newAngle = currentAngle + rotationStep
            element.dataset.rotationY = newAngle
            return newAngle
          },
          ease: Circ.easeOut
        }, "-=0.3")
        .to(this.boxes, 0.5, {
          width: "100%",
          height: "100%",
          top: "0%",
          left: "0%",
          ease: Circ.easeOut
        })
        .to(this.boxes, 0.5, {
          yPercent: 0,
          ease: Circ.easeOut
        })
        .then(() => {
          this.isRotating = false
          this.updateContent(direction)
        })
    },

    updateContent(direction) {
      // 更新当前显示的内容
      this.currentIndex = (this.currentIndex + direction + 2) % 2 // 确保索引在 0 和 1 之间循环
    }
  }
}
</script>
<style scoped>
.content-container {
  margin-top: 40px; 
  height: 77vh;
  position: relative;
}
@import url("https://fonts.googleapis.com/css?family=Montserrat:300,400,700,900");
 header {
   
    position: fixed;
    display: block;
    width: 100%;
    height: 48px;
    top: 90px;
    right: 0;
    left: 0;
    z-index: 100;
  }
header .header-inner {
    padding: 16px 1.5%;
  }
  @media screen and (max-width: 768px) {
     header .header-inner {
      padding: 16px 16px 0;
    }
  }
  @media screen and (max-width: 640px) {
     header .header-inner {
      padding: 16px 16px 0 16px;
    }
  }
 header .header-inner .logo {
    position: relative;
    display: inline;
    width: auto;
    height: auto;
    float: left;
  }
 header .header-inner .logo a {
    position: relative;
    display: inline;
    width: auto;
    height: auto;
    color: #FFFFFF;
    outline: 0px none;
    outline: 0px;
    text-decoration: none;
    transition: all 0.35s ease-in-out;
    text-transform: uppercase;
  }
   header .header-inner .logo a:hover {
    color: rgba(255, 255, 255, 0.85);
  }
   header .header-inner .logo a span {
    font-weight: 700;
  }
   header .header-inner .logo a img {
    position: relative;
    display: inline;
    width: auto;
    height: 16px;
    margin-left: 8px;
    margin-bottom: -2px;
  }
  @media screen and (max-width: 768px) {
     header .header-inner .logo a img {
      display: none;
    }
  }
   header .header-inner .header-headline {
    position: absolute;
    display: block;
    width: 280px;
    height: auto;
    margin: 0 auto;
    left: 50%;
    transform: translateX(-50%);
    text-align: center;
  }
  @media screen and (max-width: 768px) {
     header .header-inner .header-headline {
      display: none;
    }
  }
   header .header-inner .header-headline p {
    text-transform: uppercase;
    margin: 0;
    line-height: 20px;
    font-weight: 700;
  }
   header .header-inner nav {
    position: relative;
    display: inline;
    margin: 0;
    padding: 0;
    list-type-style: none;
    float: right;
  }
   header .header-inner nav li {
    position: relative;
    display: inline;
    margin-left: 16px;
  }
  @media screen and (max-width: 360px) {
     header .header-inner nav li {
      margin-left: 8px;
    }
  }
   header .header-inner nav li a {
    font-family: "Poppins", sans-serif;
    position: relative;
    font-size: 13px;
    color: #FFFFFF;
    text-decoration: none;
    line-height: 24px;
    transition: all 0.35s ease-in-out;
  }
  @media screen and (max-width: 360px) {
     header .header-inner nav li a {
      font-size: 11px;
    }
  }
   header .header-inner nav li a span {
    position: relative;
    z-index: 2;
  }
   header .header-inner nav li a:hover {
    color: rgba(255, 255, 255, 0.85);
  }
  #nav {
    position: absolute;
  display: flex;
  justify-content: space-between;
  width: 180px;
  left: 15%;
  top: 86.4%;
  transform: translateX(-50%);
  z-index: 100;
  }
  
  @media screen and (max-width: 1199px) {
    #nav {
      width: 134px;
      height: 48px;
      top: 65%;
    }
  }
   #nav .nav-item {
    background-color: #00b6ec;
    position: relative;
    display: inline-block;
    width: 40px;
    height: 40px;
    border-radius: 32px;
    border: none;
    outline: 0px none;
    outline: 0px;
    margin-left: 8px;
    margin-right: 8px;
    color: #FFFFFF;
    cursor: pointer;
  }
  @media screen and (max-width: 1199px) {
     #nav .nav-item {
      width: 48px;
      height: 48px;
      border-radius: 24px;
    }
  }
   #nav .nav-item img {
    position: relative;
    display: block;
    width: 50%;
    min-width: 50%;
    max-width: 50%;
    height: auto;
    margin: auto;
  }
   section.coidea-3d-carousel {
    position: absolute;
    width: 100%;
    height: 100%;
    -webkit-font-smoothing: antialiased;
    margin: 0;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    will-change: transform;
  }
   section.coidea-3d-carousel .stage {
    height: 100%;
    color: #ddd;
    margin: 0;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    will-change: transform;
  }
   section.coidea-3d-carousel .stage .item {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    background-color: #000000;
    display: inline-block;
    display: inline-block;
    overflow: hidden;
    transform-origin: 50% 50% -50vw !important;
    will-change: transform;
  }
   section.coidea-3d-carousel .stage .item .bcg {
    position: absolute;
    display: block;
    width: 100%;
    height: 100%;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    background-repeat: no-repeat;
    background-position: center center;
    -webkit-background-size: cover;
    -moz-background-size: cover;
    -o-background-size: cover;
    background-size: cover;
  }
   section.coidea-3d-carousel .stage .item .bcg::after {
    content: "";
    position: absolute;
    display: none;
    width: 100%;
    height: 100%;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    z-index: 2;
    background: -moz-linear-gradient(90deg, rgba(0, 0, 0, 0.35) 0%, rgba(0, 0, 0, 0) 50%, rgba(0, 0, 0, 0.35) 100%);
    background: -webkit-gradient(linear, left top, left bottom, color-stop(0%, rgba(0, 0, 0, 0.35)), color-stop(50%, rgba(0, 0, 0, 0)), color-stop(100%, rgba(0, 0, 0, 0.35)));
    background: -webkit-linear-gradient(90deg, rgba(0, 0, 0, 0.35) 0%, rgba(0, 0, 0, 0) 50%, rgba(0, 0, 0, 0.35) 100%);
    background: -o-linear-gradient(90deg, rgba(0, 0, 0, 0.35) 0%, rgba(0, 0, 0, 0) 50%, rgba(0, 0, 0, 0.35) 100%);
    background: -ms-linear-gradient(90deg, rgba(0, 0, 0, 0.35) 0%, rgba(0, 0, 0, 0) 50%, rgba(0, 0, 0, 0.35) 100%);
    background: linear-gradient(0deg, rgba(0, 0, 0, 0.35) 0%, rgba(0, 0, 0, 0) 50%, rgba(0, 0, 0, 0.35) 100%);
    filter: progid:DXImageTransform.Microsoft.gradient( startColorstr="#000000", endColorstr="#000000",GradientType=0 );
  }
   section.coidea-3d-carousel .stage .item .content {
    position: relative;
    display: block;
    width: 100%;
    height: auto;
    margin-top: 50%;
    margin-top: 50vh;
    transform: translateY(-50%);
    text-align: center;
    overflow: hidden;
    z-index: 3;
  }
   section.coidea-3d-carousel .stage .item .content .description {
    position: relative;
    display: block;
    width: 100%;
    height: 24px;
    overflow: hidden;
  }
   section.coidea-3d-carousel .stage .item .content .description p {
    color: #FFFFFA;
    font-size: 24px;
    line-height: 24px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin: 0;
    padding: 0;
  }
  @media screen and (max-width: 768px) {
     section.coidea-3d-carousel .stage .item .content .description p {
      font-size: 16px;
    }
  }
   section.coidea-3d-carousel .stage .item .content .headline {
    position: relative;
    display: block;
    width: 100%;
    height: 64px;
    overflow: hidden;
    margin: 32px 0;
  }
  @media screen and (max-width: 1199px) {
     section.coidea-3d-carousel .stage .item .content .headline {
      margin: 16px 0;
    }
  }
  @media screen and (max-width: 768px) {
     section.coidea-3d-carousel .stage .item .content .headline {
      margin: 4px 0;
    }
  }
   section.coidea-3d-carousel .stage .item .content .headline h2 {
    color: #FFFFFA;
    font-size: 64px;
    line-height: 64px;
    font-weight: 900;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin: 0;
    padding: 0;
  }
  @media screen and (max-width: 1199px) {
     section.coidea-3d-carousel .stage .item .content .headline h2 {
      font-size: 32px;
      letter-spacing: 0.1em;
    }
  }
  @media screen and (max-width: 768px) {
     section.coidea-3d-carousel .stage .item .content .headline h2 {
      font-size: 22px;
    }
  }
   section.coidea-3d-carousel .stage .item .content .discover-more {
    position: relative;
    display: block;
    width: 100%;
    height: 48px;
    overflow: hidden;
  }
   section.coidea-3d-carousel .stage .item .content .discover-more a {
    position: relative;
    display: block;
    width: 100%;
    max-width: 164px;
    height: 48px;
    margin: 0 auto;
    background-color: transparent; /* 修改这里 */
  border: 2px solid #780116; /* 添加边框保持可见性 */
  color: #780116;
    text-decoration: none;
    text-transform: uppercase;
    outline: 0px none;
    outline: 0px;
    font-size: 14px;
    line-height: 50px;
    font-weight: 700;
    text-align: center;
    transition: background-color 0.35s ease-in-out, color 0.35s ease-in-out;
  }
   section.coidea-3d-carousel .stage .item .content .discover-more a:hover {
    background-color: #780116;
    color: #FFFFFA;
  }
</style>