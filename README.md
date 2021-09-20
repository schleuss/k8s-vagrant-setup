# K8S Study Environment

## Requirements


1) [Vagrant](https://www.vagrantup.com/docs/installation)
2) [Kubectl](https://kubernetes.io/docs/tasks/tools/)


## Execute

Execute on the current folder:

```
vagrant up
```

After the process finish, a new file will be created on the local folder (kubernetes_config.conf). This file is the k8s config file.

Use the KUBECONFIG environment variable to use this k8s instance.

```
export KUBECONFIG="$(pwd)/kubernetes_config.conf"
```

To test:

```
$ kubectl get nodes
NAME         STATUS   ROLES                  AGE     VERSION
k8s-master   Ready    control-plane,master   8m9s    v1.22.2
node-1       Ready    <none>                 5m20s   v1.22.2
node-2       Ready    <none>                 2m2s    v1.22.2
```

Delete the env

```
vagrant destroy
```

Use suspend/resume to pause de execution

```
vagrant suspend
vagrant resume
```