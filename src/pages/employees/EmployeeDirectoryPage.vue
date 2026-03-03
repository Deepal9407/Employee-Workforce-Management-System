<template>
  <q-page class="q-pa-md q-pa-md-xl bg-grey-2">
    <!-- Header -->
    <div class="row items-center justify-between q-mb-lg">
      <div>
        <h1 class="text-h4 text-weight-bold text-dark q-mt-none q-mb-xs">Employee Directory</h1>
        <p class="text-grey-7 q-mb-none">
          Manage your workforce, view details, and track operations.
        </p>
      </div>
      <div class="row q-gutter-sm">
        <q-btn
          color="white"
          text-color="primary"
          icon="refresh"
          label="Sync"
          unelevated
          class="shadow-2"
          @click="fetchEmployees"
          :loading="loading"
        />
        <q-btn
          color="secondary"
          icon="download"
          label="Export CSV"
          unelevated
          class="shadow-2"
          @click="exportCSV"
        />
        <q-btn
          color="primary"
          icon="add"
          label="Add Employee"
          unelevated
          class="shadow-2"
          @click="openAddDialog"
        />
      </div>
    </div>

    <!-- Data Table -->
    <q-card class="no-shadow" style="border-radius: 12px; border: 1px solid #e2e8f0">
      <div
        class="row items-center justify-between q-pa-md bg-white"
        style="border-bottom: 1px solid #e2e8f0"
      >
        <div class="col-12 col-md-5">
          <q-input
            v-model="filter"
            dense
            outlined
            placeholder="Search by Name, EPF No, or Department..."
            class="full-width"
            clearable
          >
            <template v-slot:prepend><q-icon name="search" color="grey-6" /></template>
          </q-input>
        </div>
      </div>
      <q-table
        flat
        :rows="employees"
        :columns="columns"
        row-key="epf_no"
        :filter="filter"
        :loading="loading"
        loading-label="Synchronizing with Python API..."
        no-data-label="No employees found"
        :pagination="{ rowsPerPage: 10 }"
      >
        <template v-slot:body-cell-status="props">
          <q-td :props="props">
            <q-chip
              size="sm"
              :color="
                props.row.status === 'Active'
                  ? 'positive'
                  : props.row.status === 'Probation'
                    ? 'warning'
                    : 'negative'
              "
              :text-color="
                props.row.status === 'Active'
                  ? 'white'
                  : props.row.status === 'Probation'
                    ? 'dark'
                    : 'white'
              "
              class="text-weight-bold no-border-radius"
            >
              {{ props.row.status }}
            </q-chip>
          </q-td>
        </template>
        <template v-slot:body-cell-actions="props">
          <q-td :props="props" class="q-gutter-sm">
            <q-btn
              flat
              round
              dense
              color="primary"
              icon="visibility"
              @click="viewProfile(props.row)"
              ><q-tooltip>View Profile</q-tooltip></q-btn
            >
            <q-btn flat round dense color="secondary" icon="edit" @click="openEditDialog(props.row)"
              ><q-tooltip>Edit Detail</q-tooltip></q-btn
            >
          </q-td>
        </template>
      </q-table>
    </q-card>

    <!-- Add/Edit Employee Dialog -->
    <q-dialog
      v-model="dialogVisible"
      persistent
      maximized
      transition-show="slide-up"
      transition-hide="slide-down"
    >
      <q-card class="bg-grey-1">
        <q-card-section class="bg-primary text-white row items-center q-pb-md shadow-2">
          <div class="text-h6 text-weight-bold">
            {{ isEdit ? 'Edit Employee Data' : 'Add New Employee' }}
          </div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-card-section class="row justify-center q-pa-lg">
          <q-form
            @submit.prevent="saveEmployee"
            class="q-gutter-md"
            style="max-width: 1000px; width: 100%"
          >
            <q-card flat bordered class="q-mb-md rounded-borders bg-white">
              <q-card-section class="bg-blue-1 text-primary text-subtitle1 text-weight-bold"
                >Basic Information</q-card-section
              >
              <q-card-section class="row q-col-gutter-md">
                <div class="col-12 col-md-6">
                  <q-input
                    v-model="formData.epf_no"
                    outlined
                    dense
                    label="EPF No."
                    :disable="isEdit"
                    hint="Auto-generated if left blank"
                  />
                </div>
                <div class="col-12 col-md-6">
                  <q-input
                    v-model="formData.full_name"
                    outlined
                    dense
                    label="Full Name *"
                    :rules="[(val) => !!val || 'Name is required']"
                  />
                </div>
                <div class="col-12 col-md-6">
                  <q-input
                    v-model="formData.nic_no"
                    outlined
                    dense
                    label="NIC No. *"
                    @update:model-value="extractDetailsFromNIC"
                    :rules="[(val) => !!val || 'NIC is required']"
                  />
                </div>
                <div class="col-12 col-md-3">
                  <q-input
                    v-model="formData.sex"
                    outlined
                    dense
                    label="Sex"
                    readonly
                    hint="Auto-calculated from NIC"
                  />
                </div>
                <div class="col-12 col-md-3">
                  <q-input
                    v-model="formData.birthday"
                    outlined
                    dense
                    label="Birthday"
                    type="date"
                    readonly
                    hint="Auto-calculated from NIC"
                  />
                </div>
                <div class="col-12 col-md-4">
                  <q-input v-model="formData.religion" outlined dense label="Religion" />
                </div>
                <div class="col-12 col-md-4">
                  <q-input v-model="formData.ethnicity" outlined dense label="Ethnicity" />
                </div>
                <div class="col-12 col-md-4">
                  <q-input
                    v-model="formData.educational_qualification"
                    outlined
                    dense
                    label="Educational Qualification"
                  />
                </div>
              </q-card-section>
            </q-card>

            <q-card flat bordered class="q-mb-md rounded-borders bg-white">
              <q-card-section class="bg-blue-1 text-primary text-subtitle1 text-weight-bold"
                >Service Details</q-card-section
              >
              <q-card-section class="row q-col-gutter-md">
                <div class="col-12 col-md-4">
                  <q-input
                    v-model="formData.designation"
                    outlined
                    dense
                    label="Designation *"
                    :rules="[(val) => !!val || 'Required']"
                  />
                </div>
                <div class="col-12 col-md-4">
                  <q-input v-model="formData.category" outlined dense label="Category" />
                </div>
                <div class="col-12 col-md-4">
                  <q-select
                    v-model="formData.department"
                    outlined
                    dense
                    label="Department *"
                    :options="departmentOpts"
                    :rules="[(val) => !!val || 'Required']"
                  />
                </div>

                <div class="col-12 col-md-4">
                  <q-input v-model="formData.line" outlined dense label="Section / Line" />
                </div>
                <div class="col-12 col-md-4">
                  <q-input
                    v-model="formData.joined_date"
                    outlined
                    dense
                    label="Joined Date *"
                    type="date"
                    :rules="[(val) => !!val || 'Required']"
                  />
                </div>
                <div class="col-12 col-md-4">
                  <q-select
                    v-model="formData.status"
                    outlined
                    dense
                    label="Status"
                    :options="statusOpts"
                  />
                </div>
                <div class="col-12">
                  <q-input
                    v-model="formData.previous_employer"
                    outlined
                    dense
                    label="Previous Employer"
                  />
                </div>
              </q-card-section>
            </q-card>

            <q-card flat bordered class="q-mb-md rounded-borders bg-white">
              <q-card-section class="bg-blue-1 text-primary text-subtitle1 text-weight-bold"
                >Salary & Bank Details</q-card-section
              >
              <q-card-section class="row q-col-gutter-md">
                <div class="col-12 col-md-6">
                  <q-input
                    v-model.number="formData.basic_salary"
                    outlined
                    dense
                    label="Basic Salary (LKR)"
                    type="number"
                    prefix="Rs."
                  />
                </div>
                <div class="col-12 col-md-6">
                  <q-input
                    v-model.number="formData.bra"
                    outlined
                    dense
                    label="BRA (LKR)"
                    type="number"
                    prefix="Rs."
                  />
                </div>
                <div class="col-12 col-md-4">
                  <q-input v-model="formData.bank_name" outlined dense label="Bank Name" />
                </div>
                <div class="col-12 col-md-4">
                  <q-input v-model="formData.branch" outlined dense label="Branch" />
                </div>
                <div class="col-12 col-md-4">
                  <q-input v-model="formData.account_no" outlined dense label="Account No." />
                </div>
              </q-card-section>
            </q-card>

            <q-card flat bordered class="q-mb-md rounded-borders bg-white">
              <q-card-section class="bg-blue-1 text-primary text-subtitle1 text-weight-bold"
                >Contact Details</q-card-section
              >
              <q-card-section class="row q-col-gutter-md">
                <div class="col-12">
                  <q-input v-model="formData.address" outlined dense autogrow label="Address" />
                </div>
                <div class="col-12 col-md-6">
                  <q-input v-model="formData.telephone_no" outlined dense label="Telephone No." />
                </div>
                <div class="col-12 col-md-6">
                  <q-input
                    v-model="formData.emergency_contact"
                    outlined
                    dense
                    label="Emergency Contact (Name & No.)"
                  />
                </div>
              </q-card-section>
            </q-card>

            <q-card flat bordered class="q-mb-md rounded-borders bg-white">
              <q-card-section class="bg-blue-1 text-primary text-subtitle1 text-weight-bold"
                >Fingerprint & Documents Checklist</q-card-section
              >
              <q-card-section class="row q-col-gutter-lg">
                <div class="col-12 col-md-6" style="border-right: 1px solid #e0e0e0">
                  <div class="text-subtitle2 q-mb-md">Biometric Configuration</div>
                  <q-input
                    v-model="formData.fingerprint_id"
                    outlined
                    dense
                    label="Biometric Machine ID"
                    class="q-mb-md"
                  />
                  <q-file
                    v-model="dummyFile"
                    outlined
                    dense
                    label="Upload Template (Optional)"
                    clearable
                  >
                    <template v-slot:prepend><q-icon name="attach_file" /></template>
                  </q-file>
                  <div class="text-caption text-grey-6 q-mt-sm">
                    Note: Template raw strings are managed directly from scanner integration.
                  </div>
                </div>
                <div class="col-12 col-md-6">
                  <div class="text-subtitle2 q-mb-md">Provided Documents</div>
                  <div class="row q-col-gutter-sm">
                    <q-checkbox
                      v-model="formData.chk_appForm"
                      label="Application Form"
                      class="col-6"
                    />
                    <q-checkbox v-model="formData.chk_nic" label="NIC Copy" class="col-6" />
                    <q-checkbox
                      v-model="formData.chk_birthCert"
                      label="Birth Certificate"
                      class="col-6"
                    />
                    <q-checkbox v-model="formData.chk_police" label="Police Report" class="col-6" />
                  </div>
                </div>
              </q-card-section>
            </q-card>

            <div class="row justify-end q-mt-md q-mb-xl q-gutter-sm">
              <q-btn flat label="Cancel" color="dark" size="lg" v-close-popup />
              <q-btn
                unelevated
                :label="isEdit ? 'Update Changes' : 'Save Employee'"
                color="primary"
                size="lg"
                type="submit"
                :loading="saving"
                style="width: 200px"
              />
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>

    <!-- Full Profile UI Drawer -->
    <q-dialog v-model="profileVisible" position="right" maximized>
      <q-card class="column full-height" style="width: 500px; max-width: 100vw">
        <q-card-section class="bg-primary text-white row items-center q-pb-none">
          <q-btn flat round dense icon="arrow_back" v-close-popup class="q-mr-sm" />
          <div class="text-h6">Employee Profile</div>
        </q-card-section>

        <q-card-section
          class="bg-primary text-white flex flex-center column q-py-lg"
          v-if="activeProfile"
        >
          <q-avatar
            size="100px"
            color="white"
            text-color="primary"
            class="q-mb-md text-h2 font-weight-bold shadow-3"
          >
            {{ activeProfile.full_name ? activeProfile.full_name.charAt(0) : 'E' }}
          </q-avatar>
          <div class="text-h5 text-weight-bold text-center">{{ activeProfile.full_name }}</div>
          <div class="text-subtitle1 text-blue-grey-2">{{ activeProfile.designation }}</div>
          <q-chip size="sm" color="blue-2" text-color="blue-9" class="q-mt-sm text-weight-bold">{{
            activeProfile.department
          }}</q-chip>
        </q-card-section>

        <q-card-section class="col q-pa-md scroll" v-if="activeProfile">
          <q-list class="rounded-borders">
            <q-expansion-item
              expand-separator
              icon="badge"
              label="Basic Details"
              default-opened
              header-class="text-weight-bold text-primary"
            >
              <q-card
                ><q-card-section>
                  <div class="row q-col-gutter-sm">
                    <div class="col-6">
                      <div class="text-caption text-grey">EPF No</div>
                      <div class="text-body2 text-weight-medium">{{ activeProfile.epf_no }}</div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey">NIC</div>
                      <div class="text-body2 text-weight-medium">{{ activeProfile.nic_no }}</div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey">Birthday</div>
                      <div class="text-body2 text-weight-medium">
                        {{ activeProfile.birthday || 'N/A' }}
                      </div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey">Sex</div>
                      <div class="text-body2 text-weight-medium">
                        {{ activeProfile.sex || 'N/A' }}
                      </div>
                    </div>
                  </div>
                </q-card-section></q-card
              >
            </q-expansion-item>

            <q-expansion-item
              expand-separator
              icon="work"
              label="Service Information"
              header-class="text-weight-bold text-primary"
            >
              <q-card
                ><q-card-section>
                  <div class="row q-col-gutter-sm">
                    <div class="col-6">
                      <div class="text-caption text-grey">Joined Date</div>
                      <div class="text-body2 text-weight-medium">
                        {{ activeProfile.joined_date }}
                      </div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey">Status</div>
                      <div class="text-body2 text-weight-medium">{{ activeProfile.status }}</div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey">Category</div>
                      <div class="text-body2 text-weight-medium">
                        {{ activeProfile.category || '-' }}
                      </div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey">Section / Line</div>
                      <div class="text-body2 text-weight-medium">
                        {{ activeProfile.line || '-' }}
                      </div>
                    </div>
                  </div>
                </q-card-section></q-card
              >
            </q-expansion-item>

            <q-expansion-item
              expand-separator
              icon="account_balance"
              label="Bank Details"
              header-class="text-weight-bold text-primary"
            >
              <q-card
                ><q-card-section>
                  <div class="row q-col-gutter-sm">
                    <div class="col-12">
                      <div class="text-caption text-grey">Basic Salary & BRA</div>
                      <div class="text-body2 text-weight-medium">
                        Rs {{ activeProfile.basic_salary }} / Rs {{ activeProfile.bra }}
                      </div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey">Bank & Branch</div>
                      <div class="text-body2 text-weight-medium">
                        {{ activeProfile.bank_name || '-' }} ({{ activeProfile.branch || '-' }})
                      </div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey">Account No.</div>
                      <div class="text-body2 text-weight-medium">
                        {{ activeProfile.account_no || '-' }}
                      </div>
                    </div>
                  </div>
                </q-card-section></q-card
              >
            </q-expansion-item>

            <q-expansion-item
              expand-separator
              icon="contact_phone"
              label="Contact & Emergency"
              header-class="text-weight-bold text-primary"
            >
              <q-card
                ><q-card-section>
                  <div class="row q-col-gutter-sm">
                    <div class="col-12">
                      <div class="text-caption text-grey">Address</div>
                      <div class="text-body2 text-weight-medium">
                        {{ activeProfile.address || '-' }}
                      </div>
                    </div>
                    <div class="col-12">
                      <div class="text-caption text-grey">Telephone</div>
                      <div class="text-body2 text-weight-medium">
                        {{ activeProfile.telephone_no || '-' }}
                      </div>
                    </div>
                    <div class="col-12">
                      <div class="text-caption text-grey">Emergency Contact</div>
                      <div class="text-body2 text-weight-medium">
                        {{ activeProfile.emergency_contact || '-' }}
                      </div>
                    </div>
                  </div>
                </q-card-section></q-card
              >
            </q-expansion-item>

            <q-expansion-item
              expand-separator
              icon="fingerprint"
              label="Fingerprint & Docs"
              header-class="text-weight-bold text-primary"
            >
              <q-card
                ><q-card-section>
                  <div class="text-caption text-grey">Bio-Metric ID</div>
                  <div class="text-body2 text-weight-medium q-mb-sm">
                    {{ activeProfile.fingerprint_id || 'Not Assigned' }}
                  </div>
                  <div class="text-caption text-grey q-mb-xs">Checklist:</div>
                  <div class="row q-gutter-x-md">
                    <q-chip
                      size="sm"
                      :color="activeProfile.chk_appForm ? 'positive' : 'grey-3'"
                      :text-color="activeProfile.chk_appForm ? 'white' : 'dark'"
                      >App Form</q-chip
                    >
                    <q-chip
                      size="sm"
                      :color="activeProfile.chk_nic ? 'positive' : 'grey-3'"
                      :text-color="activeProfile.chk_nic ? 'white' : 'dark'"
                      >NIC</q-chip
                    >
                    <q-chip
                      size="sm"
                      :color="activeProfile.chk_birthCert ? 'positive' : 'grey-3'"
                      :text-color="activeProfile.chk_birthCert ? 'white' : 'dark'"
                      >Birth Cert</q-chip
                    >
                    <q-chip
                      size="sm"
                      :color="activeProfile.chk_police ? 'positive' : 'grey-3'"
                      :text-color="activeProfile.chk_police ? 'white' : 'dark'"
                      >Police Rpt</q-chip
                    >
                  </div>
                </q-card-section></q-card
              >
            </q-expansion-item>
          </q-list>

          <h3 class="text-subtitle1 text-weight-bold text-dark q-mt-xl q-mb-sm">Quick Actions</h3>
          <div class="row q-gutter-sm q-mb-xl">
            <q-btn
              outline
              color="primary"
              icon="history"
              label="View Attendance"
              class="full-width"
            />
            <q-btn
              outline
              color="secondary"
              icon="date_range"
              label="View Leaves"
              class="full-width"
            />
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from 'src/boot/axios'
import { useQuasar, exportFile } from 'quasar'

