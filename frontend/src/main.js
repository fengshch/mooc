// with polyfills
import 'core-js/stable'
import 'regenerator-runtime/runtime'

import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store/'
import { VueAxios } from './utils/request'
import { Tree } from 'ant-design-vue'
import VueVideoPlayer from 'vue-video-player'
import CKEditor from '@ckeditor/ckeditor5-vue'

// mock
// WARNING: `mockjs` NOT SUPPORT `IE` PLEASE DO NOT USE IN `production` ENV.
// import './mock'

import globalSetting from './core/bootstrap'
import './core/lazy_use'
import './permission' // permission control
import './utils/filter' // global filter
import './components/global.less'
import 'video.js/dist/video-js.css'

Vue.config.productionTip = false

// mount axios Vue.$http and this.$http
Vue.use(VueAxios)
Vue.use(Tree)
Vue.use(VueVideoPlayer)
Vue.use(CKEditor)

new Vue({
  router,
  store,
  created: globalSetting,
  render: h => h(App)
}).$mount('#app')
