<template>
  <div>
    <Head></Head>
    <!-- 固定上传按钮 -->
    <div class="fixed-upload-container">
      <label class="upload-label">
        <input
          type="file"
          multiple
          accept="image/*"
          @change="handleUpload"
          class="upload-input"
        >
        <div class="upload-button">
          <span class="upload-icon" style="margin-top:-8px">📷</span>
          <span class="upload-text">添加图片</span>
        </div>
      </label>
    </div>

    <!-- 轮播图容器 -->
    <section class="slideshow" :style="{ visibility: slideshowVisible }">
      <ul class="navigation">
        <li 
          v-for="(item, index) in items"
          :key="index"
          class="navigation-item"
          :class="{ 
            active: activeIndex === index,
            uploaded: item.img !== defaultImg 
          }"
          @mouseenter="setTweenValues"
          @click="doTween(index)"
        >
          <span class="rotate-holder" style="visibility: hidden;">{{ index * 40 }}</span>
          <span 
            class="background-holder"
            :style="{ backgroundImage: `url(${item.img})` }"
          ></span>
        </li>
      </ul>

      <div class="detail">
        <div 
          v-for="(item, index) in items"
          :key="index"
          class="detail-item"
          :class="{ active: activeIndex === index }"
        >
          <div class="headline" v-html="splitLetters(item.title)"></div>
          <div 
            class="background"
            :style="{ backgroundImage: `url(${item.img})` }"
          ></div>
        </div>
      </div>
    </section>
     <button class="shiny" style="margin-top:15px;border: none;color:white" @click="upload()">上传</button>
    <liuxing></liuxing>
  </div>
</template>

<script>
import $ from 'jquery'
import { TweenMax, TimelineMax, Sine } from 'gsap'
import imagesLoaded from 'imagesloaded'
import liuxing from './liuxing.vue'
export default {
  components: { liuxing },
  data() {
    return {
      slideshowVisible: 'hidden',
      activeIndex: 0,
      defaultImg: require('@/assets/img/default.png'),
      items: Array.from({ length: 9 }, (_, i) => ({
        title: `位置 ${i + 1}`,
        img: require('@/assets/img/default.png')
      })),
      rotation: 0,
      type: '_short',
      windowWidth: window.innerWidth
    }
  },

  mounted() {
    this.initAnimation()
    window.addEventListener('resize', this.handleResize)
  },

  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize)
  },

  methods: {
    loadScript(src) {
      return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = src;
        script.onload = resolve;
        script.onerror = reject;
        document.body.appendChild(script);
      });
    },
    async loadUploader() {
      try {
        await this.loadScript('/js/jquery-2.1.1.min.js'); // 确保 jQuery 先加载
      
        await this.loadScript('/imgpro/mloading.js');
        console.log('Both scripts loaded successfully');     
const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = '/imgpro/ssi-uploader.css';
    // 将link元素添加到head标签中
    document.head.appendChild(link);
    // var s=document.querySelector('.ssi-button');
    //     s.style.display='inline-block';
    //     s.style.textAlign = 'center';
    //     s.style.verticalAlign = 'middle';
    //     s.style.fontSize = '12px';
    //     s.style.textDecoration = 'none';
    //     s.style.border = '1px solid #aeaeae'; 
    //     s.style.cursor = 'pointer';
    //     s.style.padding = '6px 6px';
    //     s.style.margin = '0 15px 0 2px';
    //     s.style.borderRadius = '3px';
    //     s.style.color = 'whitesmoke'; 
    //     s.style.background = 'linear-gradient(-45deg, #2284fb 50%, #0a0e92 60%, #2e59d4 70%)';
    // var s1=document.querySelector('.info');
    // s1.style.background = 'linear-gradient(-45deg, #2284fb 50%, #0a0e92 60%, #2e59d4 70%)';
    } catch (error) {
        console.error('Failed to load script:', error);
      }
    },
    upload() {
            $("body").mLoading();  
            //两秒后进行路由跳转
            setTimeout(() => {
               $("body").mLoading('hide');
               this.$router.push({ path: '/searchresult' });
            }, 3000); 
        },
    handleUpload(event) {
      const files = Array.from(event.target.files)
      if (!files.length) return

      files.forEach((file, fileIndex) => {
        const reader = new FileReader()
        reader.onload = (e) => {
          const targetIndex = this.items.findIndex(item => item.img === this.defaultImg)
          if (targetIndex !== -1) {
            this.$set(this.items, targetIndex, {
              ...this.items[targetIndex],
              img: e.target.result,
              title: `已上传 ${targetIndex + 1}`
            })
            this.$nextTick(() => {
              imagesLoaded('.slideshow', { background: true }, () => {
                this.initAnimation()
              })
            })
          }
        }
        reader.readAsDataURL(file)
      })
    },

    splitLetters(text) {
      return text.replace(/([^\x00-\x80]|\w)/g, "<span class='letter'>$&</span>")
    },

    initAnimation() {
      const checkContainerSize = () => {
        const navigation = $('.navigation')
        if (navigation.width() === 0 || navigation.height() === 0) {
          setTimeout(checkContainerSize, 50)
          return
        }

        const navigationItem = $('.navigation-item')
        navigationItem.each((index, elem) => {
          TweenMax.set(elem, {
            left: navigation.width() / 2 - navigationItem.width() / 2 - 10,
            rotation: 90 + (index * 360 / navigationItem.length),
            transformOrigin: `50% ${navigation.width() / 2}px`
          })
          
          TweenMax.set($(elem).find('.background-holder'), {
            rotation: -90 - (index * 360 / navigationItem.length),
          })
        })

        TweenMax.to('.slideshow', 1, { autoAlpha: 1 })
        this.slideshowVisible = 'visible'
      }
      checkContainerSize()
    },

    setTweenValues(event) {
      this.rotation = Number($(event.target).find('.rotate-holder').text())
    },

    doTween(index) {
      this.activeIndex = index
      const timeline = new TimelineMax()

      timeline
        .to('.navigation', 0.6, {
          rotation: -this.rotation + this.type,
          transformOrigin: "50% 50%",
          ease: Sine.easeInOut
        })
        .staggerTo($('.navigation-item').find('.background-holder'), 0.6, {
          cycle: {
            rotation: (i, element) => {
              return -90 - Number($(element).prev('.rotate-holder').text()) + this.rotation + this.type
            }
          },
          transformOrigin: "50% 50%",
          ease: Sine.easeInOut,
        }, 0, '-=0.6')
        .staggerFromTo($('.active .letter'), 0.3, {
          autoAlpha: 0,
          x: -100,
        }, {
          autoAlpha: 1,
          x: 0,
          ease: Sine.easeInOut,
        }, 0.025, '-=0.3')
        .fromTo($('.active .background'), 0.9, {
          autoAlpha: 0,
          x: -100,
        }, {
          autoAlpha: 1,
          x: 0,
          ease: Sine.easeInOut,
        }, 0.05, '+=0.3')
    },

    handleResize() {
      if (window.innerWidth !== this.windowWidth) {
        this.$nextTick(this.initAnimation)
      }
      this.windowWidth = window.innerWidth
    }
  }
}
</script>

