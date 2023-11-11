
import streamlit as st
import numpy as np
import pandas as pd


def compass_vector_addition(apparent_wind, boat_velocity):
    wind_angle, wind_speed = apparent_wind
    course_bearing, boat_speed = boat_velocity

    # Convert compass bearing and magnitude to Cartesian coordinates (x, y)
    wind_angle_rad = np.radians(wind_angle)
    course_bearing_rad = np.radians(course_bearing)

    x1 = wind_speed * np.cos(wind_angle_rad)
    y1 = wind_speed * np.sin(wind_angle_rad)

    x2 = boat_speed * np.cos(course_bearing_rad)
    y2 = boat_speed * np.sin(course_bearing_rad)

    # Perform vector addition in Cartesian coordinates
    result_x = x1 + x2
    result_y = y1 + y2

    # Convert the result back to compass bearing and magnitude
    resultant_wind_magnitude = round(np.sqrt(result_x ** 2 + result_y ** 2), 1)
    resultant_wind_angle_rad = np.arctan2(result_y, result_x)
    resultant_wind_angle_deg = np.degrees(resultant_wind_angle_rad)

    resultant_wind_angle_deg = round((resultant_wind_angle_deg + 360) % 360, 0)
    wind_angle_to_cog_deg = resultant_wind_angle_deg - course_bearing
    tack = 'Starboard'
    if wind_angle_to_cog_deg < 0:
        wind_angle_to_cog_deg += 360

    if wind_angle_to_cog_deg > 180:
        tack = 'Port'


    if wind_angle_to_cog_deg >= 100 and wind_angle_to_cog_deg <= 260:
        sail = 'Spinnaker'
    else:
        sail = 'Jib'

    if resultant_wind_magnitude == 0:
        sail = 'Stop trying to break my code'

    return resultant_wind_angle_deg, resultant_wind_magnitude, wind_angle_to_cog_deg, sail, tack


st.title("Sail selection tool")
st.write("Enter the details of wind and course:")
apparent_wind_angle = st.number_input("True Wind Direction:", min_value=0, max_value=360, value=0)
apparent_wind_magnitude = st.number_input("True Wind Speed (knots):", min_value=0, value=10)

boat_velocity_magnitude = st.number_input("Estimated Boat Speed SOG(knots):", min_value=0, value=5)
df_buoys = pd.read_excel('buoys_headings.xlsx')
buoys = df_buoys['Buoys']

starting_buoy = st.selectbox("Starting Buoy", buoys)
destination_buoy = st.selectbox("Destination Buoy", buoys)
boat_velocity_angle = df_buoys.loc[df_buoys['Buoys'] == starting_buoy, destination_buoy].values[0]

override = st.checkbox("Override course")
if override:
    boat_velocity_angle = st.number_input("Bearing to next mark (degrees):", min_value=0, max_value=360, value=0)

if st.button("Select my sail"):
    st.header("Results")
    apparent_wind = (apparent_wind_angle, apparent_wind_magnitude)
    boat_velocity = (boat_velocity_angle, boat_velocity_magnitude)

    result_angle, result_magnitude, wind_angle_deg, sail, tack = compass_vector_addition(apparent_wind, boat_velocity)

    #st.write(f"Resultant Wind from tide and boat speed: {result_angle} degrees, {result_magnitude} knots.")
    st.write(f" Course to next mark: {boat_velocity_angle} degrees.")
    st.write(f" Wind angle to Course Over Ground: {wind_angle_deg} degrees.")
    st.write(f" Tack: {tack}")
    st.write(f" Apparent wind speed: {result_magnitude} knots.")
    st.write(f" Recommended sail: {sail}")
