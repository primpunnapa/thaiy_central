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
import RegisterPage from './views/RegisterPage.vue'
import { useAuthStore } from './stores/auth'

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
    path: '/register',
    name: 'register',
    component: RegisterPage
  },
  {
    path: '/profile',
    name: 'profile',
    component: UserProfilePage,
    meta: { requiresAuth: true }
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
    component: AdminUsersPage,
    meta: { requiresAuth: true, requiredRole: 'admin' }
  },
  {
    path: '/editor/series',
    name: 'editor-series',
    component: EditorSeriesPage,
    meta: { requiresAuth: true, requiredRole: 'editor' }
  },
  {
    path: '/editor/studios',
    name: 'editor-studios',
    component: EditorStudiosPage,
    meta: { requiresAuth: true, requiredRole: 'editor' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Route guard for authentication and role-based access control
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // Check if route requires authentication
  if (to.meta.requiresAuth) {
    if (!authStore.token) {
      // User not authenticated, redirect to login
      next({ name: 'login', query: { redirect: to.fullPath } })
      return
    }

    // Check if route requires specific role
    if (to.meta.requiredRole) {
      const userRole = authStore.user?.role

      // Check if user has required role (or is admin)
      if (userRole !== to.meta.requiredRole && userRole !== 'admin') {
        // User doesn't have required role, redirect to home
        next({ name: 'home' })
        return
      }
    }
  }

  next()
})

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.mount('#app')
