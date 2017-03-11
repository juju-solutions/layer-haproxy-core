# HA Proxy core layer

This is a core layer that installs haproxy and enables it to build in to other
charms.

# Design features:

-[X] Install haproxy
-[X] Enable haproxy
-[X] Use status-set messages correctly
-[ ] application-version-set the right version of haproxy
-[ ] render configuration action takes from templates
-[ ] Next separate layer kubeapi-load-balancer to build off this one
-[ ] Has a template for kubeapi server
-[ ] Include http-interface-layer
-[ ] The peering interface, can be added in future.
