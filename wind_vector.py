import streamlit as st
import numpy as np


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
    result_magnitude = round(np.sqrt(result_x ** 2 + result_y ** 2), 1)
    result_angle_rad = np.arctan2(result_y, result_x)
    result_angle_deg = np.degrees(result_angle_rad)

    result_angle_deg = round((result_angle_deg + 360) % 360, 0)
    wind_angle_deg = result_angle_deg - course_bearing
    if wind_angle_deg < 0:
        wind_angle_deg += 360

    if wind_angle_deg >= 100 and wind_angle_deg <= 260:
        sail = 'Spinnaker'
    else:
        sail = 'Jib'

    if result_magnitude == 0:
        sail = 'Stop trying to break my code'

    return result_angle_deg, result_magnitude, wind_angle_deg, sail


st.title("Sail selection tool")
st.write("Enter the details of wind and course:")
apparent_wind_angle = st.number_input("Apparent Wind Direction - due to tide(degrees):", min_value=0, max_value=360, value=0)
apparent_wind_magnitude = st.number_input("Apparent Wind Speed (knots):", min_value=0, value=10)
boat_velocity_angle = st.number_input("Bearing to next mark (degrees):", min_value=0, max_value=360, value=0)
boat_velocity_magnitude = st.number_input("Estimated Boat Speed SOG(knots):", min_value=0, value=5)

if st.button("Select my sail"):
    st.header("Results")
    apparent_wind = (apparent_wind_angle, apparent_wind_magnitude)
    boat_velocity = (boat_velocity_angle, boat_velocity_magnitude)

    result_angle, result_magnitude, wind_angle_deg, sail = compass_vector_addition(apparent_wind, boat_velocity)

    st.write(f"Resultant Wind from tide and boat speed: {result_angle} degrees, {result_magnitude} knots.")
    st.write(f" Wind angle to Course Over Ground: {wind_angle_deg} degrees.")
    st.write(f" Recommended sail: {sail}")
