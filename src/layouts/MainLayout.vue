<template>
  <q-layout view="hHh Lpr fff">
    <!-- Header -->
    <q-header elevated class="bg-white text-dark q-py-xs">
      <q-toolbar>
        <q-btn flat no-caps to="/">
          <q-avatar size="32px" class="q-mr-sm bg-primary text-white">
            <q-icon name="apartment" />
          </q-avatar>
          <div class="text-weight-bold text-h6 text-primary">WorkforcePro</div>
        </q-btn>

        <q-space />

        <div class="gt-xs">
          <template v-if="user">
            <!-- Super Admin specifics -->
            <q-chip
              v-if="userRole === 'super_admin'"
              color="negative"
              text-color="white"
              icon="security"
              size="sm"
              class="q-mr-sm text-weight-bold"
            >
              SUPER ADMIN
            </q-chip>

            <q-btn
              flat
              label="Dashboard"
              to="/dashboard"
              no-caps
              class="text-weight-bold text-dark"
            />
            <q-btn
              flat
              label="Directory"
              to="/employees"
              no-caps
              class="text-weight-medium text-grey-8"
            />
            <q-btn
              flat
              label="Leaves"
              to="/leaves"
              no-caps
              class="text-weight-medium text-grey-8"
            />
            <q-btn
              flat
              label="Attendance"
              to="/attendance"
              no-caps
              class="text-weight-medium text-grey-8"
            />

            <q-btn
              v-if="userRole === 'super_admin'"
              flat
              label="Admin Settings"
              to="/admin/settings"
              no-caps
              class="text-weight-bold text-negative"
            />
          </template>
          <template v-else>
            <q-btn flat label="Features" no-caps class="text-weight-medium text-grey-8" />
            <q-btn flat label="Modules" no-caps class="text-weight-medium text-grey-8" />
            <q-btn flat label="Pricing" no-caps class="text-weight-medium text-grey-8" />
          </template>
        </div>

        <q-space />

        <div class="gt-xs">
          <template v-if="user">
            <q-btn
              unelevated
              color="negative"
              label="Sign Out"
              no-caps
              class="text-weight-bold"
              @click="handleSignOut"
            />
          </template>
          <template v-else>
            <q-btn
              flat
              label="Login"
              to="/login"
              no-caps
              class="text-weight-bold text-primary q-mr-sm"
            />
            <q-btn
              unelevated
              color="primary"
              label="Request Demo"
              to="/register"
              no-caps
              class="text-weight-bold"
            />
          </template>
        </div>

        <q-btn flat round dense icon="menu" class="lt-sm text-grey-8" />
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>

    <!-- Footer -->
    <q-footer class="bg-dark text-white">
      <div class="q-pa-xl">
        <div class="row q-col-gutter-xl">
          <div class="col-12 col-md-4">
            <div class="text-h6 text-weight-bold q-mb-md flex items-center">
              <q-icon name="apartment" size="md" class="q-mr-sm text-secondary" />
              WorkforcePro
            </div>
            <p class="text-grey-4 text-body2">
              Advanced Employee Management & Workforce Tracking System. Streamlining enterprise
              operations worldwide.
            </p>
          </div>

          <div class="col-12 col-sm-6 col-md-2">
            <div class="text-subtitle1 text-weight-bold q-mb-md">Product</div>
            <div class="column q-gutter-y-sm">
              <a
                href="#"
                class="text-grey-4 text-body2 non-selectable"
                style="text-decoration: none"
                >Features</a
              >
              <a
                href="#"
                class="text-grey-4 text-body2 non-selectable"
                style="text-decoration: none"
                >Pricing</a
              >
              <a
                href="#"
                class="text-grey-4 text-body2 non-selectable"
                style="text-decoration: none"
                >Security</a
              >
              <a
                href="#"
                class="text-grey-4 text-body2 non-selectable"
                style="text-decoration: none"
                >Updates</a
              >
            </div>
          </div>

          <div class="col-12 col-sm-6 col-md-2">
            <div class="text-subtitle1 text-weight-bold q-mb-md">Company</div>
            <div class="column q-gutter-y-sm">
              <a
                href="#"
                class="text-grey-4 text-body2 non-selectable"
                style="text-decoration: none"
                >About Us</a
              >
              <a
                href="#"
                class="text-grey-4 text-body2 non-selectable"
                style="text-decoration: none"
                >Careers</a
              >
              <a
                href="#"
                class="text-grey-4 text-body2 non-selectable"
                style="text-decoration: none"
                >Contact</a
              >
              <a
                href="#"
                class="text-grey-4 text-body2 non-selectable"
                style="text-decoration: none"
                >Partners</a
              >
            </div>
          </div>

          <div class="col-12 col-md-4">
            <div class="text-subtitle1 text-weight-bold q-mb-md">Subscribe to our Newsletter</div>
            <p class="text-grey-4 text-body2 q-mb-md">
              Stay updated with the latest in HR tech and workforce management.
            </p>
            <div class="row no-wrap">
              <q-input outlined dense bg-color="white" placeholder="Enter your email" class="col" />
              <q-btn unelevated color="secondary" label="Subscribe" class="q-ml-sm" no-caps />
            </div>
          </div>
        </div>

        <q-separator color="grey-8" class="q-my-lg" />

        <div class="row items-center justify-between text-grey-5 text-body2">
          <div>
            <div>&copy; 2026 WorkforcePro Systems. All rights reserved.</div>
            <div class="q-mt-xs">
              Powered by <span class="text-weight-bold text-white">DJ BOTHUB Lanka (Pvt) Ltd</span>
            </div>
          </div>
          <div class="row q-gutter-md">
            <q-icon name="fab fa-twitter" size="sm" class="cursor-pointer hover-text-white" />
            <q-icon name="fab fa-linkedin" size="sm" class="cursor-pointer hover-text-white" />
            <q-icon name="fab fa-github" size="sm" class="cursor-pointer hover-text-white" />
          </div>
        </div>
      </div>
    </q-footer>
  </q-layout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { supabase } from 'src/boot/supabase'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'

const router = useRouter()
const $q = useQuasar()
const user = ref(null)
const userRole = ref('')

const fetchRole = async (userId) => {
  const { data, error } = await supabase
    .from('user_roles')
    .select('role')
    .eq('user_id', userId)
    .single()
  console.log('Role Fetch Data:', data, 'Error:', error)
  if (data) {
    userRole.value = data.role
  } else {
    userRole.value = 'employee'
  }
}

onMounted(() => {
  // Get initial session
  supabase.auth.getSession().then(({ data: { session } }) => {
    user.value = session?.user || null
    if (user.value) fetchRole(user.value.id)
  })

  // Listen for auth changes
  supabase.auth.onAuthStateChange((_event, session) => {
    user.value = session?.user || null
    if (user.value) fetchRole(user.value.id)
    else userRole.value = ''
  })
})

const handleSignOut = async () => {
  const { error } = await supabase.auth.signOut()
  if (error) {
    $q.notify({ type: 'negative', message: 'Error signing out' })
  } else {
    $q.notify({ type: 'positive', message: 'Signed out successfully' })
    router.push('/login')
  }
}
</script>

<style lang="scss">
.hover-text-white {
  transition: color 0.3s;
  &:hover {
    color: white;
  }
}
</style>
