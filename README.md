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
+ - - - +      (2)       + - - - - - - - - - +
| Drone | -- publish --> |                   |
+ - - - +                |                   |
                         |                   |        (1)       + - - - - - +
+ - - - +      (2)       |    MQTT Broker    | <-- subscribe -- |           |
| Drone | -- publish --> |                   |                  | Dashboard |
+ - - - +                |  /drone/position  | --- publish ---> |           |
                         |                   |       (3)        + - - - - - +
+ - - - +      (2)       |                   |
| Drone | -- publish --> |                   |
+ - - - +                + - - - - - - - - - +
```

For a constrained Internet of Things (IoT) application such at this one, a publish/subscribe design pattern using the MQTT protocol seems to be a perfect fit.

Quoting the official MQTT 3.1.1 specification:

> MQTT is a Client Server publish/subscribe messaging transport protocol. It is light weight, open, simple, and designed so as to be easy to implement. These characteristics make it ideal for use in many situations, including constrained environments such as for communication in Machine to Machine (M2M) and Internet of Things (IoT) contexts where a small code footprint is required and/or network bandwidth is at a premium.

The publish/subscribe pattern (also known as pub/sub) provides an alternative to traditional client/server architecture. In the client/server model, a client communicates directly with an endpoint. The pub/sub model decouples the client that sends a message (the publisher) from the client or clients that receive the messages (the subscribers). The publishers and subscribers never contact each other directly. In fact, they are not even aware that the other exists. The connection between them is handled by a third component (the broker). The job of the broker is to filter all incoming messages and distribute them correctly to subscribers.

The most important aspect of pub/sub is the decoupling of the publisher of the message from the recipient (subscriber). This decoupling has several dimensions:
- Space decoupling: Publisher and subscriber do not need to know each other (for example, no exchange of IP address and port).
- Time decoupling: Publisher and subscriber do not need to run at the same time.
- Synchronization decoupling: Operations on both components do not need to be interrupted during publishing or receiving.

Applying this design pattern to our use case, and from the architecture diagram above:
1. The dashboard is a client that subscribes to a single `/drone/position` topic
2. The drones publish their geo-location data to the same topic on the Broker
3. The broker distribute all the messages to the dashboard, so the dashboard can store and post-process all the data

# Assumptions

- The drones firmware exists. I focused on determining how the firmware will send information to the backend. to the dashboard.

# Notes

- [PyCharm](https://www.jetbrains.com/pycharm/) was used for everything related to Python development. JetBrains's IDE has built-in support for virtual environments, linting and versioning with git.
- [Atom](https://atom.io/) was used for everything else (mainly [Node.js](https://nodejs.org/en/) and [Vue.js](https://vuejs.org/)
development). GitHub's editor also has a wealth of plugins for linting, testing, versioning...
- The dashboard is built with Vue.js and a few libraries from its  ecosystem (like [Vue-Mqtt](https://github.com/nik-zp/Vue-Mqtt) to easily subscribe and react to MQTT topics). [Vue CLI](https://cli.vuejs.org/) is used to scaffold, build and package the dashboard web application. It features out-of-the-box support for Babel, TypeScript, ESLint, PostCSS, PWA, unit testing & end-to-end testing, as well as hot reloading during development.

Finally, there are a few key differences between such an exercise and a real-world project:

This assignment... | A real-world project could instead...
--- | ---
Simulates drones and hardware failures (like connectivity drops) with Python code | Display the geo-location of actual drones whose production code is managed and deployed with Resin.io
Hard-codes a small list of drones in `docker-compose.yml` | Rely on a discovery service to dynamically fetch existing and new devices in a Resin.io application
Uses a single repo for the dashboard, the MQTT broker and the dummy drones | Separate repos for the individual components
Relies on local instances of Docker and Docker Compose to pull/build and coordinate all the services in the repo | Rely on a CI/CD toolchain to build, test and push the Docker images of the individual components to a centralized registry
Stores geo-location in-memory and does not persist anything (i.e. all data is lost on `docker-compose down`). The dashboard is a direct subscriber of the MQTT broker. | Store geo-location data in a database (or at least a cache like Redis) decoupled from the presentation layer (i.e. the dashboard). The storage layer would be a direct subscriber of the MQTT broker.
