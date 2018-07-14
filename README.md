# Description

A company has a number of drones flying around the country. You have been tasked to build a system to track the location of every drone in real-time. The system's dashboard will only display the last location of the drones, so the backend doesn't need to worry about the history. You can store the state of the application in-memory for simplicity reasons.

Each drone should be associated with a unique identifier, and should report its geo-location coordinates to the central server in real-time through a cellular modem connection. Cellular modem connections are expensive, therefore you need to make sure the drones report back their location using as little data as possible.

The dashboard should be a simple single-page application displaying the list of active drones, by their unique identifiers, along with their current speed. You should visually highlight the drones that have not been moving for more than 10 seconds.

# Usage

```bash
git clone https://github.com/lvaylet/resin-fsea.git
cd resin-fsea
docker-compose up --build
```

Logs will be displayed on screen. Alternatively, you can run the services in the background and request logs separately:

```bash
docker-compose up --build -d
docker-compose logs -f
```

# Architecture Diagram

```
+ - - - +                + - - - - - - - - - +
| Drone | -- publish --> |                   |
+ - - - +                |                   |
                         |                   |                  + - - - - - +
+ - - - +                | MQTT Broker       | <-- subscribe -- |           |
| Drone | -- publish --> | eclipse-mosquitto |                  | Dashboard |
+ - - - +                | /drone/position   | --- publish ---> |           |
                         |                   |                  + - - - - - +
+ - - - +                |                   |
| Drone | -- publish --> |                   |
+ - - - +                + - - - - - - - - - +
```


# Assumptions

- The drones firmware exists. I focused on determining how the firmware will send information to the backend. to the dashboard.

# Notes

This assignment... | A real-world project would instead...
--- | ---
Simulates drones and hardware failures with Python code | Display data about actual drones that transmit data over a cellular connection
Hard-codes the list of drones in `docker-compose.yml` | Rely on a discovery service to dynamically fetch existing and new devices in a Resin.io application
Uses a single repo for the dashboard, the MQTT broker and the dummy drones | Separate repos for the individual components
Relies on local instances of Docker and Docker Compose to pull/build and coordinate all the services in the repo | Rely on a CI/CD toolchain to build, test and push the Docker images of the individual components to a centralized registry
Stores geo-location in-memory and does not persist anything (i.e. all data is lost on `docker-compose down`) | Store geo-location data in a database or at least a cache (like Redis)
