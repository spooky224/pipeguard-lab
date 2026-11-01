# PipeGuard Lab

A small Python project used to exercise PipeGuard's Jenkins, GitHub, Docker and Loki evidence integrations.

## Pipeline behavior

The Jenkins pipeline checks out this repository, builds the HTTP service image, starts a build-scoped container, calls its health and calculation endpoints, submits a SonarQube analysis, and then runs the unit tests. The latest remote demo change intentionally adds 1 to `calculate_total`, so the existing `test_calculate_total` test expects 30 but receives 31. That failure is retained as the predictable investigation trigger.

The service writes request and calculation details to stdout so Docker can expose them through `docker logs`. Each pipeline container is labeled:

- `pipeguard_project=pipeguard-lab`
- `pipeguard_build=<Jenkins BUILD_NUMBER>`

PipeGuard's Alloy collector watches containers with the configured project label and forwards their logs to Loki with project, build number and container labels. The pipeline leaves the container available for ten seconds after the stages finish so Alloy can discover it and ship its final log lines, then removes the container and image.

## Requirements

The Jenkins node running this pipeline needs Python 3, Docker CLI access to the VM's Docker daemon, and permission for the `jenkins` service account to use that daemon. Configure a Jenkins Secret text credential with ID `sonarqube-token`; the scanner stage reaches SonarQube at `http://192.168.56.1:9000` from the Vagrant VM. Create the `pipeguard-lab` project in SonarQube first. In PipeGuard Settings, use the server URL reachable from the PipeGuard backend (for SonarQube on the Mac, usually `http://localhost:9000`) and a token with Browse permission. The VM must have network access to pull `python:3.12-slim` the first time. Configure Loki in PipeGuard for project label `pipeguard-lab` before triggering the build so Alloy is already watching when Jenkins creates the test container.

Run the unit tests locally with:

```bash
python3 -m unittest -v test_app.py
```
