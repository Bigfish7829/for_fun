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
    wind_angle_deg = angle2 - result_angle_deg

    return result_angle_deg, result_magnitude, wind_angle_deg


st.write("Enter the details of two vectors:")
vector1_angle = st.number_input("True Wind Direction (degrees):", min_value=0, max_value=360, value=0)
vector1_magnitude = st.number_input("True Wind Speed (knots):", min_value=0, value=1)
vector2_angle = st.number_input("Bearing to Mark (degrees):", min_value=0, max_value=360, value=0)
vector2_magnitude = st.number_input("Boat Speed (knots):", min_value=0, value=1)

if st.button("Add Vectors"):
    vector1 = (vector1_angle, vector1_magnitude)
    vector2 = (vector2_angle, vector2_magnitude)

    result_angle, result_magnitude, wind_angle_deg = compass_vector_addition(vector1, vector2)

    st.write(f"Resultant Vector: {result_angle} degrees, {result_magnitude} knots."
             f" Wind angle to boat: {wind_angle_deg} degrees.")
