Must enable two-phase commit and candidate in confd.conf in the netsim
devices.  Note, even though we use ConfD to implement our CLI devices
and have a full transaction engine and support for two-phase commit
and so on and so forth this is not necessarily the case and we won't
enable these feature in the CLI devices in this example.

It turns out that candidate datastore and confirmed-commit is already
enabled.  How do we get NSO to enable the timeout confirmation?

Provide a python app we can use to introduce errors when NSO makes
configuration changes forcing rollback to the original configuration.
Demonstrate that this is fully automatic in the NETCONF case it
becomes best effort in the CLI case and if we lose access to the
device or the device fails to apply the old config for some other
reason there's nothing NSO can do about it.

Effectively, network wide transaction becomes just best effort
consistency due to non-transactional nodes.
