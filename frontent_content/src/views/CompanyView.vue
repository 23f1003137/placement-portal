<template>
  <div class="container mt-4">

    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Company Dashboard</h2>
    </div>

    <ul class="nav nav-tabs mb-4">
      <li class="nav-item">
        <button class="nav-link" :class="activeTab === 'drives' ? 'active' : ''"
          @click="activeTab = 'drives'">My Drives</button>
      </li>
      <li class="nav-item">
        <button class="nav-link" :class="activeTab === 'create' ? 'active' : ''"
          @click="activeTab = 'create'">Create Drive</button>
      </li>
    </ul>

     <!-- My Drives Tab  -->
    <div v-if="activeTab === 'drives'">
      <div v-if="drives.length === 0" class="text-muted">
       There is no drive — first, create a drive.
      </div>

      <div v-for="drive in drives" :key="drive.id" class="card shadow-sm mb-4">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h5 class="mb-0">{{ drive.job_title }}</h5>
          <div class="d-flex gap-2 align-items-center">
            <span class="badge" :class="getStatusClass(drive.status)">
              {{ drive.status }}
            </span>
            <button v-if="drive.status === 'approved'"
              class="btn btn-sm btn-danger" @click="closeDrive(drive.id)">
              Close Drive
            </button>
          </div>
        </div>

        <div class="card-body">
          <div class="row mb-2">
            <div class="col-md-6">
              <p class="mb-1"><b>Branch:</b> {{ drive.branch_required }}</p>
              <p class="mb-1"><b>Min CGPA:</b> {{ drive.cgpa_required }}</p>
              <p class="mb-1"><b>Year:</b> {{ drive.year_required }}</p>
            </div>
            <div class="col-md-6">
              <p class="mb-1"><b>Salary:</b> {{ drive.salary }}</p>
              <p class="mb-1"><b>Deadline:</b> {{ drive.deadline }}</p>
              <p class="mb-1">
                <b>Total Applicants:</b>
                <span class="badge bg-primary ms-1">{{ drive.total_applicants }}</span>
              </p>
            </div>
          </div>

          <button class="btn btn-outline-primary btn-sm" @click="toggleDrive(drive.id)">
            {{ openDrive === drive.id ? 'Hide Applicants ▲' : 'View Applicants ▼' }}
          </button>

          <div v-if="openDrive === drive.id" class="mt-3">
            <div v-if="drive.applicants.length === 0" class="text-muted">
              Koi applicant nahi hai
            </div>

            <div v-for="app in drive.applicants" :key="app.application_id"
              class="card p-3 mb-2 border-secondary">
              <div class="row">
                <div class="col-md-8">
                  <h6>{{ app.student_name }}</h6>
                  <p class="mb-1"><b>Email:</b> {{ app.student_email }}</p>
                  <p class="mb-1"><b>Branch:</b> {{ app.branch }}</p>
                  <p class="mb-1"><b>CGPA:</b> {{ app.cgpa }}</p>
                  <p class="mb-1"><b>Year:</b> {{ app.year }}</p>
                  <p class="mb-1">
                    <b>Status:</b>
                    <span class="badge ms-1" :class="getAppStatusClass(app.status)">
                      {{ app.status }}
                    </span>
                  </p>
                </div>
                <div class="col-md-4 text-end">
                  <div class="mb-2">
                    <a v-if="app.resume"
                      :href="'http://127.0.0.1:5000/uploads/' + app.resume"
                      target="_blank" class="btn btn-sm btn-outline-secondary">
                      View Resume
                    </a>
                    <span v-else class="text-muted">No Resume</span>
                  </div>
                  <div class="d-flex flex-column gap-1">
                    <button class="btn btn-success btn-sm"
                      @click="updateStatus(app.application_id, 'selected')">
                      Select
                    </button>
                    <button class="btn btn-warning btn-sm"
                      @click="updateStatus(app.application_id, 'shortlisted')">
                      Shortlist
                    </button>
                    <button class="btn btn-danger btn-sm"
                      @click="updateStatus(app.application_id, 'rejected')">
                      Reject
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Drive Tab  -->
    <div v-if="activeTab === 'create'">
      <div class="card p-4 shadow">
        <h3 class="mb-3">Create New Drive</h3>

        <label class="fw-bold">Job Title</label>
        <input v-model="job_title" placeholder="e.g. Software Engineer"
          class="form-control mb-2" />

        <label class="fw-bold">Job Description</label>
        <textarea v-model="job_description" placeholder="Job description..."
          class="form-control mb-2" rows="3"></textarea>

        <label class="fw-bold">Branch Required</label>
        <select v-model="branch" class="form-control mb-2">
          <option value="">-- Select Branch --</option>
          <option value="CSE">CSE</option>
          <option value="ECE">ECE</option>
          <option value="ME">ME</option>
          <option value="CE">CE</option>
          <option value="EE">EE</option>
          <option value="IT">IT</option>
        </select>

        <label class="fw-bold">Minimum CGPA</label>
        <input v-model="cgpa" type="number" step="0.1" min="0" max="10"
          placeholder="e.g. 7.5" class="form-control mb-2" />

        <label class="fw-bold">Year Required</label>
        <select v-model="year" class="form-control mb-2">
          <option value="">-- Select Year --</option>
          <option value="1">1st Year</option>
          <option value="2">2nd Year</option>
          <option value="3">3rd Year</option>
          <option value="4">4th Year</option>
        </select>

        <label class="fw-bold">Salary Package</label>
        <input v-model="salary" placeholder="e.g. 6 LPA or 50,000/month"
          class="form-control mb-2" />

        <label class="fw-bold">Application Deadline</label>
        <input v-model="deadline" type="date" class="form-control mb-3" />

        <button class="btn btn-primary w-100" @click="createDrive">
          Create Drive
        </button>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      activeTab: 'drives',
      drives: [],
      openDrive: null,
      job_title: '',
      job_description: '',
      branch: '',
      cgpa: '',
      year: '',
      salary: '',
      deadline: ''
    }
  },

  async mounted() {
    await this.fetchDrives()
  },

  methods: {

    async fetchDrives() {
      try {
        const token = localStorage.getItem("token")
        const res = await axios.get(
          "http://127.0.0.1:5000/company/my-drives",
          { headers: { Authorization: token } }
        )
        this.drives = res.data
      } catch (err) {
        console.error(err)
        alert("The drives did not load")
      }
    },

    toggleDrive(driveId) {
      this.openDrive = this.openDrive === driveId ? null : driveId
    },

    async createDrive() {
      try {
        if (!this.job_title || !this.branch || !this.cgpa ||
            !this.year || !this.deadline) {
          alert("All fields are required!")
          return
        }
        const token = localStorage.getItem("token")
        const res = await axios.post(
          "http://127.0.0.1:5000/company/create-drive",
          {
            job_title: this.job_title,
            job_description: this.job_description,
            branch: this.branch,
            cgpa: parseFloat(this.cgpa),
            year: parseInt(this.year),
            salary: this.salary,
            deadline: this.deadline
          },
          { headers: { Authorization: token } }
        )
        if (res.data.error) {
          alert(res.data.error)
          return
        }
        alert("Drive created! Waiting for admin approval ")
        this.job_title = ''
        this.job_description = ''
        this.branch = ''
        this.cgpa = ''
        this.year = ''
        this.salary = ''
        this.deadline = ''
        this.activeTab = 'drives'
        await this.fetchDrives()
      } catch (err) {
        console.error(err)
        alert("The drive was not created")
      }
    },

    async updateStatus(appId, status) {
      try {
        const token = localStorage.getItem("token")
        const res = await axios.post(
          "http://127.0.0.1:5000/company/update-status",
          { application_id: appId, status: status },
          { headers: { Authorization: token } }
        )
        alert(res.data.message)
        await this.fetchDrives()
      } catch (err) {
        console.error(err)
        alert("Status not updated.")
      }
    },

    async closeDrive(driveId) {
      if (!confirm("Do you want to close the drive?")) return
      try {
        const token = localStorage.getItem("token")
        const res = await axios.post(
          "http://127.0.0.1:5000/company/close-drive",
          { drive_id: driveId },
          { headers: { Authorization: token } }
        )
        alert(res.data.message)
        await this.fetchDrives()
      } catch (err) {
        console.error(err)
        alert("The drive did not close. ")
      }
    },

    getStatusClass(status) {
      if (status === "approved") return "bg-success"
      if (status === "pending") return "bg-warning text-dark"
      if (status === "rejected") return "bg-danger"
      if (status === "closed") return "bg-secondary"
      return "bg-secondary"
    },

    getAppStatusClass(status) {
      if (status === "selected") return "bg-success"
      if (status === "rejected") return "bg-danger"
      if (status === "shortlisted") return "bg-warning text-dark"
      return "bg-secondary"
    },

    logout() {
      localStorage.removeItem("token")
      localStorage.removeItem("role")
      this.$router.push('/login')
    }
  }
}
</script>