<template>
  <q-page class="q-pa-md q-pa-md-xl bg-grey-2">
    <!-- Header Area -->
    <div class="row items-center justify-between q-mb-lg">
      <div>
        <h1 class="text-h4 text-weight-bold text-dark q-mt-none q-mb-xs">Leave Management</h1>
        <p class="text-grey-7 q-mb-none">Apply for leave, track requests, and manage approvals.</p>
      </div>
    </div>

    <!-- Tabs Menu -->
    <q-card class="no-shadow" style="border-radius: 12px; border: 1px solid #e2e8f0">
      <q-tabs
        v-model="tab"
        dense
        class="text-grey"
        active-color="primary"
        indicator-color="primary"
        align="left"
        narrow-indicator
      >
        <q-tab name="my_leaves" label="My Leaves (Employee)" />
        <q-tab name="approvals" label="Leave Approvals (Manager)" />
      </q-tabs>

      <q-separator />

      <q-tab-panels v-model="tab" animated>
        <!-- My Leaves (Employee View) -->
        <q-tab-panel name="my_leaves">
          <div class="row q-col-gutter-lg">
            <!-- Leave Application Form -->
            <div class="col-12 col-md-5">
              <q-card flat bordered class="rounded-borders q-pa-md bg-white">
                <div class="text-h6 text-weight-bold q-mb-md">Apply for Leave</div>
                <q-form @submit.prevent="submitLeave" class="q-gutter-md">
                  <q-input
                    v-model="leaveForm.epf_no"
                    outlined
                    dense
                    label="Your EPF No. *"
                    :rules="[(val) => !!val || 'Required']"
                  />

                  <q-select
                    v-model="leaveForm.leave_type"
                    :options="['Annual', 'Casual', 'Medical', 'Short Leave', 'Half Day', 'Other']"
                    outlined
                    dense
                    label="Leave Type *"
                    :rules="[(val) => !!val || 'Select Type']"
                  />

                  <div class="row q-col-gutter-sm">
                    <div class="col-6">
                      <q-input
                        v-model="leaveForm.start_date"
                        outlined
                        dense
                        label="Start Date *"
                        type="date"
                        :rules="[(val) => !!val || 'Required']"
                      />
                    </div>
                    <div class="col-6">
                      <q-input
                        v-model="leaveForm.end_date"
                        outlined
                        dense
                        label="End Date *"
                        type="date"
                        :rules="[(val) => !!val || 'Required']"
                      />
                    </div>
                  </div>

                  <q-input
                    v-model.number="leaveForm.days"
                    outlined
                    dense
                    label="Number of Days *"
                    type="number"
                    step="0.5"
                    :rules="[(val) => !!val || 'Required']"
                  />

                  <q-input
                    v-model="leaveForm.reason"
                    outlined
                    dense
                    autogrow
                    label="Reason *"
                    :rules="[(val) => !!val || 'Required']"
                  />

                  <q-btn
                    unelevated
                    color="primary"
                    label="Submit Leave Request"
                    type="submit"
                    class="full-width"
                    :loading="submittingLeave"
                  />
                </q-form>
              </q-card>
            </div>

            <!-- Leave Balances & Notice -->
            <div class="col-12 col-md-7">
              <q-card flat bordered class="rounded-borders bg-white q-mb-md">
                <q-card-section class="bg-blue-1 text-primary">
                  <div class="text-subtitle1 text-weight-bold">
                    <q-icon name="info" class="q-mr-sm" /> Leave Policy Automation
                  </div>
                </q-card-section>
                <q-card-section>
                  <p class="text-body2 text-grey-8">
                    - Leave requests send an automatic email notification to your assigned
                    supervisor/manager.<br />
                    - Late arrivals beyond 15 or 60 minutes automatically deduct short leaves or
                    half-days from your balance via the Python automation system.<br />
                    - Annual leaves are strictly subject to approval and advanced notice.
                  </p>
                </q-card-section>
              </q-card>

              <!-- Optional: Mock Recent Leaves table showing just "Pending/Approved" statuses for this user -->
            </div>
          </div>
        </q-tab-panel>

        <!-- Leave Approvals (Manager View) -->
        <q-tab-panel name="approvals" class="q-pa-none">
          <div class="row items-center justify-between q-pa-md bg-white">
            <q-input
              v-model="filter"
              dense
              outlined
              placeholder="Search requests..."
              class="col-12 col-md-4"
              clearable
            >
              <template v-slot:prepend><q-icon name="search" /></template>
            </q-input>
            <q-btn flat color="primary" icon="refresh" label="Refresh List" @click="fetchLeaves" />
          </div>

          <q-table
            flat
            :rows="allLeaves"
            :columns="leaveColumns"
            row-key="id"
            :filter="filter"
            :loading="loadingLeaves"
            no-data-label="No pending leave requests"
          >
            <!-- Custom Status Chip -->
            <template v-slot:body-cell-status="props">
              <q-td :props="props" class="text-center">
                <q-chip
                  size="sm"
                  :color="
                    props.row.status === 'Approved'
                      ? 'positive'
                      : props.row.status === 'Rejected'
                        ? 'negative'
                        : 'warning'
                  "
                  :text-color="props.row.status === 'Pending' ? 'dark' : 'white'"
                  class="text-weight-bold text-uppercase"
                >
                  {{ props.row.status }}
                </q-chip>
              </q-td>
            </template>

            <!-- Custom Actions -->
            <template v-slot:body-cell-actions="props">
              <q-td :props="props" class="text-center q-gutter-sm">
                <q-btn
                  v-if="props.row.status === 'Pending'"
                  flat
                  round
                  dense
                  color="positive"
                  icon="check_circle"
                  @click="updateLeaveStatus(props.row.id, 'Approved')"
                  ><q-tooltip>Approve</q-tooltip></q-btn
                >
                <q-btn
                  v-if="props.row.status === 'Pending'"
                  flat
                  round
                  dense
                  color="negative"
                  icon="cancel"
                  @click="updateLeaveStatus(props.row.id, 'Rejected')"
                  ><q-tooltip>Reject</q-tooltip></q-btn
                >
                <span v-if="props.row.status !== 'Pending'" class="text-grey text-caption"
                  >Processed</span
                >
              </q-td>
            </template>

            <!-- Employee Detail -->
            <template v-slot:body-cell-epf_no="props">
              <q-td :props="props">
                <div class="text-weight-bold">{{ props.row.epf_no }}</div>
                <div class="text-caption text-grey">
                  {{ props.row.employees?.full_name || 'Unknown' }}
                </div>
                <div class="text-caption text-blue-9">
                  {{ props.row.employees?.department || 'Unknown' }}
                </div>
              </q-td>
            </template>
          </q-table>
        </q-tab-panel>
      </q-tab-panels>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from 'src/boot/axios'
