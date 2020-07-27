Let us start by setting up a minimal NSO installation.

For development we often use a tool called `netsim` which, as the name
suggests, is a way to simulate networks.  The details are not important
at this point, the thing you need to remember is that we're using an
emulated network device to demonstrate the interoperability testing
tools:

NSO uses Network Element Drivers, NEDs, to communicate with
devices. Rather than closed, hard-coded adapters, NEDs use YANG
modeled device interfaces. NSO can then render the required commands
or operations directly from this model.  NEDs support legacy NB
interfaces like CLIs or SNMP as well as modern ones like NETCONF.

`ncs-netsim create-network` creates a simulated device and sets up NSO
to use a CLI NED.  We will obviously use NETCONF so in the first part
of this demo we will show how to create a NETCONF NED.

We create a network consisting of three NETCONF devices and two CLI
devices.  The cisco-ios NED is a standard CLI NED for a simulated
Cisco IOS device that comes with all NSO installations.

TODO: Move from ned directory to the directory from which we run the
      example, i.e. the nso directory.  One question is - should we
      create the directory as part of the example or should we have it
      as part of the image?  The argument for the former is - that's
      what people doing this themselves would have to do.  The
      argument for the latter is - let's focus on the essential things
      we want to show in this demo.

`ncs-netsim create-network /neds/nc/netsim 3 nc cisco-ios 2 cli`{{execute}}

And start the network. `ncs-netsim start`

TODO: look at the devices `ncs-netsim is-alive`, `ncs-netsim ssh`, ...

When done, we will have a network consisting of three NETCONF and two
CLI devices.  We are now ready to setup and connect an NSO instance to
our simulated device:

`ncs-setup --dest . --netsim-dir netsim`{{execute}}.

This sets up an NSO instance configured (ip addresses, ports, access
credentials, etc) to use the simulated devices we just created in the
current directory. You can use `ls`{{execute}} to see the files that
were created.

It's time to start  NSO itself (this will take a few seconds)

`ncs`{{execute}}.

We can view information about the running instance:

`ncs --status`{{execute}}.

We now have a complete NSO instance running and are ready to start
exploring NSO!
