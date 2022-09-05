<template>
  <div id="app">
    <header class="card-header">
      <div style="display:flex; flex-direction: column;justify-content: space-between; align-items: flex-end; margin: auto;">
        <div style="display: flex; flex: 100%; justify-content: right">
          <button v-if="logged === 'true'"
                  style="margin: 1%"
                  @click="logOut" class="btn btn-danger btn-lg">
            Log Out
          </button>
          <button v-else
                  style="margin: 1%"
                  @click="GoToLogIn" class="btn btn-secondary btn-lg">
            Log In
          </button>
        </div>
      </div>
    </header>
    <main class="card-body">
      <div class="container">
        <div class="row">
          <div v-for="(everyEvent) in events" :key="everyEvent.id" class="col-lg-4 col-md-6 mb-4">
            <br>
            <div class="card">
              <div class="card-header">
                <h5 class="card-title"> {{ everyEvent.data.TriggerEventName }} </h5>
              </div>
              <div class="card-body">
                <div class="card-text">
                  <h6>{{ everyEvent.time }}</h6>
                  <h6>{{ everyEvent.data }}</h6>
                </div>
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
      message: 'Events',
      events: [],
      logged: 'false',
      modify: 'false',
      username: '',
      token: [],
      user: ''
    }
  },
  methods: {
    getEvents () {
      const path = `https://webhook-ms-example.herokuapp.com/events/${this.username}`
      // const path = `http://127.0.0.1:5000/events/${this.username}`
      axios.get(path, {auth: {username: this.token}})
        .then((res) => {
          this.events = res.data.events
        })
        .catch((error) => {
          console.error(error)
        })
    },
    getUser () {
      const path = `https://webhook-ms-example.herokuapp.com/user/username/${this.username}`
      // const path = `http://127.0.0.1:5000/user/username/${this.username}`

      axios.get(path)
        .then((res) => {
          this.user = res.data.user
        })
        .catch((error) => {
          console.error(error)
        })
    },
    GoToLogIn () {
      this.$router.replace({ path: '/userlogin', query: { } })
    },
    logOut () {
      if (this.logged === 'true') {
        this.logged = 'false'
      }
    }
  },
  created () {
    this.logged = 'false'
    this.logged = this.$route.query.logged
    if (this.logged === 'true') {
      this.username = this.$route.query.username
      this.token = this.$route.query.token
      this.getUser()
    }
    this.getEvents()
  }
}
</script>
