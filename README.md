# Server-Walking-Health
Application backend

## Deployment instruction:

1. Install **Docker**.
2. Pull the image from Docker Hub with `docker pull heavenlyraven/walking-health`
3. Then run your container using `docker run -p [-e IP=<I>] [-e NUMBER_OF_WORKERS=<N>] 80:8080 heavenlyraven/walking-health` optionally passing the number of workers <N> (2 by default)
and the IP-address of the host (0.0.0.0 by default)
