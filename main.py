from flask import Flask, render_template_string, request, jsonify
from datetime import datetime
import json
import re
import random

app = Flask(__name__)

chat_history = []
user_context = {}


