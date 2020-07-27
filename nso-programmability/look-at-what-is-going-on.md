Investigate the difference between NETCONF NEDs and CLI NEDs from NSOs
point-of-view.  We'll look at the work involved in creating NEDs, the
amount of code needed to create a CLI NED.

Look into the difference in the amount of work NSO has to do in order
to support rollback for devices managed through NETCONF NEDs and
compared to CLI NEDs.

Look at the commands NSO send to a NETCONF device and compare it the
commands sent for the same configuration change for a CLI device.

* netconf.trace log
* trace progress in the NSO cli
* how do we trace traffic to CLI devices?
