<template>
  <div>
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Timestamp</th>
          <th>Latitude</th>
          <th>Longitude</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(drone, uuid) in drones" :key="uuid">
          <td>{{ drone.name }}</td>
          <td>{{ drone.ts }}</td>
          <td>{{ drone.latitudeInDegrees }}</td>
          <td>{{ drone.longitudeInDegrees }}</td>
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
// eslint-disable-next-line
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
// eslint-disable-next-line
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
  mqtt: {
    'drone/position' (data) {
      // Extract JSON payload from data
      let jsonPayload = JSON.parse(String.fromCharCode.apply(null, data))

      // Append JSON payload to debug data to help troubleshoot potential issues
      this.messages.push(jsonPayload)

      // Update `drones` data property.
      // Use Vue.set to make sure the new/updated property is reactive.
      // See https://vuejs.org/v2/guide/reactivity.html#Change-Detection-Caveats
      let uuid = jsonPayload.uuid
      this.$set(this.drones, uuid, {
        ts: jsonPayload.ts,
        name: jsonPayload.name,
        latitudeInDegrees: jsonPayload.latitude,
        longitudeInDegrees: jsonPayload.longitude
      })
    }
  }
}
</script>
