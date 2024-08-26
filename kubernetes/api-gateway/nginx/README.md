If you already have the NGINX `.conf` files and are looking to configure and deploy NGINX as an API Gateway on Kubernetes, follow these steps to set up the necessary Kubernetes resources.

### Prerequisites

- You have a running Kubernetes cluster.
- `kubectl` is configured to interact with your cluster.
- You have your NGINX configuration files (`nginx.conf` and others) ready.

### 1. **Create a ConfigMap for NGINX Configuration**

Kubernetes ConfigMaps are used to store your NGINX configuration files so that they can be mounted into the NGINX container.

Assume you have an `nginx.conf` file and other configuration files like `proxy.conf`, `upstream.conf`, etc.

Create a `ConfigMap` from your configuration files:

```bash
kubectl create configmap nginx-config --from-file=nginx.conf --from-file=proxy.conf --from-file=upstream.conf
```

This command creates a ConfigMap named `nginx-config` that contains your NGINX configuration files.

Alternatively, you can define the ConfigMap in a YAML file:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config
data:
  nginx.conf: |
    # Your NGINX configuration goes here...
  proxy.conf: |
    # Your proxy settings...
  upstream.conf: |
    # Your upstream configuration...
```

Apply the ConfigMap:

```bash
kubectl apply -f nginx-config.yaml
```

### 2. **Create a Deployment for NGINX**

Now, you need to deploy NGINX as a container. This Deployment will ensure that NGINX runs in a pod and that it automatically scales if necessary.

Here’s an example Deployment manifest for NGINX:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-gateway
spec:
  replicas: 2  # Adjust as needed
  selector:
    matchLabels:
      app: nginx-gateway
  template:
    metadata:
      labels:
        app: nginx-gateway
    spec:
      containers:
      - name: nginx
        image: nginx:latest  # You can specify a particular version
        ports:
        - containerPort: 80  # Expose the HTTP port
        volumeMounts:
        - name: nginx-config-volume
          mountPath: /etc/nginx/nginx.conf
          subPath: nginx.conf
        - name: nginx-proxy-volume
          mountPath: /etc/nginx/conf.d/proxy.conf
          subPath: proxy.conf
        - name: nginx-upstream-volume
          mountPath: /etc/nginx/conf.d/upstream.conf
          subPath: upstream.conf
      volumes:
      - name: nginx-config-volume
        configMap:
          name: nginx-config
          items:
          - key: nginx.conf
            path: nginx.conf
      - name: nginx-proxy-volume
        configMap:
          name: nginx-config
          items:
          - key: proxy.conf
            path: proxy.conf
      - name: nginx-upstream-volume
        configMap:
          name: nginx-config
          items:
          - key: upstream.conf
            path: upstream.conf
```

This Deployment does the following:

- Deploys an NGINX container.
- Mounts your NGINX configuration files (`nginx.conf`, `proxy.conf`, `upstream.conf`) from the ConfigMap into the container's file system.
- Exposes port 80 for HTTP traffic.

Apply the Deployment:

```bash
kubectl apply -f nginx-deployment.yaml
```

### 3. **Expose the NGINX Deployment Using a Service**

To expose your NGINX API Gateway, you need to create a Kubernetes Service. This Service will allow external traffic to reach the NGINX pods.

Here’s an example Service definition:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-gateway-service
spec:
  selector:
    app: nginx-gateway
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: LoadBalancer  # You can use NodePort or ClusterIP depending on your needs
```

- **Type: LoadBalancer**: Exposes the NGINX service to the outside world using an external IP (e.g., on a cloud provider).
- **Type: NodePort**: Exposes the service on a specific port on each node of the cluster.
- **Type: ClusterIP**: Exposes the service only within the cluster (internal access).

Apply the Service:

```bash
kubectl apply -f nginx-service.yaml
```

### 4. **Optional: Use NGINX Ingress Controller**

If you're using an NGINX Ingress Controller, you can set up routing rules to direct traffic to your NGINX API Gateway based on URL paths or hostnames.

#### Install NGINX Ingress Controller

You can install the NGINX Ingress Controller via Helm:

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm install nginx-ingress ingress-nginx/ingress-nginx
```

#### Create an Ingress Resource

Here’s an example of an Ingress resource that routes traffic to your NGINX API Gateway:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: nginx-api-gateway-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: nginx-gateway-service
            port:
              number: 80
```

This Ingress resource routes all traffic from `api.example.com` to the NGINX API Gateway.

Apply the Ingress resource:

```bash
kubectl apply -f nginx-ingress.yaml
```

### 5. **Monitor and Scale**

You can monitor your NGINX API Gateway using Kubernetes-native monitoring tools like Prometheus and Grafana. NGINX also supports exporting metrics that can be monitored.

To scale your NGINX API Gateway, you can either adjust the replica count in your Deployment manually or use Kubernetes' Horizontal Pod Autoscaler (HPA) to automatically scale based on CPU or memory usage.

To create an HPA, use the following command:

```bash
kubectl autoscale deployment nginx-gateway --cpu-percent=50 --min=2 --max=10
```

### Summary of Key Steps:

1. **Create ConfigMap**: Store your NGINX configuration files in a ConfigMap.
2. **Deploy NGINX**: Use a Deployment to run the NGINX container, mounting the ConfigMap as the configuration.
3. **Expose NGINX**: Use a Service to expose NGINX to the outside world.
4. **Optional Ingress Controller**: Use an Ingress resource to manage traffic routing.
5. **Monitor and Scale**: Use Kubernetes monitoring and autoscaling tools to manage the API Gateway's performance.

This process should allow you to deploy and run NGINX as an API Gateway on Kubernetes efficiently.

