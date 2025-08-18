Out of Memory during Build: Increase CI/CD runner memory limit to 2–4 GB.
Build Duration Too High: Enable build caching and split build into smaller parallel services.
Prometheus Target Down: Verify IP and port in prometheus.yml and restart Prometheus.
Docker Pull Error: Log in with docker login before pulling private images.
FastAPI 404 on /metrics: Define the /metrics route in the FastAPI app and expose it on the correct port.
