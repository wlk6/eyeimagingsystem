<template>
  <div id="modal-container">
  <div class="modal-background">
    <div class="modal">
      <h2>分析结果</h2>
      <p style="text-align: left">（一）专科检查<br>
      裂隙灯显微镜检查：
眼睑：无红肿、畸形，睑缘清洁度较高，睫毛排列整齐 / 紊乱。<br>
结膜：结膜无充血 / 充血（若充血，标注具体类型，如 “睫状充血”），未见异常分泌物。<br>
角膜：透明 / 可见 下方点状上皮缺损，荧光素染色阴性<br>
前房：深度正常，房水清澈 / 可见浮游细胞（记录分级）。<br>
瞳孔：等大等圆，直径 16 mm，对光反射灵敏 / 迟钝。<br>
晶状体：透明 / 可见 皮质轻度浑浊。<br>
眼底检查（眼底镜 / 眼底照相）：<br>
视盘边界清 / 欠清，颜色正常 / 苍白，C/D 比值 （正常≤0.5）。<br>
视网膜血管走形正常，未见出血、渗出；黄斑区中心凹反光存在 / 减弱。<br>
（二）辅助检查
眼部 B 超：未见玻璃体混浊 / 可见 玻璃体后脱离<br>
光学相干断层扫描（OCT）：视网膜各层结构清晰 / 可见 黄斑区神经上皮层水肿<br>
视野检查：视野正常 / 存在 鼻侧视野缺损 缺损。<br>
三、诊断结论
 眼疾病诊断：如 右眼细菌性结膜炎”“双眼老视”“左眼开角型青光眼” 等（根据具体病情明确诊断，若为复杂病例，需分层列出主次诊断）。<br>
鉴别诊断：结合检查结果，排除 排除病毒性角膜炎 疾病
      </p>
      <svg class="modal-svg" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" preserveAspectRatio="none">
        <rect x="0" y="0" fill="none" width="226" height="162" rx="3" ry="3"></rect>
      </svg>
    </div>
  </div>
</div>
</template>

<script>
import $ from 'jquery'
export default {
name: 'SeaRes',
mounted() {
    $('#modal-container').addClass('five');
}
}
</script>

<style scoped>
@import './seares.css'
</style>