import streamlit as st
import json
import os
from debris_processor import calculate_debris_area

INPUT_FOLDER = "/tmp/inputs"
files = os.listdir(INPUT_FOLDER)

jsons = []
for file in files:
    with open(f"{INPUT_FOLDER}/file") as j:
        _coco = json.load(j)
        jsons.append(_coco)

areas = [
    calculate_debris_area(coco) for coco in jsons
]

debris_areas = [
    area[0] for area in areas
]

not_debris_areas = [
    area[1] for area in areas
]

dates = [
    f"{file.split('_')[1]}-{file.split('_')[0]}" for file in files
]

df = pd.DataFrame(areas, columns=["debris_area", "not_debris_area"])
df.index = dates

df["debris_rolling"] = df.debris_area.rolling(2).mean()
df["non_debris_rolling"] = df.not_debris_area.rolling(2).mean()
dec_debris = df.debris_rolling.mean()
dec_nondebris = df.non_debris_rolling.mean()
df.loc["2022-12"] = {"debris_area": dec_debris, "not_debris_area": dec_nondebris}
df = df[["debris_area", "not_debris_area"]]

st.title("Debris areas in time.")

st.bar_chart(data=df)


