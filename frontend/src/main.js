import './index.css'

import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia } from 'pinia'
import App from './App.vue'
import HomePage from './views/HomePage.vue'
import SeriesDetailPage from './views/SeriesDetailPage.vue'
import SeriesListPage from './views/SeriesListPage.vue'
import SchedulePage from './views/SchedulePage.vue'
import StudiosPage from './views/StudiosPage.vue'
import LoginPage from './views/LoginPage.vue'
import UserProfilePage from './views/UserProfilePage.vue'
import AdminUsersPage from './views/AdminUsersPage.vue'
import EditorSeriesPage from './views/EditorSeriesPage.vue'
import EditorStudiosPage from './views/EditorStudiosPage.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomePage
  },
  {
    path: '/login',
    name: 'login',
    component: LoginPage
  },
  {
    path: '/profile',
    name: 'profile',
    component: UserProfilePage
  },
  {
    path: '/series/:id',
    name: 'series-detail',
    component: SeriesDetailPage
  },
  {
    path: '/schedule',
    name: 'schedule',
    component: SchedulePage
  },
  {
    path: '/studios',
    name: 'studios',
    component: StudiosPage
  },
  {
    path: '/series',
    name: 'series-list',
    component: SeriesListPage
  },
  {
    path: '/admin/users',
    name: 'admin-users',
    component: AdminUsersPage
  },
  {
    path: '/editor/series',
    name: 'editor-series',
    component: EditorSeriesPage
  },
  {
    path: '/editor/studios',
    name: 'editor-studios',
    component: EditorStudiosPage
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.mount('#app')
