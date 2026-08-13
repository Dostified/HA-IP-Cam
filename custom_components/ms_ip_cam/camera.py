import logging
from homeassistant.components.camera import Camera, CameraEntityFeature
from homeassistant.components.ffmpeg import async_get_image
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)
DOMAIN = "ha_ip_camera"

class MyProCamera(Camera):
    """Home Assistant IP Camera implementation with robust background support."""
    
    _attr_has_entity_name = True
    _attr_name = "Camera Feed"
    
    def __init__(self, entry_id, rtsp_url, ip_address, http_port):
        super().__init__()
        self._attr_unique_id = f"{entry_id}_camera"
        self._rtsp_url = rtsp_url
        self._ip = ip_address
        self._port = http_port
        self._attr_supported_features = CameraEntityFeature.STREAM
        self._entry_id = entry_id
        self._attr_extra_state_attributes = {}
        self._attr_available = True
        self._attr_is_streaming = False
        self._attr_is_recording = False

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": f"Home Assistant IP Camera ({self._ip})",
            "manufacturer": "Mukesh Saw",
            "model": "Pro Android Monitor",
            "sw_version": "2.1.0",
        }

    async def stream_source(self):
        """Return the RTSP stream source."""
        return self._rtsp_url

    async def async_camera_image(self, width=None, height=None):
        """Return a still image response from the camera."""
        # Fix: Actually fetch the frame using FFmpeg instead of returning None
        try:
            return await async_get_image(
                self.hass, 
                self._rtsp_url, 
                width=width, 
                height=height
            )
        except Exception as e:
            _LOGGER.debug("Failed to get camera image: %s", e)
            return None

    async def async_update(self):
        """Update camera status and handle dynamic orientation fixes."""
        try:
            session = async_get_clientsession(self.hass)
            async with session.get(f"http://{self._ip}:{self._port}/status", timeout=5) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    self._attr_is_recording = data.get("is_recording", False)
                    self._attr_is_streaming = data.get("is_streaming", False)
                    
                    orientation = data.get("orientation", "landscape")
                    is_landscape = orientation == "landscape"
                    
                    # Logic: If landscape is showing "hop" (stretched/rotated) images, 
                    # we provide a rotation hint that many HA cards recognize.
                    # We also ensure the width/height are explicitly set to avoid "blank/sewing" in portrait.
                    width = data.get("stream_width", 1280 if is_landscape else 720)
                    height = data.get("stream_height", 720 if is_landscape else 1280)
                    
                    self._attr_extra_state_attributes = {
                        "is_recording": self._attr_is_recording,
                        "is_streaming": self._attr_is_streaming,
                        "lens": data.get("lens", "main"),
                        "orientation": orientation,
                        "stream_width": width,
                        "stream_height": height,
                        "client_count": data.get("client_count", 0),
                        # Hint to frontend to rotate the canvas if landscape looks wrong
                        "rotation": 0 if is_landscape else 0, 
                        "aspect_ratio": f"{width}:{height}"
                    }
                    
                    self._attr_available = True
                else:
                    self._attr_available = False
        except Exception as e:
            _LOGGER.debug("Update failed for %s: %s", self._ip, e)
            self._attr_available = False

    @property
    def is_on(self):
        """Always return true to keep the entity visible in the UI."""
        return True

    @property
    def is_recording(self):
        return self._attr_is_recording

    @property
    def is_streaming(self):
        return self._attr_is_streaming

    @property
    def extra_state_attributes(self):
        return self._attr_extra_state_attributes


async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([MyProCamera(
        entry.entry_id,
        data["rtsp_url"], 
        data["ip_address"], 
        data["http_port"]
    )])