const $q = useQuasar()

// State
const employees = ref([])
const loading = ref(false)
const filter = ref('')
const dialogVisible = ref(false)
const profileVisible = ref(false)
const isEdit = ref(false)
const saving = ref(false)
const dummyFile = ref(null)

const activeProfile = ref(null)

const departmentOpts = [
  'Engineering',
  'HR',
  'Finance',
  'Sales',
  'Management',
  'Operations',
  'Kitchen',
  'Reception',
]
const statusOpts = ['Active', 'Probation', 'Resigned']

const formData = ref({
  epf_no: '',
  full_name: '',
  nic_no: '',
  sex: '',
  birthday: '',
  designation: '',
  department: '',
  category: '',
  line: '',
  joined_date: '',
  status: 'Active',
  basic_salary: 0,
  bra: 0,
  bank_name: '',
  branch: '',
  account_no: '',
  address: '',
  telephone_no: '',
  emergency_contact: '',
  fingerprint_id: '',
  fingerprint_template: '',
  chk_appForm: false,
  chk_nic: false,
  chk_birthCert: false,
  chk_police: false,
  educational_qualification: '',
  religion: '',
  ethnicity: '',
  previous_employer: '',
})

const columns = [
  { name: 'epf_no', label: 'EPF No.', align: 'left', field: 'epf_no', sortable: true },
  { name: 'full_name', label: 'Employee Name', align: 'left', field: 'full_name', sortable: true },
  { name: 'nic_no', label: 'NIC', align: 'left', field: 'nic_no', sortable: true },
  { name: 'department', label: 'Department', align: 'center', field: 'department', sortable: true },
  { name: 'designation', label: 'Title', align: 'left', field: 'designation', sortable: true },
  { name: 'status', label: 'Status', align: 'center', field: 'status', sortable: true },
  { name: 'actions', label: 'Actions', align: 'center', field: 'actions' },
]

