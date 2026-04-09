<template>
  <div class="container mt-4">
    <h2 class="text-center mb-4">My Applications</h2>


    <div class="d-flex justify-content-between mb-3">
      <router-link to="/dashboard" class="btn btn-outline-secondary">
        ← Back to Dashboard
      </router-link>

      <button
        class="btn btn-outline-success"
        @click="exportCSV"
        :disabled="exporting"
      >
        {{ exporting ? 'Exporting...' : 'Export to CSV' }}
      </button>
      <div v-if="downloadUrl" class="mt-2">
          <a :href="downloadUrl" 
            download 
            class="btn btn-success">
              Download CSV ⬇️
          </a>
      </div>
    </div>

    # for Export message 
    <p v-if="exportMsg" class="text-info">{{ exportMsg }}</p>

    # Applications Table 
    <table class="table table-bordered table-hover shadow-sm">
      <thead class="table-dark">
        <tr>
          <th>Company</th>
          <th>Job Role</th>
          <th>Status</th>
          <th>Applied On</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="app in applications" :key="app.job_title">
          <td>{{ app.company_name }}</td>
          <td>{{ app.job_title }}</td>
          <td>
            <span class="badge" :class="getStatusClass(app.status)">
              {{ app.status }}
            </span>
          </td>
          <td>{{ app.applied_on }}</td>
        </tr>
      </tbody>
    </table>

    # Empty state 
    <div v-if="applications.length === 0" class="text-center mt-4">
      <p>There is no application right now </p>
    </div>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      applications: [],
      exportMsg: "",
      exporting: false,
      downloadUrl: ""
    }
  },

  async mounted() {
    this.fetchApplications()
  },

  methods: {
    async fetchApplications() {
      try {
        const token = localStorage.getItem("token")
        const res = await axios.post(
          "http://127.0.0.1:5000/student/applications",
          {},
          { headers: { Authorization: token } }
        )
        this.applications = res.data
      } catch (err) {
        console.error(err)
        alert("Error loading applications ")
      }
    },

    getStatusClass(status) {
      if (status === "selected") return "bg-success"
      if (status === "rejected") return "bg-danger"
      if (status === "shortlisted") return "bg-warning text-dark"
      return "bg-secondary"
    },

    async exportCSV() {
      try {
        this.exporting = true
        this.exportMsg = "Export shuru ho raha hai..."
        const token = localStorage.getItem("token")

        const res = await axios.post(
          "http://127.0.0.1:5000/student/export",
          {},
          { headers: { Authorization: token } }
        )

        const taskId = res.data.task_id
        this.exportMsg = "File ban rahi hai, wait karo..."

        const poll = setInterval(async () => {
          const status = await axios.get(
            `http://127.0.0.1:5000/student/task-status/${taskId}`,
            { headers: { Authorization: token } }
          )

          if (status.data.status === "done") {
            this.exportMsg = "CSV ready! File: " + status.data.file
            this.downloadUrl = status.data.download_url
            this.exporting = false
            clearInterval(poll)
          } else if (status.data.status === "FAILURE") {
            this.exportMsg = "Export failed"
            this.exporting = false
            clearInterval(poll)
          }
        }, 2000)

      } catch (err) {
        console.error(err)
        this.exportMsg = "Error durig Export "
        this.exporting = false
      }
    }
  }
}
</script>