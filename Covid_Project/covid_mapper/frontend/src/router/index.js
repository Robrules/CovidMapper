import VueRouter from 'vue-router'

import Home from '@/components/Home'
import safetyRatings from '@/pages/safetyRatings'
/* eslint-disable */

export const router = new VueRouter({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/safety-ratings',
      name: 'safetyRatings',
      component: safetyRatings
    }
  ]
})

export default router
