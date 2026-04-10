<template>
  <div class="container mt-4" style="max-width: 500px;">
    <h2 class="mb-4">My Profile</h2>

     <!-- Profile Form  -->
    <div class="card p-4 mb-4">
      <h5 class="mb-3">Profile Details</h5>

      <label>Name</label>
      <input v-model="form.name" class="form-control mb-2" />

      <label>Branch</label>
      <input v-model="form.branch" class="form-control mb-2" />

      <label>CGPA</label>
      <input v-model="form.cgpa" type="number" class="form-control mb-2" />

      <label>Year</label>
      <input v-model="form.year" type="number" class="form-control mb-3" />

      <button class="btn btn-primary w-100" @click="updateProfile">
        Save Profile
      </button>
    </div>

     <!-- Resume Upload  -->
    <div class="card p-4">
      <h5 class="mb-3">Resume Upload</h5>

      <input type="file" @change="fileSelected" class="form-control mb-2" />

      <button class="btn btn-secondary w-100" @click="uploadResume">
        Upload Resume
      </button>

      <p v-if="form.resume" class="mt-2 text-success">
        Current resume: {{ form.resume }}
      </p>
    </div>

    <div class="mt-3">
      <router-link to="/dashboard" class="btn btn-outline-secondary w-100">
        Back to Dashboard
      </router-link>
    </div>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      form: {
        name: '',
        branch: '',
        cgpa: '',
        year: '',
        resume: ''
      },
      file: null
    }
  },

  async mounted() {
    try {
      const token = localStorage.getItem("token")
      const res = await axios.get(
        "http://127.0.0.1:5000/student/profile",
        { headers: { Authorization: token } }
      )
      this.form = res.data
    } catch (err) {
      console.error(err)
    }
  },

  methods: {

    async updateProfile() {
      try {
        const token = localStorage.getItem("token")
        const res = await axios.put(
          "http://127.0.0.1:5000/student/profile",
          this.form,
          { headers: { Authorization: token } }
        )
        alert(res.data.message)
      } catch (err) {
        alert("Update failed ")
      }
    },

    fileSelected(e) {
      this.file = e.target.files[0]
    },

    async uploadResume() {
      try {
        if (!this.file) {
          alert("First, select the file.")
          return
        }
        const token = localStorage.getItem("token")
        const fd = new FormData()
        fd.append("resume", this.file)
        const res = await axios.post(
          "http://127.0.0.1:5000/student/upload-resume",
          fd,
          { headers: { Authorization: token } }
        )
        alert(res.data.message)
        this.form.resume = res.data.filename
      } catch (err) {
        alert("Upload failed ")
      }
    }

  }
}
</script>