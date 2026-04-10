<template>
  <div class="container mt-4">
    <h1 class="mb-4 text-center">Admin Dashboard </h1>

    Search
    <div class="mb-4">
      <input v-model="searchQuery" placeholder="Search students or companies..."
        class="form-control mb-2" />
      <button class="btn btn-primary" @click="search">Search</button>
    </div>

    <!-- Search Results  -->
    <div v-if="searchResult.students.length || searchResult.companies.length" class="mb-4">
      <h5> Students</h5>
      <ul>
        <li v-for="s in searchResult.students" :key="s.id">
          {{ s.name }} ({{ s.email }})
        </li>
      </ul>
      <h5>Companies</h5>
      <ul>
        <li v-for="c in searchResult.companies" :key="c.id">
          {{ c.company_name }} - {{ c.status }}
        </li>
      </ul>
    </div>

     <!-- Stats  -->
    <div class="row mb-4">
      <div class="col-md-4">
        <div class="card text-center p-3 shadow">
          <h5>Total Students</h5>
          <h3>{{ stats.students }}</h3>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card text-center p-3 shadow">
          <h5>Total Companies</h5>
          <h3>{{ stats.companies }}</h3>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card text-center p-3 shadow">
          <h5>Total Drives</h5>
          <h3>{{ stats.drives }}</h3>
        </div>
      </div>
    </div>

        
    <h3>Registered Students</h3>
    <div v-for="student in students" :key="student.id" class="card p-3 mb-2">
      <p><b>Name:</b> {{ student.name }}</p>
      <p><b>Email:</b> {{ student.email }}</p>
      <p><b>Status:</b>
        <span :class="student.is_active ? 'text-success' : 'text-danger'">
          {{ student.is_active ? 'Active' : 'Inactive' }}
        </span>
      </p>

      <button
        :class="student.is_active ? 'btn btn-warning' : 'btn btn-success'"
        @click="toggleStudent(student.id)">
        {{ student.is_active ? 'Deactivate' : 'Activate' }}
      </button>
    </div>
    

    <!-- Company Registrations — Pending approvals  -->

    <h3 class="mt-4">Company Registrations</h3>
    <div v-if="pendingCompanies.length === 0" class="text-muted mb-3">
      There are no pending registrations.
    </div>
    <div v-for="company in pendingCompanies" :key="company.id" class="card p-3 mb-2 border-warning">
      <p><b>Name:</b> {{ company.company_name }}</p>
      <p><b>Email:</b> {{ company.email }}</p>
      <p><b>Status:</b> {{ company.approval_status }}</p>

      <div class="d-flex gap-2">
        <button class="btn btn-success" @click="approveCompany(company.id)">
          Approve
        </button>
        <button class="btn btn-danger" @click="rejectCompany(company.id)">
          Reject
        </button>
      </div>
    </div>

     <!-- All Companies — Activate/Deactivate  -->

    <h3 class="mt-4">All Companies</h3>
    <div v-for="company in companies" :key="company.id" class="card p-3 mb-2">
      <p><b>Name:</b> {{ company.company_name }}</p>
      <p><b>Approval:</b> {{ company.approval_status }}</p>
      <p><b>Status:</b>
        <span :class="company.is_active ? 'text-success' : 'text-danger'">
          {{ company.is_active ? 'Active ' : 'Inactive ' }}
        </span>
      </p>

      <button
        :class="company.is_active ? 'btn btn-warning' : 'btn btn-success'"
        @click="toggleUser(company.user_id, company.id)">
        {{ company.is_active ? 'Deactivate' : 'Activate' }}
      </button>
    </div>

  
    <h3 class="mt-4">Drives</h3>
    <div v-for="drive in drives" :key="drive.id" class="card p-3 mb-2">
      <p><b>Company Name:</b> {{ drive.company_name }}</p>
      <p><b>Job:</b> {{ drive.job_title }}</p>
      <p><b>Status:</b> {{ drive.status }}</p>

      <div class="d-flex gap-2">
        <button v-if="drive.status === 'pending'"
          class="btn btn-success" @click="approveDrive(drive.id)">
          Approve
        </button>
        <button v-if="drive.status === 'pending'"
          class="btn btn-danger" @click="rejectDrive(drive.id)">
          Reject
        </button>
      </div>
    </div>

  
    <h3 class="mt-4">All Applications</h3>
    <table class="table table-bordered table-hover shadow-sm">
      <thead class="table-dark">
        <tr>
          <th>Student</th>
          <th>Email</th>
          <th>Company</th>
          <th>Job</th>
          <th>Status</th>
          <th>Date</th>
          <th>Resume</th> 
        </tr>
      </thead>
      <tbody>
        <tr v-for="app in applications" :key="app.id">
          <td>{{ app.student_name }}</td>
          <td>{{ app.student_email }}</td>
          <td>{{ app.company_name }}</td>
          <td>{{ app.job_title }}</td>
          <td>{{ app.status }}</td>
          <td>{{ app.applied_on }}</td>
          <td>
            <template v-if="app.resume">
              
              <a :href="'http://127.0.0.1:5000/uploads/' + app.resume"
                target="_blank"
                class="btn btn-sm btn-outline-primary"
              >
                View Resume
              </a>
            </template>
            <template v-else>
              <span class="text-muted">No Resume</span>
            </template>
          </td>
        </tr>
      </tbody>
    </table>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      stats: {},
      companies: [],
      pendingCompanies: [],
      drives: [],
      applications: [],
      students: [], 
      searchQuery: "",
      searchResult: { students: [], companies: [] }
    }
  },

  async mounted() {
    await this.fetchStats()
    await this.fetchCompanies()
    await this.fetchDrives()
    await this.fetchApplications()
    await this.fetchStudents()  
  },

  methods: {

    async fetchStats() {
      const token = localStorage.getItem("token")
      const res = await axios.get("http://127.0.0.1:5000/admin/stats",
        { headers: { Authorization: token } })
      this.stats = res.data
    },

    async fetchCompanies() {
      const token = localStorage.getItem("token")
      const res = await axios.get(
        "http://127.0.0.1:5000/admin/companies",
        { headers: { Authorization: token } }
      )
      
      this.companies = res.data
      this.pendingCompanies = res.data.filter(
        c => c.approval_status === 'pending'
      )
    },

    async approveCompany(id) {
      const token = localStorage.getItem("token")
      const res = await axios.post("http://127.0.0.1:5000/admin/approve-company",
        { company_id: id }, { headers: { Authorization: token } })
      alert(res.data.message)
      this.fetchCompanies()
      this.fetchStats()
    },

    async rejectCompany(id) {
      const token = localStorage.getItem("token")
      const res = await axios.post("http://127.0.0.1:5000/admin/reject-company",
        { company_id: id }, { headers: { Authorization: token } })
      alert(res.data.message)
      this.fetchCompanies()
    },

    async toggleUser(userId, companyId) {
      if (!userId) {
        alert("User ID not found!")
        return
      }

      const token = localStorage.getItem("token")
      
      try {
        const res = await axios.post(
          "http://127.0.0.1:5000/admin/toggle-user",
          { user_id: userId },
          { headers: { Authorization: token } }
        )

        if (res.data.error) {
          alert(res.data.error)
          return
        }

        // array update 
        const index = this.companies.findIndex(c => c.user_id === userId)
        if (index !== -1) {
          this.companies[index] = {
            ...this.companies[index],
            is_active: res.data.is_active
          }
        
          this.companies = [...this.companies]
        }

        alert(res.data.message)

      } catch (err) {
        console.error(err)
        alert("Toggle failed ")
      }
    },


    async fetchStudents() {
      const token = localStorage.getItem("token")
      const res = await axios.get(
        "http://127.0.0.1:5000/admin/students",
        { headers: { Authorization: token } }
      )
      this.students = res.data
    },

    async toggleStudent(userId) {
      if (!userId) {
        alert("User ID not found!")
        return
      }

      const token = localStorage.getItem("token")

      try {
        const res = await axios.post(
          "http://127.0.0.1:5000/admin/toggle-user",
          { user_id: userId },
          { headers: { Authorization: token } }
        )

        if (res.data.error) {
          alert(res.data.error)
          return
        }

        // for array update ke liye
        const index = this.students.findIndex(s => s.id === userId)
        if (index !== -1) {
          this.students[index] = {
            ...this.students[index],
            is_active: res.data.is_active
          }
          this.students = [...this.students]
        }

        alert(res.data.message)

      } catch (err) {
        console.error(err)
        alert("Toggle failed ")
      }
    },

    async fetchDrives() {
      const token = localStorage.getItem("token")
      const res = await axios.get("http://127.0.0.1:5000/admin/drives",
        { headers: { Authorization: token } })
      this.drives = res.data
    },

    async approveDrive(id) {
      const token = localStorage.getItem("token")
      const res = await axios.post("http://127.0.0.1:5000/admin/approve-drive",
        { drive_id: id }, { headers: { Authorization: token } })
      alert(res.data.message)
      this.fetchDrives()
      this.fetchStats()
    },

    async rejectDrive(id) {
      const token = localStorage.getItem("token")
      const res = await axios.post("http://127.0.0.1:5000/admin/reject-drive",
        { drive_id: id }, { headers: { Authorization: token } })
      alert(res.data.message)
      this.fetchDrives()
    },

    async fetchApplications() {
      const token = localStorage.getItem("token")
      const res = await axios.get("http://127.0.0.1:5000/admin/applications",
        { headers: { Authorization: token } })
      this.applications = res.data
    },

    async search() {
      const token = localStorage.getItem("token")
      const res = await axios.get(
        `http://127.0.0.1:5000/admin/search?q=${this.searchQuery}`,
        { headers: { Authorization: token } })
      this.searchResult = res.data
    },

    logout() {
      localStorage.removeItem("token")
      localStorage.removeItem("role")
      this.$router.push('/login')
    }
  }
}
</script>