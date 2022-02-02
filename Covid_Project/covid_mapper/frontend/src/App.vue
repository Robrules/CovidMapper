<template>
  <div id="app">
    <!--Navbar Here -->
    <div class="layout">
        <h1 class="heading"> COVID MAPPER</h1>
        <div id="align" class="menu">
           <div @click = 'openRiskModal' class="text-block">
            <p>What is the risk factor?</p>
            <div id="riskModal" class="modal">
                <!-- Modal content -->
              <div class="modal-content">
                <p class="title">Risk Factor</p>
                <p class="risk-explanation"> The <strong>COVID-19 Risk Factor</strong> is a metric created by our
                    team used to represent the risk of communities or individuals catching and spreading COVID-19. <br> <br>
                    It is determined by the <strong>weekly case numbers</strong> in an Local Government Area (LGA)
                     and the <strong>second vaccination dose rate</strong> of the LGA <br> <br> High weekly case numbers and a low second dose rate will result in a <strong>higher</strong> risk factor,
                     while lower weekly case numbers and a high second dose rate will result in a <strong>lower</strong> risk factor.</p>
              </div>
            </div>
          </div>
            <div v-show='isLoggedIn === false' @click = 'openLoginModal' class="white-box">
                <div>Login</div>
                <!-- The Modal -->
              <div id="loginModal" class="modal">

                <!-- Modal content -->
                <div class="modal-content">
                  <p class="title">Log In</p>
                  <p class="headingM">Username</p>
                    <!-- username inputbox-->
                    <div>
                      <input class="username-box" type="text" v-model="username" />
                    </div>
                    <p class="headingM">Password</p>
                    <!-- password inputbox -->
                    <div>
                      <input class="password-box" ref="input" type="password" v-model="password" />
                    </div>
                    <div>
                      <button @click='login' class = 'loginb' type="button">Log In</button>
                    </div>
                </div>
            </div>
            </div>
            <div v-show='isLoggedIn === false' @click = 'openSignupModal' class="white-box1">
                <div>Sign Up</div>
                <div id="signupModal" class="modal">

                <!-- Modal content -->
                  <div class="modal-content">
                    <p class="title">Sign Up</p>
                    <p class="headingM">Username</p>
                      <!-- username inputbox-->
                      <div>
                        <input class="username-box" type="text" v-model="username" />
                      </div>
                      <p class="headingM">Email</p>
                      <!-- email inputbox-->
                      <div>
                        <input class="email-box" type="text" v-model="email" />
                      </div>
                      <p class="headingM">Password</p>
                      <!-- password inputbox -->
                      <div>
                        <input class="password-box" ref="input" type="password" v-model="password1" />
                      </div>

                      <p class="headingM">Confirm Password</p>
                      <!-- password inputbox -->
                      <div>
                        <input class="password-box" ref="input" type="password" v-model="password2" />
                      </div>

                      <div>
                        <button @click='signup' class = 'signupb' type="button">Sign up</button>
                      </div>
                    </div>
                </div>
            </div>
          <div v-show='isLoggedIn === true' class='whitebox'>
            <button @click="logout" class='logoutb' type='button'>Log out</button>
          </div>

        </div>
    </div>
    <!--Index Page Here -->
    <div class='flex'>
      <Home/>
    </div>
    <footer>
  <p>COVID MAPPER data is collected from verified state and federal health departments</p>
</footer>
  </div>
</template>

<script>
import SavedLocations from './components/SavedLocations.vue'
import Home from './components/Home.vue'
import pubsub from 'pubsub-js'
/* eslint-disable */

window.onclick = function (event) {
  var loginModal = document.getElementById('loginModal')
  var signupModal = document.getElementById('signupModal')
  var riskModal = document.getElementById('riskModal')
  if (event.target === loginModal || event.target === signupModal || event.target === riskModal) {
    loginModal.style.display = 'none'
    signupModal.style.display = 'none'
    riskModal.style.display = 'none'
  }
}

