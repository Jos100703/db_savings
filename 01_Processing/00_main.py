import pandas as pd
import requests
import re
import json
import os
import urllib
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import DbReq

script_dir = os.path.dirname(os.path.abspath(__file__))


with open(os.path.join(script_dir,"..", "00_Input", "input_url.txt"),"r") as f:
    url_input = f.read().strip()

db_req = DbReq.DbReq.from_input_link(url_input)

db_req.retrieve_data()
db_req.get_json()
db_con = DbReq.DbCon.from_parent(db_req, db_req.json["verbindungen"])
db_con_sec = []
db_con_sec_stops = []
for conn in db_con:
    db_con_sec.extend(DbReq.DbConAbs.from_parent(conn,conn.child_dict))
    for sec in db_con_sec:
        db_con_sec_stops.extend(DbReq.DbConAbsStop.from_parent(sec, sec.child_dict))

final_data = [sec.__dict__ for sec in db_con_sec_stops]

final_stops_full = pd.DataFrame.from_records(final_data)

# Reorder columns to match the expected output
final_stops_full = final_stops_full[list(DbReq.DbConAbsStop.fields_tb_parsed.keys())+list(DbReq.DbConAbsStop.from_parent_inherit.keys())]


final_stops_full.to_csv(os.path.join(script_dir, "..","02_Output", "Full_conn_stops.csv"), index=False, encoding="utf-8-sig")

