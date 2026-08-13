# HA IP Cam for Home Assistant

This is a custom integration that connects Home Assistant to the HA IP Cam Android app. It provides a true on-demand RTSP feed, flashlight toggles, and lens controls directly from your Home Assistant dashboard.

## Installation via HACS

1. Open Home Assistant and go to **HACS**.
2. Click the three dots (`⋮`) in the top right corner and select **Custom repositories**.
3. Paste the URL of this repository into the repository URL box.
4. Select **Integration** as the category and click **ADD**.
5. Close the popup. "MS IP Cam" will now appear in your HACS store. 
6. Click it, then click **Download** in the bottom right corner.
7. **Restart Home Assistant**.

## Configuration

After restarting, open your `configuration.yaml` file and add the following:

```yaml
ms_ip_cam:
