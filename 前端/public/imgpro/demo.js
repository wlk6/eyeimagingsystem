// public/imgpro/demo.js
const { TweenMax, TimelineMax, Sine } = window; // 解决现代浏览器模块作用域问题

document.addEventListener('DOMContentLoaded', function() {
  const slideshow = document.querySelector('.slideshow');
  
  // 使用 imagesLoaded 检测背景图片
  imagesLoaded(
    document.querySelectorAll('.background-holder'),
    { background: true },
    () => {
      // 隐藏加载器
      const loader = document.querySelector('.loader');
      loader.classList.add('is-loaded');

      // 初始化变量
      const navigation = document.querySelector('.navigation');
      const navigationItems = document.querySelectorAll('.navigation-item');
      const detailItems = document.querySelectorAll('.detail-item');
      let rotation;
      const type = '_short';

      // 准备标题字母动画
      document.querySelectorAll('.headline').forEach(headline => {
        headline.innerHTML = headline.textContent.replace(/([^\x00-\x80]|\w)/g, '<span class="letter">$&</span>');
      });

      // 初始化导航项位置
      navigationItems.forEach((item, index) => {
        const navigationWidth = navigation.offsetWidth;
        const itemWidth = item.offsetWidth;
        
        item.style.left = `${navigationWidth / 2 - itemWidth / 2 - 10}px`;
        item.style.transform = `rotate(${90 + (index * 360 / navigationItems.length)}deg)`;
        item.style.transformOrigin = `50% ${navigationWidth / 2}px`;

        const rotateHolder = item.querySelector('.rotate-holder');
        const backgroundHolder = item.querySelector('.background-holder');
        
        rotateHolder.textContent = index * 360 / navigationItems.length;
        backgroundHolder.style.transform = `rotate(${-90 - (index * 360 / navigationItems.length)}deg)`;
      });

      // 设置补间值
      function setTweenValues(event) {
        const rotateHolder = event.target.closest('.navigation-item').querySelector('.rotate-holder');
        rotation = Number(rotateHolder.textContent);
      }

      // 执行补间动画
      function doTween(target) {
        const targetIndex = [...navigationItems].indexOf(target);
        const timeline = new TimelineMax();

        // 切换激活状态
        navigationItems.forEach(item => item.classList.remove('active'));
        detailItems.forEach(item => item.classList.remove('active'));
        target.classList.add('active');
        detailItems[targetIndex].classList.add('active');

        timeline
          .to(navigation, 0.6, {
            rotation: -rotation + type,
            transformOrigin: "50% 50%",
            ease: Sine.easeInOut
          })
          .staggerTo(
            [...navigationItems].map(item => item.querySelector('.background-holder')),
            0.6,
            {
              rotation: (index, element) => {
                const rotateHolder = element.previousElementSibling;
                return -90 - Number(rotateHolder.textContent) + rotation + type;
              },
              transformOrigin: "50% 50%",
              ease: Sine.easeInOut
            },
            0,
            '-=0.6'
          )
          .staggerFromTo(
            detailItems[targetIndex].querySelectorAll('.letter'),
            0.3,
            { autoAlpha: 0, x: -100 },
            { autoAlpha: 1, x: 0, ease: Sine.easeInOut },
            0.025,
            '-=0.3'
          )
          .fromTo(
            detailItems[targetIndex].querySelector('.background'),
            0.9,
            { autoAlpha: 0, x: -100 },
            { autoAlpha: 1, x: 0, ease: Sine.easeInOut },
            0.05,
            '+=0.3'
          );
      }

      // 绑定事件
      navigationItems.forEach(item => {
        item.addEventListener('mouseenter', setTweenValues);
        item.addEventListener('click', (e) => {
          e.preventDefault();
          doTween(e.currentTarget);
        });
      });

      // 初始动画
      TweenMax.to(slideshow, 1, { autoAlpha: 1 });
      const activeItem = document.querySelector('.navigation-item.active');
      TweenMax.to(activeItem.querySelectorAll('.letter'), 0.7, { autoAlpha: 1, x: 0 });
      TweenMax.to(activeItem.querySelector('.background'), 0.7, { autoAlpha: 1, x: 0 });
    }
  );
});

// 窗口调整大小刷新（根据原代码保留）
(function() {
  let width = window.innerWidth;
  window.addEventListener('resize', function() {
    if (window.innerWidth !== width) {
      window.location.reload(true);
      width = window.innerWidth;
    }
  });
})();