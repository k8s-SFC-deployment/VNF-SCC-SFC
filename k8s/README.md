# K8S Deploy Example

- [x] test k8s deployment
- [ ] organize with helm
- [ ] apply hpa
- [ ] apply monitoring
  - [ ] cilium
  - [ ] hubble
  - [ ] grafana
  - [ ] prometheus

## Run

### 1. Build Cluster

below is baremetal environment.

```bash
master@user:~$ kubeadm init
```


```bash
slave@user:~$ kubeadm join
```

### 2. Deploy Firewall and IDS

```bash
master@user:~/vnf-scc-sfc/k8s$ kubectl create ns testbed
master@user:~/vnf-scc-sfc/k8s$ kubectl apply -f firewall
master@user:~/vnf-scc-sfc/k8s$ kubectl apply -f ids
```

### 3. Deploy Ingress-Nginx

```bash
master@user:~/vnf-scc-sfc/k8s$ kubectl apply -f externals/nginx-ingress-baremetal-deploy.yaml
```

And, replace [`/k8s/ingress`](/k8s/ingress.yaml) `<Please Replace>` with domain.

```bash
master@user:~/vnf-scc-sfc/k8s$ kubectl apply -f ingress.yaml
```

### 4. Check Result

```bash
# check ingress-nginx-controller's ports(<http-port>, and <https-port>)
master@user:~/vnf-scc-sfc/k8s$ kubectl get svc -n ingress-nginx 
# NAME                                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                                   AGE
# ingress-nginx-controller             NodePort    10.109.147.179   <none>        80:<http-port>/TCP,443:<https-port>/TCP   123m
# ingress-nginx-controller-admission   ClusterIP   10.103.10.235    <none>        443/TCP                                   123m

# check <host> and <your-ip>
master@user:~/vnf-scc-sfc/k8s$ kubectl get ing -n testbed
# NAME      CLASS   HOSTS    ADDRESS     PORTS   AGE
# ingress   nginx   <host>   <your-ip>   80      121m

# call
master@user:~/vnf-scc-sfc/k8s$ curl http://<host>:<http-port>/ids/openapi.json
master@user:~/vnf-scc-sfc/k8s$ curl http://<host>:<http-port>/firewall/openapi.json
```
