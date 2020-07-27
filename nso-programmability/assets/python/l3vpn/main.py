# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.application import Service

#### ECI EANTC19
## ip_size_to_mask = [
##     "0.0.0.0",
##     "128.0.0.0",       "192.0.0.0",       "224.0.0.0",       "240.0.0.0",
##     "248.0.0.0",       "252.0.0.0",       "254.0.0.0",       "255.0.0.0",
##     "255.128.0.0",     "255.192.0.0",     "255.224.0.0",     "255.240.0.0",
##     "255.248.0.0",     "255.252.0.0",     "255.254.0.0",     "255.255.0.0",
##     "255.255.128.0",   "255.255.192.0",   "255.255.224.0",   "255.255.240.0",
##     "255.255.248.0",   "255.255.252.0",   "255.255.254.0",   "255.255.255.0",
##     "255.255.255.128", "255.255.255.192", "255.255.255.224", "255.255.255.240",
##     "255.255.255.248", "255.255.255.252", "255.255.255.254", "255.255.255.255" ]

ECI_ns       = "urn:eci:params:xml:ns:yang:eci-interfaces-aug"
ERICSSON_ns  = "urn:rdns:com:ericsson:oammodel:ericsson-interfaces-ext-ipos"
UTSTARCOM_ns = "urn.utstar:uar:SRv6VpnCmmCfg"

class Unsupported(Exception):
    pass

