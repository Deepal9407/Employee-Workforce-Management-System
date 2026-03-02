import { defineRouter } from '#q-app/wrappers'
import {
  createRouter,
  createMemoryHistory,
  createWebHistory,
  createWebHashHistory,
} from 'vue-router'
import routes from './routes'
import { supabase } from 'src/boot/supabase'

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Router instance.
 */

export default defineRouter(function (/* { store, ssrContext } */) {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : process.env.VUE_ROUTER_MODE === 'history'
      ? createWebHistory
      : createWebHashHistory

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,
    history: createHistory(process.env.VUE_ROUTER_BASE),
  })

  Router.beforeEach(async (to, from, next) => {
    const {
      data: { session },
    } = await supabase.auth.getSession()
    const isAuthenticated = !!session

    if (to.matched.some((record) => record.meta.requiresAuth)) {
      if (!isAuthenticated) {
        return next('/login')
      }
    } else if (to.matched.some((record) => record.meta.requiresGuest)) {
      if (isAuthenticated) {
        return next('/dashboard')
      }
    }

    next()
  })

  return Router
})
