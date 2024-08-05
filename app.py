# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


#################################################
# Database Setup
#################################################
app = Flask(__name__)
engine = create_engine("sqlite:///C:/Users/Nick/Downloads/Starter_Code (8)/Starter_Code/Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
# Import the sessionmaker class
from sqlalchemy.orm import sessionmaker

# Create a session maker and bind it to the engine
Session = sessionmaker(bind=engine)

# Create a session to link Python to the database
session = Session()

#################################################
# Flask Setup
#################################################

#################################################
# Flask Routes
#################################################
@app.route('/')
def home():
    return (
        f"Welcome to the Climate App API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    # Add your logic here to retrieve and format precipitation data
    return jsonify({"key": "value"})  # Return the JSON representation of the data

@app.route('/api/v1.0/stations')
def stations():
    # Add your logic here to retrieve stations data
    return jsonify({"stations": ["station1", "station2"]})  # Return the JSON list of stations

@app.route('/api/v1.0/tobs')
def tobs():
    # Calculate the date one year ago from the last date in the database
    prev_year_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query the most active station for the previous year of data
    most_active_station = session.query(Measurement.station, func.count(Measurement.tobs)).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.tobs).desc()).first()[0]

    most_active_station_tobs = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= prev_year_date).all()

    # Create a list of dictionaries with date and temperature observations
    tobs_data = []
    for date, tobs in most_active_station_tobs:
        tobs_data.append({"date": date, "tobs": tobs})

    return jsonify(tobs_data)

@app.route('/api/v1.0/<start>')
def temp_start(start):
    # Query the temperature data for dates greater than or equal to the start date
    temp_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    # Create a dictionary with temperature statistics
    temp_stats = {
        "TMIN": temp_data[0][0],
        "TAVG": temp_data[0][1],
        "TMAX": temp_data[0][2]
    }

    return jsonify(temp_stats)

@app.route('/api/v1.0/<start>/<end>')
def temp_start_end(start, end):
    # Query the temperature data for the date range from start to end (inclusive)
    temp_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Create a dictionary with temperature statistics
    temp_stats = {
        "TMIN": temp_data[0][0],
        "TAVG": temp_data[0][1],
        "TMAX": temp_data[0][2]
    }

    return jsonify(temp_stats)
