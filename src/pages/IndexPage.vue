<template>
  <q-page class="bg-grey-1">
    <!-- Hero Section -->
    <section class="hero-section bg-primary text-white">
      <div
        class="row items-center q-col-gutter-lg q-px-sm q-px-md-md q-py-xl"
        style="max-width: 1200px; margin: 0 auto; width: 100%"
      >
        <div class="col-12 col-md-6 q-py-lg q-py-md-xl text-center text-md-left">
          <q-badge
            color="accent"
            text-color="dark"
            label="Version 2.0 Is Here"
            class="q-mb-lg text-weight-bold text-subtitle2 q-pa-sm shadow-1"
            rounded
          />

          <h1
            class="text-h4 text-sm-h3 text-md-h2 text-weight-bolder q-mt-none q-mb-md"
            style="line-height: 1.2"
          >
            Streamlining <br v-if="$q.screen.gt.sm" />
            <span class="text-secondary">Workforce Productivity</span>
          </h1>

          <p
            class="text-subtitle1 text-md-h6 text-weight-regular text-blue-grey-2 q-mb-xl mx-auto-sm px-xs px-md-none"
            style="max-width: 500px; line-height: 1.6"
          >
            The all-in-one advanced employee management system built for scaling enterprises. Track
            time, manage leaves, and oversee assets from a single unified dashboard.
          </p>

          <div class="row q-gutter-md justify-center justify-md-start q-mb-lg">
            <q-btn
              :size="$q.screen.gt.sm ? 'lg' : 'md'"
              unelevated
              color="secondary"
              label="Start Free Trial"
              to="/register"
              no-caps
              class="text-weight-bold shadow-2 full-width-xs"
              style="border-radius: 8px; width: 180px; height: 52px"
            />
            <q-btn
              :size="$q.screen.gt.sm ? 'lg' : 'md'"
              outline
              color="white"
              label="Login"
              to="/login"
              no-caps
              class="text-weight-bold full-width-xs"
              style="border-radius: 8px; width: 180px; height: 52px"
            />
          </div>

          <div
            class="row items-center justify-center justify-md-start q-gutter-x-md q-gutter-y-sm text-blue-grey-2 text-body2"
          >
            <div class="row items-center">
              <q-icon name="check_circle" color="secondary" class="q-mr-xs" />
              <span>No credit card required</span>
            </div>
            <div class="row items-center">
              <q-icon name="check_circle" color="secondary" class="q-mr-xs" />
              <span>14-day free trial</span>
            </div>
          </div>
        </div>

        <div class="col-12 col-md-6 text-center text-md-right q-py-md q-py-md-xl q-px-md">
          <div
            class="relative-position inline-block w-full q-mt-lg q-mt-md-none"
            style="max-width: 600px"
          >
            <q-img
              src="https://picsum.photos/800/600?random=1"
              style="border-radius: 16px; width: 100%"
              class="shadow-10 hover-lift"
            />

            <!-- Safe Overlay -->
            <q-card
              class="absolute-bottom-left shadow-15 q-pa-sm q-pa-md-md bg-white text-dark mobile-card-adjust"
              style="border-radius: 12px; z-index: 5"
            >
              <q-item class="q-pa-none">
                <q-item-section avatar style="min-width: 30px" class="q-pr-sm">
                  <q-avatar
                    color="positive"
                    text-color="white"
                    icon="trending_up"
                    :size="$q.screen.gt.xs ? 'md' : 'sm'"
                  />
                </q-item-section>
                <q-item-section>
                  <q-item-label class="text-weight-bolder text-h6 text-md-h5 text-dark"
                    >98%</q-item-label
                  >
                  <q-item-label
                    caption
                    class="text-weight-medium text-grey-8"
                    style="font-size: 0.75rem"
                    >Productivity Boost</q-item-label
                  >
                </q-item-section>
              </q-item>
            </q-card>
          </div>
        </div>
      </div>
    </section>

    <!-- Core Modules Grid Section -->
    <section class="q-py-xl q-px-md bg-white">
      <div
        class="text-center q-mb-xl q-pt-md q-pt-md-lg px-sm px-md-none"
        style="max-width: 800px; margin: 0 auto"
      >
        <h2 class="text-h4 text-md-h3 text-weight-bolder text-dark q-mt-none q-mb-sm">
          Powerful Core Modules
        </h2>
        <p class="text-body1 text-md-subtitle1 text-grey-7" style="line-height: 1.6">
          Everything you need to manage your enterprise workforce from day one. Say goodbye to
          scattered spreadsheets and disjointed tools.
        </p>
      </div>

      <div style="max-width: 1200px; margin: 0 auto">
        <div class="row q-col-gutter-lg justify-start">
          <!-- Attendance Tracking -->
          <div class="col-12 col-sm-6 col-md-4">
            <q-card
              class="module-card full-height no-shadow bg-grey-1 q-pa-md transition-all flex column"
              style="border-radius: 12px; border: 1px solid #e2e8f0"
            >
              <q-avatar color="primary" text-color="white" size="56px" class="q-mb-md">
                <q-icon name="schedule" size="28px" />
              </q-avatar>
              <div class="text-h6 text-weight-bold text-dark q-mb-sm">Attendance Tracking</div>
              <p class="text-body2 text-grey-7 q-mb-md col-grow">
                Real-time logging and monitoring of employee shifts, clock-ins, and overtime.
                Geolocation tagging enabled for remote workers.
              </p>
              <div>
                <q-btn
                  flat
                  color="primary"
                  label="Learn more"
                  icon-right="arrow_forward"
                  no-caps
                  class="q-px-none text-weight-bold"
                />
              </div>
            </q-card>
          </div>

          <!-- Leave Management -->
          <div class="col-12 col-sm-6 col-md-4">
            <q-card
              class="module-card full-height no-shadow bg-grey-1 q-pa-md transition-all flex column relative-position"
              style="border-radius: 12px; border: 1px solid #e2e8f0"
            >
              <q-avatar color="positive" text-color="white" size="56px" class="q-mb-md">
                <q-icon name="event_seat" size="28px" />
              </q-avatar>
              <div class="text-h6 text-weight-bold text-dark q-mb-sm">Leave Management</div>
              <p class="text-body2 text-grey-7 q-mb-md col-grow">
                Simple application and approval workflow. Multi-level hierarchy approvals, dynamic
                holiday calendars, and accrual policies.
              </p>
              <div>
                <q-btn
                  flat
                  color="primary"
                  label="Learn more"
                  icon-right="arrow_forward"
                  no-caps
                  class="q-px-none text-weight-bold"
                />
              </div>
            </q-card>
          </div>

          <!-- Employee Database -->
          <div class="col-12 col-sm-6 col-md-4">
            <q-card
              class="module-card full-height no-shadow bg-grey-1 q-pa-md transition-all flex column"
              style="border-radius: 12px; border: 1px solid #e2e8f0"
            >
              <q-avatar color="warning" text-color="white" size="56px" class="q-mb-md">
                <q-icon name="folder_shared" size="28px" />
              </q-avatar>
              <div class="text-h6 text-weight-bold text-dark q-mb-sm">Employee Database</div>
              <p class="text-body2 text-grey-7 q-mb-md col-grow">
                Centralized workforce records. Store tax documents, certifications, emergency
                contacts, and performance histories securely.
              </p>
              <div>
                <q-btn
                  flat
                  color="primary"
                  label="Learn more"
                  icon-right="arrow_forward"
                  no-caps
                  class="q-px-none text-weight-bold"
                />
              </div>
            </q-card>
          </div>

          <!-- Complaint System -->
          <div class="col-12 col-sm-6 col-md-4">
            <q-card
              class="module-card full-height no-shadow bg-grey-1 q-pa-md transition-all flex column"
              style="border-radius: 12px; border: 1px solid #e2e8f0"
            >
              <q-avatar color="negative" text-color="white" size="56px" class="q-mb-md">
                <q-icon name="report_problem" size="28px" />
              </q-avatar>
              <div class="text-h6 text-weight-bold text-dark q-mb-sm">Complaint System</div>
              <p class="text-body2 text-grey-7 q-mb-md col-grow">
                Internal grievance and feedback management. Anonymous reporting features, SLA
                tracking, and resolution pathways.
              </p>
              <div>
                <q-btn
                  flat
                  color="primary"
                  label="Learn more"
                  icon-right="arrow_forward"
                  no-caps
                  class="q-px-none text-weight-bold"
                />
              </div>
            </q-card>
          </div>

          <!-- Device Management -->
          <div class="col-12 col-sm-6 col-md-4">
            <q-card
              class="module-card full-height no-shadow bg-grey-1 q-pa-md transition-all flex column"
              style="border-radius: 12px; border: 1px solid #e2e8f0"
            >
              <q-avatar color="accent" text-color="white" size="56px" class="q-mb-md">
                <q-icon name="devices" size="28px" />
              </q-avatar>
              <div class="text-h6 text-weight-bold text-dark q-mb-sm">Device Management</div>
              <p class="text-body2 text-grey-7 q-mb-md col-grow">
                Tracking hardware and company assets. Monitor laptop assignments, vehicle dispatch
                logs, and office equipment lifecycles.
              </p>
              <div>
                <q-btn
                  flat
                  color="primary"
                  label="Learn more"
                  icon-right="arrow_forward"
                  no-caps
                  class="q-px-none text-weight-bold"
                />
              </div>
            </q-card>
          </div>
        </div>
      </div>
    </section>

    <!-- Dashboard Preview Section -->
    <section class="q-py-md q-py-md-xl bg-grey-2 q-px-md">
      <div
        class="row items-center q-col-gutter-xl q-py-lg"
        style="max-width: 1200px; margin: 0 auto; width: 100%"
      >
        <div
          class="col-12 col-md-6 order-last order-md-first q-pr-sm q-pr-md-md q-mt-lg q-mt-md-none"
        >
          <div class="relative-position inline-block w-full">
            <q-img
              src="https://picsum.photos/1000/700?random=2"
              class="rounded-borders shadow-4 w-full"
              style="
                border: 4px solid white;
                border-radius: 12px;
                border-md: 6px solid white;
                border-radius-md: 16px;
              "
            >
              <template v-slot:error>
                <div
                  class="absolute-full flex flex-center bg-grey-3 text-grey-8 text-weight-medium"
                >
                  Dashboard Preview Graphic
                </div>
              </template>
            </q-img>

            <!-- Safe Overlay -->
            <q-card
              class="shadow-10 q-pa-xs q-pa-md-sm bg-white text-dark absolute-top-right mobile-card-adjust-dash"
              style="border-radius: 8px; z-index: 10"
            >
              <q-item class="q-pa-xs q-pa-md-sm">
                <q-item-section>
                  <q-item-label
                    caption
                    class="text-weight-medium text-grey-8"
                    style="font-size: 0.7rem"
                    >Active Employees</q-item-label
                  >
                  <q-item-label class="text-weight-bold text-h6 text-md-h5 text-primary"
                    >1,248</q-item-label
                  >
                </q-item-section>
                <q-item-section side style="padding-left: 4px">
                  <q-avatar
                    color="secondary"
                    text-color="white"
                    icon="group"
                    :size="$q.screen.gt.xs ? 'md' : 'sm'"
                  />
                </q-item-section>
              </q-item>
            </q-card>
          </div>
        </div>

        <div class="col-12 col-md-6 text-center text-md-left px-sm px-md-none">
          <q-chip
            color="primary"
            text-color="white"
            icon="analytics"
            class="q-mb-md text-weight-bold"
          >
            Analytics Dashboard
          </q-chip>

          <h2
            class="text-h4 text-md-h3 text-weight-bolder text-dark q-mt-none q-mb-md"
            style="line-height: 1.2"
          >
            Intelligence at your fingertips.
          </h2>

          <p
            class="text-body1 text-md-subtitle1 text-grey-7 q-mb-lg q-mb-md-xl mx-auto-sm"
            style="max-width: 500px; line-height: 1.6"
          >
            Gain deep insights into your Daily Summary and overall workforce trends. Customizable
            widgets let you prioritize the metrics that matter most to your executive team.
          </p>

          <q-list
            class="q-mb-lg text-left inline-block w-full text-md-left"
            style="max-width: 500px"
          >
            <q-item class="q-px-none q-mb-sm">
              <q-item-section avatar top class="q-pr-sm">
                <q-avatar
                  color="primary"
                  text-color="white"
                  icon="insights"
                  :size="$q.screen.gt.xs ? 'lg' : 'md'"
                />
              </q-item-section>
              <q-item-section>
                <q-item-label class="text-weight-bold text-dark text-body1 text-md-h6"
                  >Daily Summary Widgets</q-item-label
                >
                <q-item-label
                  caption
                  class="text-grey-7"
                  style="line-height: 1.4; font-size: 0.85rem"
                  >Instantly view today's absentees, pending requests, and scheduled shifts in
                  real-time.</q-item-label
                >
              </q-item-section>
            </q-item>

            <q-item class="q-px-none">
              <q-item-section avatar top class="q-pr-sm">
                <q-avatar
                  color="secondary"
                  text-color="white"
                  icon="pie_chart"
                  :size="$q.screen.gt.xs ? 'lg' : 'md'"
                />
              </q-item-section>
              <q-item-section>
                <q-item-label class="text-weight-bold text-dark text-body1 text-md-h6"
                  >Interactive Reports</q-item-label
                >
                <q-item-label
                  caption
                  class="text-grey-7"
                  style="line-height: 1.4; font-size: 0.85rem"
                  >Exportable data visualizations for turnover rates, payroll forecasts, and
                  diversity metrics.</q-item-label
                >
              </q-item-section>
            </q-item>
          </q-list>

          <div class="q-mt-sm row justify-center justify-md-start">
            <q-btn
              outline
              color="primary"
              label="Explore Analytics"
              icon-right="chevron_right"
              no-caps
              class="text-weight-bold px-lg full-width-xs"
              style="border-radius: 6px"
            />
          </div>
        </div>
      </div>
    </section>

    <!-- Call to Action Banner -->
    <section class="q-py-xl bg-primary text-white text-center q-px-md">
      <div class="q-py-md q-py-md-lg px-sm px-md-none" style="max-width: 800px; margin: 0 auto">
        <h2 class="text-h4 text-md-h3 text-weight-bolder q-mt-none q-mb-sm">
          Ready to transform your HR?
        </h2>
        <p class="text-body1 text-md-subtitle1 text-blue-grey-2 q-mb-xl" style="line-height: 1.6">
          Join 10,000+ modern companies managing their workforce seamlessly with WorkforcePro.
        </p>
        <div class="row justify-center q-px-sm">
          <q-btn
            :size="$q.screen.gt.sm ? 'lg' : 'md'"
            unelevated
            color="accent"
            text-color="dark"
            label="Get Started for Free"
            to="/register"
            no-caps
            class="text-weight-bold shadow-2 full-width-xs"
            style="border-radius: 8px; width: 220px; height: 52px"
          />
        </div>
      </div>
    </section>
  </q-page>