const extractDetailsFromNIC = (nic) => {
  if (!nic || (nic.length !== 10 && nic.length !== 12)) return

  let year = ''
  let days = 0

  if (nic.length === 10) {
    year = '19' + nic.substring(0, 2)
    days = parseInt(nic.substring(2, 5))
  } else if (nic.length === 12) {
    year = nic.substring(0, 4)
    days = parseInt(nic.substring(4, 7))
  } else {
    return
  }

  // Determine sex
  if (days > 500) {
    formData.value.sex = 'Female'
    days -= 500
  } else {
    formData.value.sex = 'Male'
  }

  // Determine Birthday
  if (days > 0 && days <= 366) {
    let date = new Date(year, 0) // Initialize at Jan 1st of the derived year
    date.setDate(days) // Auto handles leap years nicely in JS if derived year is leap

    // JS dates can be tricky with NIC leap year logic, adjusting for NIC standard which assumes leap year for formula.
    // If it's not a leap year and days > 60 (after Feb 29), we might need to subtract 1 day in strict SL NIC logic.
    const isLeapYear = (year % 4 === 0 && year % 100 !== 0) || year % 400 === 0
    if (!isLeapYear && days > 59) {
      date.setDate(date.getDate() - 1)
    }

    formData.value.birthday = date.toISOString().split('T')[0]
  }
}

