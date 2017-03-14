# HAProxy core layer

This is base reactive layer providing core HAProxy functionality so it can be
built into other charms. If you are looking for full HAProxy support please
use the full [haproxy](https://jujucharms.com/haproxy/) charm.

It provides modern status message setting and application version in the
that will show up in the `juju status` command that the original charm
does not yet have.

The layer takes a template from the templates directory and renders that with
the configuration and relation data to use those values in the rendering
context.

# Usage

Include `layer:haproxy-core` in the layer.yaml of the charm you want to build
this layer into. The `charm build` command will insert this layer into the
final charm.

## Adding templates

The charm is designed to render a Jinja2 template for the haproxy
configuration. Other layers can overwrite or render different templates
based on the need of the layer/charm.

## States

The layer sets the following states:

- **apt.installed.haproxy** - Set once the apt layer installs the haproxy
package.
- **haproxy.enabled** - Set once the layer code enables haproxy to starts on
reboot.

## Interface

This layer requires the
[http interface](http://interfaces.juju.solutions/interface/http/)
used to reverseproxy to other charms that provide the http interface.

This layer provides the
[http interface](http://interfaces.juju.solutions/interface/http/)
which can be used in the application layer that consumes this layer.
