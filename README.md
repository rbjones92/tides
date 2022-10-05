# Summary
The best time to ride a fat-tire ebike on the beach is low tide. If I want to ride my ebike to work, it means I have to leave my house around 7am. I will write a program
to find and filter the best days to ride my bike to work. 

![Alt Text](images/bike.jpg?raw=true "ebike on beach")

![Alt Text](images/tides.JPG?raw=true "tide chart")


# Methods
I will use tide data from the National Oceanic and Atmospheric Administration to find the best times to ride my ebike to work on the beach. 

# Technology
Python 3.7 <br>
Pyspark <br>
Google API <br>

# Program Run

1. Run tides.py to scrape NOAA webpages and grab all tide data between chosen dates.

![Alt Text](images/tides_data.JPG?raw=true "tide data")

2. Transform tide_df.csv with transform_tides_df.py to filter for your chosen conditions. Mine are...<br>
...1. Monday thru Friday <br>
...2. Low Tide <br>
...3. Between 7am and 9am <br>

![Alt Text](images/tides_transformed.JPG?raw=true "tide data")

3. Add elements to Google Calendar with gcal_api_conn.py

![Alt Text](images/tide_calendar.JPG?raw=true "calendar")
