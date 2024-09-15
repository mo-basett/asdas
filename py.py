from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from geopy.distance import geodesic
from plyer import gps
import platform
import android

# Define road bumps coordinates
road_bumps = [
    (37.7749, -122.4194),  # Example: San Francisco
    (34.0522, -118.2437),  # Example: Los Angeles
]



class RoadBumpApp(App):
    def build(self):
        self.label = Label(text="Fetching location...")
        self.start_gps()
        return self.label
    
    # def get_current_location(self):
    #     if platform.system() == 'Windows':
    #         # Simulated location for testing on Windows
    #         return (37.7749, -122.4194)  # San Francisco, CA
    #     else:
    #         # Actual GPS location (will work on mobile platforms)
    #         gps.configure(on_location=self.on_location, on_status=self.on_status)
    #         gps.start()

    def start_gps(self):
        try:
            gps.configure(on_location=self.on_location, on_status=self.on_status)
            gps.start()
        except NotImplementedError:
            self.label.text = "GPS is not available on your device."

    def on_location(self, **kwargs):
        current_location = (kwargs['lat'], kwargs['lon'])
        self.label.text = f"Current location: {current_location}"
        self.check_proximity(current_location)

    def on_status(self, stype, status):
        self.label.text = f"GPS status: {status}"

    def check_proximity(self, current_location):
        for bump in road_bumps:
            distance = geodesic(current_location, bump).km
            if distance < 0.1:  # 100 meters
                self.label.text = "Warning: Approaching a road bump!"
                break

    def on_stop(self):
        gps.stop()

if __name__ == '__main__':
    RoadBumpApp().run()
