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

## Kubernetes demo connection

PipeGuard can connect directly to a Kubernetes API and show live deployments, pods, services, and warning events for one namespace. For the local demo, the cluster is a single-node `kind` cluster running in Docker Desktop; Jenkins and the observability VM remain separate.

Build and deploy the current lab image:

```bash
docker build -t pipeguard-lab:demo .
../PipeGuard/.tools/kind load docker-image pipeguard-lab:demo --name pipeguard-demo
kubectl --context kind-pipeguard-demo apply -f k8s/demo.yaml
kubectl --context kind-pipeguard-demo -n pipeguard-lab rollout status deployment/pipeguard-lab
```

Create the namespace-scoped read-only identity:

```bash
kubectl --context kind-pipeguard-demo apply -f k8s/pipeguard-reader.yaml
kubectl --context kind-pipeguard-demo -n pipeguard-lab auth can-i list pods --as=system:serviceaccount:pipeguard-lab:pipeguard-reader
kubectl --context kind-pipeguard-demo -n pipeguard-lab auth can-i get secrets --as=system:serviceaccount:pipeguard-lab:pipeguard-reader
```

The first authorization check should say `yes`; the secret check should say `no`. Generate an expiring token for the connection:

```bash
kubectl --context kind-pipeguard-demo -n pipeguard-lab create token pipeguard-reader --duration=8h
```

In PipeGuard **Settings → Kubernetes**, enter the API URL from `kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}'`, namespace `pipeguard-lab`, that token, and the CA PEM decoded from `kubectl config view --raw --minify -o jsonpath='{.clusters[0].cluster.certificate-authority-data}' | base64 -D`. The credentials are held in memory for the current PipeGuard session.
