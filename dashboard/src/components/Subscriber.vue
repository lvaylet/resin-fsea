<template>
  <div>
    <table class="table is-striped is-hoverable is-fullwidth">
      <thead>
        <tr>
          <th>Name</th>
          <th>Last Update</th>
          <th>Latitude</th>
          <th>Longitude</th>
          <th>Speed (km/h)</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(drone, uuid) in drones" :key="uuid" :class="{ 'is-selected': Math.abs(getCurrentTime() - drone.ts) > 10 }">
          <td>{{ drone.name }}</td>
          <td>{{ Math.abs(getCurrentTime() - drone.ts) }} seconds ago</td>
          <td>{{ drone.latitudeInDegrees }}</td>
          <td>{{ drone.longitudeInDegrees }}</td>
          <td>{{ drone.speedInKph }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
/**
 * Calculates the distance between two points, given the latitude/longitude of those points.
 *
 * Assumptions:
 *   South latitudes are negative, east longitudes are positive.
 *
 * @param {float} lat1 - The latitude of point 1 (in decimal degrees)
 * @param {float} lon1 - The longitude of point 1 (in decimal degrees)
 * @param {float} lat2 - The latitude of point 2 (in decimal degrees)
 * @param {float} lon2 - The longitude of point 2 (in decimal degrees)
 * @param {str} unit - The unit desired for results ('M' is statute miles (default), 'K' is kilometers, 'N' is nautical miles)
 * @returns {float} - The distance in desired unit
 */
function computeDistance(lat1, lon1, lat2, lon2, unit='M') {
	var radlat1 = Math.PI * lat1/180
	var radlat2 = Math.PI * lat2/180
	var theta = lon1 - lon2
	var radtheta = Math.PI * theta/180
	var dist = Math.sin(radlat1) * Math.sin(radlat2) + Math.cos(radlat1) * Math.cos(radlat2) * Math.cos(radtheta);
  if (dist > 1) { dist = 1 }
	dist = Math.acos(dist)
	dist = dist * 180/Math.PI
	dist = dist * 60 * 1.1515
	if (unit == 'K') { dist = dist * 1.609344 }
	if (unit == 'N') { dist = dist * 0.8684 }
	return dist
}

/**
 * Calculates the speed between two points, given the distance between these two points and their timestamps.
 *
 * @param {float} distance - The distance between the two points (in statute miles, kilometers or nautical miles)
 * @param {int} ts1 - The timestamp of point 1 (in seconds)
 * @param {int} ts2 - The latitude of point 2 (in seconds)
 * @returns {float} - The speed in the same unit as the distance (statute miles/second, kilometers/second or nautical miles/second)
 */
function computeSpeed(distance, ts1, ts2) {
  return distance / (ts2 - ts1)
}

export default {
  data () {
    return {
      drones: {},
      messages: []
    }
  },
  methods: {
    /**
     * Return the number of seconds since epoch.
     *
     * @returns {int} - The number of seconds since epoch.
     */
    getCurrentTime: function () {
      let d = new Date()
      let seconds = Math.round(d.getTime() / 1000)
      return seconds
    },
    /**
     * Calculates the speed between two points, given the distance between these two points and their timestamps.
     *
     * @param {str} uuid - The UUID of the drone
     * @param {int} ts - The timestamp of the last update (in seconds)
     * @param {float} lat1 - The latitude of point 1 (in decimal degrees)
     * @param {float} lon1 - The longitude of point 1 (in decimal degrees)
     * @param {str} unit - The distance unit desired for results ('M' is statute miles (default), 'K' is kilometers, 'N' is nautical miles)
     * @returns {float} - The speed in desired unit per hour (statute miles/hour, kilometers/hour, nautical miles/hour)
     */
    computeSpeedOfDroneWithUuid: function (uuid, ts, latitude, longitude, unit='M') {
      var speed = NaN  // initialize to NaN in case next test fails

      // Check if a drone with the same UUID already exists.
      // If so, compute speed from previous coordinates.
      // If not, keep speed set to NaN until new geo-location is available.
      if (uuid in this.drones) {
        let previousTimestamp = this.drones[uuid].ts
        let previousLatitude = this.drones[uuid].latitudeInDegrees
        let previousLongitude = this.drones[uuid].longitudeInDegrees
        let distance = computeDistance(previousLatitude, previousLongitude, latitude, longitude, unit)
        speed = computeSpeed(distance, previousTimestamp, ts)
        speed = speed * 3600 // convert from 'per second' to 'per hour'
        speed = Math.round(speed * 100) / 100  // truncate to two decimals
      }

      return speed
    }
  },
  mqtt: {
    'drone/position' (message) {
      // Extract JSON payload from message
      let jsonPayload = JSON.parse(String.fromCharCode.apply(null, message))

      // Append JSON payload to debug data to help troubleshoot potential issues
      this.messages.push(jsonPayload)

      // Update `drones` data property.
      let uuid = jsonPayload.uuid
      let timestamp = jsonPayload.ts
      let latitude = jsonPayload.latitude
      let longitude = jsonPayload.longitude

      // Use Vue.set to make sure the new/updated object is reactive and shows
      // up in the table as soon as it is added/updated.
      // See https://vuejs.org/v2/guide/reactivity.html#Change-Detection-Caveats
      this.$set(this.drones, uuid, {
        ts: jsonPayload.ts,
        name: jsonPayload.name,
        latitudeInDegrees: jsonPayload.latitude,
        longitudeInDegrees: jsonPayload.longitude,
        speedInKph: this.computeSpeedOfDroneWithUuid(uuid, timestamp, latitude, longitude, 'K')
      })
    }
  }
}
</script>

<style>
  .error: { color: #ff0000; }
</style>
