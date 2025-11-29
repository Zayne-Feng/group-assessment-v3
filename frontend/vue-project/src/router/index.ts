import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import StudentLoginView from '../views/StudentLoginView.vue'
import StudentRegisterView from '../views/StudentRegisterView.vue'
import MyProfileView from '../views/MyProfileView.vue'
import StudentsView from '../views/StudentsView.vue'
import StudentDetailView from '../views/StudentDetailView.vue'
import DashboardView from '../views/DashboardView.vue'
import ModulesView from '../views/ModulesView.vue'
import AlertsView from '../views/AlertsView.vue'
import UsersView from '../views/UsersView.vue'
import SurveyView from '../views/SurveyView.vue'
import SurveyResponsesView from '../views/SurveyResponsesView.vue'
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
      name: 'staff-login',
      component: LoginView,
      meta: { title: 'Staff Login' }
    },
    {
      path: '/register',
      name: 'staff-register',
      component: RegisterView,
      meta: { title: 'Staff Register' }
    },
    {
      path: '/student/login',
      name: 'student-login',
      component: StudentLoginView,
      meta: { title: 'Student Login' }
    },
    {
      path: '/student/register',
      name: 'student-register',
      component: StudentRegisterView,
      meta: { title: 'Student Register' }
    },
    {
      path: '/my-profile',
      name: 'my-profile',
      component: MyProfileView,
      meta: { requiresAuth: true, requiresRole: ['student'], title: 'My Profile' }
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
      path: '/survey-responses',
      name: 'survey-responses',
      component: SurveyResponsesView,
      meta: { requiresAuth: true, requiresRole: ['admin', 'wellbeing_officer'], title: 'Survey Responses' }
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
  const isAuthenticated = authStore.isAuthenticated

  // Redirect unauthenticated users to the staff login page
  if (to.meta.requiresAuth && !isAuthenticated) {
    authStore.clearToken();
    return next('/')
  }

  // Handle authenticated users
  if (isAuthenticated) {
    const authRoutes = ['staff-login', 'staff-register', 'student-login', 'student-register'];
    if (authRoutes.includes(to.name as string)) {
      return authStore.isStudent ? next('/my-profile') : next('/dashboard');
    }

    // Student-specific routing
    if (authStore.isStudent) {
      const allowedStudentRoutes = ['my-profile', 'survey'];
      if (!allowedStudentRoutes.includes(to.name as string)) {
        return next('/my-profile'); // Default to profile page for students
      }
    }

    // Role-based access for staff
    if (to.meta.requiresRole) {
      const requiredRoles = Array.isArray(to.meta.requiresRole) ? to.meta.requiresRole : [to.meta.requiresRole];
      if (!authStore.userRole || !requiredRoles.includes(authStore.userRole)) {
        return authStore.isStudent ? next('/my-profile') : next('/dashboard');
      }
    }
  }

  next()
})

export default router
