<template>
  <q-page class="bg-grey-1 flex flex-center">
    <!-- Main Card -->
    <q-card
      class="q-ma-md shadow-10"
      style="width: 1000px; max-width: 95vw; border-radius: 12px; overflow: hidden"
    >
      <div class="row">
        <!-- Left Column: Branding / Marketing -->
        <div
          class="col-12 col-md-5 bg-primary text-white flex flex-center q-pa-xl relative-position"
          v-if="$q.screen.gt.sm"
        >
          <!-- Background decoration -->
          <div class="absolute-top-left q-pa-md">
            <q-avatar color="white" text-color="primary" icon="dashboard_customize" size="md" />
            <span class="text-weight-bold q-ml-sm text-subtitle1">WorkforcePro</span>
          </div>

          <div class="text-center z-top">
            <h4 class="text-weight-bolder q-mb-md" style="line-height: 1.2">Welcome Back</h4>
            <p class="text-blue-grey-2 text-body1" style="line-height: 1.6">
              Sign in to manage your workforce, review pending leaves, and track real-time
              analytics.
            </p>
          </div>

          <!-- Decorative overlay graphic -->
          <div class="absolute-bottom-right" style="opacity: 0.1">
            <q-icon name="group" size="200px" style="transform: translate(20%, 20%)" />
          </div>
        </div>

        <!-- Right Column: Login Form -->
        <div class="col-12 col-md-7 q-pa-lg q-pa-md-xl bg-white">
          <div class="q-mb-xl text-center text-md-left">
            <div class="q-mb-md hide-on-desktop" v-if="$q.screen.lt.md">
              <q-avatar color="primary" text-color="white" icon="dashboard_customize" size="md" />
              <span class="text-weight-bold q-ml-sm text-primary text-h6">WorkforcePro</span>
            </div>
            <h2 class="text-h4 text-weight-bolder text-dark q-mt-none q-mb-sm">Sign In</h2>
            <p class="text-grey-7">Please enter your credentials to continue.</p>
          </div>

          <q-form @submit.prevent="handleLogin" class="q-gutter-md">
            <div>
              <div class="text-weight-medium text-dark q-mb-xs">Email Address</div>
              <q-input
                v-model="email"
                outlined
                dense
                type="email"
                placeholder="you@company.com"
                lazy-rules
                :rules="[
                  (val) => !!val || 'Email is required',
                  (val) => /.+@.+\..+/.test(val) || 'Enter a valid email',
                ]"
                class="q-mb-sm"
              >
                <template v-slot:prepend>
                  <q-icon name="email" color="grey-6" size="xs" />
                </template>
              </q-input>
            </div>

            <div>
              <div class="row items-center justify-between q-mb-xs">
                <div class="text-weight-medium text-dark">Password</div>
                <q-btn
                  flat
                  no-caps
                  color="primary"
                  label="Forgot password?"
                  size="sm"
                  class="q-px-none hide-underline hover-text-secondary"
                />
              </div>
              <q-input
                v-model="password"
                outlined
                dense
                :type="isPwd ? 'password' : 'text'"
                placeholder="••••••••"
                lazy-rules
                :rules="[(val) => !!val || 'Password is required']"
              >
                <template v-slot:prepend>
                  <q-icon name="lock" color="grey-6" size="xs" />
                </template>
                <template v-slot:append>
                  <q-icon
                    :name="isPwd ? 'visibility_off' : 'visibility'"
                    class="cursor-pointer"
                    @click="isPwd = !isPwd"
                    color="grey-6"
                    size="xs"
                  />
                </template>
              </q-input>
            </div>

            <div class="q-mt-md">
              <q-checkbox
                v-model="rememberMe"
                label="Remember me"
                color="primary"
                size="sm"
                class="text-grey-8"
              />
            </div>

            <div class="q-mt-xl">
              <q-btn
                unelevated
                color="secondary"
                size="lg"
                class="full-width text-weight-bold shadow-2"
                label="Sign In"
                type="submit"
                :loading="loading"
                style="border-radius: 8px"
              />
            </div>
          </q-form>

          <div class="text-center q-mt-lg text-grey-8">
            Don't have an account?
            <router-link
              to="/register"
              class="text-primary text-weight-bold"
              style="text-decoration: none"
            >
              Create one now
            </router-link>
          </div>
        </div>
      </div>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref } from 'vue'
import { supabase } from 'src/boot/supabase'
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router'

const $q = useQuasar()
const router = useRouter()

const email = ref('')
const password = ref('')
const isPwd = ref(true)
const rememberMe = ref(false)
const loading = ref(false)

const handleLogin = async () => {
  loading.value = true

  try {
    const { error } = await supabase.auth.signInWithPassword({
      email: email.value,
      password: password.value,
    })

    if (error) throw error

    $q.notify({
      type: 'positive',
      message: 'Successfully logged in!',
      position: 'top-right',
    })

    // Redirect to dashboard (for now we can redirect back to home or a protected route)
    router.push('/')
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: error.message || 'Login failed',
      position: 'top-right',
    })
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.hover-text-secondary:hover {
  color: var(--q-secondary) !important;
}
</style>