export default {
  name: 'App',
  data () {
    var loggedIn
    if (localStorage.getItem('token') != null) {
      loggedIn = true
    } else {
      loggedIn = false
    }
    return {
      isLoggedIn: loggedIn,
      username: '',
      password: '',
      email: '',
      password1: '',
      password2: ''
    }
  },
  components: {
    Home, SavedLocations
  },
  methods: {
    openLoginModal () {
      var modal = document.getElementById('loginModal')
      modal.style.display = 'block'
    },
    openSignupModal () {
      var modal = document.getElementById('signupModal')
      modal.style.display = 'block'
    },
    openRiskModal () {
      var modal = document.getElementById('riskModal')
      modal.style.display = 'block'
    },
    closeModal () {
      var modal = document.getElementById('loginModal')
      modal.style.display = 'none'
    },
    login () {
      this.$axios.post('account/login/', {
        username: this.username,
        password: this.password
      })
        .then((response) => {
          alert('Logged in')
          pubsub.publish('login', true)
          localStorage.setItem('token', response.data.key)
          SavedLocations.putToken(response.data.key)
          this.$router.go(0)
        })
        .catch((reason) => {
          alert('Failed to login: ' + JSON.stringify(reason.response.data))
        })
    },
    signup () {
      this.$axios.post('account/register/', {
        username: this.username,
        email: this.email,
        password1: this.password1,
        password2: this.password2
      })
        .then((response) => {
          alert('Signed up, please confirm your email', response)
          pubsub.publish('disablessignup', true)
          localStorage.setItem('token', response.data.key)
          this.$router.go(0)
        })
        .catch((reason) => {
          alert('Failed to sign up: ' + JSON.stringify(reason.response.data))
        })
    },
    logout () {
      this.$axios.post('account/logout/', {
        headers: {
          'Authorization': 'Token ' + localStorage.getItem('token')
        }
      })
        .then((response) => {
          alert('Logged out', response)
          pubsub.publish('logout', false)
          localStorage.removeItem('token')
          this.$router.go(0)
        })
        .catch((reason) => {
          alert('Failed to log out: ' + JSON.stringify(reason.response.data))
        })
    }
  },
  mounted () {
    this.loginPID = pubsub.subscribe('login', (msgName, data) => {
      this.isLoggedIn = data
      localStorage.setItem('isLoggedIn', this.isLoggedIn)
      console.log(msgName)
    })
    this.logoutPID = pubsub.subscribe('logout', (msgName, data) => {
      this.isLoggedIn = data
      console.log(msgName)
      localStorage.removeItem('isLoggedIn')
    })
    this.signupPID = pubsub.subscribe('signup', (msgName, data) => {
      this.isLoggedIn = data
      console.log(msgName)
      localStorage.setItem('isLoggedIn', this.isLoggedIn)
    })
  },
  beforeDestroy () {
    pubsub.unsubscribe(this.loginPID)
    pubsub.unsubscribe(this.logoutPID)
    pubsub.unsubscribe(this.signupPID)
  }
}
</script>

<style scoped>

.layout {
    display: -ms-grid;
    display: grid;
    grid-auto-columns: 1fr;
    -ms-grid-columns: 1fr 1fr;
    grid-template-columns: 1fr 1fr;

    padding: 10px;
    -ms-grid-rows: auto;
    grid-template-rows: auto;
    background-color: #c9b9e6;
}

.heading {
    margin-bottom: 20px;
}

.white-box {
    display: flex;
    padding: 10px;
    -ms-flex-direction: column;
    flex-direction: column;
    border-radius: 7px;
    background-color: #fff;
    transition: box-shadow 200ms ease;
    text-align: center;
}

.white-box1{
    margin-left: 10px;
    display: flex;
    padding: 10px;
    -ms-flex-direction: column;
    flex-direction: column;
    border-radius: 7px;
    background-color: #fff;
    transition: box-shadow 200ms ease;
    text-align: center;
}

.white-box:hover, .white-box1:hover {
    box-shadow: 1px 1px 3px 0 #000;
    cursor: pointer;
}

.menu {
    display: flex;
    padding-left: 10px;
    align-items: center;
    border-left: 1px solid #000;
}

.text-block {
    margin-right: 16px;
    margin-top: 15px;
    text-align: center;
}

.text-block:hover {
  cursor: pointer;
}

#align {
    -ms-grid-column-align: end;
    justify-self: end;
}

/* The Modal (background) */
.modal {
  display: none; /* Hidden by default */
  position: fixed; /* Stay in place */
  z-index: 1; /* Sit on top */
  padding-top: 100px; /* Location of the box */
  left: 0;
  top: 0;
  width: 100%; /* Full width */
  height: 100%; /* Full height */
  overflow: auto; /* Enable scroll if needed */
  background-color: rgb(0,0,0); /* Fallback color */
  background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
}

.title {
  font-family: "Arial";
  font-size: 24px;
  font-weight: 500;
  line-height: normal;
  color: black;
  margin-bottom: 25px;
  text-align: center;
  color: dimgray;
}

.username-box, .password-box, .email-box {
  width: 396px;
  height: 32px;
  background-color: white;
  margin-bottom: 20px;
  border-radius: 4px;
  border: 2px solid linen;
}

.headingM, .risk-explanation {
  font-family: "Arial";
  font-size: 16px;
  font-weight: 500;
  line-height: normal;
  color: dimgray;
  margin-bottom: 9px;
  display: inline-block;
}

.loginb, .signupb {
  border: 2px solid linen;
  background-color: white;
  font-size: 16px;
  height: 40px;
  color: dimgray;
  font-family: "Arial";
  font-weight: 500;
  line-height: normal;
  transition: box-shadow 200ms ease;
}

.loginb:hover, .signupb:hover{
  box-shadow: 1px 1px 3px 0 #000;
}

/* Modal Content */
.modal-content {
  background-color: #fefefe;
  margin: auto;
  padding: 20px;
  border: 3px solid #c9b9e6;
  width: 50%;
}

/* The Close Button */
.close {
  color: #aaaaaa;
  float: right;
  justify-content: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: #000;
  text-decoration: none;
  cursor: pointer;
}

footer {
  text-align: right;
  padding: 3px;
  background-color: #c9b9e6;
  color: black;
}

.flex {
  align-content: flex-end;
  justify-content: flex-end;
}

</style>
