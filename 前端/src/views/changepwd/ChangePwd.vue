<template>
  <div>
   <Head></Head>
   <article class="htmleaf-content" style="height: 500px;">
        <!-- multistep form -->
        <form id="msform">
            <!-- progressbar -->
            <ul id="progressbar">
                <li class="active" style="font-size:16px">账号设置</li>
                <li style="font-size:16px">验证码</li>
                <li style="font-size:16px">个人详细信息</li>
            </ul>
            <!-- fieldsets -->
            <fieldset>
                <h2 class="fs-title">创建新密码</h2>
                <h3 class="fs-subtitle">第一步</h3>
                <!-- <input type="text" name="email" placeholder="Email地址" /> -->
                <input type="password" name="pass" placeholder="新密码" v-model="npwd" />
                <input type="password" name="cpass" placeholder="确认新密码" v-model="cnpwd"/>
                <input type="button" name="next" class="next action-button" value="下一步" @click="next1($event)"/>
            </fieldset>
            <fieldset style="">
               <h2 class="fs-title" >工号</h2>
                <h3 class="fs-subtitle">第二步</h3>
                <input type="text" name="fname" placeholder="填写工号" v-model="id"/>
                <input type="button" name="previous" class="previous action-button" value="上一步" />
                <input type="button" name="next" class="next action-button" value="下一步" @click="next2($event)"/>
            </fieldset>
            <fieldset style="">
                 <h2 class="fs-title">填写验证码</h2>
                <h3 class="fs-subtitle">第三步</h3>
                <div style="height:40px;margin-top:10px;"> 
        <input type="text" id="Txtidcode" class="txtVerification" placeholder="请输入验证码" v-model="captchacode" style="width:163px;float:left;margin-right:7px">
        <img id="idcode" :src="code" style="float:left;height:30px;margin-top:12px;cursor:pointer" title="点击刷新" @click="Code"/>
    </div>
                <input type="button" name="previous" class="previous action-button" value="上一步" />
                <input type="button" name="submit" class="submit action-button" value="提交" @click='changepwd'/>
            </fieldset>
        </form>
    </article>
   <liuxing></liuxing>
  </div>
</template>

<script>
import liuxing from '../../components/liuxing.vue';
import {code} from '@/api/code.js';
import {changepwd} from '@/api/changepwd.js';

function loadScript(src) {
  return new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = src;
    script.onload = resolve;
    script.onerror = reject;
    document.body.appendChild(script);
  });
}

export default {
  components: { liuxing },
  data(){
    return {
        captchacode:'',
        code:'',
        captcha_key:'',
        id:'',
        npwd:'',
        cnpwd:''
    };
  },
  async mounted() {
    this.Code();
    try {
      await loadScript('changepwd/jquerymin.js');
      await loadScript('changepwd/easingmin.js');

      let current_fs, next_fs, previous_fs;
      let left, opacity, scale;
      let animating = false;

      // 获取所有的 previous 按钮
      const previousButtons = document.querySelectorAll('.previous');
      previousButtons.forEach(button => {
        button.addEventListener('click', function () {
          if (animating) return false;
          animating = true;
          current_fs = this.parentNode;
          previous_fs = current_fs.previousElementSibling;

          const progressbarItems = document.querySelectorAll('#progressbar li');
          const fieldsetList = document.querySelectorAll('fieldset');
          const currentIndex = Array.from(fieldsetList).indexOf(current_fs);
          progressbarItems[currentIndex].classList.remove('active');

          previous_fs.style.display = 'block';
          previous_fs.style.left = '0%';
          previous_fs.style.opacity = 0;

          let start = null;
          const duration = 800;
          function step(timestamp) {
            if (!start) start = timestamp;
            const elapsed = timestamp - start;
            const now = Math.min(elapsed / duration, 1);

            scale = now;
            left = now * 1;
            opacity = 1 - now;

            current_fs.style.left = left;
            current_fs.style.opacity = 1 - now;
            previous_fs.style.transform = `scale(${scale})`;
            previous_fs.style.opacity = 1 - opacity;

            if (elapsed < duration) {
              window.requestAnimationFrame(step);
            } else {
              current_fs.style.display = 'none';
              animating = false;
            }
          }
          window.requestAnimationFrame(step);
        });
      });

      // 获取所有的 submit 按钮
      const submitButtons = document.querySelectorAll('.submit');
      submitButtons.forEach(button => {
        button.addEventListener('click', function (e) {
          e.preventDefault();
          return false;
        });
      });
    } catch (error) {
      console.error('脚本加载失败:', error);
    }
  },
  methods: {
    async Code() {
      try {
        const response = await code();
        this.code = response.image;
        this.captcha_key = response.key;
      } catch (error) {
        console.error('请求出错:', error);
      }
    },
   changepwd() {
  changepwd(this.id, this.npwd, this.cnpwd, this.captcha_key, this.captchacode)
    .then(ischange => {
      const h = this.$createElement;
      this.$notify({
        title: '标题名称',
        message: h('i', { style: 'color: teal' }, ischange.msg)
      });
    })
    .catch(error => {
      console.error('Error:', error);
      // 在这里处理错误情况，例如显示错误通知
      const h = this.$createElement;
      this.$notify({
        title: '错误',
        message: h('i', { style: 'color: red' }, '验证码错误')
      });
    });
},
    next1(event) {
      if (this.npwd !== this.cnpwd) {
        this.$message({
          message: '两次密码不一致',
          type: 'error'
        });
        return;
      } else if (this.npwd == '') {
        this.$message({
          message: '新密码信息不能为空',
          type: 'error'
        });
      }
      else {
        let current_fs, next_fs, previous_fs;
        let left, opacity, scale;
        let animating = false;
        if (animating) return false;
        animating = true;
        // 通过 event.target 获取当前点击的按钮，再获取其父元素（即 fieldset）
        current_fs = event.target.parentNode;
        next_fs = current_fs.nextElementSibling;
        console.log(this.npwd);
        // 获取 progressbar 中的 li 元素
        const progressbarItems = document.querySelectorAll('#progressbar li');
        const fieldsetList = document.querySelectorAll('fieldset');
        const nextIndex = Array.from(fieldsetList).indexOf(next_fs);
        progressbarItems[nextIndex].classList.add('active');

        next_fs.style.display = 'block';
        next_fs.style.left = '50%';
        next_fs.style.opacity = 0;

        let start = null;
        const duration = 800;
        function step(timestamp) {
          if (!start) start = timestamp;
          const elapsed = timestamp - start;
          const now = Math.min(elapsed / duration, 1);

          scale = 1 - (1 - now) * 0.2;
          left = now * 1;
          opacity = 1 - now;

          current_fs.style.opacity = 1 - now;
          current_fs.style.transform = `scale(${scale})`;
          next_fs.style.left = left;
          next_fs.style.opacity = 1 - opacity;

          if (elapsed < duration) {
            window.requestAnimationFrame(step);
          } else {
            current_fs.style.display = 'none';
            animating = false;
          }
        }
        window.requestAnimationFrame(step);
      }
    },
    next2(event){
          if(this.id==''){
             this.$message({
          message: '工号信息不能为空',
          type: 'error'
        });
        return;
          }
          else {
        let current_fs, next_fs, previous_fs;
        let left, opacity, scale;
        let animating = false;
        if (animating) return false;
        animating = true;
        // 通过 event.target 获取当前点击的按钮，再获取其父元素（即 fieldset）
        current_fs = event.target.parentNode;
        next_fs = current_fs.nextElementSibling;
        console.log(this.npwd);
        // 获取 progressbar 中的 li 元素
        const progressbarItems = document.querySelectorAll('#progressbar li');
        const fieldsetList = document.querySelectorAll('fieldset');
        const nextIndex = Array.from(fieldsetList).indexOf(next_fs);
        progressbarItems[nextIndex].classList.add('active');

        next_fs.style.display = 'block';
        next_fs.style.left = '50%';
        next_fs.style.opacity = 0;

        let start = null;
        const duration = 800;
        function step(timestamp) {
          if (!start) start = timestamp;
          const elapsed = timestamp - start;
          const now = Math.min(elapsed / duration, 1);

          scale = 1 - (1 - now) * 0.2;
          left = now * 1;
          opacity = 1 - now;

          current_fs.style.opacity = 1 - now;
          current_fs.style.transform = `scale(${scale})`;
          next_fs.style.left = left;
          next_fs.style.opacity = 1 - opacity;

          if (elapsed < duration) {
            window.requestAnimationFrame(step);
          } else {
            current_fs.style.display = 'none';
            animating = false;
          }
        }
        window.requestAnimationFrame(step);
      }
    }
  }
}
</script>

