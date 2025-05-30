import pandas as pd
import plotly.graph_objects as go

# Load data
df = pd.read_csv("data_for_map.csv")

# Aggregate data
df_avg = df.groupby(['Country_x', 'Country Code'], as_index=False).agg({
    'htn': 'mean',
    'phy': 'mean',
    'nurse': 'mean',
    'pharma': 'mean',
    'chws': 'mean',
    'hw': 'mean'
})
df_avg.columns = ['Country', 'Country Code', 'HTN', 'Physicians', 'Nurses', 'Pharmacists', 'CHWs', 'Total HW']

# Define custom styles for each variable
style_config = {
    'HTN':         {'colorscale': 'Reds', 'zmin': 0,  'zmax': 60,  'title': 'HTN Prevalence (%)'},
    'Physicians':  {'colorscale': 'Blues', 'zmin': 0, 'zmax': 50,  'title': 'Physicians (/10K)'},
    'Nurses':      {'colorscale': 'Greens', 'zmin': 0, 'zmax': 100, 'title': 'Nurses (/10K)'},
    'Pharmacists': {'colorscale': 'Purples', 'zmin': 0, 'zmax': 30,  'title': 'Pharmacists (/10K)'},
    'CHWs':        {'colorscale': 'Oranges', 'zmin': 0, 'zmax': 50,  'title': 'CHWs (/10K)'},
}

# Create rotation frames
frames = [go.Frame(layout=dict(geo=dict(projection_rotation=dict(lon=lon)))) for lon in range(0, 360, 2)]

# Initial variable
initial_var = 'HTN'

# Build figure with frames passed to go.Figure
fig = go.Figure(
    data=[go.Choropleth(
        locations=df_avg['Country Code'],
        z=df_avg[initial_var],
        text=df_avg['Country'],
        colorscale='Reds',
        zmin=0,
        zmax=60,
        colorbar_title=f'{initial_var} (%)',
        marker_line_color='black'
    )],
    frames=frames,
    layout=go.Layout(
        title=dict(
            text='<i>“Where the burden of hypertension rises,<br>'
                'the strength of the health system must follow.<br> Lets pitch a story using 3D maps”</i>',
            x=0.05,
            xanchor='left',
            font=dict(
                family='Georgia, Times New Roman, Serif',
                size=22,
                color='black'
            )
        ),
        geo=dict(
            projection_type='orthographic',
            showland=True,
            landcolor='rgb(100, 243, 243)',
            showcountries=True,
            countrycolor='rgb(100, 100, 100)',
            showocean=True,
            oceancolor='rgb(100, 224, 255)',
            projection_rotation=dict(lon=0)
        ),
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                x=0.5,
                y=1.1,
                xanchor="center",
                yanchor="bottom",
                showactive=False,
                bgcolor='red',
                bordercolor='black',
                font=dict(color='white'),
                buttons=[dict(
                    label="▶ Play",
                    method="animate",
                    args=[None, {
                        "frame": {"duration": 50, "redraw": True},
                        "fromcurrent": True,
                        "mode": "immediate"
                    }]
                )]
            ),
            dict(
                buttons=[
                    dict(
                        label=col,
                        method='update',
                            args=[
                                {'z': [df_avg[col]], 'colorbar.title': f'{col} (%)'},
                                {'title': {
                                    'text': f'<i>{col} Distribution <br> and Shortfalls</i>',
                                    'x': 0.0,
                                    'y':0.6,
                                    'xanchor': 'left',
                                    'font': {
                                        'family': 'Arial',
                                        'size': 48,
                                        'color': 'Green'
                                    }
                                }}
                            ]
                    )
                    for col in ['HTN', 'Physicians', 'Nurses', 'Pharmacists', 'CHWs']
                ],
                direction="down",
                showactive=True,
                x=0.5,
                xanchor="center",
                y=1.2,
                yanchor="bottom"
            )
        ],
        annotations=[
            dict(
                text="Note: Workforce indicators per 10,000 population. HTN prevalence shown in %",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.01, y=0.02,
                xanchor="left", yanchor="bottom",
                font=dict(size=10, color="white"),
                bgcolor="red",
                bordercolor="black",
                borderwidth=0.5
            )
        ],
    )
)

# Save as HTML for deployment
fig.write_html("rotating_globe_map.html", full_html=True, include_plotlyjs='cdn')
print("✅ Saved: rotating_globe_map.html")
