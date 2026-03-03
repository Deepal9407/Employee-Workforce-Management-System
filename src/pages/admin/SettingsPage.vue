<template>
  <q-page class="q-pa-md q-pa-md-xl bg-grey-2">
    <!-- Header -->
    <div class="row items-center justify-between q-mb-lg">
      <div>
        <h1 class="text-h4 text-weight-bold text-dark q-mt-none q-mb-xs">Admin Settings</h1>
        <p class="text-grey-7 q-mb-none">Manage system configurations, users, and roles.</p>
      </div>
    </div>

    <div class="row q-col-gutter-lg">
      <div class="col-12 col-md-3">
        <!-- Vertical Tabs -->
        <q-card flat bordered class="rounded-borders no-shadow bg-white">
          <q-tabs
            v-model="tab"
            vertical
            class="text-teal"
            active-color="negative"
            active-bg-color="red-1"
            indicator-color="negative"
          >
            <q-tab
              name="users"
              icon="manage_accounts"
              label="User Roles"
              class="q-py-md text-weight-bold"
            />
            <q-tab
              name="system"
              icon="tune"
              label="System Preferences"
              class="q-py-md text-weight-bold"
            />
            <q-tab
              name="logs"
              icon="history"
              label="Audit Logs"
              class="q-py-md text-weight-bold"
              disable
            />
          </q-tabs>
        </q-card>
      </div>

      <div class="col-12 col-md-9">
        <q-tab-panels
          v-model="tab"
          animated
          swipeable
          vertical
          transition-prev="jump-up"
          transition-next="jump-up"
          class="bg-transparent"
        >
          <!-- User Roles Panel -->
          <q-tab-panel name="users" class="q-pa-none">
            <q-card flat bordered class="rounded-borders bg-white shadow-1">
              <q-card-section>
                <div class="text-h6 text-weight-bold">System Users & Access Control</div>
                <div class="text-caption text-grey q-mb-md">
                  Manage who has access to the web dashboard and assign administrative roles.
                </div>

                <q-table
                  flat
                  :rows="systemUsers"
                  :columns="columns"
                  row-key="user_id"
                  :loading="loadingUsers"
                >
                  <template v-slot:body-cell-role="props">
                    <q-td :props="props">
                      <q-chip
                        v-if="props.row.role === 'super_admin'"
                        color="negative"
                        text-color="white"
                        size="sm"
                        class="text-weight-bold"
                        icon="security"
                      >
                        Super Admin
                      </q-chip>
                      <q-chip
                        v-else
                        color="grey-3"
                        text-color="dark"
                        size="sm"
                        class="text-weight-bold"
                        icon="person"
                      >
                        Employee
                      </q-chip>
                    </q-td>
                  </template>

                  <template v-slot:body-cell-actions="props">
                    <q-td :props="props">
                      <q-btn
                        flat
                        dense
                        icon="edit"
                        color="primary"
                        @click="editUserRole(props.row)"
                      />
                    </q-td>
                  </template>
                </q-table>
              </q-card-section>
            </q-card>
          </q-tab-panel>

          <!-- System Preferences Panel -->
          <q-tab-panel name="system" class="q-pa-none">
            <q-card flat bordered class="rounded-borders bg-white shadow-1">
              <q-card-section>
                <div class="text-h6 text-weight-bold">Global System Rules</div>
                <div class="text-caption text-grey q-mb-lg">
                  Configure defaults for payroll, leaves, and attendance thresholds.
                </div>

                <div class="row q-col-gutter-lg">
                  <div class="col-12 col-md-6">
                    <q-input
                      outlined
                      dense
                      label="Standard Shift Start"
                      v-model="settings.shiftStart"
                      type="time"
                      hint="Used for late marking"
                    />
                  </div>
                  <div class="col-12 col-md-6">
                    <q-input
                      outlined
                      dense
                      label="Standard Shift End"
                      v-model="settings.shiftEnd"
                      type="time"
                      hint="Used for OT calculation"
                    />
                  </div>
                  <div class="col-12 col-md-6">
                    <q-input
                      outlined
                      dense
                      label="Short Leave Late Tolerance (Mins)"
                      v-model.number="settings.lateTolerance"
                      type="number"
                      hint="Grace period before deduction"
                    />
                  </div>
                </div>

                <div class="q-mt-xl text-right">
                  <q-btn color="primary" label="Save Settings" unelevated :disable="true" />
                </div>
              </q-card-section>
            </q-card>
          </q-tab-panel>
        </q-tab-panels>
      </div>
    </div>

    <!-- Edit Role Dialog -->
    <q-dialog v-model="showEditDialog">
      <q-card style="min-width: 350px">
        <q-card-section class="bg-primary text-white">
          <div class="text-h6">Edit User Role</div>
        </q-card-section>

        <q-card-section class="q-pt-md">
          <div class="text-subtitle1 text-weight-bold q-mb-xs">{{ selectedUser?.email }}</div>
          <p class="text-grey caption">
            Caution: Granting Super Admin provides full access to data and settings.
          </p>
          <q-select
            v-model="newRole"
            :options="['employee', 'super_admin']"
            outlined
            dense
            label="Assigned Role"
          />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" v-close-popup />
          <q-btn
            flat
            label="Apply Changes"
            color="negative"
            @click="updateRole"
            :loading="savingRole"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { supabase } from 'src/boot/supabase'
import { useQuasar } from 'quasar'

const $q = useQuasar()

// State
const tab = ref('users')
const systemUsers = ref([])
const loadingUsers = ref(false)

const settings = ref({
  shiftStart: '08:00',
  shiftEnd: '17:00',
  lateTolerance: 15,
})

// Edit Role mapping
const showEditDialog = ref(false)
const selectedUser = ref(null)
const newRole = ref('')
const savingRole = ref(false)

const columns = [
  { name: 'email', label: 'Email Address', align: 'left', field: 'email', sortable: true },
  { name: 'role', label: 'Access Level', align: 'left', field: 'role', sortable: true },
  {
    name: 'created_at',
    label: 'Joined On',
    align: 'left',
    field: (val) => new Date(val.created_at).toLocaleDateString(),
    sortable: true,
  },
  { name: 'actions', label: 'Manage', align: 'center' },
]

const loadUsers = async () => {
  loadingUsers.value = true
  const { data, error } = await supabase
    .from('user_roles')
    .select('*')
    .order('created_at', { ascending: false })

  if (error) {
    if (error.code === '42501') {
      $q.notify({ type: 'negative', message: 'You do not have permission to view users.' })
    } else {
      console.error(error)
      $q.notify({ type: 'negative', message: 'Failed to fetch user roles.' })
    }
  } else {
    systemUsers.value = data || []
  }
  loadingUsers.value = false
}

const editUserRole = (user) => {
  selectedUser.value = user
  newRole.value = user.role
  showEditDialog.value = true
}

const updateRole = async () => {
  savingRole.value = true
  const { error } = await supabase
    .from('user_roles')
    .update({ role: newRole.value })
    .eq('user_id', selectedUser.value.user_id)

  if (error) {
    console.error(error)
    $q.notify({ type: 'negative', message: 'Failed to update user role.' })
  } else {
    $q.notify({ type: 'positive', message: 'User role updated successfully!' })
    showEditDialog.value = false
    loadUsers()
  }
  savingRole.value = false
}

onMounted(() => {
  loadUsers()
})
</script>

<style scoped>
.rounded-borders {
  border-radius: 12px;
}
</style>
