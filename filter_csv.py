import pandas as pd
import chardet
from io import StringIO

def read_encoding(csv):
    with open(csv, "rb") as fhand:
        text = fhand.read()
    data = chardet.detect(text)
    print(data)
    encoding = data["encoding"]
    return encoding

csv = "db_discography.csv"
encoding = read_encoding(csv)
df = pd.read_csv(csv, encoding=encoding)
albums = ["Currents", "Lonerism","Innerspeaker","Tame Impala"]
new_df = df[~df["discography.album"].isin (albums)]
new_df.to_csv("Import_To_DB.csv", index=False, encoding="utf-8")