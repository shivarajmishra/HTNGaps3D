import pandas as pd
import plotly.graph_objects as go
import imageio.v2 as imageio
import os

# Load data
df = pd.read_csv("data_for_map.csv")

# Aggregate
df_avg = df.groupby(['Country_x', 'Country Code'], as_index=False).agg({
    'htn': 'mean',
    'phy': 'mean',
    'nurse': 'mean',
    'pharma': 'mean',
    'chws': 'mean',
    'hw': 'mean'
})
df_avg.columns = ['Country', 'Country Code', 'HTN', 'Physicians', 'Nurses', 'Pharmacists', 'CHWs', 'Total HW']

# Style config
style = {
    'HTN': {'colorscale': 'Reds', 'zmin': 0, 'zmax': 60, 'title': 'HTN Prevalence (%)'}
}

# Create GIF frames folder
gif_folder = "frames"
os.makedirs(gif_folder, exist_ok=True)

# Generate 3D globe images
image_paths = []
for i, lon in enumerate(range(0, 360, 5)):  # 15° steps = 24 frames
    fig = go.Figure(
        data=go.Choropleth(
            locations=df_avg['Country Code'],
            z=df_avg['HTN'],
            text=df_avg['Country'],
            colorscale=style['HTN']['colorscale'],
            zmin=style['HTN']['zmin'],
            zmax=style['HTN']['zmax'],
            marker_line_color='black',
            colorbar_title=style['HTN']['title']
        ),
        layout=go.Layout(
            title=dict(
                text='<i>“Where hypertension rises,<br>let health systems rise too.”</i>',
                x=0.05,
                xanchor='left',
                font=dict(family='Georgia, Times New Roman', size=18)
            ),
            geo=dict(
                projection_type='orthographic',
                projection_rotation=dict(lon=lon),
                showland=True,
                landcolor='rgb(100, 243, 243)',
                showcountries=True,
                countrycolor='rgb(100, 100, 100)',
                showocean=True,
                oceancolor='rgb(100, 224, 255)'
            ),
            annotations=[
                dict(
                    text="Note: Workforce indicators per 10,000 population. HTN in %",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.01, y=0.02,
                    font=dict(size=10, color="white"),
                    bgcolor="red",
                    bordercolor="black",
                    borderwidth=0.5
                )
            ]
        )
    )

    image_path = f"{gif_folder}/frame_{i:03d}.png"
    fig.write_image(image_path, engine="kaleido", width=800, height=600)
    image_paths.append(image_path)

# Create GIF
with imageio.get_writer("rotating_htn_globe.gif", mode='I', duration=0.15) as writer:
    for path in image_paths:
        image = imageio.imread(path)
        writer.append_data(image)

print("✅ Saved rotating_htn_globe.gif")

# Optional: clean up frame images
# for path in image_paths:
#     os.remove(path)
