# Open Ports on 10.10.11.133

- 22 - SSH
- 2379 - kube-apiserver, etcd
- 2380 - kube-apiserver, etcd
- 8443 - alternative for port 443 (also related with kubernetes, possible remplace of 6443) - endpoints available without auth
- 10249 - kube-proxy, Kubelet? - endpoints available without auth
- 10250 - Kubelet API (Self, Control plane) - various endpoints such as executing commands in running containers
- 10256 - kube-proxy (Self, Load balancers) - only for /healthz - available without auth
