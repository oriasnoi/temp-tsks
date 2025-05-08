from checkov.common.models.enums import CheckCategories, CheckResult
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck

class FirewallDBPortsNoPublicAccess(BaseResourceCheck):
    def __init__(self):
        name = "Ensure 5432 port is not publicly accessible"
        id = "XXX-GCP-6001"
        s_r = ["google_compute_firewall"]
        categs = [CheckCategories.NETWORKING]
        super().__init__(name=name, id=id, categories=categs, supported_resources=s_r)

    def scan_resource_conf(self, conf):
        is_ports = '5432' in conf['allow'][0]['ports'][0]
        is_range = ['0.0.0.0/0'] in conf['source_ranges']
        return CheckResult.FAILED if is_ports and is_range \
          else CheckResult.PASSED

check = FirewallDBPortsNoPublicAccess()
