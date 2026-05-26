import time
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

data = pd.read_csv("/Users/Jon/USRA2026/data/desk.csv")

fig, axs = plt.subplots(3, 2)

attributes = ["rssi", "snr", "latency", "hopsUsed", "deliveryRate"]
attribute = 0

for x in range(3):
    for y in range(2):
        axs[x, y].plot(data[attributes[attribute]])
        axs[x, y].set_title(attributes[attribute])
        if attribute < 6:
            attribute += 1

st.pyplot(fig)

time.sleep(5)
st.rerun()