// Fetch employees
const fetchEmployees = async () => {
  loading.value = true
  try {
    const response = await api.get('http://localhost:8000/get-employees')
    if (response.data.success) {
      employees.value = response.data.data
    }
  } catch (err) {
    if (err.message === 'Network Error') {
      $q.notify({ type: 'negative', message: 'Could not connect to Python Backend on Port 8000.' })
    } else {
      $q.notify({ type: 'negative', message: 'Failed to fetch directory data' })
    }
  } finally {
    loading.value = false
  }
}

const openAddDialog = () => {
  formData.value = {
    epf_no: '',
    full_name: '',
    nic_no: '',
    sex: '',
    birthday: '',
    designation: '',
    department: '',
    category: '',
    line: '',
    joined_date: new Date().toISOString().split('T')[0],
    status: 'Active',
    basic_salary: 0,
    bra: 0,
    bank_name: '',
    branch: '',
    account_no: '',
    address: '',
    telephone_no: '',
    emergency_contact: '',
    fingerprint_id: '',
    fingerprint_template: '',
    chk_appForm: false,
    chk_nic: false,
    chk_birthCert: false,
    chk_police: false,
    educational_qualification: '',
    religion: '',
    ethnicity: '',
    previous_employer: '',
  }
  isEdit.value = false
  dialogVisible.value = true
}

