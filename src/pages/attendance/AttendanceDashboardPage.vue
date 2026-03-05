<template>
  <q-page class="q-pa-md q-pa-md-xl bg-grey-2">
    <!-- Header -->
    <div class="row items-center justify-between q-mb-lg">
      <div>
        <h1 class="text-h4 text-weight-bold text-dark q-mt-none q-mb-xs">Attendance Dashboard</h1>
        <p class="text-grey-7 q-mb-none">
          Track daily attendance, punctuality, and manual entries.
        </p>
      </div>
      <div>
        <q-btn
          color="primary"
          icon="add"
          label="Manual Punch"
          @click="showManualPunch = true"
          unelevated
        />
      </div>
    </div>

    <!-- Quick Stats -->
    <div class="row q-col-gutter-md q-mb-lg" v-if="stats">
      <div class="col-12 col-sm-6 col-md-3">
        <q-card flat bordered class="rounded-borders bg-white">
          <q-card-section>
            <div class="text-overline text-grey-6">TOTAL EMPLOYEES</div>
            <div class="text-h4 text-weight-bold text-dark">{{ stats.total }}</div>
          </q-card-section>
        </q-card>
      </div>
      <div class="col-12 col-sm-6 col-md-3">
        <q-card flat bordered class="rounded-borders bg-white">
          <q-card-section>
            <div class="text-overline text-grey-6">PRESENT TODAY</div>
            <div class="text-h4 text-weight-bold text-positive">{{ stats.present }}</div>
            <div class="text-caption text-grey">Including {{ stats.late }} Late</div>
          </q-card-section>
        </q-card>
      </div>
      <div class="col-12 col-sm-6 col-md-3">
        <q-card flat bordered class="rounded-borders bg-white">
          <q-card-section>
            <div class="text-overline text-grey-6">ON LEAVE</div>
            <div class="text-h4 text-weight-bold text-warning">{{ stats.on_leave }}</div>
          </q-card-section>
        </q-card>
      </div>
      <div class="col-12 col-sm-6 col-md-3">
        <q-card flat bordered class="rounded-borders bg-white">
          <q-card-section>
            <div class="text-overline text-grey-6">ABSENT</div>
            <div class="text-h4 text-weight-bold text-negative">{{ stats.absent }}</div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Attendance Live Log -->
    <q-card flat bordered class="rounded-borders bg-white">
      <div class="row items-center justify-between q-pa-md border-bottom">
        <div class="text-h6 text-weight-bold">Today's Attendance Log</div>
        <div class="row q-gutter-sm">
          <q-input
            v-model="filterDate"
            outlined
            dense
            type="date"
            label="Filter Date"
            @update:model-value="fetchAttendance"
          />
          <q-btn flat color="primary" icon="refresh" @click="fetchStatsAndLogs" />
        </div>
      </div>

      <q-table
        flat
        :rows="attendanceRecords"
        :columns="columns"
        row-key="id"
        :loading="loading"
        no-data-label="No attendance records found"
      >
        <template v-slot:body-cell-status="props">
          <q-td :props="props" class="text-center">
            <q-chip
              size="sm"
              :color="getStatusColor(props.row.calculated_status)"
              text-color="white"
              class="text-weight-bold"
            >
              {{ props.row.calculated_status }}
            </q-chip>
          </q-td>
        </template>

        <template v-slot:body-cell-time_format="props">
          <q-td :props="props" class="text-center text-weight-medium">
            <div v-if="props.row.in_time">
              IN: <span class="text-primary">{{ formatTime(props.row.in_time) }}</span>
            </div>
            <div v-if="props.row.out_time">
              OUT: <span class="text-secondary">{{ formatTime(props.row.out_time) }}</span>
            </div>
          </q-td>
        </template>

        <template v-slot:body-cell-employee="props">
          <q-td :props="props">
            <div class="text-weight-bold">{{ props.row.employees?.full_name || 'Unknown' }}</div>
            <div class="text-caption text-grey">{{ props.row.epf_no }}</div>
          </q-td>
        </template>

        <template v-slot:body-cell-stats="props">
          <q-td :props="props" class="text-caption text-grey-8">
            <div v-if="props.row.late_minutes > 0" class="text-orange">
              Late: {{ props.row.late_minutes }}m
            </div>
            <div v-if="props.row.early_out_minutes > 0" class="text-orange">
              Early: {{ props.row.early_out_minutes }}m
            </div>
            <div v-if="props.row.ot_hours > 0" class="text-positive text-weight-bold">
              OT: {{ props.row.ot_hours }}h
            </div>
            <div v-if="props.row.working_hours > 0">Worked: {{ props.row.working_hours }}h</div>
          </q-td>
        </template>
      </q-table>
    </q-card>

    <!-- Manual Punch Modal -->
    <q-dialog v-model="showManualPunch">
      <q-card style="min-width: 400px; border-radius: 12px">
        <q-card-section class="bg-primary text-white">
          <div class="text-h6">Manual Attendance Punch</div>
        </q-card-section>

        <q-form @submit.prevent="submitManualPunch">
          <q-card-section class="q-gutter-md q-mt-md">
            <q-input
              v-model="punchForm.epf_no"
              outlined
              autofocus
              label="Employee EPF No *"
              :rules="[(val) => !!val || 'Required']"
            />

            <q-input
              v-model="punchForm.punch_time"
              outlined
              type="datetime-local"
              label="Punch Date & Time *"
              :rules="[(val) => !!val || 'Required']"
            />

            <q-banner rounded class="bg-amber-1 text-amber-9 text-caption">
              <template v-slot:avatar><q-icon name="warning" color="amber-9" /></template>
              Manual punch uses the exact automated logic. Late, early outs, and leave deductions
              will apply automatically based on the time you choose.
            </q-banner>
          </q-card-section>

          <q-card-actions align="right" class="text-primary q-pa-md">
            <q-btn flat label="Cancel" v-close-popup />
            <q-btn
              unelevated
              color="primary"
              label="Punch Time"
              type="submit"
              :loading="punching"
            />
          </q-card-actions>
        </q-form>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from 'src/boot/axios'
