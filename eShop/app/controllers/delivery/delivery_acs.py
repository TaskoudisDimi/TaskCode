from flask import Blueprint, request, jsonify, session
import requests
import os
import xml.etree.ElementTree as ET
from datetime import datetime


delivery = Blueprint('delivery', __name__)

ACS_API_KEY = "your_acs_api_key"
ACS_BASE_URL = "https://api.acscourier.net/v1"