# ----------------
# SERVICE CALLBACK
# ----------------
class ServiceCallbacks(Service):

    #### TODO: Do we need something better here?
    def allocate_vlanid(self, vlan_name):
        return "4046" #return str(hash(vlan_name)%1000+1000)

    def allocate_rd(self, vlan_name):
        return "100:10"

    #### Ericsson EANTC18
    ## def get_device_rd(self, device_name):
    ##     if device_name=="e6471": return "100.0.0.53:300"
    ##     return "300:2224"

    def get_others(self, root, our_site, our_vpn_id):
        others = []
        for site in root.l3vpn_svc__l3vpn_svc.sites.site:
            if site == our_site:
                continue
            for pol in site.vpn_policies.vpn_policy:
                for ent in pol.entries:
                    for vpn in ent.vpn:
                        if vpn.vpn_id == our_vpn_id:
                            self.log.info('otherside site: ', site.site_id)
                            others += [site]
        return others

    #### Not used????
    ## def ip_add(self, s, incr):
    ##     return s[:s.rfind('.')]+'.'+str(int(s[s.rfind('.')+1:])+incr)        # Not perfect, copy at your own risk

    @Service.create
    def cb_create(self, tctx, root, service, proplist):
      self.log.info('Service create (service=', service._path, ')')
      self.log.info('Copy that (service=', service._path, ')')

      try:
        self.log.info('site ', service.site_id)
        for site_network_access in service.site_network_accesses.site_network_access:
            self.log.info('site-network-access-id: ', site_network_access.site_network_access_id)
            ## pol_id = site_network_access.vpn_attachment.vpn_policy_id
            vpn_name = site_network_access.vpn_attachment.vpn_id
            vpn_site_role = site_network_access.vpn_attachment.site_role
            if vpn_site_role != 'l3vpn-svc:any-to-any-role':
                raise Unsupported("Only any-to-any-role supported")
            self.log.info('vpn_name, i.e. vpn-id=', vpn_name)
            self.log.info('vpn_site_role=', vpn_site_role)
            # vpn_policy_id rather than vpn_id directly because we
            # need "site_role" which is attached to vpn_policy, not
            # vpn_id?  No, that seems like it's wrong.  You can get
            # site-role indirectly through vpn-attachment.  Would that
            # shorten this code - I think it would because you
            # wouldn't need to loop (not once but twice) since
            # vpn-attachment is not a list.
            device_name = site_network_access.device_reference
            ## device_capas = root.devices.device[device_name].capability
            self.log.info('device: ', device_name)
            ## for pol_entry in service.vpn_policies.vpn_policy[pol_id].entries:
            ##     self.log.info('policy: ', pol_entry.id)
            ##     for vpn in pol_entry.vpn:
            ##         self.log.info('role: ', vpn.site_role)
            ##         if vpn.site_role != 'l3vpn-svc:any-to-any-role':
            ##             raise Unsupported("Only any-to-any-role supported")
            ##         vpn_name = vpn.vpn_id
            # Indented as above in the original code.
            self.log.info('vpn: ', vpn_name)
            vlan_id = self.allocate_vlanid(vpn_name)
            rd = self.allocate_rd(vpn_name)
            self.log.info('vlan_id: ', vlan_id)
            interface_name         = root.topo__topo[vpn_name,device_name].interface
            phys_interface_name    = root.topo__topo[vpn_name,device_name].phys_interface
            ## IOSXR EANTC19 router_address         = root.topo__topo[vpn_name,device_name].address

            self.log.info('vpn_name: ', vpn_name)
            self.log.info('device_name: ', device_name)
            self.log.info('interface: ', interface_name)
            net_addresses = site_network_access.ip_connection.ipv4.addresses
            net6_addresses = site_network_access.ip_connection.ipv6.addresses
            self.log.info('interface: ', interface_name,
                          ' net (ipv4): ', net_addresses.provider_address, '/',
                          net_addresses.prefix_length)
            self.log.info('interface: ', interface_name,
                          ' net (ipv6): ', net6_addresses.provider_address, '/',
                          net6_addresses.prefix_length)

            ## Not used ## for other in self.get_others(root, service, vpn_name):
            ## Not used ##     self.log.info('otherside sites2: ', other.site_id)
            ## Not used ##     for other_site_network_access in other.site_network_accesses.site_network_access:
            ## Not used ##         self.log.info('other-site-acc: ', other_site_network_access.site_network_access_id)
                    ## Not used ## other_pol_id = other_site_network_access.vpn_attachment.vpn_policy_id
                    ## Not used ## other_device_name = other_site_network_access.device_reference
                    ## Not used ## other_device = root.topo__topo[vpn_name,other_device_name]

            vars = ncs.template.Variables()
            vars.add('DEVICE',               device_name)
            vars.add('INTERFACE',            interface_name)
            vars.add('PHYS_INTERFACE',       phys_interface_name)
            vars.add('VLANID',               vlan_id)
            vars.add('VRF_ID',               str(int(vlan_id) % 90 + 10)) # 10..99
            vars.add('VPN_NAME',             vpn_name)
            ## Ericsson EANTC18 ## vars.add('RD1',                  self.get_device_rd(device_name))
            ## IOSXR EANTC19 ## vars.add('ROUTER_ADDRESS',       router_address)
            vars.add('RD',                   rd)
            vars.add('NET',                  net_addresses.provider_address)
            vars.add('PREFIXLEN',            net_addresses.prefix_length)
            ## ECI EANTC19 ## vars.add('MASK',                 ip_size_to_mask[net_addresses.prefix_length])
            vars.add('NET6',                 net6_addresses.provider_address)
            vars.add('PREFIXLEN6',           net6_addresses.prefix_length)
            ## Not used ## vars.add('NEXT_HOP',             other_device.address)
            self.log.info('DEVICE = ', device_name)
            self.log.info('INTERFACE = ', interface_name)
            self.log.info('PHYS_INTERFACE = ', phys_interface_name)
            self.log.info('VLANID = ', vlan_id)
            self.log.info('VRF_ID = ', str(int(vlan_id) % 90 + 10))
            self.log.info('VPN_NAME = ', vpn_name)
            self.log.info('RD = ', rd)
            self.log.info('NET = ', net_addresses.provider_address)
            self.log.info('PREFIXLEN = ', net_addresses.prefix_length)
            self.log.info('NET6 = ', net6_addresses.provider_address)
            self.log.info('PREFIXLEN6 = ', net6_addresses.prefix_length)

            template = ncs.template.Template(service)
            template.apply('ce-interface', vars)
            self.log.info('applied ce-interface template')
            template.apply('vrf', vars)
            self.log.info('applied vrf template')

        self.log.info('Service create done.')
      except Exception as e:
        self.log.info('Service exception: %s'%e)

# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class Main(ncs.application.Application):
    def setup(self):
        self.log.info('Main RUNNING')
        self.register_service('l3vpn-servicepoint', ServiceCallbacks)
    def teardown(self):
        self.log.info('Main FINISHED')
