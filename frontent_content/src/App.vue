<template>
  <div>
    <!-- navar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-3">
      <a class="navbar-brand" href="#">Placement Portal</a>

      <div class="ms-auto">
        <button 
          v-if="isLoggedIn" 
          class="btn btn-danger"
          @click="logout"
        >
          Logout
        </button>
      </div>
    </nav>

  
    <div class="container mt-4">
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    isLoggedIn() {
      return localStorage.getItem("token")
    }
  },
  methods: {
    logout() {
      localStorage.removeItem("token")
      this.$router.push('/login')
    }
  }
}
</script>