# Import the dependencies.
#%matplotlib inline

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import pandas as pd
import datetime as dt
# Python SQL toolkit and Object Relational Mapper

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine,reflect = True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# 2. Create an app, being sure to pass __name__
@app.route("/")
def Wlecome():

# 3. Define what to do when a user hits the index route
#Start at the homepage.

     '''List all available api route'''
     return (
        f"Welcome to Hawii Weather Api!<br/>"
        f"precipitation data for 12 months <br/>"
        f"/api/v1.0/precipitation <br/>"
        f" Activation Weather Station: <br/>"
        f"/api/v1.0/stations<br/>"
        f"temperature observations of the most-active station for the previous year<br/>"
        f"/api/v1.0/<start><br/>"
        f"The average,maximum, minimum, temperature for a specified start datr<br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )
@app.route(" /api/v1.0/precipitation")
def precipitation():

# 2. Create an app, being sure to pass __name__
 session = Session(engine)
# Design a query to retrieve the last 12 months of precipitation data and plot the results. 
date_last_12months= dt.date(2017,8,23) - dt.timedelta(days=365)

# Perform a query to retrieve the data and precipitation scores

results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= date_last_12months).order_by(Measurement.date).all()

session.close()

session.close()
all_prcp_data =[]
for date,prcp in results:
    prcp_dict ={}
    prcp_dict[date] = prcp
    all_prcp_data.append(prcp_dict)
    
print.jsonify(all_prcp_data)

# run server  
if __name__ == "__main__":
    app.run(debug=True)
