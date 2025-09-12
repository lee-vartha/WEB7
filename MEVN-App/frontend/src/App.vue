<template>
  <div>
    <nav class="bg-gray-900 text-white p-4 flex justify-between">
      <h1 class="font-bold text-lg"> Charity App - MEVN + JWT</h1>
      <div class="space-x-4">
        <router-link to="/register">Register</router-link>
        <router-link to="/login">Login</router-link>
        <router-link to="/donor">Donor Dashboard</router-link>
        <router-link to="/beneficiary">Beneficiary Dashboard</router-link>
      </div>
    </nav>
    <router-view />
  </div>
</template>
