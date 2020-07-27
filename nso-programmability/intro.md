## Explain what we will do in this demo.

The example will show network wide transactions in a network that
includes network elements managed using NETCONF and CLI interfaces.
The purpose of the demo is to demonstrate the benefits of NETCONF, in
terms of support for network-wide transactions, confirmed commit,
automatic NED support, standard (device) YANG models for ease
integration with service models etc. etc.

The example is based on standard device models and standard service
models as much as possible.  The NETCONF device should use RFC 8349,
the latest IETF YANG (NMDA enabled) routing model and NSO should use
RFC 8299, the latest L3VPN service model.  CLI devices will obviously
not use standard modules, instead will use a subset of one of the IOS
models we already have (a subset because not everything in these
models are routing and don't want to hide the forest among the
trees).  Netsim will provide the network devices, some publishing
NETCONF interfaces and some publishing CLI interfaces.

This interactive example will demonstrate network wide transactions
using Cisco NSO (Network Services Orchestrator) and how it use
Network Element Drivers, or NEDs, to interface with the different
northbound interfaces published by network elements.

Cisco® NSO is an industry-leading orchestration platform for hybrid
networks.  It provides comprehensive lifecycle service automation to
enable you to design and deliver high-quality services faster and more
easily.

The example will make use of standard device models and standard
service models as much as possible.  The NETCONF device should use RFC
8349, the latest IETF YANG (NMDA enabled) routing model and NSO should
use RFC 8299, the latest L3VPN service model.  CLI devices will
obviously not use standard modules, instead will use a subset of one
of the IOS models we already have (a subset because not everything in
these models are routing and don't want to hide the forest among the
trees).

The example will use netsim, a [ConfD]{https://www.tail-f.com) based
tool targeted at NCS application developers, to provide a simulated
network of managed devices.  Some of the devices will provide NETCONF
interfaces others will provide traditional CLI interfaces.

We will first walk-through setting up the simulated network and NSO
and then we will run through a basic tutorial that demonstrates a few
of the main features:

* Accessing devices
* Making simple configuration changes to devices.
* Looking at what NSO have to do to make these changes on NETCONF and
  CLI devices.

Building NEDs. Building a NETCONF NED is straight forward, creating a
CLI NED requires Tailf-f expert level knowledge.  We won't require the
users that running the example create their own NED but maybe we can
give them a sense of the effort involved and the opportunities of
things to go wrong.

Investigate the difference between NETCONF NEDs and CLI NEDs from the
point-of-view of NSO.  We'll look at the work involved in creating
NEDs, the amount of code needed to create a CLI NED.

Make a small addition to the device model and compare the effort
needed to cover the extender interface for NETCONF NEDs and CLI NEDs.
Look into the difference in the amount of work NSO has to do in order
to support rollback for devices managed through NETCONF NEDs and
compared to CLI NEDs.

Show how a network wide transaction becomes just best effort
consistency due to non-transactional nodes.  Look into the service
model mapping, this should be straight forward for the NETCONF devices
since they use IETF standard YANG models but a little bit tricky for
CLI devices which presents non-standard interfaces.

You can click on the commands to automatically copy them to the
terminal window.

Finally, feel free to disregard the instructions and explore the
system at any point - reloading your browser window will create an
entirely fresh instance so you can always start over!