<style scoped>
@import './mloading.css';
/* 固定上传按钮 */
.fixed-upload-container {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
  pointer-events: none;
}

.upload-label {
  display: inline-block;
  pointer-events: all;
}

.upload-input {
  display: none;
}

.upload-button {
  background: rgba(255, 255, 255, 0.95);
  color: #2c3e50;
  padding: 12px 24px;
  border-radius: 30px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  border: 2px solid rgba(44, 62, 80, 0.1);
  transition: all 0.3s ease;
}

.upload-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
  background: rgba(255, 255, 255, 1);
}

.upload-icon {
  font-size: 20px;
}

.upload-text {
  font-size: 16px;
  font-weight: 500;
}

/* 轮播图样式 */
.slideshow {
  position: relative;
  width: 100%;
  height: 77vh;
  visibility: hidden;
  overflow: hidden;
}

.navigation {
  position: absolute;
  width: 640px;
  height: 640px;
  left: -230px;
  top: 50%;
  margin-top: -320px;
  z-index: 100;
}

.navigation-item {
  position: absolute;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.navigation-item:hover {
  transform: scale(1.05);
}

.background-holder {
  position: absolute;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  border-radius: 50%;
}

.navigation-item.uploaded .background-holder {
  box-shadow: 0 0 0 3px #4CAF50;
}

.detail {
  position: absolute;
  width: 100%;
  height: 100%;
  z-index: 90;
}

.detail-item {
  position: absolute;
  width: 100%;
  height: 100%;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.5s ease;
}

.detail-item.active {
  opacity: 1;
  visibility: visible;
}

.background {
  position: absolute;
  top: -50px;
  left: -50px;
  right: -50px;
  bottom: -50px;
  background-size: cover;
  background-position: center;
}

.headline {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 110;
}

.letter {
  font-family: 'Playfair Display', serif;
  font-size: 6rem;
  font-weight: 900;
  color: white;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

/* 响应式调整 */
@media (max-width: 768px) {
  .navigation {
    width: 480px;
    height: 480px;
    left: -170px;
    margin-top: -240px;
  }

  .navigation-item {
    width: 92px;
    height: 92px;
  }

  .upload-button {
    padding: 10px 20px;
  }

  .upload-icon {
    font-size: 18px;
  }

  .upload-text {
    font-size: 14px;
  }

  .letter {
    font-size: 4rem;
  }
}

@media (max-width: 480px) {
  .navigation {
    width: 320px;
    height: 320px;
    left: -190px;
    margin-top: -160px;
  }

  .navigation-item {
    width: 48px;
    height: 48px;
  }

  .upload-button {
    padding: 8px 16px;
    border-radius: 24px;
  }

  .letter {
    font-size: 2.5rem;
  }
}
</style>