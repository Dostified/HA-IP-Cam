import logging
from homeassistant.components.camera import Camera, CameraEntityFeature
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)
DOMAIN = "ms_ip_cam"

class MyProCamera(Camera):
    """MS IP Cam implementation with robust background support."""
    
    _attr_has_entity_name = True
    _attr_name = "Camera Feed"
    
    def __init__(self, entry_id, rtsp_url, ip_address, http_port):
        super().__init__()
        self._attr_unique_id = f"{entry_id}_camera"
        self._rtsp_url = rtsp_url
        self._ip = ip_address
        self._port = http_port
        self._attr_supported_features = CameraEntityFeature.STREAM
        self._is_recording = False
        self._is_streaming = False
        self._entry_id = entry_id

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
        }

    async def stream_source(self):
        """Return the RTSP stream source."""
        return self._rtsp_url

    async def async_update(self):
        """Update camera status by polling the phone app's status endpoint."""
        try:
            session = async_get_clientsession(self.hass)
            async with session.get(f"http://{self._ip}:{self._port}/status", timeout=5) as response:
                if response.status == 200:
                    data = await response.json()
                    self._is_recording = data.get("is_recording", False)
                    self._is_streaming = data.get("is_streaming", False)
                    self._attr_extra_state_attributes = {
                        "is_recording": self._is_recording,
                        "is_streaming": self._is_streaming,
                        "lens": data.get("lens", "unknown"),
                        "client_count": data.get("client_count", 0),
                    }
                    self._attr_available = True
                else:
                    self._attr_available = False
        except Exception as e:
            _LOGGER.debug("Error updating MS IP Cam status: %s", e)
            self._attr_available = False

async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([MyProCamera(
        entry.entry_id,
        data["rtsp_url"], 
        data["ip_address"], 
        data["http_port"]
    )])
