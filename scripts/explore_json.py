#!/usr/bin/env python3

import json
import pandas as pd
import matplotlib.pyplot as plt

with open("easy_final_v1-0/easy_final/0036abdf.json") as f:
    data = json.load(f)

# Detection measurements
df = pd.DataFrame(
    data["detections"],
    columns=["toa", "pulse_width", "bandwidth", "frequency"]
)

# labels
labels_df = pd.DataFrame(data["labels"])

# Each detection corresponds to the label at the same position
df = pd.concat([df, labels_df], axis=1)

# Sort pulses by source and arrival time
df = df.sort_values(["source_uuid", "toa"])

# Calculate DTOA within each individual source
df["dtoa"] = (df.groupby("source_uuid")["toa"].diff())

#print(df.groupby("source_uuid")[["toa", "pulse_width", "frequency", "dtoa"]].describe())

# How many distinct values?
#print("\nUnique frequencies:", df["frequency"].nunique())
#print("Unique pulse widths:", df["pulse_width"].nunique())
#print("Unique bandwidths:", df["bandwidth"].nunique())

#print("\nFrequency counts:")
#print(df["frequency"].value_counts().sort_index())

#print("\nPulse-width counts:")
#print(df["pulse_width"].value_counts().sort_index())

fig, ax = plt.subplots(figsize=(12, 6))

for source, group in df.groupby("source_uuid"):

    group = group[group["toa"] <= 0.020]

    ax.scatter(
        group["toa"].to_numpy() * 1000,
        group["pulse_width"].to_numpy() * 1e6,
        s=20,
        label=source[:8]
    )

ax.set_xlabel("Time of Arrival (s)")
ax.set_ylabel("Pulse Width (µs)")
ax.set_title("Radar Pulse Width Pattern — First 20 ms")
ax.legend(title="Source")

fig.savefig("pulsewidth_first_20ms.png", dpi=150, bbox_inches="tight")

plt.close(fig)

print("Saved: pulsewidth_first_20ms.png")
