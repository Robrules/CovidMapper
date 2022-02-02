// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import vueRouter from 'vue-router'
import axios from 'axios'
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'
Vue.use(BootstrapVueIcons)

Vue.use(BootstrapVue)
Vue.config.productionTip = false
Vue.prototype.$axios = axios
Vue.use(vueRouter)

axios.defaults.baseURL = 'http://localhost:8000/'
axios.defaults.headers['Accept-Language'] = 'en'

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router: router,
  components: { App },
  template: '<App/>'
})
