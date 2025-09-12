// importing the necessary modules
import { createRouter, createWebHistory } from "vue-router";
import Register from "../pages/Register.vue";
import Login from "../pages/Login.vue";
import DonorDashboard from "../pages/DonorDashboard.vue";
import BeneficiaryDashboard from "../pages/BeneficiaryDashboard.vue";

// referencing the routes and their components
const routes = [
  { path: "/", redirect: "/login" },
  { path: "/register", component: Register },
  { path: "/login", component: Login },
  { path: "/donor", component: DonorDashboard },
  { path: "/beneficiary", component: BeneficiaryDashboard },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