<style scoped>
#msform {
  width: 400px;
  margin: 50px auto;
  text-align: center;
  position: relative;
}
#msform fieldset {
  background: white;
  border: 0 none;
  border-radius: 3px;
  box-shadow: 0 0 15px 1px rgba(0, 0, 0, 0.4);
  padding: 20px 30px;
  box-sizing: border-box;
  width: 80%;
  margin: 0 10%;
  /*stacking fieldsets above each other*/
  position: absolute;
}
/*Hide all except first fieldset*/
#msform fieldset:not(:first-of-type) {
  display: none;
}
/*inputs*/
#msform input, #msform textarea {
  padding: 15px;
  border: 1px solid #ccc;
  border-radius: 3px;
  margin-bottom: 10px;
  width: 100%;
  box-sizing: border-box;
  font-family: "Microsoft YaHei",montserrat;
  color: #2C3E50;
  font-size: 13px;
}
/*buttons*/
#msform .action-button {
  width: 100px;
  background: #2284FB;
  font-weight: bold;
  color: white;
  border: 0 none;
  border-radius: 1px;
  cursor: pointer;
  padding: 10px 5px;
  margin: 10px 5px;
}
#msform .action-button:hover, #msform .action-button:focus {
  box-shadow: 0 0 0 2px white, 0 0 0 3px #2284FB;
}
/*headings*/
.fs-title {
  font-size: 15px;
  text-transform: uppercase;
  color: #2C3E50;
  margin-bottom: 10px;
}
.fs-subtitle {
  font-weight: normal;
  font-size: 13px;
  color: #666;
  margin-bottom: 20px;
}
/*progressbar*/
#progressbar {
  margin-bottom: 30px;
  overflow: hidden;
  /*CSS counters to number the steps*/
  counter-reset: step;
}
#progressbar li {
  list-style-type: none;
  color: white;
  text-transform: uppercase;
  font-size: 9px;
  width: 33.33%;
  float: left;
  position: relative;
}
#progressbar li:before {
  content: counter(step);
  counter-increment: step;
  width: 20px;
  line-height: 20px;
  display: block;
  font-size: 10px;
  color: #333;
  background: white;
  border-radius: 3px;
  margin: 0 auto 5px auto;
}
/*progressbar connectors*/
#progressbar li:after {
  content: '';
  width: 100%;
  height: 2px;
  background: white;
  position: absolute;
  left: -50%;
  top: 9px;
  z-index: -1; /*put it behind the numbers*/
}
#progressbar li:first-child:after {
  /*connector not needed before the first step*/
  content: none; 
}
/*marking active/completed steps green*/
/*The number of the step and the connector before it = green*/
#progressbar li.active:before,  #progressbar li.active:after{
  background: #2284FB;
  color: white;
}
</style>