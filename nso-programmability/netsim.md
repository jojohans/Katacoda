## Create a netsim aware NETCONF NED

`ncs-netsim create-network` creates a network a number of simulated
devices and sets up NSO to use a NEDs to communicate with these
devices.  We will use a mix of NETCONF and CLI devices and show how
the different properties of these devices affects how they are managed
by NSO. NSO doesn't come with pre-existing NETCONF any netsim devices
so our first task is to create such a device.

The `ncs-make-package` command is used to create different types of
NCS packages.  When the package is a NED, `ncs-make-package` creates a
netsim directory by default, which means that the package can be used
to run a network of simulated devices using created by the
`ncs-netsim` command.

## Standard YANG models we'll use in the demo

In this example we'll build a NED for the following standard YANG-models:
* [iana-hardware.yang - RFC 8348: A YANG Data Model for Hardware Management](https://tools.ietf.org/html/rfc8348)
* [ietf-hardware.yang - RFC 8348: A YANG Data Model for Hardware Management](https://tools.ietf.org/html/rfc8348)
* [ietf-interfaces.yang - RFC 8343: A YANG Data Model for Interface Management](https://tools.ietf.org/html/rfc8343)
* [ietf-ip.yang - RFC 8344: A YANG Data Model for IP Management](https://tools.ietf.org/html/rfc8344)
* [ietf-routing.yang - RFC 8349: A YANG Data Model for Routing Management (NMDA Version)](https://tools.ietf.org/html/rfc8349)

- The IETF interface model:`/tmp/yamgs/device/ietf-interfaces.yang`{{open}}

- The IETF ip YANG model: `/tmps/yangs/device/ietf-ip.yng`{{open}}

- The IETF routing YANG model: `/tmp/yangs/device/ietf-routing.yang`{{open}}

In addition to the device models we will make use of the standard L2
and L3 VPN models: `ietf-l3vpn-svc.yang`{{open}} from RFC 8299: YANG
Data Model for L3VPN Service Delivery and
`ietf-l2vpn-svc.yang`{{open}} from RFC 8466: A YANG Data Model for
Layer 2 Virtual Private Network (L2VPN) Service Delivery.
* [ietf-l3vpn-svc.yang - RFC 8299: YANG Data Model for L3VPN Service Delivery](https://tools.ietf.org/html/rfc8299)
* [ietf-l2vpn-svc.yang - RFC 8466: A YANG Data Model for Layer 2 Virtual Private Network (L2VPN) Service Delivery](https://tools.ietf.org/html/rfc8466)

## Create the NETCONF NED. No issues at the this point

We create the NETCONF NED package and point to the directory where the
YANG models are located.  In addition to the location of the YANG
model we provide vendor and version information and turns off java and
Python builds which are typically not needed when building NETCONF
NEDs.  As noted above `ncs-make-package` will by default add netsim
support to our NED package.

Creating a NETCONF NED is really easy, just create a new package
pointing to the YANG-files to include (no java or python code is
required).

`ncs-make-package --netconf-ned /tmp/yang/device nc --vendor cisco --version 1.0 --no-python --no-java`{{execute}}

Build the NED: `make -C packages/nc/src{{execute}}`

If everything went well we now have a new NETCONF NED we can use
either to communicate with real devices that implements the YANG
models we included in the NED or simulated devices created by
`netsim`.

## Create a CLI NED. CLI NEDs are a bit more involved

TODO: Build a CLI NED based on a simplified(?) IOS model (or should we
      create a new CLI NED model from scratch?  The advantage of the
      latter option is that the model is easier to follow than the
      full Cisco model. The advantage of the former is that it's more
      realistic and since we have standard YANG models for the NETCONF
      NED, perhaps fairer.  Whet we should do, though, is remove
      features not relevant to the example.  CLI NEDs are quite a bit
      more involved than NETCONF NEDs since they require code to map
      from the device model used by NSO to configuration commands
      understood by the device.

TODO: Add CLI devices to our simulated network by running `ncs-netsim`
      again with the `add-to-network` sub command.  `ncs-netsim
      add-to-network /path/to/cli-ned c 1`{{execute}}.
