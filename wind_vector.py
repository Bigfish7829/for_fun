import streamlit as st
import numpy as np


def compass_vector_addition(vector1, vector2):
    angle1, magnitude1 = vector1
    angle2, magnitude2 = vector2

    # Convert compass bearing and magnitude to Cartesian coordinates (x, y)
    angle1_rad = np.radians(angle1)
    angle2_rad = np.radians(angle2)

    x1 = magnitude1 * np.cos(angle1_rad)
    y1 = magnitude1 * np.sin(angle1_rad)

    x2 = magnitude2 * np.cos(angle2_rad)
    y2 = magnitude2 * np.sin(angle2_rad)

    # Perform vector addition in Cartesian coordinates
    result_x = x1 + x2
    result_y = y1 + y2

    # Convert the result back to compass bearing and magnitude
    result_magnitude = round(np.sqrt(result_x ** 2 + result_y ** 2), 1)
    result_angle_rad = np.arctan2(result_y, result_x)
    result_angle_deg = np.degrees(result_angle_rad)

    result_angle_deg = round((result_angle_deg + 360) % 360, 0)
    wind_angle_deg = result_angle_deg - angle2
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
vector1_angle = st.number_input("Apparent Wind Direction - due to tide(degrees):", min_value=0, max_value=360, value=0)
vector1_magnitude = st.number_input("Apparent Wind Speed (knots):", min_value=0, value=10)
vector2_angle = st.number_input("Bearing to next mark (degrees):", min_value=0, max_value=360, value=0)
vector2_magnitude = st.number_input("Estimated Boat Speed SOG(knots):", min_value=0, value=5)

if st.button("Select my sail"):
    st.header("Results")
    vector1 = (vector1_angle, vector1_magnitude)
    vector2 = (vector2_angle, vector2_magnitude)

    result_angle, result_magnitude, wind_angle_deg, sail = compass_vector_addition(vector1, vector2)

    st.write(f"Resultant Wind from tide and boat speed: {result_angle} degrees, {result_magnitude} knots.")
    st.write(f" Wind angle to Course Over Ground: {wind_angle_deg} degrees.")
    st.write(f" Recommended sail: {sail}")
