<template>
  <div class="middle">
    <div class="scene">
        <div class="box">
            <ul class="ring">

            </ul>
        </div>
        <div class="item">
            <p>医者仁心妙手间，悬壶济世乐无边。</p>
            <a href="javascript:;" class="close"></a>
        </div>
    </div>
    <div class="text">
        <p>在下面输入你自己的文字（建议50-350字）</p>
        <textarea cols="30" rows="10"></textarea>
        <div class="btn">
            <button>提交</button>
            <button>重置</button>
        </div>
        <a href="javascript:;" class="close"></a>
    </div>
    <div class="table" style="display: none;">
        <a href="javascript:;" class="active">圆球</a>
        <a href="javascript:;">圆锥</a>
        <a href="javascript:;">柱状</a>
        <a href="javascript:;">柱状扭曲</a>
    </div>
    <div class="line" style="display: none;"></div>
    <div class="btn2" style="diaplay: none;">
        <button style="display:none">展开</button>
        <button style="display:none">自定义文字</button>
    </div>
</div>
</template>

<script>
export default {
mounted() {
     const script = document.createElement('script');
    script.src = 'js/css3.js';
    script.onload = () => {
      // 外部脚本加载完成后，可以在此处编写相关的处理逻辑
      console.log('External JavaScript file loaded');
    };
    document.body.appendChild(script);
},
}
</script>

<style scoped>


/*浮动*/



li {
	list-style: none;
}

.middle {
	width: 1000px;
	height: 620px;
	position: absolute;
	left: 50%;
	top: 50%;
	margin-left: -500px;
	margin-top: -310px;
}

.scene {
	width: 400px;
	height: 400px;
	margin: 0 auto;
	perspective: 900px;
	-webkit-perspective: 900px;
	position: relative;
	transform-style: preserve-3d;
	-webkit-transform-style: preserve-3d;
	color: #16E5FF;
}

.box {
	width: 100%;
	height: 100%;
	position: relative;
	transform-style: preserve-3d;
	-webkit-transform-style: preserve-3d;
	perspective-origin: center 250px;
}

.ring {
	width: 100%;
	height: 100%;
	transform-style: preserve-3d;
	-webkit-transform-style: preserve-3d;
	position: absolute;
}

.ring li {
	line-height: 30px;
	text-align: center;
	font-size: 25px;
	position: absolute;
	margin-top: -25px;
	margin-left: -15px;
	transition: all .6s;
}

li.all {
	transition: all .6s cubic-bezier(.75,.25,1,1);
}

li.one {
	transition: transform .6s cubic-bezier(0,0,.25,.75);
}

.text {
	position: absolute;
	top: 30px;
	left: 50%;
	margin-left: -329px;
	padding: 15px 18px;
	width: 602px;
	height: 318px;
	border: 1px solid #e5e5e5;
	border-radius: 8px;
	box-shadow: 0 5px 5px #d4dbe1;
	background-color: #fff;
	transform: scale(.5);
	opacity: 0;
	transition: opacity .3s cubic-bezier(.15,.84,.35,1), transform .3s cubic-bezier(.15,.84,.35,1);
	display: none;
}

.text p {
	margin-bottom: 12px;
	font-size: 12px;
}

.text textarea {
	resize: none;
	width: 580px;
	height: 220px;
	padding: 10px;
	border: 1px solid #cacaca;
	border-radius: 8px;
	background-color: #f3f7fa;
	margin-bottom: 15px;
	color: #00a0e9;
}

.text a {
	position: absolute;
	top: 10px;
	right: 10px;
	width: 19px;
	height: 19px;
	/* background: url("images/icons/close.png") no-repeat center; */
}

.btn {
	margin: 0 auto;
	width: 260px;
	overflow: hidden;
}

.btn button {
	width: 120px;
	height: 30px;
	border: 1px solid #cacaca;
	border-radius: 15px;
	float: left;
}

.btn button:nth-of-type(1) {
	margin-right: 18px;
}

.table {
	width: 400px;
	margin: 20px auto 10px;
	overflow: hidden;
}

.table a {
	float: left;
	width: 100px;
	height: 12px;
	padding-top: 94px;
	font-size: 12px;
	line-height: 12px;
	text-align: center;
	color: #889199;
}

/* .table a:nth-of-type(1) {
	background: url("images/icons/circle.png") no-repeat center 2px;
}

.table a:nth-of-type(2) {
	background: url("images/icons/Cone.png") no-repeat center top;
}

.table a:nth-of-type(3) {
	background: url("images/icons/Column.png") no-repeat center top;
} */

/* .table a:nth-of-type(4) {
	background: url("images/icons/Column2.png") no-repeat center top;
}

.table a:nth-of-type(1):hover {
	background: url("images/icons/circle-hover.png") no-repeat center 2px;
}

.table a:nth-of-type(2):hover {
	background: url("images/icons/Cone-hover.png") no-repeat center top;
}

.table a:nth-of-type(3):hover {
	background: url("images/icons/Column-hover.png") no-repeat center top;
}

.table a:nth-of-type(4):hover {
	background: url("images/icons/Column2-hover.png") no-repeat center top;
} */
/* 
.table a:nth-of-type(1).active {
	background: url("images/icons/circle-active.png") no-repeat center 2px;
}

.table a:nth-of-type(2).active {
	background: url("images/icons/Cone-active.png") no-repeat center top;
}

.table a:nth-of-type(3).active {
	background: url("images/icons/Column-active.png") no-repeat center top;
}

.table a:nth-of-type(4).active {
	background: url("images/icons/Column2-active.png") no-repeat center top;
} */

.line {
	width: 734px;
	height: 1px;
	margin: 0 auto 14px;
	background: -webkit-linear-gradient(left,#7ecef4,#94cc8e,#fff45c);
}

.btn2 {
	width: 204px;
	margin: 0 auto;
	overflow: hidden;
}

.btn2 button {
	width: 100px;
	height: 30px;
	border: 1px solid #cacaca;
	float: left;
}

.btn2 button:nth-of-type(1) {
	border-radius: 15px 0 0 15px;
}

.btn2 button:nth-of-type(2) {
	margin-left: -1px;
	border-radius: 0 15px 15px 0;
}

button {
	background: linear-gradient(#fff,#e3ecf3);
	color: #889199;
}

button:hover {
	background: linear-gradient(#fff,#bef5ff 10%,#6cb7df);
	border-color: #bef5ff;
	color: #00a0e9;
}

button:active {
	background: linear-gradient(#fff,#6cb7df 10%,#bef5ff);
}

button.active {
	background: linear-gradient(#fff,#6cb7df 10%,#bef5ff);
}

.item {
	width: 400px;
	padding: 30px;
	top: 100px;
	margin: -30px;
	position: fixed;
	transform: scale(2);
	-webkit-transform: scale(2);
	opacity: 0;
	display: none;
	transform-origin: center center 200px;
	-webkit-transform-origin: center center 200px;
	opacity: 0;
	transition: all .5s ease;
}

.item a {
	position: absolute;
	top: 10px;
	right: 10px;
	width: 19px;
	height: 19px;
	/* background: url("images/icons/close.png") no-repeat center; */
}

.item p {
	font-size: 14px;
	line-height: 24px;
	word-break: break-all;
}

</style>