"""Every KNOWN_SERVICES variable must actually reach `app.config`.

Found while deploying alert.pdhc's grant. `KNOWN_SERVICES` named
`ALERT_PDHC_SERVICE_KEY`, the operator would have put it in `.env`, and the
caller would still have been refused forever -- because
`api/auth.py::_service_key_outcome` resolves the expected key through
`current_app.config`, and `config.py` maps each variable BY HAND. A variable
nobody mapped resolves to `''`, and `if not expected: return False`.

So the allowlist entry and the config mapping are two halves of one wire, and
nothing tied them together. The #912 suite could not catch it: it supplies the
key by assigning `app.config[...]` directly, which is the ingredient, not the
dish.

Asserting PRESENCE rather than a value is deliberate. `Config` is a class
body, so `os.environ.get(...)` runs once at import time; a test that sets the
variable afterwards and rebuilds the app proves nothing. Presence is the
signal that survives import order: a mapped variable is a config key (possibly
empty), an unmapped one is absent entirely.
"""

from app.api.auth import KNOWN_SERVICES

_ABSENT = object()


class TestEveryAllowlistVariableIsMapped:

    def test_known_services_is_not_empty(self):
        """Premise. An empty allowlist would make every assertion below
        vacuously true, which is the shape of a test that cannot fail."""
        assert len(KNOWN_SERVICES) >= 2

    def test_every_variable_reaches_config(self, app):
        unmapped = [
            (service, cfg_var)
            for service, (cfg_var, _role) in KNOWN_SERVICES.items()
            if app.config.get(cfg_var, _ABSENT) is _ABSENT
        ]
        assert unmapped == [], (
            'these KNOWN_SERVICES variables are not mapped in config.py, so '
            'setting them in .env has NO effect and the caller is refused '
            'with a correct-looking .env: %s' % unmapped)

    def test_the_control_variable_is_mapped(self, app):
        """sim.pdhc has been wired since 2026-10-05 and must pass the same
        assertion. If this fails, the probe above is broken, not the code."""
        cfg_var, _role = KNOWN_SERVICES['sim.pdhc']
        assert app.config.get(cfg_var, _ABSENT) is not _ABSENT
