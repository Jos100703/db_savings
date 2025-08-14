import os
import json
import requests
from copy import deepcopy

import urllib

script_dir = os.path.dirname(os.path.abspath(__file__))

class DbReq:
    with open(os.path.join(script_dir, "..", "Configs", "base_params.json"), "r") as f:
        base_params =  json.load(f)

    with open(os.path.join(script_dir, "..", "Configs", "headers.json"), "r") as f:
        headers = json.load(f)

    base_url = "https://www.bahn.de/web/api/angebote/fahrplan"

    def __init__(self,start_id:str,end_id:str):
        self.base_params = deepcopy(self.base_params)
        self.start_id = start_id
        self.end_id = end_id

        self.raw_res = None

        self.base_params["abfahrtsHalt"] = start_id
        self.base_params["anfrageZeitpunkt"] = start_id
        

    @classmethod
    def from_input_link(cls,url:str):
        parsed = urllib.parse.urlparse(url)
        params = dict(urllib.parse.parse_qsl(parsed.fragment))

        # Extract soid and zoid
        soid = params.get("soid")
        zoid = params.get("zoid")

        if not soid or not zoid:
            raise ValueError("URL must contain 'soid' and 'zoid' parameters.")
        
        return cls(soid, zoid)

    def retrieve_data(self):

        self.raw_res = requests.post(
            self.base_url,
            headers=self.headers,
            data=self.base_params.encode("utf-8")  # explicit UTF-8 encoding
        )

        return self


class DbCon:
    def __init__(self, db_req:DbReq):
        self.raw_res = db_req.raw_res
        
