# Import the dependencies.
from sqlalchemy import func
from sqlalchemy import create_engine, inspect
from flask import Flask, jsonifyimport sqlalchemy
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
    return  (
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/stations"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

prcp_query=session.query(Measurement.prcp).filter(Measurement.date.between('2016-08-23' , '2017-08-23')).all()


#################################################
# Flask Routes
@app.route("/precipitation")
def precipitation():
     """Return the precipitationas json"""

    return jsonify(prcp_query)
  
#################################################
