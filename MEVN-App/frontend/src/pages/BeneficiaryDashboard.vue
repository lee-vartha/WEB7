<template>
  <div class="p-8 bg-gray-100 min-h-screen">
    <div class="max-w-4xl mx-auto">
      <!-- Header -->
      <h2 class="text-3xl font-bold text-center mb-6 text-indigo-700">
        🎟 Beneficiary Dashboard
      </h2>


      <!-- Balance Card -->
      <div class="bg-white shadow-md rounded-lg p-6 mb-6 text-center">
        <p class="text-xl font-semibold text-gray-800">
          Token Balance:
          <span class="ml-2 font-mono text-green-600">{{ balance }}</span>
        </p>
      </div>

      <!-- Product Grid -->
      <div v-if="products.length" class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div
          v-for="product in products"
          :key="product._id"
          class="bg-white shadow-md rounded-lg p-5 flex flex-col justify-between hover:shadow-lg transition"
        >
          <div>
            <p class="text-lg font-semibold text-gray-900">{{ product.name }}</p>
            <p class="text-sm text-gray-500 mb-2">{{ product.description }}</p>
            <p class="text-green-600 font-medium">{{ product.cost }} tokens</p>
          </div>

          <button
            @click="buy(product)"
            class="mt-4 bg-green-500 hover:bg-green-600 text-white py-2 rounded transition"
          >
            Buy
          </button>
        </div>
      </div>

      <!-- No Products -->
      <p v-else class="text-gray-500 text-center">No products available</p>

      <!-- Messages -->
      <div class="mt-6 text-center">
        <p v-if="msg" class="text-blue-500 font-medium">{{ msg }}</p>
        <p v-if="error" class="text-red-500 font-medium">{{ error }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import API from "../services/api";

export default {
  data() {
    return {
      balance: 0,
      products: [],
      msg: "",
      error: "",
    };
  },
  async mounted() {
    try {
      const user = await API.get("/auth/me");
      this.balance = user.data.tokenBalance || 5;

      const res = await API.get("/products");
      this.products = res.data;
    } catch (err) {
      this.error = err.response?.data?.msg || "Failed to load data.";
    }
  },
  methods: {
    async buy(product) {
      try {
        if (this.balance < product.cost) {
          this.error = "Insufficient tokens!";
          return;
        }

        const res = await API.post("/tokens/spend", { productId: product._id });
        this.balance = res.data.balance;
        this.msg = res.data.msg;
        this.error = "";
      } catch (err) {
        this.error = err.response?.data?.msg || "Transaction failed.";
      }
    },
  },
};
</script>
