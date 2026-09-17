"""Live local integration view for workflow Steps 1–13."""
import streamlit as st
import pandas as pd
import plotly.express as px
from dashboard.data.pipeline import artifact_status, engine_forecast, engine_health, fused_data, metrics, read_artifact

st.set_page_config(page_title='Pipeline Control', page_icon='⚙️', layout='wide')
st.title('⚙️ Pipeline Control Center')
st.caption('Local connection to the tropical-cyclone pipeline. No cloud service is required.')

status = artifact_status(); health = engine_health()
cols = st.columns(4)
for column, (name, available) in zip(cols, status.items()):
    column.metric(name.title(), 'Ready' if available else 'Not generated')
st.subheader('Step 13 prediction engine')
st.write('Status:', health['status'])
st.json(health.get('models', {}))

fused = fused_data()
if fused.empty:
    st.error('Fused dataset not found. Complete Step 5 first.')
    st.stop()

storm_ids = sorted(fused['SID'].dropna().astype(str).unique())
storm_id = st.selectbox('Cyclone / storm ID', storm_ids)
storm = fused[fused['SID'].astype(str) == storm_id].sort_values('TIME').dropna(subset=['LAT_IBTRACS','LON_IBTRACS','USA_WIND','USA_PRES'])
st.dataframe(storm.tail(8), use_container_width=True, hide_index=True)

if len(storm) >= 4:
    latest = storm.iloc[-1]; st.subheader('Latest fused observation')
    a,b,c,d = st.columns(4)
    a.metric('Latitude', f"{latest.LAT_IBTRACS:.2f}°")
    b.metric('Longitude', f"{latest.LON_IBTRACS:.2f}°")
    c.metric('Wind', f"{latest.USA_WIND:.0f} kt")
    d.metric('Pressure', f"{latest.USA_PRES:.0f} hPa")
    if st.button('Run local forecast', type='primary'):
        history = storm[['LAT_IBTRACS','LON_IBTRACS','USA_WIND','USA_PRES']].tail(4).astype(float).values.tolist()
        result = engine_forecast(storm_id, history)
        if 'error' in result: st.error(f"Prediction engine unavailable: {result['error']}")
        else:
            st.success('Forecast generated'); st.json(result)
            for alert in result.get('alerts', []):
                (st.error if alert['level'] == 'critical' else st.warning)(alert['message'])
else: st.warning('This storm has fewer than four complete observations.')

st.subheader('Generated artifacts')
for key in ('detections','categories','intensity','track','temporal'):
    frame = read_artifact(key)
    with st.expander(f'{key.title()} ({len(frame)} rows)'):
        if frame.empty: st.info('Run the corresponding pipeline stage to create this artifact.')
        else: st.dataframe(frame.tail(25), use_container_width=True, hide_index=True)

report = metrics()
if report:
    st.subheader('Latest model evaluation'); st.json(report)
track = read_artifact('track')
if not track.empty and {'actual_LAT_IBTRACS','actual_LON_IBTRACS','predicted_LAT_IBTRACS','predicted_LON_IBTRACS'}.issubset(track):
    plot = pd.concat([track[['actual_LAT_IBTRACS','actual_LON_IBTRACS']].rename(columns={'actual_LAT_IBTRACS':'latitude','actual_LON_IBTRACS':'longitude'}).assign(series='Actual'), track[['predicted_LAT_IBTRACS','predicted_LON_IBTRACS']].rename(columns={'predicted_LAT_IBTRACS':'latitude','predicted_LON_IBTRACS':'longitude'}).assign(series='Predicted')])
    st.plotly_chart(px.line(plot, x='longitude', y='latitude', color='series', title='Track model: actual vs predicted'), use_container_width=True)
