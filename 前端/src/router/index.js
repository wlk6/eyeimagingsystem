import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '@/views/login'
import EimIndex from '@/views/eimindex/eimindex.vue'
import ImgPro from '@/views/imgpro/imgpro.vue'
import SeaRes from '@/views/searchresult/SeaRes.vue'
import Admin from '@/views/admin/admin.vue'
import patient from '@/views/patient/patient.vue'
import Info from '@/views/info/info.vue'
import ChangePwd from '@/views/changepwd/ChangePwd.vue'
import DocMag from '@/views/docmag/docmag'
import CheckList from '@/views/checklist/check'
import ModList from '@/views/modlist/modlist.vue'
import store from '@/store'
import Dashboard from '@/views/dashboard/Dashboard.vue'
import Patients from '@/views/Patients/Patients.vue'
import His from '@/views/His/His.vue'
import Help from '@/views/help/help.vue'
import Settings from '@/views/settings/settings.vue'
import review from '@/views/review/review.vue'
Vue.use(VueRouter)

const router = new VueRouter({
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    { path: '/login', component: Login },
    { path: '/doctor', 
      redirect: '/dashboard',
      component: EimIndex,
      children:[
        { path: '/dashboard', component: Dashboard },
  { path: '/diagnosis', component: ImgPro },
  { path: '/patients', component: Patients },
  { path: '/dghistory', component: His },
  { path: '/info', component: Info },
  { path: '/settings', component: Settings },
  { path: '/help', component: Help },
  // { path: '/logout', component: Logout }
      ]

     },
    { path: '/imgpro', component: ImgPro },
    { path: '/searchresult', component: SeaRes },
    { path: '/admin', component: Admin,
      redirect: '/admin/doctors',
      children:[
  // { path: '/diagnosis', component: ImgPro },
  { path: '/admin/doctors', 
    name: 'doctors',
    component: DocMag  },
  // { path: '/dghistory', component: His },
  // { path: '/info', component: Info },
  // { path: '/settings', component: Settings },
  { path: '/admin/review', 
    name: 'review',
    component: review },
  { path: '/admin/model', 
    name:'model',
    component: ModList }
      ]
     },
    { path:'/patient',component:patient},
    { path:'/info',component:Info},
    { path:'/changepassword',component:ChangePwd},
    { path:'/doctormanage',component:DocMag},
    { path:'/checklist',component:CheckList},
    { path:'/modlist',component:ModList}
  ]
})
const authUrls = ['/doctor', '/imgpro', '/searchresult', '/admin','/patient','/info']
router.beforeEach((to, from, next) => {
  if(!authUrls.includes(to.path)){
    next()
    return
  }
  const userInfo = store.state.user.userInfo;
  const token = store.getters.token
  console.log(token)
  if (token) {
    next()
  } else {
    next('/login')
  }
})
export default router
