import ldap
import settings
from util import serialize, dn2domain, domain2dn
from forms import required, validate

class DomainListResource:
    def __init__(self, conn):
        self.conn = conn

    @serialize
    def on_get(self, req, resp):
        keys = "dn", "description"
        args = domain2dn(settings.BASE_DOMAIN), ldap.SCOPE_SUBTREE, "objectClass=domain", keys
        domains = dict()
        for dn, attributes in self.conn.search_s(*args):
            domains[dn2domain(dn)] = attributes.get("description", [None]).pop()
        return domains
        
    @serialize
    @required("description")
    @validate("name", regex="[a-z][a-z0-9]+$")
    def on_post(self, req, resp):
        ldif_domain = modlist.addModlist(dict(
            description=req.get_param("description"),
            dc=req.get_param("name"),
            objectclass=["top", "domain"]
        ))
        print ldif_domain
        
        # add ou=people?
        # add ou=groups?