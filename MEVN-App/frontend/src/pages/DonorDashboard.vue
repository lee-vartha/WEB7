<template>
  <div class="p-8 bg-gray-100 min-h-screen">
    <div class="max-w-lg mx-auto bg-white shadow-md rounded-lg p-6">
      <h2 class="text-2xl font-bold mb-4 text-indigo-700">Donor Dashboard</h2>

      <form @submit.prevent="addProduct" class="space-y-4">
        <input v-model="name" placeholder="Product Name"
          class="w-full border rounded px-3 py-2" />
        <input v-model="description" placeholder="Description"
          class="w-full border rounded px-3 py-2" />
        <input v-model.number="cost" placeholder="Cost (tokens)" type="number"
          class="w-full border rounded px-3 py-2" />

        <button type="submit"
          class="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-2 rounded">
          Add Product
        </button>
      </form>

      <p v-if="msg" class="text-green-600 mt-4">{{ msg }}</p>
      <p v-if="error" class="text-red-600 mt-4">{{ error }}</p>
    </div>
  </div>
</template>

<script>
import API from "../services/api";

export default {
  data() {
    return {
      name: "",
      description: "",
      cost: 0,
      msg: "",
      error: "",
    };
  },
  methods: {
    async addProduct() {
      try {
        const res = await API.post("/products", {
          name: this.name,
          description: this.description,
          cost: this.cost,
          owner: this.owner
        });
        this.msg = `Product ${res.data.name} added successfully`;
        this.error = "";
      } catch (err) {
        this.error = err.response?.data?.msg || "Error adding product";
      }
    },
  },
};
</script>
