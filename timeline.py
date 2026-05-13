import plotly.graph_objects as go

def render_timeline(scores, climax):
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=scores, mode='lines', line=dict(color='#FF10F0', width=3), name='Intensidad'))
    # Línea blanca en el clímax
    fig.add_vline(x=climax / 3, line_color='white', line_width=2)
    fig.update_layout(
        paper_bgcolor='#07080d', plot_bgcolor='#07080d', font_color='white',
        height=200, margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=False)
    )
    return fig