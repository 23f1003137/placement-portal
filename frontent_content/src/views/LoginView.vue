<template>
  <div class="container mt-4" style="max-width: 500px;">
    <h2 class="text-center mb-4">Placement Portal Login</h2>

    <div class="card p-4 shadow">

      <label class="fw-bold">Email</label>
      <input v-model="email" type="email" placeholder="Enter your email"
        class="form-control mb-3" />

      <label class="fw-bold">Password</label>
      <input v-model="password" type="password" placeholder="Enter your password"
        class="form-control mb-3" />

      <button class="btn btn-primary w-100 mt-2" @click="handleLogin">
        Login
      </button>

    </div>

    <div class="card p-3 shadow mt-3 text-center">
      <p class="mb-1 fw-bold">New User?</p>

      <div class="d-flex justify-content-center gap-3 mt-2">
        <router-link to="/register" class="btn btn-outline-primary">
          Student Register
        </router-link>
        <router-link to="/register/company" class="btn btn-outline-success">
          Company Register
        </router-link>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      email: '',
      password: ''
    }
  },

  methods: {
    async handleLogin() {
      try {

        // Validation
        if (!this.email || !this.password) {
          alert("Both email and password are required!")
          return
        }

        const res = await axios.post(
          'http://127.0.0.1:5000/auth/login',
          {
            email: this.email,
            password: this.password
          }
        )

        if (res.data.error) {
          alert(res.data.error)
          return
        }

        // Token aur role save karne ke liye
        localStorage.setItem("token", res.data.token)
        localStorage.setItem("role", res.data.role)

        // Role ke hisaab se redirect karenge
        if (res.data.role === "student") {
          this.$router.push('/dashboard')
        } else if (res.data.role === "company") {
          this.$router.push('/company')
        } else if (res.data.role === "admin") {
          this.$router.push('/admin')
        }

      } catch (err) {
        console.error(err)
        alert("Login Failed ")
      }
    }
  }
}
</script>