import requests
from libqtile.widget.base import _TextBox


class VPNWidget(_TextBox):

    def __init__(self, country: str, **config):
        _TextBox.__init__(self, **config)
        self.country = country
        self.text = self.get_VPN_status()

    def get_VPN_status(self):
        try:
            r = requests.get('https://api.myip.com')
            is_VPN = r.json()['country'] == self.country
        except Exception:
            return 'N/A'
        
        if is_VPN:
            return 'VPN'
        else:
            return 'Not VPN'

