<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const open = ref(false)
const route = useRoute()
const auth = useAuthStore()

const publicLinks = [
  { to: '/', label: 'หน้าแรก' },
  { to: '/series', label: 'ซีรีส์ทั้งหมด' },
  { to: '/schedule', label: 'ตารางออกอากาศ' },
  { to: '/studios', label: 'สตูดิโอ' }
]

const adminLinks = computed(() => {
  const links = []
  if (auth.isAdmin) {
    links.push({ to: '/admin/users', label: 'จัดการผู้ใช้', icon: 'users' })
  }
  if (auth.isEditor) {
    links.push(
      { to: '/editor/series', label: 'จัดการซีรีส์'},
      { to: '/editor/studios', label: 'จัดการสตูดิโอ'}
    )
  }
  return links
})

onMounted(() => {
  auth.getCurrentUser()
})

const handleLogout = () => {
  auth.logout()
  open.value = false
}
</script>

<template>
  <nav class="sticky top-0 z-50 bg-card/80 backdrop-blur-md border-b border-border">
    <div class="container mx-auto px-4 flex items-center justify-between h-16">

      <!-- Logo -->
      <router-link
        to="/"
        class="flex items-center gap-2 font-heading text-xl font-bold text-primary"
      >
        <svg class="w-6 h-6 fill-primary" viewBox="0 0 24 24">
          <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" />
        </svg>
        <span>Thai BL Hub</span>
      </router-link>

      <!-- Desktop nav -->
      <div class="hidden md:flex items-center gap-1">
        <!-- Public links -->
        <router-link
          v-for="link in publicLinks"
          :key="link.to"
          :to="link.to"
          :class="[
            'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
            route.path === link.to
              ? 'bg-primary text-primary-foreground'
              : 'text-foreground/70 hover:bg-muted hover:text-foreground'
          ]"
        >
          {{ link.label }}
        </router-link>

        <!-- Admin links separator -->
        <div v-if="adminLinks.length > 0" class="w-px h-6 bg-border mx-1" />

        <!-- Admin links -->
        <router-link
          v-for="link in adminLinks"
          :key="link.to"
          :to="link.to"
          :class="[
            'px-3 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-1.5',
            route.path === link.to
              ? 'bg-primary text-primary-foreground'
              : 'text-foreground/70 hover:bg-muted hover:text-foreground'
          ]"
        >
          <!-- Icon based on type -->
          <svg v-if="link.icon === 'users'" class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 8.048M12 4.354a4 4 0 110 8.048M12 4.354V2m2.879 15.854a4 4 0 11-5.758 0M15.879 17.904a4 4 0 11-5.758 0" />
          </svg>
          <svg v-else-if="link.icon === 'film'" class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 4v16m10-16v16m-10-4h10M7 8h10m0 8H7" />
          </svg>
          <svg v-else-if="link.icon === 'building'" class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5.581m0 0H9m5.581 0a2 2 0 100-4 2 2 0 000 4z" />
          </svg>
          {{ link.label }}
        </router-link>

        <!-- Auth separator -->
        <div v-if="adminLinks.length > 0 || auth.isAuthenticated" class="w-px h-6 bg-border mx-1" />

        <!-- Auth section -->
        <template v-if="auth.isAuthenticated && auth.user">
          <router-link
            :to="{ name: 'profile' }"
            :class="[
              'px-3 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-1.5',
              route.path === '/profile'
                ? 'bg-primary text-primary-foreground'
                : 'text-foreground/70 hover:bg-muted hover:text-foreground'
            ]"
          >
            <span class="text-xs font-bold">{{ auth.user.username.charAt(0).toUpperCase() }}</span>
          </router-link>
          <button
            @click="handleLogout"
            class="px-3 py-2 rounded-lg text-sm font-medium text-foreground/70 hover:bg-muted flex items-center gap-1.5 transition-colors"
          >
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            Logout
          </button>
        </template>
        <router-link
          v-else
          to="/login"
          class="px-3 py-2 rounded-lg text-sm font-medium text-foreground/70 hover:bg-muted flex items-center gap-1.5 transition-colors"
        >
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
          </svg>
          Login
        </router-link>
      </div>

      <!-- Mobile toggle -->
      <button
        class="md:hidden p-2 rounded-lg hover:bg-muted"
        @click="open = !open"
      >
        <svg v-if="open" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
        <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>
    </div>

    <!-- Mobile menu -->
    <div
      v-if="open"
      class="md:hidden border-t border-border bg-card animate-fade-in"
    >
      <!-- Public links -->
      <router-link
        v-for="link in publicLinks"
        :key="link.to"
        :to="link.to"
        @click="open = false"
        :class="[
          'block px-6 py-3 text-sm font-medium transition-colors',
          route.path === link.to
            ? 'bg-primary/10 text-primary'
            : 'text-foreground/70 hover:bg-muted'
        ]"
      >
        {{ link.label }}
      </router-link>

      <!-- Admin section -->
      <template v-if="adminLinks.length > 0">
        <div class="border-t border-border my-1" />
        <div class="px-6 py-2 text-xs font-medium text-foreground/60 flex items-center gap-1">
          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          Admin Panel
        </div>
        <router-link
          v-for="link in adminLinks"
          :key="link.to"
          :to="link.to"
          @click="open = false"
          :class="[
            'block px-6 py-3 text-sm font-medium transition-colors flex items-center gap-2',
            route.path === link.to
              ? 'bg-primary/10 text-primary'
              : 'text-foreground/70 hover:bg-muted'
          ]"
        >
          <svg v-if="link.icon === 'users'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 8.048M12 4.354a4 4 0 110 8.048M12 4.354V2m2.879 15.854a4 4 0 11-5.758 0M15.879 17.904a4 4 0 11-5.758 0" />
          </svg>
          <svg v-else-if="link.icon === 'film'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 4v16m10-16v16m-10-4h10M7 8h10m0 8H7" />
          </svg>
          <svg v-else-if="link.icon === 'building'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5.581m0 0H9m5.581 0a2 2 0 100-4 2 2 0 000 4z" />
          </svg>
          {{ link.label }}
        </router-link>
      </template>

      <!-- Auth section -->
      <div class="border-t border-border my-1" />
      <template v-if="auth.isAuthenticated && auth.user">
        <router-link
          :to="{ name: 'profile' }"
          @click="open = false"
          class="block px-6 py-3 text-sm font-medium text-foreground/70 hover:bg-muted flex items-center gap-2"
        >
          <span class="text-xs font-bold">👤</span> {{ auth.user.username }}
        </router-link>
        <button
          @click="handleLogout"
          class="block w-full text-left px-6 py-3 text-sm font-medium text-foreground/70 hover:bg-muted flex items-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          Logout
        </button>
      </template>
      <router-link
        v-else
        to="/login"
        @click="open = false"
        class="block px-6 py-3 text-sm font-medium text-foreground/70 hover:bg-muted flex items-center gap-2"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
        </svg>
        เข้าสู่ระบบ
      </router-link>
    </div>
  </nav>
</template>

<style scoped>
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 0.3s ease-out;
}
</style>
