import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import dage from '../views/yinshihao.vue'
import liu from '../views/liu.vue'
import KnowledgeDetail from '../views/KnowledgeDetail.vue'
import fileDetail from '../views/fileDetail.vue'
import AddKnowledgeBase from '../views/AddKnowledgeBase.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/home',
      name: 'home',
      component: HomeView
    },
    {
      path: '/yinshihao',
      name: 'yinshihao',
      component: dage
    },
    {
      path: '/liu',
      name: 'liu',
      component: liu
    },
    {
      path: '/KnowledgeDetail/:id/:name',
      name: 'KnowledgeDetail',
      component: KnowledgeDetail,
      props: true
    }, 
    {
      path: '/fileDetail/:id/:name',
      name: 'fileDetail',
      component: fileDetail,
      props: true
    }, 
    {
      path: '/AddKnowledgeBase',
      name: 'AddKnowledgeBase',
      component: AddKnowledgeBase,
      // props: true
    }
  ]
})

export default router
