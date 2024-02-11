from zipfile import ZipFile
import pandas as pd
import json
from timezonefinder import TimezoneFinder
from datetime import datetime, timedelta

# set the path to your Google Location History takeout file here
history_data_file = "takeout-20240210T125213Z-001.zip"

# store all places into this array
place_visits = []

with ZipFile(history_data_file) as myzip:
    for file in myzip.filelist[:]:
        filename = file.filename
        
        if "Semantic Location History" in filename:
            # process all files in "Semantic Location History" directory
            history_json = json.load(myzip.open(filename))

            for timeline_object in history_json["timelineObjects"]:
               
                if "placeVisit" in timeline_object:
                    place_visit_json = timeline_object["placeVisit"]
                    
                    # skip places without geographical coordinates
                    if not "location" in place_visit_json or not "latitudeE7" in place_visit_json["location"]:
                        continue
                    
                    place_visit = {
                        #"placeId": place_visit_json["location"]["placeId"],
                        "locationConfidence": place_visit_json["location"]["locationConfidence"],
                        "startTimestamp": place_visit_json["duration"]["startTimestamp"],
                        "endTimestamp": place_visit_json["duration"]["endTimestamp"],
                        "placeVisitImportance": place_visit_json["placeVisitImportance"],
                        "placeVisitType": place_visit_json["placeVisitType"],
                        "latitudeE7": place_visit_json["location"]["latitudeE7"],
                        "longitudeE7": place_visit_json["location"]["longitudeE7"],
                    }
                    
                    for optional_field in ["centerLatE7", "centerLngE7"]:
                        if optional_field in place_visit_json:
                            place_visit[optional_field] = place_visit_json[optional_field]
                        else:
                            place_visit[optional_field] = None
                    
                    for optional_field in ["name", "address"]:
                        if optional_field in place_visit_json["location"]:
                            place_visit[optional_field] = place_visit_json["location"][optional_field]
                        else:
                            place_visit[optional_field] = None
                                            
                    place_visits.append(place_visit)

place_visits_df = pd.DataFrame(place_visits)

place_visits_df["startTimestamp"] = pd.to_datetime(place_visits_df["startTimestamp"], format="ISO8601")
place_visits_df["endTimestamp"] = pd.to_datetime(place_visits_df["endTimestamp"], format="ISO8601")

# get geo coordinates as float value
place_visits_df["latitude"] = place_visits_df.latitudeE7/1E7
place_visits_df["longitude"] = place_visits_df.longitudeE7/1E7
place_visits_df["centerLat"] = place_visits_df.centerLatE7/1E7
place_visits_df["centerLng"] = place_visits_df.centerLngE7/1E7

# add timezone based on geo coordinates
tf = TimezoneFinder()
place_visits_df["timezone"] = place_visits_df.apply(lambda row: tf.timezone_at(lng=row.longitude, lat=row.latitude), axis=1)

# convert UTC time to local timezone
place_visits_df['startTimestamp_local'] = place_visits_df.apply(lambda row: row.startTimestamp.tz_convert(row.timezone), axis=1)
place_visits_df['endTimestamp_local'] =place_visits_df.apply(lambda row: row.endTimestamp.tz_convert(row.timezone), axis=1)

# remove TZ info from datetime
place_visits_df['startTimestamp_local'] = pd.to_datetime(place_visits_df['startTimestamp_local'].apply(lambda x: x.replace(tzinfo=None)))
place_visits_df['endTimestamp_local'] = pd.to_datetime(place_visits_df['endTimestamp_local'].apply(lambda x: x.replace(tzinfo=None)))

# add datetime parts as a separate column to data frame
for datetime_type in [("year", lambda x: x.year), ("month", lambda x: x.month), ("day", lambda x: x.day), ("hour", lambda x: x.hour), ("minute", lambda x: x.minute), ("weekday", lambda x: x.weekday)]:
   for tztype in ["", "_local"]:
       place_visits_df[f"{datetime_type[0]}{tztype}"] = datetime_type[1](place_visits_df[f"startTimestamp{tztype}"].dt)
     
place_visits_df.drop(columns=["latitudeE7", "longitudeE7", "centerLatE7", "centerLngE7"], inplace=True)

place_visits_df["duration"] = place_visits_df.endTimestamp - place_visits_df.startTimestamp
place_visits_df["duration_minutes"] = place_visits_df.duration.dt.total_seconds()/60

place_visits_df.to_csv("place_visits.csv", index=False)
