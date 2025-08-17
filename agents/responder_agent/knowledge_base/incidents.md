## Out of Memory during Build
If a build fails due to memory exhaustion, increase the CI/CD runner memory limit to at least 2–4 GB depending on the project size. Reduce the level of parallelism so fewer processes run at the same time. Enable build caching to avoid recomputing large intermediate steps. In Docker-based builds, consider multi-stage builds to reduce memory requirements and keep images lean. Monitoring memory usage with Prometheus and setting alerts can help proactively detect and prevent future OOM issues.

## Build Duration Too High
If build duration is too high, enable build caching so that previously compiled layers can be reused. Parallelize the build process or split it into smaller services where possible. Use incremental builds with tools such as `ccache` or Bazel remote cache. Switching to optimized base images (for example `python:slim` or `alpine`) can significantly reduce size and build time. Removing unnecessary dependencies and redundant steps in the Dockerfile helps speed up builds. If the issue persists, run the builds on machines with more CPU and memory or enable auto-scaling build agents.

---

## Prometheus Target Down
When a Prometheus target is down, first verify that the correct IP address and port are configured in `prometheus.yml`. Check firewall and network rules to ensure that the required ports (such as 8000, 8500, or 8600) are open. Confirm that the agent services are running and have not crashed by testing with `curl http://<agent-ip>:8000/metrics`. After fixing any configuration, restart Prometheus using `systemctl restart prometheus`. In larger deployments, consider using service discovery solutions such as Kubernetes or Consul to avoid hardcoding IPs.

---

## Docker Pull Error
A Docker pull error may occur due to lack of internet connectivity, so verify that the build agent has access to the internet. If the image is private, log in with `docker login` before pulling. Double-check the spelling of the image name and ensure the tag exists. If the problem persists, clear the local Docker cache with `docker system prune` or try pulling with a different registry mirror. In enterprise environments, confirm that proxy settings and firewall rules allow Docker to connect to the registry.

---

## FastAPI 404 on /metrics
If a FastAPI service returns 404 on the `/metrics` endpoint, ensure that the `/metrics` route is actually defined in the application. Verify that the Prometheus client integration is properly included and that the endpoint is exposed on the correct port. Check the logs of the FastAPI service to confirm it is running without errors. If you are running multiple agents, confirm that the right service is being scraped by Prometheus. Fin
