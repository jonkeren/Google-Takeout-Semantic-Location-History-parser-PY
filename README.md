# Google-Takeout-Semantic-Location-History-parser-PY
Python script to parse the Semantic Location History files from Google Takeout, and create a CSV file from the data.
The CSV file will contain the following data for each row: `locationConfidence, startTimestamp, endTimestamp, placeVisitImportance, placeVisitType, name, address, latitude, longitude, centerLat, centerLng, timezone, startTimestamp_local, endTimestamp_local, year, year_local, month, month_local, day, day_local, hour, hour_local, minute, minute_local, weekday, weekday_local, duration, duration_minutes`.

You do not need to unzip the Google Takout file. It takes the ZIP as an input (set file name in the script), and iterates over all files in the `Semantic Location History` directory.

# How to use
1. Visit Google Takeout.
2. Click Select _None_ at the top of the list to deselect all other options.
3. Navigate down to Location History and select it. Leave the default export at JSON.
4. Click Next, and choose your File Type, Archive Size, and Delivery Method.
5. Save the file somewhere on your machine.
6. Download this script, and place it in the same directory as the Google Takout file.
7. Edit the .py, and set your Google Takeout file name on line 9.
8. Run this .py script
9. A file will be saved in the same location; `place_visits.csv`.

![Schermafbeelding 2024-02-11 134629](https://github.com/jonkeren/Google-Takeout-Semantic-Location-History-parser-PY/assets/15706797/8182ce17-6a1e-45e0-a8da-05072e952e11)

# Needed
- Python 3.9+
- installed `pandas`, `zipfile`, `timezonefinder`, `json` and `datetime` (if not present; use `pip install`).

This is an adapted script from several other sources on the web. I have commented out the `placeId` item, as not all of my locations had a placeId in the array.