</template>

<script setup>
import { useQuasar } from 'quasar'
const $q = useQuasar()
</script>

<style lang="scss" scoped>
/* Base overrides */
.h-full {
  height: 100%;
}
.w-full {
  width: 100%;
}

/* Custom paddings */
.px-lg {
  padding-left: 24px;
  padding-right: 24px;
}
.px-sm {
  padding-left: 12px;
  padding-right: 12px;
}

/* Responsive utility */
@media (max-width: 599px) {
  /* xs */
  .full-width-xs {
    width: 100%;
    display: block;
  }
  .q-mt-sm-xs {
    margin-top: 12px !important;
  }
  .mobile-card-adjust {
    margin-bottom: -15px !important;
    margin-left: 5px !important;
  }
  .mobile-card-adjust-dash {
    margin-top: -10px !important;
    margin-right: 0px !important;
  }
}
@media (max-width: 1023px) {
  /* sm, md */
  .mx-auto-sm {
    margin-left: auto;
    margin-right: auto;
  }
}
@media (min-width: 600px) {
  .mobile-card-adjust {
    margin-bottom: -20px !important;
    margin-left: -10px !important;
  }
  .mobile-card-adjust-dash {
    margin-top: -15px !important;
    margin-right: -15px !important;
  }
}

/* Hover effects */
.hover-lift {
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15) !important;
  }
}

.module-card {
  &:hover {
    background-color: #ffffff !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08) !important;
    transform: translateY(-4px);
    border-color: var(--q-primary) !important;
  }
}
.transition-all {
  transition: all 0.3s ease;
}
</style>
