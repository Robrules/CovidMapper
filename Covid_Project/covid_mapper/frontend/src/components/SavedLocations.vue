<template>
  <div class="main">
    <div class="flex">
    <section id="saved-locations-group" class="drop-down">
        <div id="label" class="item"> <strong>My Saved Locations</strong></div>
        <b-form-select id="dropdown" v-model="selected" @change="mapSelectedLocation($event)" :options="options" class="item">
          <template #first>
            <b-form-select-option :value="null">-- Select an option from your saved addresses--</b-form-select-option>
          </template>
        </b-form-select>
        <b-dropdown id='dropdown-form-button' variant="light" text="Save Location" no-caret ref="dropdownFormButton" class="item">
            <template #button-content>
              <span style="color:#715c99;">Save New Location +</span>
            </template>
            <b-dropdown-form id="dropdown-form">
                <b-form-group label="List" label-for="dropdown-form-list" @submit.stop.prevent class="form-item">
                <b-form-input
                    list="savedListsAutoComplete"
                    autocomplete="off"
                    id="dropdown-form-list"
                    size="sm"
                    placeholder="List name..."
                ></b-form-input>
                <datalist id="savedListsAutoComplete">
                </datalist>
                </b-form-group>

                <b-form-group label="Location" label-for="dropdown-form-location" class="form-item">
                <b-form-input disabled
                    id="dropdown-form-location"
                    size="sm"
                    placeholder= 'Select a location on the map...'
                ></b-form-input>
                </b-form-group>

                <b-button variant="primary" size="sm" @click="onClick" class="form-item">Add</b-button>
            </b-dropdown-form>
        </b-dropdown>
    </section>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

// Where the lists from the database are stored for formatting the dropdown
var savedLists = new Map()
// Where the listLocations from the database are stored for formatting the dropdown
var savedListLocations = []
// Where the locations from the database are stored for formatting the dropdown
var savedLocations = new Map()

// The array that the HTML template uses for the list autocomplete feature in the dropdown form
var savedListsAutoComplete = []
// The array that the HTML template uses for the saved locations dropdown list
var savedOptions = []

// The currently selected location from the dropdown list
var selected = ''

