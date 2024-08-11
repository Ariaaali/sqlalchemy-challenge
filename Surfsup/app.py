# Import the dependencies.
from sqlalchemy import func
import numpy as np
import datetime as dt
from sqlalchemy import create_engine, inspect
from flask import Flask, jsonify 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import Column, Integer, String, Float

#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement=Base.classes.measurement
Station=Base.classes.station

# Create a session
session=Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
@app.route("/")
def home():
    """List all available api routes."""
    return  (
        f"//api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/<start> <br/>"
        f"/api/v1.0/<start>/<end>"
    )

#################################################
# Flask Routes
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation"""
    prcp_query=session.query(Measurement.date,Measurement.prcp).filter(Measurement.date.between('2016-08-23' , '2017-08-23')).all()
    session.close()
    precipitation = []

    for date, prcp in prcp_query:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["precipitation"] = prcp
        
        precipitation.append(precipitation_dict)
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def station():
    """Return the list of station"""
    station_query=session.query(Measurement.station).group_by(Measurement.station).all()
    session.close()
    station_names = list(np.ravel(station_query))
    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def tobs():
    """return the dates and temperature observations of the most-active station for the previous year of data"""
    active_station=session.query(Measurement.date,Measurement.tobs, func.count(Measurement.station)).\
    filter(Measurement.date.between('2016-08-23' , '2017-08-23')).\
    group_by(Measurement.station).order_by(Measurement.station.desc()).first()
    session.close()
    active_station_name = list(np.ravel(active_station))
    return jsonify(active_station_name)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def date(start= None, end=None):
    selection= [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    if not end:
        start = dt.datetime.strptime(start, "%m%d%Y")
        results = session.query(*selection).filter(Measurement.date >= start).all()
        session.close()
        temps = list(np.ravel(results))
        return jsonify(temps)

    
    start = dt.datetime.strptime(start, "%m%d%Y")
    end = dt.datetime.strptime(start, "%m%d%Y")

    results = session.query(*selection).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    temps = list(np.ravel(results))
    return jsonify(temps)
    
    

    
#################################################
if __name__ == '__main__':
    app.run(debug=True)



