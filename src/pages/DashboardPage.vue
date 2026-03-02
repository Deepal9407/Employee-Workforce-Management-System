<template>
  <q-page class="q-pa-md q-pa-md-xl bg-grey-2">
    <!-- Header Area -->
    <div class="row items-center justify-between q-mb-lg">
      <div>
        <h1 class="text-h4 text-weight-bold text-dark q-mt-none q-mb-xs">Dashboard Overview</h1>
        <p class="text-grey-7 q-mb-none">Welcome back! Here's what's happening today.</p>
      </div>
      <div>
        <q-btn
          color="primary"
          icon="refresh"
          label="Refresh Data"
          no-caps
          unelevated
          class="shadow-2"
          @click="fetchDashboardData"
          :loading="loading"
        />
      </div>
    </div>

    <!-- Top Summary Cards -->
    <div class="row q-col-gutter-md q-mb-lg">
      <div class="col-12 col-sm-6 col-md-3">
        <q-card
          class="dashboard-stats-card no-shadow bg-white q-pa-md"
          style="border-radius: 12px; border: 1px solid #e2e8f0"
        >
          <div class="row items-center no-wrap">
            <q-avatar color="blue-1" text-color="primary" icon="group" size="lg" class="q-mr-md" />
            <div>
              <div class="text-grey-7 text-caption text-weight-medium text-uppercase">
                Total Employees
              </div>
              <div class="text-dark text-h5 text-weight-bold">{{ stats.totalEmployees }}</div>
            </div>
          </div>
        </q-card>
      </div>

      <div class="col-12 col-sm-6 col-md-3">
        <q-card
          class="dashboard-stats-card no-shadow bg-white q-pa-md"
          style="border-radius: 12px; border: 1px solid #e2e8f0"
        >
          <div class="row items-center no-wrap">
            <q-avatar
              color="green-1"
              text-color="positive"
              icon="how_to_reg"
              size="lg"
              class="q-mr-md"
            />
            <div>
              <div class="text-grey-7 text-caption text-weight-medium text-uppercase">
                Present Today
              </div>
              <div class="text-dark text-h5 text-weight-bold">{{ stats.presentToday }}</div>
            </div>
          </div>
        </q-card>
      </div>

      <div class="col-12 col-sm-6 col-md-3">
        <q-card
          class="dashboard-stats-card no-shadow bg-white q-pa-md"
          style="border-radius: 12px; border: 1px solid #e2e8f0"
        >
          <div class="row items-center no-wrap">
            <q-avatar
              color="orange-1"
              text-color="warning"
              icon="directions_run"
              size="lg"
              class="q-mr-md"
            />
            <div>
              <div class="text-grey-7 text-caption text-weight-medium text-uppercase">
                Late Arrivals
              </div>
              <div class="text-dark text-h5 text-weight-bold">{{ stats.lateArrivals }}</div>
            </div>
          </div>
        </q-card>
      </div>

      <div class="col-12 col-sm-6 col-md-3">
        <q-card
          class="dashboard-stats-card no-shadow bg-white q-pa-md"
          style="border-radius: 12px; border: 1px solid #e2e8f0"
        >
          <div class="row items-center no-wrap">
            <q-avatar
              color="red-1"
              text-color="negative"
              icon="person_off"
              size="lg"
              class="q-mr-md"
            />
            <div>
              <div class="text-grey-7 text-caption text-weight-medium text-uppercase">
                Absent / On Leave
              </div>
              <div class="text-dark text-h5 text-weight-bold">{{ stats.absentToday }}</div>
            </div>
          </div>
        </q-card>
      </div>
    </div>

    <!-- Visualizations (Charts) -->
    <div class="row q-col-gutter-lg q-mb-lg">
      <div class="col-12 col-md-8">
        <q-card
          class="no-shadow q-pa-md h-full"
          style="border-radius: 12px; border: 1px solid #e2e8f0"
        >
          <div class="text-h6 text-weight-bold text-dark q-mb-md">Leave Trends (Monthly)</div>
          <vue-apex-charts
            type="area"
            height="300"
            :options="leaveTrendOptions"
            :series="leaveTrendSeries"
          ></vue-apex-charts>
        </q-card>
      </div>

      <div class="col-12 col-md-4">
        <q-card
          class="no-shadow q-pa-md h-full"
          style="border-radius: 12px; border: 1px solid #e2e8f0"
        >
          <div class="text-h6 text-weight-bold text-dark q-mb-md">Workforce Distribution</div>
          <vue-apex-charts
            type="donut"
            height="320"
            :options="distributionOptions"
            :series="distributionSeries"
          ></vue-apex-charts>
        </q-card>
      </div>
    </div>

    <!-- Tables & Feeds -->
    <div class="row q-col-gutter-lg">
      <!-- Recent Activity Feed -->
      <div class="col-12 col-md-6 col-lg-4">
        <q-card
          class="no-shadow q-pa-md h-full"
          style="border-radius: 12px; border: 1px solid #e2e8f0"
        >
          <div class="row items-center justify-between q-mb-md">
            <div class="text-h6 text-weight-bold text-dark">Activity Feed</div>
            <q-btn flat dense icon="more_horiz" color="grey-7" />
          </div>

          <q-list separator>
            <q-item v-for="(activity, index) in activities" :key="index" class="q-py-md q-px-none">
              <q-item-section avatar top>
                <q-avatar
                  :color="activity.color"
                  text-color="white"
                  :icon="activity.icon"
                  size="md"
                />
              </q-item-section>
              <q-item-section>
                <q-item-label class="text-weight-bold">{{ activity.title }}</q-item-label>
                <q-item-label caption>{{ activity.details }}</q-item-label>
              </q-item-section>
              <q-item-section side top>
                <q-item-label caption>{{ activity.time }}</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
          <div v-if="activities.length === 0" class="text-center text-grey-6 q-py-lg">
            No recent activity
          </div>
        </q-card>
      </div>

      <!-- Live Device Status & Birthdays -->
      <div class="col-12 col-md-6 col-lg-8">
        <q-card
          class="no-shadow q-pa-md q-mb-lg"
          style="border-radius: 12px; border: 1px solid #e2e8f0"
        >
          <div class="text-h6 text-weight-bold text-dark q-mb-md">On Leave & Birthdays Today</div>
          <q-table
            flat
            :rows="todayEvents"
            :columns="eventColumns"
            row-key="id"
            hide-bottom
            :pagination="{ rowsPerPage: 5 }"
          >
            <template v-slot:body-cell-type="props">
              <q-td :props="props">
                <q-chip
                  size="sm"
                  :color="props.row.type === 'Birthday' ? 'pink-2' : 'blue-2'"
                  :text-color="props.row.type === 'Birthday' ? 'pink-9' : 'blue-9'"
                  class="text-weight-bold"
                >
                  {{ props.row.type }}
                </q-chip>
              </q-td>
            </template>
          </q-table>
        </q-card>

        <q-card class="no-shadow q-pa-md" style="border-radius: 12px; border: 1px solid #e2e8f0">
          <div class="text-h6 text-weight-bold text-dark q-mb-sm">Device Status</div>
          <div class="row q-gutter-md">
            <q-chip color="positive" text-color="white" icon="wifi" class="text-subtitle2 shadow-1">
              Main Entrance Scanner (Online)
            </q-chip>
            <q-chip
              color="negative"
              text-color="white"
              icon="wifi_off"
              class="text-subtitle2 shadow-1"
            >
              Backdoor Scanner (Offline)
            </q-chip>
          </div>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import VueApexCharts from 'vue3-apexcharts'
