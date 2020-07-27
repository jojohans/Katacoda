It's important to realize that CLI NEDs typically just cover the use
cases someone has been interested in and if new behavior is required
new code and new modeling is required.  Further more, even after this
has been added only a small extra use case is supported.  For NETCONF
on the other hand, we get full support for everything a device support
right out of the box and even if new functionality (new YANG-models)
are added to the device this only requires a simple re-compilation (no
code).

Make a small addition to the device model and compare the effort
needed to cover the extender interface for NETCONF NEDs and CLI NEDs.

For a NETCONF NED we just add the new or update the model to the YANG
directory in the package and run make to have a new NED.  For CLI
devices we must update the CLI model and add code to the device API.
