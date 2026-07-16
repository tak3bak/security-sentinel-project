import datetime

class AuditWriter:
    def __init__(self, path="audit.md"):
        self.path = path

    def write(self, event, intel):
        timestamp = datetime.datetime.utcnow().isoformat()

        entry = f"""
## Event @ {timestamp}

**Input:**  
`{event}`

**Domain:** {intel.get("domain")}
**Risk Score:** {intel.get("score")}
**Risk Level:** {intel.get("risk_level")}

### Key Factors
{self._format_list(intel.get("factors", []))}

### Domain Intel
- Registrar: {intel["intel"].get("registrar")}
- Created: {intel["intel"].get("creation_date")}
- Expires: {intel["intel"].get("expiration_date")}
- Nameservers: {", ".join(intel["intel"].get("nameservers", []))}
- IPv4: {", ".join(intel["intel"].get("ipv4", []))}
- IPv6: {", ".join(intel["intel"].get("ipv6", []))}

---

"""

        with open(self.path, "a") as f:
            f.write(entry)

    def _format_list(self, items):
        return "\n".join([f"- {item}" for item in items])
