import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegisterView from '../views/RegisterView.vue'
import LoginView from '../views/LoginView.vue'
import PostView from '../views/PostView.vue'
import BaseView from '../views/BaseView.vue'
import UserView from '../views/UserView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/post',
      name: 'post',
      component: PostView
    },
    {
      path: '/user/:id',
      name: 'user',
      component: UserView,
      params: true
    },
    {
      path: '/base',
      name: 'base',
      component: BaseView
    }
  ]
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('user-token')
  
  if (token) {
    if (to.name == 'login' || to.name == 'register' || to.name == 'base'){
      next({ name: 'home' })
    }else{
      next()
    }
  } else {
    if (to.name == 'login' || to.name == 'register' || to.name == 'base') {
      next()
    }else {
      next({ name: 'base' })
    }
  }
})

export default router
