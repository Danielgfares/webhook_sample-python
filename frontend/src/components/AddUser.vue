<template>
  <div id="app">
    <header class="card-header">
      <h1 style="padding: 0; margin: 0"> Add User </h1>
    </header>
    <main class="card-body">
      <!-- cart view -->
      <div class="container">
        <div class="row" style="align-items: start; justify-content: start; display: flex">
          <div>
            <button class="btn btn-secondary btn-lg"
                    style="margin-bottom: 2%"
                    @click="goToLogIn">Go Back
            </button>
          </div>
        </div>
        <div class="row" style="align-items: center; justify-content: center; display: flex">
          <div style="min-width: 400px; margin: 10px; border: 1px solid #ced4da">
            <div class="form-label-group" style="margin: 10px">
              <div>
                <b-form @submit="onSubmit" @reset="onReset" v-if="show">
                  <b-form-group id="input-group-1" label="Username:" label-for="input-1">
                    <b-form-input
                      id="input-1"
                      v-model="addUserForm.username"
                      placeholder="Enter username"
                      required
                    ></b-form-input>
                  </b-form-group>

                  <b-form-group id="input-group-2" label="Password:" label-for="input-2">
                    <b-form-input
                      id="input-2"
                      type="password"
                      v-model="addUserForm.password"
                      placeholder="Enter password"
                      required
                    ></b-form-input>
                  </b-form-group>

                  <b-form-group id="input-group-3" label="Email:" label-for="input-3">
                    <b-form-input
                      id="input-3"
                      v-model="addUserForm.useremail"
                      placeholder="Enter email"
                      required
                    ></b-form-input>
                  </b-form-group>

                  <b-button type="submit" variant="primary" @click="checkCreate">Submit</b-button>
                  <b-button type="reset" variant="danger" @click="onReset">Reset</b-button>
                </b-form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
    <footer class="card-footer">
    </footer>
  </div>

</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      addUserForm: {
        username: '',
        password: '',
        useremail: ''
      },
      show: true,
      modify: false,
      token: []
    }
  },
  methods: {
    onSubmit (event) {
      event.preventDefault()
    },
    initForm () {
      this.addUserForm.username = ''
      this.addUserForm.password = ''
      this.addUserForm.useremail = ''
    },
    goToLogIn () {
      this.$router.replace({ path: '/userlogin', query: { } })
    },
    checkCreate () {
      const parameters = {
        username: this.addUserForm.username,
        password: this.addUserForm.password,
        email: this.addUserForm.useremail,
        telephone: this.addUserForm.telephone
      }
      const path = 'https://webhook-ms-example.herokuapp.com/user/'
      //const path = 'http://127.0.0.1:5000/user/'
      axios.post(path, parameters)
        .then((res) => {
          this.user = res.data.user
          alert('User created successfully!')
          this.goToLogIn()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.user = ''
          alert(error.response.data.message)
        })
    },
    onReset (event) {
      event.preventDefault()
      // Reset our form values
      this.addUserForm.username = ''
      this.addUserForm.password = ''
      this.addUserForm.useremail = ''
      this.show = false
      this.$nextTick(() => {
        this.show = true
      })
    }
  },
  created () {
  }
}
</script>
