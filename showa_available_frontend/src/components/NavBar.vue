<script setup></script>

<template>
  <nav class="navbar">
    <div class="navbar-brand">Showa Available</div>
    <ul class="navbar-links">
      <li><a href="#home">Home</a></li>
      <li><a href="#menu">Restaurants</a></li>
      <li><a href="#about">About Us</a></li>
      <li><a href="#contact">Contact</a></li>
      <li><a href="#contact">Sign Up</a></li>
    </ul>
  </nav>
</template>

<style scoped>
/* General styles */
body {
  margin: 0;
  font-family: Arial, sans-serif;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  height: 100vh;
  background-color: #f8f8f8;
}

/* Navbar styling */
.navbar {
  text-align: center;
  position: absolute;
  top: 0;
  width: 100%;
  background-color: #333;
  color: rgb(201, 178, 178);
  padding: 1rem 0;
}

.navbar-brand {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.navbar-links {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  justify-content: center;
  gap: 2rem;
}

.navbar-links li {
  display: inline;
}

.navbar-links a {
  color: #fff;
  text-decoration: none;
  font-size: 1.1rem;
  transition: color 0.3s ease;
}

.navbar-links a:hover {
  color: #f39c12;
}
</style>
