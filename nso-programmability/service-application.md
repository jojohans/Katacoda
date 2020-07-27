`ncs-make-package has more uses that just to create NEDs. In fact, we
use it to create all kinds of NSO packages and in this section we'll
show how to build a network service package with both a little bit of
python code and a small XML template.

A network service package, often called a service package or just
'service' (as in the rest of this tutorial), is a package that can be
loaded into NSO and which contains all the code needed to provision a
service to the network.

The service creates a mapping from input parameters (representing the
service intent) and the output configuration that should be
provisioned to the network.

NSO makes the process of creating a service very straight forward and
we will walk through the main steps of service design in this
tutorial:

* Modeling
* Template creation
* Deployment

We will assume that you have basic understanding of NSO from our
initial tutorial, but will provide all the commands you need
throughout.

We will create a standard L3VPN service based on model from RFC 8299
and will a simple topology model

* [ietf-l2vpn-svs.yang - RFC 8466: A YANG Data Model for Layer 2 Virtual Private Network (L2VPN) Service Delivery](https://tools.ietf.org/html/rfc8466)
* [ietf-l3vpn-svc.yang - RFC 8299: YANG Data Model for L3VPN Service Delivery](https://tools.ietf.org/html/rfc8299)

`ncs-make-package` creates the directory structure we need to build
the service including the python code and the templates.

We are creating a python and template based service package:
`ncs-make-package --dest packages/l3vpn --service-skeleton python-and-template l3vpn`{{execute}}

We can explore any file in the shell and/or the editor but there are
three file in particular that are of interest for service developers:

* The Service YANG model. `packages/l3vpn/src/yang/ietf-l3vpn-svc.yang`{{open}}
* The python code that applies the template and creates the service: `packages/l3vpn/python/l3vpn/main.py`{{open}}
* The template that configures the device: `packages/l3vpn/templates/l3vpn-template.xml`{{open}}


A code snippet we can copy and paste into the editor window.
```
    leaf ntp-server {
        type inet:ipv4-address;
    }
```{{copy}}

TODO: Figure out how to copy the standard service model and the file
      that augments the standard service model from assets
      (resources?) to our service skeleton.
