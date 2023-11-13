
import streamlit as st
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt, offsetbox
from PIL import Image


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

    wind_0_180 = abs(wind_angle_to_cog_deg)

    if wind_angle_to_cog_deg < 0:
        wind_angle_to_cog_deg += 360

    if wind_angle_to_cog_deg > 180:
        tack = 'Port'

    df_sail_data = pd.read_excel('sail_data.xlsx')
    df_sail_data = df_sail_data.set_index('AWS')

    rounded_resultant_wind_magnitude = round(resultant_wind_magnitude/5)*5
    rounded_wind_0_180 = round(wind_0_180/10)*10

    sail = df_sail_data.loc[rounded_resultant_wind_magnitude, rounded_wind_0_180]

    return resultant_wind_angle_deg, resultant_wind_magnitude, wind_angle_to_cog_deg, sail, tack, wind_0_180


st.title("Sail selection tool")
st.write("Enter the details of wind and course:")
apparent_wind_angle = st.number_input("True Wind Direction:", min_value=0, max_value=360, value=0)
apparent_wind_magnitude = st.number_input("True Wind Speed (knots):", min_value=0, value=10)
if apparent_wind_magnitude > 25 and apparent_wind_magnitude <= 29:
    st.warning("Wind speed is over 25 knots, are you sure you want to sail?")
if apparent_wind_magnitude > 29:
    st.warning("Wind speed is over 30 knots, you should not sail, I will not give you a sail recommendation.")

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

    result_angle, result_magnitude, wind_angle_deg, sail, tack, wind_0_180 = compass_vector_addition(apparent_wind, boat_velocity)

    #st.write(f"Resultant Wind from tide and boat speed: {result_angle} degrees, {result_magnitude} knots.")
    st.write(f" Course to next mark: {boat_velocity_angle} degrees.")
    st.write(f" Tack: {tack}")
    st.write(f" Wind angle (Bow is 0): {wind_0_180} degrees.")
    st.write(f" Apparent wind speed: {result_magnitude} knots.")
    st.markdown(f"<p style='font-size:18px'><b>Recommended sail:</b> {sail}</p>", unsafe_allow_html=True)


    #st.write(f" Wind angle to Course Over Ground: {wind_angle_deg} degrees.")

    image = Image.open('boat_2.png')
    image = image.rotate(-90)
    image.putalpha(128)


    # Plot resultant_wind_angle on a polar plot
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.set_theta_direction(-1)  # Set the direction of increasing angles to be clockwise
    ax.set_theta_offset(np.pi / 2.0)  # Set the zero angle to be at the top (North) of the plot

    # Convert the angle to radians for the polar plot
    result_angle_rad = np.radians(wind_angle_deg)

    # Plot an arrow at the calculated angle
    ax.annotate("", xy=(result_angle_rad, result_magnitude), xytext=(0, 0),
                arrowprops=dict(facecolor='red', edgecolor='red', arrowstyle='<-', linewidth=2))

    imagebox = offsetbox.AnnotationBbox(offsetbox.OffsetImage(image, zoom=0.1), (0.5, 0.5),
                                        frameon=False, pad=0.5)
    ax.add_artist(imagebox)

    # Set plot attributes
    ax.set_rlabel_position(0)  # Move radial labels away from plotted line
    ax.set_rmax(result_magnitude + 5)  # Set the maximum radial value
    ax.grid(True)

    # Display the polar plot in the Streamlit app
    st.pyplot(fig)


