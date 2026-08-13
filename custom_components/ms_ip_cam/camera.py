from homeassistant.components.camera import Camera, CameraEntityFeature

class MyProCamera(Camera):
    def __init__(self, ip_address: str, rtsp_port: int):
        """Initialize the camera with data from the UI Config Flow."""
        super().__init__()
        self._attr_name = "MS IP Cam Feed"
        
        # Dynamically build the RTSP stream URL
        self._stream_source = f"rtsp://{ip_address}:{rtsp_port}/live"
        self._attr_supported_features = CameraEntityFeature.STREAM

    @property
    def name(self):
        return self._attr_name

    async def stream_source(self):
        """Return the stream source URL."""
        return self._stream_source

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the camera from a config entry."""
    ip_address = entry.data["ip_address"]
    rtsp_port = entry.data["rtsp_port"]
    
    async_add_entities([MyProCamera(ip_address, rtsp_port)])