// import { supabase } from 'src/boot/supabase'

const loading = ref(false)

// Placeholder Data for Stats
const stats = ref({
  totalEmployees: 0,
  presentToday: 0,
  lateArrivals: 0,
  absentToday: 0,
})

// Charts Configurations
const leaveTrendSeries = ref([
  {
    name: 'Leaves Taken',
    data: [12, 18, 10, 15, 22, 14, 25, 19, 11],
  },
])

const leaveTrendOptions = ref({
  chart: {
    type: 'area',
    toolbar: { show: false },
    sparkline: { enabled: false },
  },
  colors: ['#0ea5e9'],
  fill: {
    type: 'gradient',
    gradient: { shadeIntensity: 1, opacityFrom: 0.4, opacityTo: 0.0, stops: [0, 90, 100] },
  },
  dataLabels: { enabled: false },
  stroke: { curve: 'smooth', width: 2 },
  xaxis: {
    categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'],
  },
})

const distributionSeries = ref([45, 25, 15, 15])
const distributionOptions = ref({
  labels: ['Engineering', 'HR', 'Sales', 'Finance'],
  chart: { type: 'donut' },
  colors: ['#1e40af', '#0ea5e9', '#f59e0b', '#10b981'],
  plotOptions: {
    pie: { donut: { size: '70%' } },
  },
  dataLabels: { enabled: false },
  legend: { position: 'bottom' },
})

// Feeds & Tables Data
const activities = ref([])

const todayEvents = ref([])

const eventColumns = [
  {
    name: 'name',
    required: true,
    label: 'Employee Name',
    align: 'left',
    field: (row) => row.name,
    sortable: true,
  },
  { name: 'department', align: 'center', label: 'Department', field: 'department', sortable: true },
  { name: 'type', align: 'center', label: 'Event Type', field: 'type', sortable: true },
]

const fetchDashboardData = async () => {
  loading.value = true

  // Here we will do the Supabase API calls later to replace placeholders.
  // For now, load dummy data after artificial delay.
  setTimeout(() => {
    stats.value = {
      totalEmployees: 248,
      presentToday: 215,
      lateArrivals: 18,
      absentToday: 15,
    }

    todayEvents.value = [
      { id: 1, name: 'Saman Kumara', department: 'Engineering', type: 'Birthday' },
      { id: 2, name: 'Nuwan Perera', department: 'HR', type: 'Leave' },
      { id: 3, name: 'Kasun Kalhara', department: 'Sales', type: 'Leave' },
    ]

    activities.value = [
      {
        title: 'Leave Approved',
        details: 'Nuwan Perera (HR) - 2 days',
        time: '10 mins ago',
        color: 'positive',
        icon: 'check_circle',
      },
      {
        title: 'New Hardware Assigned',
        details: 'MacBook Pro to Kasun',
        time: '1 hr ago',
        color: 'accent',
        icon: 'devices',
      },
      {
        title: 'New Employee Added',
        details: 'Saman Silva joined Engineering',
        time: '3 hrs ago',
        color: 'primary',
        icon: 'person_add',
      },
    ]

    loading.value = false
  }, 800)
}

onMounted(() => {
  fetchDashboardData()
})
</script>

<style scoped>
.h-full {
  height: 100%;
}
.dashboard-stats-card {
  transition: transform 0.2s;
}
.dashboard-stats-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
}
</style>
