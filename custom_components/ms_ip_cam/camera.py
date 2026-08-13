from homeassistant.components.camera import Camera, CameraEntityFeature

ANDROID_IP = "192.168.1.100" # Replace with your Android phone's IP

class MyProCamera(Camera):
    def __init__(self):
        super().__init__()
        self._attr_name = "Android Pro Cam Feed"
        self._stream_source = f"rtsp://{ANDROID_IP}:8554/live"
        # Enabling STREAM feature automatically enables Home Assistant's native Recording & Snapshot features!
        self._attr_supported_features = CameraEntityFeature.STREAM

    @property
    def name(self):
        return self._attr_name

    async def stream_source(self):
        # When you open the dashboard, HA calls this URL.
        # The Android app detects the connection and turns on the lens!
        return self._stream_source

def setup_platform(hass, config, add_entities, discovery_info=None):
    add_entities([MyProCamera()])