<template>
  <div class="p-8 max-w-md mx-auto">
    <h2 class="text-2xl font-bold mb-4">Login</h2>
    <form @submit.prevent="login">
      <input v-model="email" type="email" placeholder="Email" class="border p-2 w-full mb-3" />
      <input v-model="password" type="password" placeholder="Password" class="border p-2 w-full mb-3" />
      <button type="submit" class="bg-green-500 text-white px-4 py-2">Login</button>
    </form>
    <p class="text-red-500 mt-3">{{ error }}</p>
  </div>
</template>

<script>
import API from "../services/api";

export default {
  data() {
    return {
      email: "",
      password: "",
      error: "",
    };
  },
  methods: {
    // logging in 
    async login() {
      try {
        // await the API call to login
        const res = await API.post("/auth/login", {
          email: this.email,
          password: this.password,
        });
        // get token and user role from response
        localStorage.setItem("token", res.data.token);
        if (res.data.user.role === "member") {
          this.$router.push("/donor");
        } else {
          this.$router.push("/beneficiary");
        }
      } catch (err) {
        this.error = err.response?.data?.msg || "Login failed";
      }
    },
  },
};
</script>
