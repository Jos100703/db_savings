import requests
import re
import json
import os
import urllib
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import DbReq

script_dir = os.path.dirname(os.path.abspath(__file__))


with open(os.path.join(script_dir,"..", "Testing","test_res", "input_url.txt"),"r") as f:
    url_input = f.read().strip()

db_req = DbReq.DbReq.from_input_link(url_input)

print("hello world")