export default {
  name: 'SavedLocations',
  methods: {
    // GET the users lists, listLocations, locations from the database
    async loadDropdown () {
      if (localStorage.getItem('token') != null) {
        await axios.get('http://localhost:8000/account/user/lists/', {
          headers: {
            'Authorization': 'Token ' + localStorage.getItem('token')
          }
        }).then((getResponse) => {
          for (let i = 0; i < getResponse.data.length; i++) {
            savedLists.set(getResponse.data[i].list_name, getResponse.data[i].list_id)
          }
        }).catch(error => error)
        await axios.get('http://localhost:8000/account/user/listLocations/', {
          headers: {
            'Authorization': 'Token ' + localStorage.getItem('token')
          }
        }).then((getResponse) => {
          for (let i = 0; i < getResponse.data.length; i++) {
            savedListLocations.push({list: getResponse.data[i].list, location: getResponse.data[i].location})
          }
        }).catch(error => error)
        await axios.get('http://localhost:8000/account/user/locations/', {
          headers: {
            'Authorization': 'Token ' + localStorage.getItem('token')
          }
        }).then((getResponse) => {
          for (let i = 0; i < getResponse.data.length; i++) {
            savedLocations.set(getResponse.data[i].location_id, getResponse.data[i].street)
          }
        }).catch(error => error)
        this.fillDropDown()
      }
    },
    // Formats the user's lists and saved locations in the bootstrap vue dropdown list's format for the HTML template
    fillDropDown () {
      // First add the lists to the dropdown
      let savedListsKeys = [...savedLists.keys()]
      for (let i = 0; i < savedListsKeys.length; i++) {
        var list = {label: savedListsKeys[i], options: []}
        savedListsAutoComplete.push(savedListsKeys[i])
        savedOptions.push(list)
      }
      // Fill the array for the list autocomplete feature in the dropdown form
      var element = document.getElementById('savedListsAutoComplete')
      savedListsAutoComplete.forEach(function (item) {
        var option = document.createElement('option')
        option.value = item
        element.appendChild(option)
      })
      // Add the options (locations) for each list
      for (let i = 0; i < savedListLocations.length; i++) {
        for (let j = 0; j < savedListsKeys.length; j++) {
          if (savedListLocations[i].list === savedLists.get(savedListsKeys[j])) {
            let savedLocationKeys = [...savedLocations.keys()]
            for (let k = 0; k < savedLocationKeys.length; k++) {
              if (savedListLocations[i].location === savedLocationKeys[k]) {
                var option = {value: savedLocations.get(savedLocationKeys[k]), text: savedLocations.get(savedLocationKeys[k])}
                savedOptions[j].options.push(option)
              }
            }
          }
        }
      }
    },
    // Emits an event that a location from the dropdown list has been selected (So that the map in Home.vue can receive the event)
    mapSelectedLocation (event) {
      selected = document.getElementById('dropdown').value
      this.$emit('selectionMade', document.getElementById('dropdown').value)
    },
    // Behaviour of the dropdown form when the 'add' button is clicked
    async onClick () {
      var listName = document.getElementById('dropdown-form-list').value
      var street = document.getElementById('dropdown-form-location').value
      if (listName === '' || street === '') {
        alert('List name or Location field is empty!')
        return
      }
      var invalid = false
      var listId = -1
      var locationId = -1
      var userId = -1
      // Get the UID of the current user
      await axios.get('http://localhost:8000/account/user/current/',
        {
          headers: {
            'Authorization': 'Token ' + localStorage.getItem('token')
          }
        }).then((getResponse) => {
        userId = getResponse.data.user_id
      }).catch(error => error)
      // Check if location is already in database
      await axios.get('http://localhost:8000/account/user/locations/?street=' + street,
        {
          headers: {
            'Authorization': 'Token ' + localStorage.getItem('token')
          }
        }).then((getResponse) => {
        if (getResponse.data !== []) {
          locationId = getResponse.data[0].location_id
        }
      }).catch(error => error)
      // Check if list is already in database
      await axios.get('http://localhost:8000/account/user/lists/?list_name=' + listName,
        {
          headers: {
            'Authorization': 'Token ' + localStorage.getItem('token')
          }
        }).then((getResponse) => {
        if (getResponse.data !== []) {
          listId = getResponse.data[0].list_id
        }
      }).catch(error => error)
      // list and location both exist!
      if (listId !== -1 && locationId !== -1) {
        console.log('list and location both exist!')
        // See if the location is already in the selected list
        await axios.get('http://localhost:8000/account/user/listLocations/?list=' + listId + '&location=' + locationId,
          {
            headers: {
              'Authorization': 'Token ' + localStorage.getItem('token')
            }
          }).then((getResponse) => {
          if (getResponse.data.length > 0) {
            alert('This location already exists in this list!')
            invalid = true
          }
        }).catch(error => error)
        // Abort if listLocation already exists
        if (invalid) {
          return
        }
        // POST new listLocation object
        await axios.post('http://localhost:8000/account/user/listLocations/',
          {
            list: listId,
            location: locationId
          },
          {
            headers: {
              'Authorization': 'Token ' + localStorage.getItem('token')
            }
          }).catch(error => error)
        // Add the new option to the dropdown list
        for (let i = 0; i < savedOptions.length; i++) {
          if (savedOptions[i].label === listName) {
            savedOptions[i].options.push({value: street, text: street})
            break
          }
        }
        // list exists!
      } else if (listId !== -1 && locationId === -1) {
        console.log('list exists!')
        // POST the new location object
        await axios.post('http://localhost:8000/account/user/locations/',
          {
            street: street
          },
          {
            headers: {
              'Authorization': 'Token ' + localStorage.getItem('token')
            }
          }).then((getResponse) => {
          locationId = getResponse.data.location_id
        }).catch(error => error)
        // POST the new listLocation object
        await axios.post('http://localhost:8000/account/user/listLocations/',
          {
            list: listId,
            location: locationId
          },
          {
            headers: {
              'Authorization': 'Token ' + localStorage.getItem('token')
            }
          }).catch(error => error)
        // Add the new option to the dropdown list
        for (let i = 0; i < savedOptions.length; i++) {
          if (savedOptions[i].label === listName) {
            savedOptions[i].options.push({value: street, text: street})
            break
          }
        }
        // location exists!
      } else if (listId === -1 && locationId !== -1) {
        console.log('location exists!')
        // POST the new List object
        await axios.post('http://localhost:8000/account/user/lists/',
          {
            list_name: listName,
            user: userId
          },
          {
            headers: {
              'Authorization': 'Token ' + localStorage.getItem('token')
            }
          }).then((getResponse) => {
          listId = getResponse.data.list_id
        }).catch(error => error)
        // POST the new listLocation object
        await axios.post('http://localhost:8000/account/user/listLocations/',
          {
            list: listId,
            location: locationId
          },
          {
            headers: {
              'Authorization': 'Token ' + localStorage.getItem('token')
            }
          }).catch(error => error)
        // Add the new option to the dropdown list
        savedOptions.push({
          label: listName,
          options: [
            {value: street, text: street}
          ]
        })
        // Creating new list and location as they were not found in the database
      } else if (listId === -1 && locationId === -1) {
        console.log('creating new list and location')
        // POST the new List object
        await axios.post('http://localhost:8000/account/user/lists/',
          {
            list_name: listName,
            user: userId
          },
          {
            headers: {
              'Authorization': 'Token ' + localStorage.getItem('token')
            }
          }).then((getResponse) => {
          listId = getResponse.data.list_id
        }).catch(error => error)
        // POST the new Location object
        await axios.post('http://localhost:8000/account/user/locations/',
          {
            street: street
          },
          {
            headers: {
              'Authorization': 'Token ' + localStorage.getItem('token')
            }
          }).then((getResponse) => {
          locationId = getResponse.data.location_id
        }).catch(error => error)
        // POST the new listLocation object
        await axios.post('http://localhost:8000/account/user/listLocations/',
          {
            list: listId,
            location: locationId
          },
          {
            headers: {
              'Authorization': 'Token ' + localStorage.getItem('token')
            }
          }).catch(error => error)
        // Add the new option to the dropdown list
        savedOptions.push({
          label: listName,
          options: [
            {value: street, text: street}
          ]
        })
      }
      // Clear and close the dropdown form
      document.getElementById('dropdown-form-list').value = ''
      this.$refs.dropdownFormButton.hide(true)
      selected = street
    }
  },
  // Takes in the authorization token as an argument and stores it in local storage
  putToken (arg) {
    localStorage.setItem('token', arg)
  },
  // Takes in the location name of the map marker as an argument and puts it in the 'Location' input of the form
  putLocationInForm (arg) {
    document.getElementById('dropdown-form-location').value = arg
  },
  // Returns the current selected options, and a list of all options for the dropdown list
  data () {
    return {
      selected: selected,
      options: savedOptions
    }
  },
  mounted () {
    this.loadDropdown()
  }
}
</script>

<style scoped>

.main {
  position: relative;
}

#saved-locations-group {
  display: grid;
  width: relative;
  column-gap: 50px;
  align-self: center;
  align-content: center;
  justify-content: center;
  top: 50%;
  left: 50%;
  margin-top: 50px;
}
.item {
  align-self: center;
  height: 40px;
  width: 100%;
}

#label {
  position: relative;
  grid-column-start: 1;
  grid-column-end: 4;
  grid-row-start: 1;
  grid-row-end: 1;
}

#dropdown {
  position: relative;
  grid-column-start: 1;
  grid-column-end: 2;
  grid-row-start: 2;
  grid-row-end: 2;
}

#dropdown-form {
  width: 300px;
  grid-column-start: 2;
  grid-column-end: 3;
  grid-row-start: 2;
  grid-row-end: 2;
}

.form-item {
    padding-top: 10px;
    padding-bottom: 10px;
}
</style>
