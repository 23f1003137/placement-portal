<template>
  <div class="container mt-4">

    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Student Dashboard </h2>
      <div>
        <router-link to="/profile" class="btn btn-outline-secondary me-2">
          My Profile
        </router-link>
        <router-link to="/applications" class="btn btn-outline-primary me-2">
          My Applications
        </router-link>
      </div>
    </div>

    # Organizations / Companies 
    <h4 class="mb-3">Organizations</h4>

    <div v-if="companies.length === 0" class="text-muted mb-4">
      There are no approved companies at the moment.
    </div>

    <div v-for="company in companies" :key="company.id" class="card shadow-sm mb-4">

      # Company Header 
      <div class="card-header d-flex justify-content-between align-items-center">
        <h5 class="mb-0"> {{ company.company_name }}</h5>
        <button
          class="btn btn-sm btn-outline-primary"
          @click="toggleCompany(company.id)"
        >
          {{ openCompany === company.id ? 'Hide Drives ▲' : 'View Drives ▼' }}
        </button>
      </div>

      # Company Details 
      <div class="card-body pb-1">
        <p class="mb-1">
          <b>Website:</b> {{ company.website }}
        </p>
        <p class="mb-1">
          <b>HR Contact:</b> {{ company.hr_contact }}
        </p>
        <p class="mb-2">
          <b>Total Drives:</b> {{ company.drives.length }}
        </p>
      </div>

       Drives List — toggle se khulta hai 
      <div v-if="openCompany === company.id" class="px-3 pb-3">
        <hr />
        <h6 class="mb-3">Available Drives</h6>

        <div v-if="company.drives.length === 0" class="text-muted">
          No drive is available.
        </div>

        <div
          v-for="drive in company.drives"
          :key="drive.id"
          class="card mb-2 border-primary"
        >
          <div class="card-body">
            <h6 class="card-title">{{ drive.job_title }}</h6>
            <p class="mb-1"><b>Description:</b> {{ drive.job_description }}</p>
            <p class="mb-1"><b>Branch:</b> {{ drive.branch_required }}</p>
            <p class="mb-1"><b>Min CGPA:</b> {{ drive.cgpa_required }}</p>
            <p class="mb-1"><b>Year:</b> {{ drive.year_required }}</p>
            <p class="mb-1"><b>Salary:</b> {{ drive.salary }}</p> 
            <p class="mb-2"><b>Deadline:</b> {{ drive.deadline }}</p>
            

            <button
              class="btn btn-primary"
              @click="applyDrive(drive.id)"
            >
              Apply Now
            </button>
          </div>
        </div>

      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      companies: [],
      openCompany: null   
    }
  },

  async mounted() {
    await this.fetchCompanies()
  },

  methods: {

    // Companies + unki drives fetch ke liye
    async fetchCompanies() {
      try {
        const token = localStorage.getItem("token")
        const res = await axios.get(
          "http://127.0.0.1:5000/student/companies",
          { headers: { Authorization: token } }
        )
        this.companies = res.data
      } catch (err) {
        console.error(err)
        alert("The companies did not load.")
      }
    },

    // Company click karne pe drives toggle karegi
    toggleCompany(companyId) {
      if (this.openCompany === companyId) {
        this.openCompany = null   
      } else {
        this.openCompany = companyId 
      }
    },

    // Drive  apply ke liye 
    async applyDrive(driveId) {
      try {
        const token = localStorage.getItem("token")
        const res = await axios.post(
          "http://127.0.0.1:5000/student/apply",
          { drive_id: driveId },
          { headers: { Authorization: token } }
        )
        if (res.data.error) {
          alert(res.data.error)
        } else {
          alert(res.data.message)
        }
      } catch (err) {
        alert("Applying is not complete ")
      }
    },

    logout() {
      localStorage.removeItem("token")
      localStorage.removeItem("role")
      this.$router.push('/login')
    }
  }
}
</script>