<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const roleLabels = {
  'normal_user': 'ผู้ใช้ปกติ',
  'content_editor': 'บรรณาธิการ',
  'admin': 'ผู้ดูแลระบบ'
}

onMounted(async () => {
  if (!auth.isAuthenticated) {
    router.push('/login')
  } else if (!auth.user) {
    await auth.getCurrentUser()
  }
})

</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-lavender/20 via-background to-mint/20 p-4">
    <div class="container mx-auto max-w-md mt-20">
      <div class="bg-card rounded-xl border border-border shadow-lg overflow-hidden">
        <!-- Header -->
        <div class="bg-gradient-to-r from-primary/20 to-accent/20 p-6">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 rounded-full bg-primary/20 flex items-center justify-center">
              <svg class="w-6 h-6 text-primary" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z" />
              </svg>
            </div>
            <div>
              <h1 class="text-xl font-bold font-heading text-foreground">{{ auth.user?.username }}</h1>
              <p class="text-sm text-foreground/60">{{ auth.user?.email }}</p>
            </div>
          </div>
        </div>

        <!-- User info -->
        <div class="p-6 space-y-4">
          <!-- Role badge -->
          <div class="flex items-center justify-between p-4 bg-muted/50 rounded-lg border border-border">
            <span class="text-sm font-medium text-foreground/60">Role</span>
            <span class="font-mono text-sm font-semibold">
              {{ roleLabels[auth.user?.role] || auth.user?.role }}
            </span>
          </div>

          <!-- Account status -->
          <div class="flex items-center justify-between p-4 bg-muted/50 rounded-lg border border-border">
            <span class="text-sm font-medium text-foreground/60">Status</span>
            <span v-if="auth.user?.is_active" class="flex items-center gap-2">
              <span class="w-2 h-2 bg-green-500 rounded-full"></span>
              <span class="text-sm font-medium">Active</span>
            </span>
            <span v-else class="flex items-center gap-2">
              <span class="w-2 h-2 bg-gray-500 rounded-full"></span>
              <span class="text-sm font-medium">Inactive</span>
            </span>
          </div>

        </div>

        <!-- Footer -->
        <div class="bg-muted/30 border-t border-border p-4 text-center">
          <router-link
            to="/"
            class="text-sm text-foreground/60 hover:text-primary transition-colors"
          >
            ← Back to Home
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>
