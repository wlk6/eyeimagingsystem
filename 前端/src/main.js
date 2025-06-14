import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import Head from './components/head.vue'; 
import LiuXing from './components/liuxing.vue'; 
import Table from './components/table.vue';
import Table1 from './components/table1.vue';
import Table2 from './components/table2.vue';
import Table3 from './components/table3.vue';
import Art from './components/art.vue';
import Upload from './components/upload.vue';
import 'xe-utils'
import VXETable from 'vxe-table'
import 'vxe-table/lib/style.css'
import ElementUI from 'element-ui';
// import VXETablePluginElement from 'vxe-table-plugin-element';
// import 'vxe-table-plugin-element/dist/style.css';
import 'element-ui/lib/theme-chalk/index.css';
import { gsap } from 'gsap';
Vue.prototype.$gsap = gsap;
Vue.use(VXETable)
Vue.use(ElementUI);
// VXETable.use(VXETablePluginElement);
// 注册全局组件
Vue.component('Head', Head);
Vue.component('LiuXing', LiuXing);
Vue.component('Table', Table);
Vue.component('Table1', Table1);
Vue.component('Table2', Table2);
Vue.component('Table3', Table3);
Vue.component('Art',Art)
Vue.component('Upload',Upload)
Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app');
