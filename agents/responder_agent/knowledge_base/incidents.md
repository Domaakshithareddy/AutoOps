## Build Failure: Out of Memory
Solution: Optimize Docker memory usage. Use swap or reduce parallel jobs.

## Build Duration Too High
Solution: Use build caching, parallel builds, or incremental steps.

## Prometheus Target Down
Solution: Ensure correct IP in `prometheus.yml`, open ports in firewall, restart agent.

## Docker Pull Error
Solution: Check internet connection or Docker Hub login. Verify image name and network settings.

## FastAPI 404 on /metrics
Solution: Ensure `/metrics` route exists in agent and is exposed properly.
