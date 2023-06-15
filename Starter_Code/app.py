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
        f"/api/v1.0/tobs</br/>"
        f"The average,maximum, minimum, temperature for a specified start date<br/>"
        f"/api/v1.0/start<br/>"
        f"The average,maximum, minimum, temperature for a specified start date and end date<br/>"
        f"/api/v1.0/start/end<br/>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
        
    # 2. Create an app, being sure to pass __name__
    session = Session(engine)
    # Design a query to retrieve the last 12 months of precipitation data and plot the results. 
    date_last_12months= dt.date(2017,8,23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores

    results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= date_last_12months).order_by(Measurement.date).all()

    all_prcp_data =[]
    for date,prcp in results:
        prcp_dict ={}
        prcp_dict[date] = prcp
        all_prcp_data.append(prcp_dict)
        
    return jsonify(all_prcp_data)


if __name__ == "__main__":
 app.run(debug=True)

#
# 2. Create an app, being sure to pass  /api/v1.0/stations"
#Activation Weather Station: 
@app.rout("/api/v1.0/stations")
def stations():

     # create setion link from python to the DB
    session = Session(engine)

     #Return a JSON list of stations from the dataset.
    station_name = session.query(Station.name,Station.stations,Station.elevation,Station.latitude,Station.longitude).all()
  
    # Perform a query to retrieve the data stations scores

#create  dictionanry 
    station_list=[]
    for name, stations, elevation, latitude,longitude in station_name: 
        station_dict ={}
        station_dict['Name']= name
        station_dict['Station']= Station
        station_dict['Elevation']= elevation
        station_dict['Latitude']= latitude
        station_dict['Longitude']= longitude
        station_list.append(station_dict)
    return jsonify(station_dict)
    
if __name__ == "__main__":
 app.run(debug=True)
    
#"temperature observations of the most-active station for the previous year<br/>"
#"/api/v1.0/tobs</br/>"  
@app.rout("/api/v1.0/tobs")
def tobs():
    # create setion link from python to the DB
    session = Session(engine)
    
    
    date_last_12months= dt.date(2017,8,23) - dt.timedelta(days=365)
    
    result_station = session.query( Measurement.tobs).\
    filter(Measurement.station =='USC00519281').\
    filter(Measurement.date >= date_last_12months).all()
    
    
    session.close()
    
    active_station =[]
    for date,temp in result_station:
        active_dict={}
        active_dict[date]= temp
        active_station.append(active_dict)
    return jsonify(active_station)
    
 #run server     
if __name__ == "__main__":
 app.run(debug=True)
 
# #The average,maximum, minimum, temperature for a specified start date<br/>"
#   # f"/api/v1.0/<start><br/>"
@app.rout("/api/v1.0/start")
def start():
# 
    #  # 2. Create an app, being sure to pass __name__
    session = Session(engine)
    #  Design a query to retrieve the last 12 months of precipitation data and plot the results. 
    avrg_temp = session.query(Measurement.station, func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.station == 'USC00519281').all()

    
    start_date_tem =[]
    for min,max,avg in avrg_temp:
            start_date={}
            start_date['Min Temp']= min
            start_date['Max Temp']= max
            start_date['Avg Temp']= avg
            start_date_tem.append(start_date)
    return jsonify(start_date)
    # Perform a query to retrieve the data and precipitation scores

# The average,maximum, minimum, temperature for a specified start date and end date<br/>"
# f"/api/v1.0/<start>/<end><br/>"
    
@app.rout("/api/v1.0/start/end")
def start_end():
# 
    #  # 2. Create an app, being sure to pass __name__
    session = Session(engine)
    #  Design a query to retrieve the last 12 months of precipitation data and plot the results. 


    star_end_temp = session.query(Measurement.station, func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.station >= date_start ).filter(Measurement.date <= last_date_year).all()
    
    start_date_tem =[]
    for min,max,avg in star_end_temp:
            start_date={}
            start_date['Min Temp']= min
            start_date['Max Temp']= max
            start_date['Avg Temp']= avg
            start_date_tem.append(start_date)
    return jsonify(start_date_tem)
    
# #run server     
if __name__ == "__main__":
 app.run(debug=True)
