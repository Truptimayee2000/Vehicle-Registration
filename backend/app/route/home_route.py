from flask import request, jsonify
from app import app
from dbconfig import db
from app.services.growth_service import query_monthly_data, calculate_growth
from app.models.vehicle import VehicleCategoryMonthly, ManufacturerMonthly


@app.route('/growth', methods=['GET'])
def get_growth():
    category = request.args.get('category')
    manufacturer = request.args.get('manufacturer')
    start_year = request.args.get('start_year', type=int)
    end_year = request.args.get('end_year', type=int)

    year_range = (start_year, end_year) if start_year and end_year else None

    if category:
        df = query_monthly_data(VehicleCategoryMonthly, category_filter=category, year_range=year_range)
    elif manufacturer:
        df = query_monthly_data(ManufacturerMonthly, manufacturer_filter=manufacturer, year_range=year_range)
    else:
        df = query_monthly_data(VehicleCategoryMonthly, year_range=year_range)

    monthly_data, quarterly_data = calculate_growth(df)

    return jsonify({
        "monthly": monthly_data,
        "quarterly": quarterly_data
    })


@app.route('/growth/filters', methods=['GET'])
def get_growth_filters():
    try:
        categories = db.session.query(VehicleCategoryMonthly.vehicle_category) \
            .distinct().order_by(VehicleCategoryMonthly.vehicle_category).all()
        categories = [c[0] for c in categories if c[0]]

        manufacturers = db.session.query(ManufacturerMonthly.manufacturer) \
            .distinct().order_by(ManufacturerMonthly.manufacturer).all()
        manufacturers = [m[0] for m in manufacturers if m[0]]

        return jsonify({
            "categories": categories,
            "manufacturers": manufacturers
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
