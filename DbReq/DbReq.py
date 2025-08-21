import os

from typing import List,Dict,Any
from .utils import get_from_list,parse_hafas_lid
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

        self.raw_res:requests.Response = None
        self.json:dict = None

        self.base_info:dict = {"origin":parse_hafas_lid(start_id),
                               "destination": parse_hafas_lid(end_id)}

        self.base_params["abfahrtsHalt"] = start_id
        self.base_params["ankunftsHalt"] = end_id
        

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
            data=json.dumps(self.base_params).encode("utf-8")  # explicit UTF-8 encoding
        )

        return self

    def get_json(self):
        if self.raw_res is None:
            raise ValueError("Data has not been retrieved yet. Call retrieve_data() first.")
        if self.raw_res.status_code != 201:
            raise ValueError(f"Request failed with status code {self.raw_res.status_code}")
        self.json = self.raw_res.json()
        return self
    

class DbParser:
    fields_tb_parsed: Dict[str, List[str]] 

    @classmethod
    def from_parent(cls,parent,dict_data: List[Dict[str, Any]]):
        return [cls(parent,item) for item in get_from_list(dict_data,cls.fields_tb_parsed)]



class DbCon(DbParser):
    fields_tb_parsed = {"ctxRec":["ctxRecon"],
                        "Fahrtkosten":["angebotsPreis","betrag"],
                        "child" : ["verbindungsAbschnitte"]}

    def __init__(self,parent:DbReq, parsed:Dict[str, Any]):
        self.base_info = parent.base_info
        self.ctxRec = parsed["ctxRec"]
        self.betrag = parsed["AngebotsPreis"]["betrag"]
        
        self.dep_time = parent.base_params["anfrageZeitpunkt"]
        self.dep_bhf = parent.base_info["origin"]["name"]
        self.end_id = parent.base_info["destination"]["name"]

        self.dict_cont = parsed["child"]

class DbConAbs(DbParser):
    fields_tb_parsed = ["externeBahnhofsinfoIdOrigin","externeBahnhofsinfoIdDestination","abfahrtsZeitpunkt","abfahrtsOrt","abfahrtsOrtExtId","abschnittsDauer","abschnittsAnteil","ankunftsZeitpunkt","ankunftsOrt","ankunftsOrtExtId"]
    
    def __init__(self, db_req:DbCon):
        super().__init__(db_req.parsed)

    

    
        
