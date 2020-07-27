# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.application import Service

# service=root.l2vpn_svc__l2vpn_svc.sites.site["berlin"]
# acc2=service.site_network_accesses.site_network_access["acc-2"]
# acc2.ip_connection.ipv4.addresses

# ----------------
# SERVICE CALLBACK
# ----------------
class ServiceCallbacks(Service):

    def get_pw_id(self, device):
        if device == 'meta134':
            return 4145
        elif device == 'juniper105':
            return 4046
        else:
            return 0

    def get_others(self, root, our_site, our_vpn_id):
        others = []
        for site in root.l2vpn_svc__l2vpn_svc.sites.site:
            if site == our_site:
                continue
            for pol in site.vpn_policies.vpn_policy:
                for ent in pol.entries:
                    for vpn in ent.vpn:
                        if vpn.vpn_id == our_vpn_id:
                            self.log.info('otherside site: ', site.site_id)
                            others += [site]
        return others

    @Service.create
    def cb_create(self, tctx, root, service, proplist):

        self.log.info('Service create(service=', service._path, ')')

        self.log.info('site ', service.site_id)
        for site_network_access in service.site_network_accesses.site_network_access:
            self.log.info('site-acc: ', site_network_access.network_access_id)
            pol_id = site_network_access.vpn_attachment.vpn_policy_id
            device_name = site_network_access.device_reference
            self.log.info('device: ', device_name)
            for pol_entry in service.vpn_policies.vpn_policy[pol_id].entries:
                self.log.info('policy: ', pol_entry.id)
                for vpn in pol_entry.vpn:
                    vpn_name = vpn.vpn_id
                    self.log.info('vpn_name: ', vpn_name)
                    topo_this = root.topo_l2__topo_l2[vpn_name,device_name]
                    interface_name = topo_this.interface
                    self.log.info('device_name: ', device_name)
                    self.log.info('interface: ', interface_name)

                    for other in self.get_others(root, service, vpn_name):
                        self.log.info('otherside sites2: ', other.site_id)
                        for other_site_network_access in other.site_network_accesses.site_network_access:
                            self.log.info('other-site-acc: ', other_site_network_access.network_access_id)
                            other_pol_id = other_site_network_access.vpn_attachment.vpn_policy_id
                            other_device_name = other_site_network_access.device_reference
                            other_device = root.topo_l2__topo_l2[vpn_name,other_device_name]
                            #pw_id = self.get_pw_id(device_name)
                            pw_id = 4046

                            self.log.info('DEVICE: ', device_name)
                            self.log.info('PHYS_INTERFACE: ', interface_name)
                            self.log.info('VPN_NAME: ', vpn_name)
                            self.log.info('REM_ROUTER_ID: ', other_device.router_id)
                            self.log.info('PW_ID: ', pw_id)

                            vars = ncs.template.Variables()
                            vars.add('DEVICE',        device_name)
                            vars.add('PHYS_INTERFACE',interface_name)
                            vars.add('VPN_NAME',      vpn_name)
                            vars.add('REM_ROUTER_ID', other_device.router_id)
                            vars.add('PW_ID',         pw_id)

                            template = ncs.template.Template(service)
                            template.apply('l2vpn-svc-create', vars)

        self.log.info('Service create done.')

    def cb_create_18(self, tctx, root, service, proplist):
        self.log.info('Service create(service=', service._path, ')')

        self.log.info('site ', service.site_id)
        for site_network_access in service.site_network_accesses.site_network_access:
            self.log.info('site-acc: ', site_network_access.network_access_id)
            pol_id = site_network_access.vpn_attachment.vpn_policy_id
            device_name = site_network_access.device_reference
            self.log.info('device: ', device_name)
            for pol_entry in service.vpn_policies.vpn_policy[pol_id].entries:
                self.log.info('policy: ', pol_entry.id)
                for vpn in pol_entry.vpn:
                    vpn_name = vpn.vpn_id
                    self.log.info('vpn: ', vpn_name)

                    interface_name         = root.topo_l2__topo_l2[vpn_name,device_name].interface
                    locator_name           = root.topo_l2__topo_l2[vpn_name,device_name].locator

                    for other in self.get_others(root, service, vpn_name):
                        self.log.info('otherside sites2: ', other.site_id)
                        for other_site_network_access in other.site_network_accesses.site_network_access:
                            self.log.info('other-site-acc: ', other_site_network_access.network_access_id)
                            other_pol_id = other_site_network_access.vpn_attachment.vpn_policy_id
                            other_device_name = other_site_network_access.device_reference
                            other_locator_name = root.topo_l2__topo_l2[vpn_name,other_device_name].locator

                            vars = ncs.template.Variables()
                            vars.add('DEVICE',       device_name)
                            vars.add('INTERFACE',    interface_name)
                            vars.add('VPN_NAME',     vpn_name)

                            #UTSTARCOM
                            vars.add('SP_VLAN_ID',        "1001")
                            vars.add('INTERFACE_NAME',    "eth1.1.444")
                            vars.add('LOCATOR',           locator_name)
                            vars.add('OTHERSIDE_LOCATOR', other_locator_name)
                            vars.add('PHY_INTF',          '\\\\\\interface=536873984')
                            vars.add('VPN_ID',            "111")
                            vars.add('VRF',               "111")

                            #ZTE
                            #vars.add('OTHERSIDE_IP', "100.0.0.125")
                            #xgei-0/0/1/9 INTERFACE
                            #100.0.0.125 OTHERSIDE_IP

                            template = ncs.template.Template(service)
                            template.apply('l2vpn-svc-create', vars)

        self.log.info('Service create done.')

# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class Main(ncs.application.Application):
    def setup(self):
        self.log.info('Main RUNNING')
        self.register_service('l2vpn-servicepoint', ServiceCallbacks)
    def teardown(self):
        self.log.info('Main FINISHED')
