<template>
  <div class="container mt-4" style="max-width: 500px;">
    <h2 class="text-center mb-4">Student Registration</h2>

    <div class="card p-4 shadow">

      <label class="fw-bold">Full Name</label>
      <input v-model="name" placeholder="Enter your full name"
        class="form-control mb-3" />

      <label class="fw-bold">Email</label>
      <input v-model="email" type="email" placeholder="Enter your email"
        class="form-control mb-3" />

      <label class="fw-bold">Password</label>
      <input v-model="password" type="password" placeholder="Enter password"
        class="form-control mb-3" />

      <label class="fw-bold">Branch</label>
      <select v-model="branch" class="form-control mb-3">
        <option value="">-- Select Branch --</option>
        <option value="CSE">CSE — Computer Science Engineering</option>
        <option value="ECE">ECE — Electronics & Communication</option>
        <option value="ME">ME — Mechanical Engineering</option>
        <option value="CE">CE — Civil Engineering</option>
        <option value="EE">EE — Electrical Engineering</option>
        <option value="IT">IT — Information Technology</option>
      </select>

      <label class="fw-bold">CGPA</label>
      <input v-model="cgpa" type="number" step="0.1" min="0" max="10"
        placeholder="Enter CGPA (0.0 to 10.0, e.g. 8.5)"
        class="form-control mb-3" />

      <label class="fw-bold">Current Year of Study</label>
      <select v-model="year" class="form-control mb-1">
        <option value="">-- Select Year --</option>
        <option value="1">1st Year — Freshman</option>
        <option value="2">2nd Year — Sophomore</option>
        <option value="3">3rd Year — Junior</option>
        <option value="4">4th Year — Final Year</option>
      </select>
      <small class="text-muted mb-3 d-block">
        Select your current year — the year you are currently studying in.
      </small>

      <button class="btn btn-primary w-100 mt-2" @click="handleRegister">
        Register
      </button>

    </div>

    <p class="text-center mt-3">
      Already have an account?
      <router-link to="/login">Login</router-link>
    </p>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      name: '',
      email: '',
      password: '',
      branch: '',
      cgpa: '',
      year: ''
    }
  },

  methods: {
    async handleRegister() {
      try {
        // Validation
        if (!this.name || !this.email || !this.password ||
            !this.branch || !this.cgpa || !this.year) {
          alert("All fields are required.!")
          return
        }

        const response = await axios.post(
          'http://127.0.0.1:5000/auth/register/student',
          {
            name: this.name,
            email: this.email,
            password: this.password,
            branch: this.branch,
            cgpa: parseFloat(this.cgpa),
            year: parseInt(this.year)
          }
        )

        if (response.data.error) {
          alert(response.data.error)
          return
        }

        alert("Registration Successful then login!")
        this.$router.push('/login')

      } catch (error) {
        console.error(error)
        alert("Register Failed ")
      }
    }
  }
}
</script>