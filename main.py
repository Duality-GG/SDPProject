from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
import requests
from bs4 import BeautifulSoup
import cv2 
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.core.clipboard import Clipboard
from kivy.uix.screenmanager import SlideTransition
from flask import Flask

# Define your Screen classes first
class MainScreen(Screen):
    pass

class FirstScreen(Screen):
    def display_coordinates(self, coords):
        # Displaying coordinates in a popup
        popup = Popup(title='Coordinates',
                      content=Label(text=coords),
                      size_hint=(None, None), size=(600, 200))
        popup.open()

class ImageButton(ButtonBehavior, Image):
    pass

class SecondScreen(Screen):
    def display_coordinates(self, coords):
        # Displaying coordinates in a popup
        popup = Popup(title='Coordinates',
                      content=Label(text=coords),
                      size_hint=(None, None), size=(400, 200))
        popup.open()

    def copy_to_clipboard(self, coords):
        Clipboard.copy(coords)

class ThirdScreen(Screen):
    capture = None
    def start_camera(self):
        #  USB connection through DroidCam
        
        # Start the camera capture
        self.capture = cv2.VideoCapture(1)
        Clock.schedule_interval(self.update, 1.0 / 30.0)  #  for 30 FPS, 60 might work? not sure entirely 

    def stop_camera(self):
        # Stop the camera capture
        if self.capture:
            Clock.unschedule(self.update)
            self.capture.release()
            self.capture = None

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # Convert it to texture
            buf = cv2.flip(frame, 0).tostring()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.ids.camera_image.texture = texture
        else:
            self.stop_camera()

    def move_up(self):
        print("Up pressed")
        # later movement logic here

    def move_down(self):
        print("Down pressed")
        # later movement logic here

    def move_left(self):
        print("Left pressed")
        # later movement logic here

    def move_right(self):
        print("Right pressed")
        # later movement logic here
            
class SettingsScreen(Screen):
    pass

# After the classes, load the kv file
Builder.load_file('myapp.kv')

class MyApp(App):
    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(FirstScreen(name='first'))
        sm.add_widget(SecondScreen(name='second'))
        sm.add_widget(ThirdScreen(name='third'))
        sm.add_widget(SettingsScreen(name='settings'))
        return sm
    
class Links():
    def main():
        # Prompt user to paste the URL
        url = input("Please paste the URL here: ")

        print(f"Fetching data from: {url}")
        ra, dec = fetch_astro_data(url)

        if ra and dec:
            print(f"Right Ascension: {ra}, Declination: {dec}")
        else:
            print("Data not found or the website structure has changed.")

    def fetch_astro_data(url):
        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the div with class 'keyinfobox'
            key_info_boxes = soup.find_all('div', class_='keyinfobox')

            right_ascension = None
            declination = None

            for box in key_info_boxes:
                label = box.find('label')
                if label:
                    label_text = label.get_text().strip()
                    if 'Right Ascension J2000' in label_text:
                        right_ascension = label.find_next_sibling().get_text().strip()
                    elif 'Declination J2000' in label_text:
                        declination = label.find_next_sibling().get_text().strip()

            return right_ascension, declination

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from the website: {e}")

if __name__ == '__main__':
    MyApp().run()