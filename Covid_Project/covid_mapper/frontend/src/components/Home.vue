<template>
  <div class="main">
    <div v-show='isLoggedIn === true' class='LocationListWrapper'>
      <SavedLocations v-on:selectionMade="focusLocationFromSaved"/>
    </div>
    <div class="flex">
      <div class = "legend">
        <dl>
          <dt class="green"></dt>
          <dd>Very Low Risk</dd>
          <dt class="blue"></dt>
          <dd>Low Risk</dd>
          <dt class="orange"></dt>
          <dd>Medium Risk</dd>
          <dt class="red"></dt>
          <dd>High Risk</dd>
          </dl>
        </div>
      <!-- Map Display here -->
      <div class="map-holder">
        <div id="map"></div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import SavedLocations from './SavedLocations.vue'
import mapboxgl from 'mapbox-gl'
import MapboxGeocoder from '@mapbox/mapbox-gl-geocoder'
import '@mapbox/mapbox-gl-geocoder/dist/mapbox-gl-geocoder.css'

// The location that is displayed in the search bar after search

const lowRiskIds = []
const mediumRiskIds = []
const highRiskIds = []

var map = null
var geocoder = null
// The marker that will be positioned depending on the selected location
const marker = new mapboxgl.Marker({
  color: '#F84C4C'
})

export default {
  name: 'Home',
  components: {
    SavedLocations
  },
  data () {
    var loggedIn
    if (localStorage.getItem('token') != null) {
      loggedIn = true
    } else {
      loggedIn = false
    }
    return {
      loading: false,
      location: '',
      access_token: 'pk.eyJ1Ijoicm9iZXJ0YmFubmF5YW4iLCJhIjoiY2t2OTFrNTl6Mjl0eDJ2bDA3Y3czMzhjayJ9.FiTpd8qaCGjXUFRrqO1shw',
      center: [0, 0],
      map: {},
      isLoggedIn: loggedIn
    }
  },
  methods: {
    // Called when a saved location is selected
    async focusLocationFromSaved () {
      SavedLocations.putLocationInForm(SavedLocations.data().selected)
      var urlString = 'https://api.mapbox.com/geocoding/v5/mapbox.places/' + SavedLocations.data().selected + '.json?types=poi,address&access_token=' + this.access_token + '&limit=1'
      await axios.get(urlString).then((getResponse) => {
        // Map camera flies to the new selected location
        map.flyTo({
          center: getResponse.data.features[0].geometry.coordinates,
          zoom: 15,
          bearing: 0,
          essential: true
        })
        // Marker is put down
        marker.setLngLat([
          getResponse.data.features[0].geometry.coordinates[0],
          getResponse.data.features[0].geometry.coordinates[1]
        ])
        marker.addTo(map)
        geocoder.clear()
      }).catch(error => error)
    },
    // Called when a location is selected using mouse
    focusLocationFromCoordinates (lng, lat) {
      if (lng != null && lat != null) {
        // Map camera flies to the new selected location
        map.flyTo({
          center: {lng, lat},
          zoom: 15,
          bearing: 0,
          essential: true
        })
        // Put down marker
        marker.setLngLat([
          lng,
          lat
        ])
        marker.addTo(map)
        try {
          this.loading = true
          var urlString = 'https://api.mapbox.com/geocoding/v5/mapbox.places/' + String(lng) + ',' + String(lat) + '.json?access_token=' + this.access_token
          axios.get(urlString).then((getResponse) => {
            // Display the location in the save form
            SavedLocations.putLocationInForm(getResponse.data.features[0].place_name)
            // Display the search bar autocomplete list for user to confirm the address
            geocoder.setInput(getResponse.data.features[0].place_name)
          }).catch(error => error)
          this.loading = false
        } catch (err) {
          this.loading = false
          console.log(err)
        }
      }
    },
    createMap () {
      this.getData()
      if (lowRiskIds.length === 0) {
        // eslint-disable-next-line
        lowRiskIds.push("")
      }
      if (mediumRiskIds.length === 0) {
        // eslint-disable-next-line
        mediumRiskIds.push(" ")
      }
      if (highRiskIds.length === 0) {
        // eslint-disable-next-line
        highRiskIds.push("  ")
      }
      try {
        this.accessToken = 'pk.eyJ1Ijoicm9iZXJ0YmFubmF5YW4iLCJhIjoiY2t2OTFrNTl6Mjl0eDJ2bDA3Y3czMzhjayJ9.FiTpd8qaCGjXUFRrqO1shw'
        mapboxgl.accessToken = this.access_token
        // Initialising the map
        map = new mapboxgl.Map({
          container: 'map',
          style: 'mapbox://styles/mapbox/streets-v11',
          center: [147, -32],
          zoom: 5.5,
          maxBounds: [[139, -38], [155, -27]],
          marker: false
        })
        // Initialising the geocoder
        geocoder = new MapboxGeocoder({
          accessToken: this.access_token,
          // Limit seach results to Australia.
          countries: 'au',
          // Remove default map marker (replaced with custom one later)
          marker: false,
          // Close autocomplete dropdown list upon selection
          keepOpen: false,
          // Use a bounding box to further limit results
          // to the geographic bounds representing the
          // region of New South Wales.
          bbox: [139.965, -38.03, 155.258, -27.839],

          // Apply a client-side filter to further limit results
          // to those strictly within the New South Wales region.
          filter: function (item) {
            // returns true if item contains New South Wales region
            return item.context.some((i) => {
              // ID is in the form {index}.{id} per https://github.com/mapbox/carmen/blob/master/carmen-geojson.md
              // This example searches for the `region`
              // named `New South Wales`.
              return (
                i.id.split('.').shift() === 'region' && i.text === 'New South Wales'
              )
            })
          },
          mapboxgl: mapboxgl
        })
        map.addControl(geocoder)
        map.on('load', () => {
          map.addSource('lgas', {
            'type': 'geojson',
            'data': './static/lga_2019_nsw_simplified.json'
          })
          map.addLayer({
            'id': 'lga-fill',
            'type': 'fill',
            'source': 'lgas', // reference the data source
            'layout': {},
            'paint': {
              'fill-color': [
                'match',
                ['get', 'LGA_CODE19'],
                lowRiskIds,
                '#4267ad',
                mediumRiskIds,
                '#e3b418',
                highRiskIds,
                '#ff2424',
                '#4fc946'
              ],
              'fill-opacity': 0.5
            }
          })
          // Behaviour when user searches a location in the search bar
          geocoder.on('result', (event) => {
            // Put in SavedLocations dropdown form location input
            SavedLocations.putLocationInForm(event.result.place_name)
            // Put down marker
            marker.setLngLat([
              event.result.geometry.coordinates[0],
              event.result.geometry.coordinates[1]
            ])
            marker.addTo(map)
          })
          map.on('click', (event) => {
            // Put in SavedLocations dropdown form location input
            this.focusLocationFromCoordinates(event.lngLat.lng, event.lngLat.lat)
          })
          // Add a black outline around the polygon.
          map.addLayer({
            'id': 'outline',
            'type': 'line',
            'source': 'lgas',
            'layout': {},
            'paint': {
              'line-color': '#000',
              'line-width': 1
            }
          })
        })
      } catch (error) {
        console.log(error)
      }
    },
    getData () {
      axios.get('https://api.covidmapper.tavitian.cloud/cases')
        .then(function (response) {
          Object.keys(response.data).forEach(function (lga) {
            const secondDose = response.data[lga].percPopFullyVaccinated
            const weeklyCaseCount = response.data[lga].weeklyCaseCount
            const result = determineRisk(secondDose, weeklyCaseCount)
            if (result === 1) {
              lowRiskIds.push(lga)
            } else if (result === 2) {
              mediumRiskIds.push(lga)
            } else if (result === 3) {
              highRiskIds.push(lga)
            }
          })
        }).catch(function (error) {
          console.error(error)
        })
    }
  },
  mounted () {
    this.createMap()
  }
}