import { useQuasar } from 'quasar'

const $q = useQuasar()

const stats = ref(null)
const filterDate = ref(new Date().toISOString().split('T')[0])
const attendanceRecords = ref([])
const loading = ref(false)

const showManualPunch = ref(false)
const punching = ref(false)

// Init datetime to now local
const now = new Date()
now.setMinutes(now.getMinutes() - now.getTimezoneOffset())
const punchForm = ref({
  epf_no: '',
  punch_time: now.toISOString().slice(0, 16),
})

const columns = [
  { name: 'employee', label: 'Employee', align: 'left', sortable: true },
  { name: 'date', label: 'Date', align: 'left', field: 'date', sortable: true },
  { name: 'time_format', label: 'Timings', align: 'center' },
  { name: 'status', label: 'Status', align: 'center', sortable: true },
  { name: 'stats', label: 'Details', align: 'left' },
]

const formatTime = (isoString) => {
  if (!isoString) return ''
  return new Date(isoString).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const getStatusColor = (status) => {
  if (!status) return 'grey'
  if (status.includes('Late')) return 'orange-8'
  if (status.includes('Present')) return 'positive'
  return 'primary'
}

const fetchStatsAndLogs = () => {
  fetchStats()
  fetchAttendance()
}

const fetchStats = async () => {
  try {
    const res = await api.get('/attendance/stats/today')
    if (res.data.success) {
      stats.value = res.data.data
    }
  } catch (err) {
    console.error(err)
  }
}

const fetchAttendance = async () => {
  loading.value = true
  try {
    let url = '/attendance'
    if (filterDate.value) url += `?date=${filterDate.value}`

    const res = await api.get(url)
    if (res.data.success) {
      attendanceRecords.value = res.data.data
    }
  } catch (err) {
    if (err.message === 'Network Error') {
      $q.notify({ type: 'negative', message: 'Could not connect to Backend on Port 8000.' })
    }
  } finally {
    loading.value = false
  }
}

const submitManualPunch = async () => {
  punching.value = true
  try {
    // format as ISO 8601 UTC
    const dt = new Date(punchForm.value.punch_time)

    await api.post('/attendance/manual-punch', {
      epf_no: punchForm.value.epf_no,
      punch_time: dt.toISOString(),
    })

    $q.notify({ type: 'positive', message: 'Manual punch successful!' })
    showManualPunch.value = false
    punchForm.value.epf_no = '' // Reset
    fetchStatsAndLogs() // Refresh views
  } catch (err) {
    const msg = err.response?.data?.detail || 'Failed to submit manual punch.'
    $q.notify({ type: 'negative', message: msg })
  } finally {
    punching.value = false
  }
}

onMounted(() => {
  fetchStatsAndLogs()
})
</script>

<style scoped>
.rounded-borders {
  border-radius: 10px;
}
.border-bottom {
  border-bottom: 1px solid #e2e8f0;
}
</style>
