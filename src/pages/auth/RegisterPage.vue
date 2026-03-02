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
          class="col-12 col-md-5 bg-secondary text-white flex flex-center q-pa-xl relative-position"
          v-if="$q.screen.gt.sm"
        >
          <!-- Background decoration -->
          <div class="absolute-top-left q-pa-md">
            <q-avatar color="white" text-color="secondary" icon="dashboard_customize" size="md" />
            <span class="text-weight-bold q-ml-sm text-subtitle1">WorkforcePro</span>
          </div>

          <div class="text-center z-top">
            <h4 class="text-weight-bolder q-mb-md" style="line-height: 1.2">Join Enterprise</h4>
            <p class="text-light-blue-1 text-body1" style="line-height: 1.6">
              Sign up today and get 14 days of full access to your own private workforce management
              tenant.
            </p>
          </div>

          <!-- Decorative overlay graphic -->
          <div class="absolute-bottom-right" style="opacity: 0.1">
            <q-icon name="apartment" size="200px" style="transform: translate(20%, 20%)" />
          </div>
        </div>

        <!-- Right Column: Register Form -->
        <div class="col-12 col-md-7 q-pa-lg q-pa-md-xl bg-white">
          <div class="q-mb-xl text-center text-md-left">
            <div class="q-mb-md hide-on-desktop" v-if="$q.screen.lt.md">
              <q-avatar color="secondary" text-color="white" icon="dashboard_customize" size="md" />
              <span class="text-weight-bold q-ml-sm text-secondary text-h6">WorkforcePro</span>
            </div>
            <h2 class="text-h4 text-weight-bolder text-dark q-mt-none q-mb-sm">Create Account</h2>
            <p class="text-grey-7">Set up a new workspace for your organization.</p>
          </div>

          <q-form @submit.prevent="handleRegister" class="q-gutter-md">
            <div class="row q-col-gutter-md">
              <div class="col-12 col-sm-6">
                <div class="text-weight-medium text-dark q-mb-xs">First Name</div>
                <q-input
                  v-model="firstName"
                  outlined
                  dense
                  placeholder="John"
                  lazy-rules
                  :rules="[(val) => !!val || 'First name is required']"
                />
              </div>
              <div class="col-12 col-sm-6">
                <div class="text-weight-medium text-dark q-mb-xs">Last Name</div>
                <q-input
                  v-model="lastName"
                  outlined
                  dense
                  placeholder="Doe"
                  lazy-rules
                  :rules="[(val) => !!val || 'Last name is required']"
                />
              </div>
            </div>

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
              <div class="text-weight-medium text-dark q-mb-xs">Password</div>
              <q-input
                v-model="password"
                outlined
                dense
                :type="isPwd ? 'password' : 'text'"
                placeholder="••••••••"
                lazy-rules
                :rules="[(val) => (val && val.length >= 6) || 'Minimum 6 characters required']"
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

            <div class="q-mt-sm">
              <q-checkbox v-model="termsAgreed" color="primary" size="sm" class="text-grey-8">
                I agree to the
                <span class="text-weight-bold text-primary cursor-pointer">Terms of Service</span>
                and
                <span class="text-weight-bold text-primary cursor-pointer">Privacy Policy</span>.
              </q-checkbox>
            </div>

            <div class="q-mt-xl">
              <q-btn
                unelevated
                color="primary"
                size="lg"
                class="full-width text-weight-bold shadow-3"
                label="Sign Up"
                type="submit"
                :loading="loading"
                :disable="!termsAgreed"
                style="border-radius: 8px"
              />
            </div>
          </q-form>

          <div class="text-center q-mt-lg text-grey-8">
            Already have an account?
            <router-link
              to="/login"
              class="text-secondary text-weight-bold"
              style="text-decoration: none"
            >
              Sign in Instead
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

const firstName = ref('')
const lastName = ref('')
const email = ref('')
const password = ref('')
const isPwd = ref(true)
const termsAgreed = ref(false)
const loading = ref(false)

const handleRegister = async () => {
  if (!termsAgreed.value) {
    $q.notify({ type: 'warning', message: 'You must agree to the terms to proceed.' })
    return
  }

  loading.value = true

  try {
    const { error } = await supabase.auth.signUp({
      email: email.value,
      password: password.value,
      options: {
        data: {
          first_name: firstName.value,
          last_name: lastName.value,
        },
      },
    })

    if (error) throw error

    $q.notify({
      type: 'positive',
      message: 'Registration successful! Check your email to verify your account.',
      position: 'top-right',
    })

    // Auto redirect to login or dashboard depending on setup
    router.push('/login')
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: error.message || 'Registration failed',
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