const openEditDialog = (row) => {
  formData.value = { ...row }
  isEdit.value = true
  dialogVisible.value = true
}

const viewProfile = (row) => {
  activeProfile.value = row
  profileVisible.value = true
}

const saveEmployee = async () => {
  saving.value = true
  try {
    if (isEdit.value) {
      await api.put(
        `http://localhost:8000/update-employee/${formData.value.epf_no}`,
        formData.value,
      )
      $q.notify({ type: 'positive', message: 'Employee updated successfully' })
    } else {
      await api.post('http://localhost:8000/add-employee', formData.value)
      $q.notify({ type: 'positive', message: 'New employee added successfully' })
    }
    dialogVisible.value = false
    fetchEmployees()
  } catch (err) {
    const errMsg = err.response?.data?.detail || 'Failed to save changes.'
    $q.notify({ type: 'negative', message: errMsg })
  } finally {
    saving.value = false
  }
}

function wrapCsvValue(val, formatFn, row) {
  let formatted = formatFn !== void 0 ? formatFn(val, row) : val
  formatted = formatted === void 0 || formatted === null ? '' : String(formatted)
  formatted = formatted.split('"').join('""')
  return `"${formatted}"`
}

const exportCSV = () => {
  // basic csv export based on columns
  const content = [columns.map((col) => wrapCsvValue(col.label))]
    .concat(
      employees.value.map((row) =>
        columns
          .map((col) =>
            wrapCsvValue(
              typeof col.field === 'function'
                ? col.field(row)
                : row[col.field === void 0 ? col.name : col.field],
              col.format,
              row,
            ),
          )
          .join(','),
      ),
    )
    .join('\r\n')

  const status = exportFile(
    `employee-directory-${new Date().toISOString().split('T')[0]}.csv`,
    content,
    'text/csv',
  )

  if (status !== true) {
    $q.notify({
      message: 'Browser denied file download...',
      color: 'negative',
      icon: 'warning',
    })
  }
}

onMounted(() => {
  fetchEmployees()
})
</script>

<style scoped>
.rounded-borders {
  border-radius: 8px;
}
</style>
