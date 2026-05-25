import pandas as pd
import matplotlib as plt
import streamlit as st

data = pd.read_csv("/Users/Jon/USRA2026/data/packet_data.csv")

fig, axs = plt.subplots(2, 2)

attributes = ["rssi", "snr", "latency", "hopsUsed"]
attribute = 0

for x in range(2):
    for y in range(2):
        axs[x, y].plot(data[attributes[attribute]])
        axs[x, y].set_title(attributes[attribute])
        attribute += 1

st.pyplot(fig)