function determineRisk (sdose, casesLastWeek) {
  if (sdose === '>95%') {
    sdose = 96.0
  }
  sdose = (parseFloat(sdose) * 0.01)
  if (casesLastWeek >= 1000) {
    return 3
  }

  if (casesLastWeek >= 500 && casesLastWeek < 1000) {
    if (sdose < 95) {
      return 3
    } else {
      return 2
    }
  }

  if (casesLastWeek >= 100 && casesLastWeek < 500) {
    if (sdose <= 0.80) { return 3 }
    if (sdose > 0.80 && sdose < 0.95) { return 2 }
    if (sdose >= 0.95) { return 1 }
  }

  if (casesLastWeek < 100) {
    if (sdose <= 0.80) {
      return 2
    } else {
      return 1
    }
  }
  return 1
}
</script>

<style scoped>

.main {
  position: relative;
}

#map {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  top: 50%;
  left: 50%;
  transform: translate(-50%, 0%);
  width: 80%;
  height: 700px;
  margin-top: 10px;
  margin-left: 10px;
  margin-right: 10px;
  margin-bottom: 25px;
}

.legend {
  display: flex;
  flex-direction: column;
  align-items: center;
}

dt {
width: 30px;
height: 30px;
display: inline-block;
overflow: hidden;
border: 1px solid #000;
margin-top: 50px;
}

.green {background-color: #4fc946; }
.blue {background-color: #4267ad;}
.orange {background-color: #e3b418;}
.red {background-color: #ff2424;}

dd {
display: inline-block;
width: 7em;
margin: 0 0 0 0em;
}

</style>
