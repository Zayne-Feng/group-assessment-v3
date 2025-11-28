import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import StudentsView from '../views/StudentsView.vue'
import StudentDetailView from '../views/StudentDetailView.vue'
import DashboardView from '../views/DashboardView.vue'
import ModulesView from '../views/ModulesView.vue'
import AlertsView from '../views/AlertsView.vue'
import UsersView from '../views/UsersView.vue'
import SurveyView from '../views/SurveyView.vue'
import EnrolmentsView from '../views/EnrolmentsView.vue'
import AttendanceView from '../views/AttendanceView.vue'
import SubmissionsView from '../views/SubmissionsView.vue'
import GradesView from '../views/GradesView.vue'
import AnalyticsView from '../views/AnalyticsView.vue'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginView,
      meta: { title: 'Login' }
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
      meta: { title: 'Register' }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true, title: 'Dashboard' }
    },
    {
      path: '/students',
      name: 'students',
      component: StudentsView,
      meta: { requiresAuth: true, title: 'Student Management' }
    },
    {
      path: '/students/:id',
      name: 'student-detail',
      component: StudentDetailView,
      meta: { requiresAuth: true, title: 'Student Details' }
    },
    {
      path: '/modules',
      name: 'modules',
      component: ModulesView,
      meta: { requiresAuth: true, requiresRole: ['admin', 'course_director'], title: 'Module Management' }
    },
    {
      path: '/alerts',
      name: 'alerts',
      component: AlertsView,
      meta: { requiresAuth: true, requiresRole: ['admin', 'wellbeing_officer'], title: 'Wellbeing Alerts' }
    },
    {
      path: '/users',
      name: 'users',
      component: UsersView,
      meta: { requiresAuth: true, requiresRole: 'admin', title: 'User Management' }
    },
    {
      path: '/survey',
      name: 'survey',
      component: SurveyView,
      meta: { requiresAuth: true, title: 'Submit Weekly Survey' }
    },
    {
      path: '/enrolments',
      name: 'enrolments',
      component: EnrolmentsView,
      meta: { requiresAuth: true, requiresRole: ['admin', 'course_director'], title: 'Enrolment Management' }
    },
    {
      path: '/attendance',
      name: 'attendance',
      component: AttendanceView,
      meta: { requiresAuth: true, requiresRole: ['admin', 'course_director'], title: 'Attendance Tracking' }
    },
    {
      path: '/submissions',
      name: 'submissions',
      component: SubmissionsView,
      meta: { requiresAuth: true, requiresRole: ['admin', 'course_director'], title: 'Submission Records' }
    },
    {
      path: '/grades',
      name: 'grades',
      component: GradesView,
      meta: { requiresAuth: true, requiresRole: ['admin', 'course_director'], title: 'Grade Management' }
    },
    {
      path: '/analytics',
      name: 'analytics',
      component: AnalyticsView,
      meta: { requiresAuth: true, requiresRole: ['admin', 'course_director', 'wellbeing_officer'], title: 'System Analytics' }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    authStore.clearToken(); // Clear any stale token
    next('/') // Redirect to login if not authenticated
  }
  else if (to.meta.requiresRole && !to.meta.requiresRole.includes(authStore.userRole)) {
    next('/dashboard')
  }
  else if ((to.name === 'login' || to.name === 'register') && authStore.isAuthenticated) {
    next('/dashboard')
  }
  else {
    next()
  }
})

export default router
