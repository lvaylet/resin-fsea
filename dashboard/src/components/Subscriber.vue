<template>
  <div class="sub">
    <ul>
      <li v-for="message in messages" :key="message">
        {{ message }}
      </li>
    </ul>
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
function distance(lat1, lon1, lat2, lon2, unit='M') {
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
function speed(distance, ts1, ts2) {
  return distance / (ts2 - ts1)
}

export default {
  data () {
    return {
      messages: []
    }
  },
  mqtt: {
    'drone/position' (data) {
      let message = String.fromCharCode.apply(null, data)
      this.messages.push(message)
    }
  }
}
</script>

<style>
.sub {
  width: 100%;
  border: 1px solid #ccc;
  margin: 20px 1%;
  padding: 20px 0;
}
.sub ul {
  list-style-type: none;
}
</style>
