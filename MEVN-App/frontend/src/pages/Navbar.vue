<template>
  <nav class="navbar">
    <div class="nav-container">
      <h1 class="logo">Charity App</h1>
      <ul class="nav-links">
        <li><router-link to="/register">Register</router-link></li>
        <li><router-link to="/login">Login</router-link></li>
        <li><router-link to="/donor-dashboard">Donor Dashboard</router-link></li>
        <li><router-link to="/beneficiary-dashboard">Beneficiary Dashboard</router-link></li>
      </ul>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  background: #1e293b; /* dark navy */
  padding: 1rem;
  color: white;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}

.nav-container {
  display: flex;
  justify-content: center; /* centers everything */
  align-items: center;
  gap: 2rem;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: #22c55e;
}

.nav-links {
  list-style: none;
  display: flex;
  gap: 1.5rem;
  margin: 0;
  padding: 0;
}

.nav-links a {
  color: white;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s ease;
}

.nav-links a:hover {
  color: #22c55e;
}
</style>
