<template>

  <div id="app">
    <header class="card-header">
      <h1 style="padding: 0; margin: 0"> Sign in </h1>
    </header>
    <main class="card-body">
      <!-- cart view -->
      <div class="container">
        <div class="row" style="align-items: center; justify-content: center; display: flex">
          <div style="min-width: 400px; margin: 10px; border: 1px solid #ced4da">
            <div class="form-label-group" style="margin: 10px">
              <label for="inputUsername" style="width: 100%; text-align: left">Username</label>
              <input id="inputUsername" class="form-control"
                     placeholder="Username" required autofocus v-model="username">
            </div>

            <div class="form-label-group" style="margin: 10px">
              <br>
              <label for="inputPassword" style="width: 100%; text-align: left">Password</label>
              <input type="password" id="inputPassword" class="form-control"
                     placeholder="Password" required v-model="password">
            </div>
            <div class="form-label-group" style="margin: 10px">
              <button class="btn btn-primary btn-lg"
                      style="width: 100%; margin-bottom: 2%"
                      @click="checkLogin">
                SIGN IN
              </button>
              <br>
              <button class="btn btn-success btn-lg"
                      style="width: 100%; margin-bottom: 2%"
                      @click="addUser">
                ADD USER
              </button>
              <br>
              <button class="btn btn-secondary btn-lg"
                      style="width: 100%; margin-bottom: 2%"
                      @click="backToEvents">
                BACK TO EVENTS
              </button>
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
      username: '',
      password: '',
      user: '',
      find_match: false,
      logged: false,
      token: '',
      is_admin: 0,
      available_money: 0
    }
  },
  methods: {
    backToEvents () {
      this.$router.replace({path: '/', query: { }})
    },
    addUser () {
      this.$router.replace({path: '/addUser', query: { }})
    },
    checkLogin () {
      const parameters = {
        username: this.username,
        password: this.password
      }
      const path = 'https://webhook-ms-example.herokuapp.com/login/'
      // const path = 'http://127.0.0.1:5000/login/'
      axios.post(path, parameters)
        .then((res) => {
          this.logged = true
          this.token = res.data.token
          this.find_match = true
          this.getUser()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.user = ''
          alert('Username or Password incorrect')
        })
    },
    getUser () {
      const path = `https://webhook-ms-example.herokuapp.com/user/username/${this.username}`
      // const path = `http://127.0.0.1:5000/user/username/${this.username}`
      axios.get(path)
        .then((res) => {
          this.user = res.data.user
          this.login()
        })
        .catch((error) => {
          console.error(error)
        })
    },
    login () {
      alert('User Logged Successfully')
      this.$router.replace({path: '/',
        query: {
          username: this.username,
          logged: this.logged,
          token: this.token
        }
      })
    }
  },
  created () {
  }
}
</script>
