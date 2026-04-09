import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import DashboardView from '../views/DashboardView.vue'
import ApplicationsView from '../views/ApplicationsView.vue'
import CompanyView from '../views/CompanyView.vue'
import AdminView from '../views/AdminView.vue'
import CompanyRegisterView from '../views/CompanyRegisterView.vue'
import StudentProfileView from '../views/StudentProfileView.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: LoginView },
  { path: '/register', component: RegisterView },
  { path: '/register/company', component: CompanyRegisterView },
  { path: '/dashboard', component: DashboardView },
  { path: '/applications', component: ApplicationsView },
  { path: '/profile', component: StudentProfileView },
  { path: '/company', component: CompanyView },
  { path: '/admin', component: AdminView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router