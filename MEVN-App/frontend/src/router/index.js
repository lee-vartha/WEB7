// importing the necessary modules
import { createRouter, createWebHistory } from "vue-router";

// importing page components
import DonorDashboard from "../pages/DonorDashboard.vue";
import BeneficiaryDashboard from "../pages/BeneficiaryDashboard.vue";
import RegisterPage from "../pages/RegisterPage.vue";
import LoginPage from "../pages/LoginPage.vue";

// defining routes
const routes = [
  { path: "/", redirect: "/login" },
  { path: "/register", component: RegisterPage },
  { path: "/login", component: LoginPage },
  { path: "/donor", component: DonorDashboard },
  { path: "/beneficiary", component: BeneficiaryDashboard },
];

// creating router instance
const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
