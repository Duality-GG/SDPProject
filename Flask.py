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
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
