<template>
  <div class="container mt-4" style="max-width: 500px;">
    <h2 class="text-center mb-4">Company Registration</h2>

    <div class="card p-4 shadow">

      <label class="fw-bold">Contact Person Name</label>
      <input v-model="name" placeholder="Enter contact person name"
        class="form-control mb-3" />

      <label class="fw-bold">Email</label>
      <input v-model="email" type="email" placeholder="Enter company email"
        class="form-control mb-3" />

      <label class="fw-bold">Password</label>
      <input v-model="password" type="password" placeholder="Enter password"
        class="form-control mb-3" />

      <label class="fw-bold">Company Name</label>
      <input v-model="company_name" placeholder="Enter company name"
        class="form-control mb-3" />

      <label class="fw-bold">HR Contact Number</label>
      <input v-model="hr_contact" type="tel" placeholder="Enter HR contact number"
        class="form-control mb-3" />

      <label class="fw-bold">Company Website</label>
      <input v-model="website" placeholder="Enter website URL (e.g. www.tcs.com)"
        class="form-control mb-3" />

      <label class="fw-bold">Industry Type</label>
      <select v-model="industry" class="form-control mb-3">
        <option value="">-- Select Industry --</option>
        <option value="IT">IT — Information Technology</option>
        <option value="Finance">Finance & Banking</option>
        <option value="Healthcare">Healthcare</option>
        <option value="Manufacturing">Manufacturing</option>
        <option value="Consulting">Consulting</option>
        <option value="Ecommerce">E-Commerce</option>
        <option value="Other">Other</option>
      </select>

      <button class="btn btn-primary w-100 mt-2" @click="handleRegister">
        Register Company
      </button>

    </div>

    <p class="text-center mt-3">
      Already registered?
      <router-link to="/login">Login</router-link>
    </p>

    <p class="text-center">
      Register as student?
      <router-link to="/register">Student Register</router-link>
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
      company_name: '',
      hr_contact: '',
      website: '',
      industry: ''
    }
  },

  methods: {
    async handleRegister() {
      try {

        // Validation
        if (!this.name || !this.email || !this.password ||
            !this.company_name || !this.hr_contact || !this.website) {
          alert("All fields are required.!")
          return
        }

        const res = await axios.post(
          'http://127.0.0.1:5000/auth/register/company',
          {
            name: this.name,
            email: this.email,
            password: this.password,
            company_name: this.company_name,
            hr_contact: this.hr_contact,
            website: this.website
          }
        )

        if (res.data.error) {
          alert(res.data.error)
          return
        }

        alert("Company Registered! Waiting for Admin approval!")
        this.$router.push('/login')

      } catch (err) {
        console.error(err)
        alert("Register Failed ")
      }
    }
  }
}
</script>