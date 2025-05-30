import pandas as pd
import plotly.graph_objects as go

# Load data
df = pd.read_csv("data_for_map.csv")
df_avg = df.groupby(['Country_x', 'Country Code'], as_index=False)['htn'].mean()

# Create frames for rotation
frames = []
for lon in range(0, 360, 2):  # Rotate in 10-degree steps
    frame = go.Frame(
        layout=dict(
            geo=dict(projection_rotation=dict(lon=lon))
        )
    )
    frames.append(frame)

# Build base figure
fig = go.Figure(
    data=go.Choropleth(
        locations=df_avg['Country Code'],
        z=df_avg['htn'],
        text=df_avg['Country_x'],
        colorscale='Reds',
        colorbar_title='HTN Prevalence (%)',
    ),
    layout=go.Layout(
        title_text='Rotating Globe: Hypertension Prevalence',
        geo=dict(
            projection_type='orthographic',
            showland=True,
            landcolor='rgb(243, 243, 243)',
            showcountries=True,
            countrycolor='rgb(204, 204, 204)',
            showocean=True,
            oceancolor='rgb(204, 224, 255)',
            projection_rotation=dict(lon=0)
        ),
        updatemenus=[dict(
            type="buttons",
            direction="right",
            x=0.5,         # Center horizontally
            y=1.1,         # Place above the plot
            xanchor="center",
            yanchor="bottom",
            showactive=False,
            bgcolor='red',              # Button background color
            bordercolor='black',
            font=dict(color='white'),   # Button font color
            buttons=[dict(
                label="▶ Play",
                method="animate",
                args=[None, {
                    "frame": {"duration": 100, "redraw": True},
                    "fromcurrent": True,
                    "mode": "immediate"}
                ]      
            )]
        )]
    ),
    frames=frames
)

fig.show()
