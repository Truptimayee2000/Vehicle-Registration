import streamlit as st
import requests
import pandas as pd
import altair as alt

API_URL = "http://localhost:5000/growth"


st.set_page_config(
    page_title="📊 Vehicle Growth Dashboard",
    layout="wide"
)

st.markdown("""
   <style>
  /* Hide Streamlit header & menu */
  header { visibility: hidden; }
  button[title="Open main menu"] { display: none; }

  /* Page title style */
  .big-font {
    font-size: 20px !important;
    font-weight: bold;
    color: #0f4c81;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin-bottom: 20px;
  }

  /* KPI Card container */
  .kpi-card {
    background-color: #fff9f0;
    border-radius: 12px;
    padding: 5px 5px;
    text-align: center;
    box-shadow: 0 6px 18px rgba(15, 76, 129, 0.1);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    cursor: default;
    user-select: none;
  }
  .kpi-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 24px rgba(15, 76, 129, 0.2);
  }

  /* KPI label */
  .metric-label {
    font-size: 14px;
    font-weight: 600;
    color: #567d9a;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 6px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }

  /* KPI main value */
  .metric-value {
    font-size: 20px;
    font-weight: 800;
    color: #0f4c81;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin-bottom: 6px;
  }

  /* KPI percentage change with subtle pill */
  .metric-change {
    font-size: 13px;
    font-weight: 600;
    padding: 5px 12px;
    border-radius: 9999px;
    display: inline-block;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }
  .metric-change.positive {
    background-color: #daf6e3;
    color: #2a7a34;
  }
  .metric-change.negative {
    background-color: #fbdada;
    color: #a42424;
  }
</style>


""", unsafe_allow_html=True)

st.title("🚗📈 Vehicle Growth Dashboard")

@st.cache_data
def fetch_filter_options():
    try:
        resp = requests.get(API_URL + "/filters")
        if resp.status_code == 200:
            return resp.json()
    except:
        pass
    return {"categories": [], "manufacturers": []}

filters = fetch_filter_options()

with st.sidebar:
    st.header("🔍 Filters")
    category = st.selectbox(
        "Vehicle Category", 
        ["All"] + filters.get("categories", [])
    )
    manufacturer = st.selectbox(
        "Manufacturer", 
        ["All"] + filters.get("manufacturers", [])
    )
    start_year, end_year = st.slider("Select Year Range", 2000, 2030, (2018, 2025))

params = {
    "start_year": start_year,
    "end_year": end_year
}
if category != "All":
    params["category"] = category
if manufacturer != "All":
    params["manufacturer"] = manufacturer

try:
    response = requests.get(API_URL, params=params)
    data = response.json()
except Exception as e:
    st.error(f" API request failed: {e}")
    st.stop()

if data and "monthly" in data:
    df_monthly = pd.DataFrame(data['monthly'])
    df_quarterly = pd.DataFrame(data['quarterly'])

    if not df_monthly.empty:
        latest = df_monthly.iloc[-1]

  
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="kpi-card" style="padding-top: 10px"><div class="metric-label">Latest Monthly Count</div>'
                        f'<div class="metric-value">{latest["count"]:,}</div>'
                        f'<div>{latest.get("mom_growth_%", 0):.2f}% MoM</div></div>', unsafe_allow_html=True)
        with col2:
                yoy_growth = latest.get("yoy_growth_%", 0)
                arrow = "▲" if yoy_growth >= 0 else "▼"
                arrow_color = "#0b6b34" if yoy_growth >= 0 else "#9b1c1c"

                st.markdown(f"""
                    <div class="kpi-card" style="padding: 20px">
                        <div class="metric-label">YoY Growth</div>
                        <div class="metric-value">
                            <span style="color:{arrow_color}; font-weight:bold;">{arrow}</span>
                            {yoy_growth:.2f}%
                        </div>
                    </div>
                """, unsafe_allow_html=True)

        with col3:
            st.markdown('<div class="kpi-card" style="padding-top: 5px"><div class="metric-label">Filters</div>'
                        f'<div class="metric-value">{category if category != "All" else "All Categories"}, '
                        f'{manufacturer if manufacturer != "All" else "All Manufacturers"}</div></div>', unsafe_allow_html=True)

        st.markdown("---")

        df_monthly['date'] = pd.to_datetime(df_monthly['date'])
        with st.expander("📅 Monthly Trends", expanded=True):
            base = alt.Chart(df_monthly).encode(x='date:T')

            bar_count = base.mark_bar(color='#3498db').encode(
                y=alt.Y('count:Q', axis=alt.Axis(title='Count')),
                tooltip=['date:T', 'count:Q']
            )
            line_mom = base.mark_line(color='#e67e22').encode(
                y=alt.Y('mom_growth_%:Q', axis=alt.Axis(title='% Change'), scale=alt.Scale(zero=False)),
                tooltip=['date:T', 'mom_growth_%:Q']
            )
            line_yoy = base.mark_line(color='#27ae60').encode(
                y='yoy_growth_%:Q',
                tooltip=['date:T', 'yoy_growth_%:Q']
            )

            chart = alt.layer(bar_count, line_mom, line_yoy).resolve_scale(y='independent').interactive()
            st.altair_chart(chart, use_container_width=True)

        if not df_quarterly.empty:
            df_quarterly['quarter_label'] = df_quarterly['year'].astype(str) + ' Q' + df_quarterly['quarter'].astype(str)
            with st.expander("📆 Quarterly Trends", expanded=False):
                base_q = alt.Chart(df_quarterly).encode(x='quarter_label:N')

                bar_count_q = base_q.mark_bar(color='#5dade2').encode(
                    y=alt.Y('count:Q', axis=alt.Axis(title='Count')),
                    tooltip=['quarter_label', 'count:Q']
                )
                line_qoq = base_q.mark_line(color='#f39c12').encode(
                    y=alt.Y('qoq_growth_%:Q', axis=alt.Axis(title='% Change'), scale=alt.Scale(zero=False)),
                    tooltip=['quarter_label', 'qoq_growth_%:Q']
                )
                line_yoy_q = base_q.mark_line(color='#2ecc71').encode(
                    y='yoy_growth_%:Q',
                    tooltip=['quarter_label', 'yoy_growth_%:Q']
                )

                chart_q = alt.layer(bar_count_q, line_qoq, line_yoy_q).resolve_scale(y='independent').interactive()
                st.altair_chart(chart_q, use_container_width=True)

else:
    st.warning(" No data available for the selected filters.")
