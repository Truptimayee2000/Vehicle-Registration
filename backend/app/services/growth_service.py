import pandas as pd
from dbconfig import db
from app.models.vehicle import VehicleCategoryMonthly, ManufacturerMonthly

def query_monthly_data(model, category_filter=None, manufacturer_filter=None, year_range=None):
    query = db.session.query(model)

    if category_filter:
        query = query.filter(model.vehicle_category == category_filter)
    if manufacturer_filter:
        query = query.filter(model.manufacturer == manufacturer_filter)
    if year_range:
        start, end = year_range
        query = query.filter(model.year >= start, model.year <= end)

    rows = query.all()

    data = []
    for r in rows:
        data.append({
            "category": getattr(r, "vehicle_category", None),
            "manufacturer": getattr(r, "manufacturer", None),
            "year": r.year,
            "jan": r.jan,
            "feb": r.feb,
            "mar": r.mar,
            "apr": r.apr,
            "may": r.may,
            "jun": r.jun,
            "jul": r.jul,
            "aug": r.aug,
            "sep": r.sep,
            "oct": r.oct,
            "nov": r.nov,
            "dec": r.dec,
            "total": r.total,
        })
    return pd.DataFrame(data)


def calculate_growth(df):
    if df.empty:
        return [], []

    months = ["jan", "feb", "mar", "apr", "may", "jun",
              "jul", "aug", "sep", "oct", "nov", "dec"]

    df_melt = df.melt(
        id_vars=["year", "category", "manufacturer"],
        value_vars=months,
        var_name="month",
        value_name="count"
    )

    df_melt['date'] = pd.to_datetime(
        df_melt['year'].astype(str) + "-" + df_melt['month'], format="%Y-%b"
    )

    group_col = "category" if "category" in df.columns else "manufacturer"
    df_melt = df_melt.sort_values(["year", "date"])

    df_melt['mom_growth_%'] = df_melt.groupby(group_col)['count'].pct_change() * 100

    df_melt['yoy_growth_%'] = df_melt.groupby(group_col)['count'].pct_change(12) * 100

    quarter_map = {
        "jan": "Q1", "feb": "Q1", "mar": "Q1",
        "apr": "Q2", "may": "Q2", "jun": "Q2",
        "jul": "Q3", "aug": "Q3", "sep": "Q3",
        "oct": "Q4", "nov": "Q4", "dec": "Q4"
    }
    df_melt["quarter"] = df_melt["month"].map(quarter_map)

    q_df = df_melt.groupby([group_col, "year", "quarter"])["count"].sum().reset_index()

    q_df["qoq_growth_%"] = q_df.groupby([group_col])["count"].pct_change() * 100

    q_df["yoy_growth_%"] = q_df.groupby([group_col])["count"].pct_change(4) * 100

    return df_melt.to_dict(orient="records"), q_df.to_dict(orient="records")
