from homeassistant.components.camera import Camera, CameraEntityFeature

DOMAIN = "ms_ip_cam"

class MyProCamera(Camera):
    def __init__(self, rtsp_url: str):
        super().__init__()
        self._attr_name = "MS IP Cam Feed"
        self._stream_source = rtsp_url
        self._attr_supported_features = CameraEntityFeature.STREAM

    @property
    def name(self):
        return self._attr_name

    async def stream_source(self):
        return self._stream_source

async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([MyProCamera(data["rtsp_url"])])