import { useQuasar } from 'quasar'

const $q = useQuasar()

// State
const tab = ref('my_leaves')
const filter = ref('')
const loadingLeaves = ref(false)
const submittingLeave = ref(false)
const allLeaves = ref([])

const leaveForm = ref({
  epf_no: '',
  leave_type: 'Casual',
  start_date: '',
  end_date: '',
  days: 1,
  reason: '',
})

const leaveColumns = [
  { name: 'epf_no', label: 'Employee', align: 'left', field: 'epf_no', sortable: true },
  { name: 'leave_type', label: 'Type', align: 'left', field: 'leave_type', sortable: true },
  { name: 'start_date', label: 'From Date', align: 'left', field: 'start_date', sortable: true },
  { name: 'end_date', label: 'To Date', align: 'left', field: 'end_date', sortable: true },
  { name: 'days', label: 'Days', align: 'center', field: 'days' },
  { name: 'reason', label: 'Reason', align: 'left', field: 'reason' },
  { name: 'status', label: 'Status', align: 'center', field: 'status', sortable: true },
  { name: 'actions', label: 'Review Actions', align: 'center', field: 'actions' },
]

// Methods
const submitLeave = async () => {
  submittingLeave.value = true
  try {
    const response = await api.post('http://localhost:8000/leaves/apply', leaveForm.value)
    if (response.data.success) {
      $q.notify({ type: 'positive', message: 'Leave request submitted to Manager! Email sent.' })
      leaveForm.value = {
        epf_no: leaveForm.value.epf_no,
        leave_type: 'Casual',
        start_date: '',
        end_date: '',
        days: 1,
        reason: '',
      }
    }
  } catch (err) {
    const errMsg = err.response?.data?.detail || 'Failed to submit leave.'
    $q.notify({ type: 'negative', message: errMsg })
  } finally {
    submittingLeave.value = false
  }
}

const fetchLeaves = async () => {
  loadingLeaves.value = true
  try {
    const response = await api.get('http://localhost:8000/leaves')
    if (response.data.success) {
      allLeaves.value = response.data.data
    }
  } catch (err) {
    if (err.message === 'Network Error') {
      $q.notify({ type: 'negative', message: 'Could not connect to Backend on Port 8000.' })
    } else {
      $q.notify({ type: 'negative', message: 'Failed to fetch leaves data' })
    }
  } finally {
    loadingLeaves.value = false
  }
}

const updateLeaveStatus = async (id, status) => {
  try {
    $q.loading.show()
    await api.put(`http://localhost:8000/leaves/${id}/status`, { status })
    $q.notify({ type: 'positive', message: `Leave ${status} successfully. Email dispatched.` })
    fetchLeaves() // Refresh data
  } catch (err) {
    console.error(err)
    $q.notify({ type: 'negative', message: 'Failed to update leave.' })
  } finally {
    $q.loading.hide()
  }
}

onMounted(() => {
  fetchLeaves()
})
</script>

<style scoped>
.rounded-borders {
  border-radius: 8px;
}
</style>
