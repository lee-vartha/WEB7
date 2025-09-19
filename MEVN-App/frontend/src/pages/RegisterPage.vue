<template>
  <div class="p-8 max-w-md mx-auto">
    <h2 class="text-2xl font-bold mb-4">Register</h2>
    <form @submit.prevent="register">
      <input v-model="name" placeholder="Name" class="border p-2 w-full mb-3" />
      <input v-model="email" type="email" placeholder="Email" class="border p-2 w-full mb-3" />
      <input v-model="password" type="password" placeholder="Password" class="border p-2 w-full mb-3" />
      <select v-model="role" class="border p-2 w-full mb-3">
        <option value="donor">Donor</option>
        <option value="beneficiary">Beneficiary</option>
      </select>
      <button type="submit" class="bg-blue-500 text-white px-4 py-2">Register</button>
    </form>
    <p class="text-red-500 mt-3">{{ error }}</p>
  </div>
</template>

<script>
import API from "../services/api";

export default {
  data() {
    return {
      name: "",
      email: "",
      password: "",
      role: "beneficiary",
      error: "",
    };
  },
  methods: {
    // method to register user
    async register() {
      try {
        const res = await API.post("/auth/register", {
          name: this.name,
          email: this.email,
          password: this.password,
          role: this.role,
        });
        // sending token to local storage and redirecting based on role
        localStorage.setItem("token", res.data.token);
        if (this.role === "donor") {
          this.$router.push("/donor");
        } else {
          this.$router.push("/beneficiary");
        }
      } catch (err) {
        this.error = err.response?.data?.msg || "Error registering";
      }
    },
  },
};
</script>
