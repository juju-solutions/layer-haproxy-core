# HA Proxy core layer

This is base reactive layer providing core HAProxy functionality so it can be
built into other charms. If you are looking for full HAProxy support please
use the full [haproxy](https://jujucharms.com/haproxy/) charm.



# Design features:

- [X] Install haproxy
- [X] Enable haproxy
- [X] Use status-set messages correctly
- [X] application-version-set the right version of haproxy
- [X] Include http-interface-layer, implement the reverseproxy relation.
- [X] render configuration from templates on reverseproxy relation
- [ ] Create a separate layer kubeapi-load-balancer to build off this one
- [ ] Create a template to reverseproxy the kube-apiserver.
- [ ] The peering interface, can be added in future.
