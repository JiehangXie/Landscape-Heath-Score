import { createApp } from 'vue'
import ElementPlus from 'element-plus';
import 'element-plus/lib/theme-chalk/index.css';
import App from './App.vue';
import { createRouter, createWebHistory } from 'vue-router'

import Upload from './components/upload.vue'
import Result from './components/result.vue'


const routes = [
    { path: '/', component: Upload },
    { path: '/result', component: Result ,name:'result'}

  ]
  
  // 3. 创建 router 实例，然后传 `routes` 配置
  // 你还可以传别的配置参数, 不过先这么简单着吧。


const router = createRouter({
    history: createWebHistory(),
    routes // (缩写) 相当于 routes: routes
    });

router.beforeEach((to, from, next) => {    
      // chrome
      document.body.scrollTop = 0
      // firefox
      document.documentElement.scrollTop = 0
      // safari
      window.pageYOffset = 0
      next()
  })

const app = createApp(App)
app.use(router)
app.use(ElementPlus)
app.mount('#app')
