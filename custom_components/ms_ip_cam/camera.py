from homeassistant.components.camera import Camera, CameraEntityFeature

class MyProCamera(Camera):
    def __init__(self, ip_address: str, rtsp_port: int):
        super().__init__()
        self._attr_name = "MS IP Cam Feed"
        self._stream_source = f"rtsp://{ip_address}:{rtsp_port}/live"
        self._attr_supported_features = CameraEntityFeature.STREAM

    @property
    def name(self):
        return self._attr_name

    async def stream_source(self):
        return self._stream_source

async def async_setup_entry(hass, entry, async_add_entities):
    ip_address = entry.data["ip_address"]
    rtsp_port = entry.data["rtsp_port"]
    async_add_entities([MyProCamera(ip_address, rtsp_port)])
