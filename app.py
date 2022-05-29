#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import sys #
from datetime import datetime
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from requests import session
from sqlalchemy import null
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)

app.config.from_object('config')
db = SQLAlchemy(app)


# TODO: connect to a local postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/fyyurdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    venue_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_descriptions = db.Column(db.String(500))

    def __repr__(self):
        return f'<Todo ID: {self.venue_id}, name: {self.name}, city: {self.city}, state: {self.state}, address: {self.address}, phone: {self.phone}, genres: {self.genres}, image_link: {self.image_link}>, facebook_link: {self.facebook_link}, website_link: {self.website_link}, seeking_talent: {self.seeking_talent}, seeking_descriptions: {self.seeking_descriptions}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    artist_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    seeking_venues = db.Column(db.Boolean, nullable=False, default=False)
    seeking_descriptions = db.Column(db.String(500))
    
    def __repr__(self):
        return f'ID: {self.artist_id}, name: {self.name}, city: {self.city}, state: {self.state}, phone: {self.phone}, genres: {self.genres}, image_link: {self.image_link}>, facebook_link: {self.facebook_link}, website_link: {self.website_link}, seeking_venues: {self.seeking_venues}, seeking_descriptions: {self.seeking_descriptions}'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
  __tablename__ = 'Show'

  show_id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.artist_id'))
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.venue_id'))
  start_time = db.Column(db.DateTime)

  def __repr__(self):
        return f'<Todo show_id: {self.show_id}, artist_id: {self.artist_id}, venue_id: {self.venue_id}, start_time: {self.start_time}>'

#db.create_all()
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#
def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#
@app.route('/')
def index():
  """ Displays home page of web application. """
  return render_template('pages/home.html')

#  Venues
#  ----------------------------------------------------------------
@app.route('/venues')
def venues():
  """ Displays all venues within Fyyurdb database. """
  x = datetime.now()
  venues = Venue.query.all() # Querying all venues in Venue table
  data = []
  final_data = []

  for i in venues: # Loops through venues city and state data 
    new_dict = {}
    new_dict['city'] = i.city
    new_dict['state'] = i.state
    if new_dict not in data: 
      data.append(new_dict)

  for i in data: 
    new_dict = {} # Creates new dictionary to hold city, state and shows data. 
    new_dict['city'] = i['city']
    new_dict['state'] = i['state']
    
    shows_data = Show.query.join(Venue, Venue.venue_id == Show.venue_id).filter(Venue.city == i['city']).order_by('name').all()
    num_of_shows = len(shows_data)

    venues = []
    
    for j in shows_data:
      sec_dict = {} # Second dictionary created to add all shows relevant to specified venue. 
      show = Venue.query.join(Show, Venue.venue_id == Show.venue_id).filter(Venue.venue_id == j.venue_id).one_or_none()
      num_of_shows = len(Show.query.join(Venue, Venue.venue_id == Show.venue_id).filter(Venue.venue_id == j.venue_id).filter(Show.start_time > x).all())
      
      sec_dict['id'] = j.venue_id
      sec_dict['name'] = show.name
      sec_dict['num_upcoming_shows'] = num_of_shows
      if sec_dict not in venues:
        venues.append(sec_dict)
      new_dict['venues'] = venues

      if new_dict not in final_data:
        final_data.append(new_dict) # New entry is added to main list. Main list will be used to display the Venue data. 

  """data=[{
    "city": "San Francisco",
    "state": "CA",
    "venues": [{
      "id": 1,
      "name": "The Musical Hop",
      "num_upcoming_shows": 0,
    }, {
      "id": 3,
      "name": "Park Square Live Music & Coffee",
      "num_upcoming_shows": 1,
    }]
  }, {
    "city": "New York",
    "state": "NY",
    "venues": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
    #  "num_upcoming_shows": 0,
    }]
  }]"""
  return render_template('pages/venues.html', areas=final_data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  """ User will search for particular string within venues data. Function will return the results. """
  x = datetime.now()
  search_term=request.form.get('search_term', '').lower() # Retrieve search term and set it to lower case. 
  venues = Venue.query.distinct().all() # Return all unique venues 
  count = 0
  data = []

  for i in venues:
    if search_term in (i.name).lower():
      new_dict = {} # Created dictionary to store venue_id, name and upcoming shows at venue. 
      new_dict['id'] = i.venue_id
      new_dict['name'] = i.name
      new_dict['num_upcoming_shows'] = Artist.query.join(Show).where(Show.venue_id == i.venue_id).where(Show.start_time > x).count() # Count the number of artists that have upcoming shows at the venue
      data.append(new_dict)
      count += 1 

  response={
    "count": count,
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  """ Display venue data. All venue details including upcoming shows and past shows. """
  x = datetime.now()
  venues = Venue.query.distinct().all()
  count = 0
  venue_list = []

  for i in venues:
    venue_dict = {} # Dictionary created to store all venue data
    genres = i.genres[1:-1].split(",")
    venue_dict['id'] = i.venue_id
    venue_dict['genres'] = genres
    venue_dict['name'] = i.name
    venue_dict['address'] = i.address
    venue_dict['city'] = i.city
    venue_dict['state'] = i.state
    venue_dict['phone'] = i.phone
    venue_dict['website'] = i.website_link
    venue_dict['facebook_link'] = i.facebook_link
    venue_dict['seeking_talent'] = i.seeking_talent
    venue_dict['seeking_descriptions'] = i.seeking_descriptions
    venue_dict['image_link'] = i.image_link

    past_show_shows = Show.query.join(Artist, Show.artist_id == Artist.artist_id).where(Show.venue_id == i.venue_id).where(Show.start_time < x).order_by('start_time').all() # Returns all past shows 
    upcoming_show_shows = Show.query.join(Artist, Show.artist_id == Artist.artist_id).where(Show.venue_id == i.venue_id).where(Show.start_time > x).order_by('start_time').all() # Returns all upcoming shows
 
    past_show = []
    past_dict = {}
    past_count = 0

    for j in past_show_shows:
      past_dict = {} # Stores all relevant artist information including past shows
      artist = Artist.query.join(Show, Show.artist_id == Artist.artist_id).where(Show.artist_id == j.artist_id).one_or_none() # Returns one specified artist 
      past_dict['artist_id'] = artist.artist_id
      past_dict['artist_name'] = artist.name
      past_dict['artist_image_link'] = artist.image_link
      
      if len(past_show_shows) != 0:
        show_list = [i.start_time for i in past_show_shows]
        past_dict['start_time'] = show_list[past_count].strftime('%Y-%m-%dT%H:%M:%SZ') # Converts date and time to relevant format
      past_show.append(past_dict)
      past_count += 1
    
    venue_dict['past_shows'] = past_show
    venue_dict['past_shows_count'] = len(past_show)
    
    upcoming_show = []
    upcoming_count = 0

    for j in upcoming_show_shows:
      upcoming_dict = {} # Stores all relevant artist information including upcoming shows
      artist = Artist.query.join(Show, Show.artist_id == Artist.artist_id).where(Show.artist_id == j.artist_id).one_or_none() # Returns one specified artist 
      upcoming_dict['artist_id'] = artist.artist_id
      upcoming_dict['artist_name'] = artist.name
      upcoming_dict['artist_image_link'] = artist.image_link
      
      if len(upcoming_show_shows) > 0:
        upcoming_show_list = [j.start_time for j in upcoming_show_shows]
        upcoming_dict['start_time'] = upcoming_show_list[upcoming_count].strftime('%Y-%m-%dT%H:%M:%SZ') # Converts date and time to relevant format
      upcoming_count += 1
      
      upcoming_show.append(upcoming_dict)
    
    venue_dict['upcoming_shows'] = upcoming_show
    venue_dict['upcoming_shows_count'] = len(upcoming_show)
    

    venue_list.append(venue_dict)
    count += 1

  """data1={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    
    "past_shows": [{
      "artist_id": 1,
      "artist_name": "Guns N Petals",
      "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],

    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data2={
    "id": 2,
    "name": "The Dueling Pianos Bar",
    "genres": ["Classical", "R&B", "Hip-Hop"],
    "address": "335 Delancey Street",
    "city": "New York",
    "state": "NY",
    "phone": "914-003-1132",
    "website": "https://www.theduelingpianos.com",
    "facebook_link": "https://www.facebook.com/theduelingpianos",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0,
  }
  data3={
    "id": 3,
    "name": "Park Square Live Music & Coffee",
    "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
    "address": "34 Whiskey Moore Ave",
    "city": "San Francisco",
    "state": "CA",
    "phone": "415-000-1234",
    "website": "https://www.parksquarelivemusicandcoffee.com",
    "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    "past_shows": [{
      "artist_id": 2,
      "artist_name": "Matt Quevedo",
      "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [{
      "artist_id": 3,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "artist_id": 3,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "artist_id": 3,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 1,
    "upcoming_shows_count": 1,
  }"""
  data = list(filter(lambda d: d['id'] == venue_id, venue_list))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------
@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  """ Displays form to capture Venue data. """
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  """ Captures Venue data and commits the entry into the fyyurdb database. """
  form = VenueForm()
  error = False
  body = {}

  try:
    venue = Venue(name=form.name.data, city=form.city.data, state=form.state.data,
                  genres=form.genres.data, facebook_link=form.facebook_link.data, address=form.address.data, 
                  image_link=form.image_link.data, website_link=form.website_link.data, seeking_talent=form.seeking_talent.data,
                  seeking_descriptions=form.seeking_description.data)

    db.session.add(venue) # Add data to Database.
    db.session.commit() # Make commitment to database. 

    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    error = True
    flash('Venue ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
  if error:
    abort(500)
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  #flash('Venue ' + request.form['name'] + ' was successfully listed!')
  ## TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  """Deletes venue data according the venue ID. """
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error = False

  try:
      venue = Venue.query.get(venue_id)
      db.session.delete(venue)
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully deleted!')
  except:
      db.session.rollback()
      error = True
      flash('Venue ' + request.form['name'] + ' could not be deleted.')
  finally:
      db.session.close()
  if error:
      abort(500)
  else:
      return jsonify({'success': True})

  return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  """ Dsiplays all artists within the Database. """
  artists = Artist.query.distinct().order_by('name').all()

  data = [{"id": artists[i].artist_id, "name": artists[i].name} for i in range(len(artists))]

  """#data=[{
    "id": 1,
    "name": "Guns N Petals",
  }, {
    "id": 2,
    "name": "Matt Quevedo",
  }, {
    "id": 3,
    "name": "The Wild Sax Band",
  }, {
  "id": 3, 
  "name": "The Wild Sax Band"
  }
  ]"""
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  """ Returns all artist names that contain a user-defined string. """
  x = datetime.now()

  search_term=request.form.get('search_term', '').lower()
  artists = Artist.query.distinct().all() # Returns all unique artist names. 
  count = 0
  data = []

  for i in artists:
    if search_term in (i.name).lower():
      new_dict = {}
      new_dict['id'] = i.artist_id
      new_dict['name'] = i.name
      new_dict['num_upcoming_shows'] = Artist.query.join(Show).where(Show.artist_id == i.artist_id).where(Show.start_time > x).count()
      data.append(new_dict)
      count += 1 

  response={
    "count": count,
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  """ Displays all data associated with a particular artist. """
  x = datetime.now()
  artists = Artist.query.distinct().all()

  
  artist_list = []
  for i in artists:
    artist_dict = {}
    genres = i.genres[1:-1].split(",")
    artist_dict['id'] = i.artist_id
    artist_dict['name'] = i.name
    artist_dict['genres'] = genres
    artist_dict['city'] = i.city
    artist_dict['state'] = i.state
    artist_dict['phone'] = i.phone
    artist_dict['website'] = i.website_link
    artist_dict['facebook_link'] = i.facebook_link
    artist_dict['seeking_venues'] = i.seeking_venues
    artist_dict['seeking_descriptions'] = i.seeking_descriptions
    artist_dict['image_link'] = i.image_link

    past_show_shows = Show.query.join(Venue, Show.venue_id == Venue.venue_id).join(Artist, Artist.artist_id == Show.artist_id).where(Show.artist_id == i.artist_id).where(Show.start_time < x).order_by('start_time').all()
    upcoming_show_shows = Show.query.join(Venue, Show.venue_id == Venue.venue_id).join(Artist, Artist.artist_id == Show.artist_id).where(Show.artist_id == i.artist_id).where(Show.start_time > x).order_by('start_time').all()
    
    past_show = []
    past_count = 0

    for j in past_show_shows:
      past_dict = {}
      venue = Venue.query.join(Show, Show.venue_id == Venue.venue_id).where(Show.venue_id == j.venue_id).one_or_none()
      past_dict['venue_id'] = venue.venue_id
      past_dict['venue_name'] = venue.name
      past_dict['venue_image_link'] = venue.image_link
     
      if len(past_show_shows) != 0:
        show_list = [i.start_time for i in past_show_shows]

      if len(show_list) != 0:
        past_dict['start_time'] = show_list[past_count].strftime('%Y-%m-%dT%H:%M:%SZ')
      past_count += 1
      past_show.append(past_dict)
    
    artist_dict['past_shows'] = past_show
    artist_dict['past_shows_count'] = len(past_show)
    
    upcoming_show = []
    upcoming_count = 0

    for j in upcoming_show_shows:
      upcoming_dict = {}
      venue = Venue.query.join(Show, Show.venue_id == Venue.venue_id).where(Show.venue_id == j.venue_id).one_or_none()
      upcoming_dict['venue_id'] = venue.venue_id
      upcoming_dict['venue_name'] = venue.name
      upcoming_dict['venue_image_link'] = venue.image_link
      
      if len(upcoming_show_shows) != 0:
        upcoming_show_list = [j.start_time for j in upcoming_show_shows]

      if len(upcoming_show_list) != 0:
        upcoming_dict['start_time'] = upcoming_show_list[upcoming_count].strftime('%Y-%m-%dT%H:%M:%SZ')
      upcoming_count += 1
        
      upcoming_show.append(upcoming_dict)
    
    artist_dict['upcoming_shows'] = upcoming_show
    artist_dict['upcoming_shows_count'] = len(upcoming_show)

    artist_list.append(artist_dict)
  
  
  """data1={
    "id": 1,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    
    "past_shows": [{
      "venue_id": 1,
      "venue_name": "The Musical Hop",
      "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],

    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data2={
    "id": 2,
    "name": "Matt Quevedo",
    "genres": ["Jazz"],
    "city": "New York",
    "state": "NY",
    "phone": "300-400-5000",
    "facebook_link": "https://www.facebook.com/mattquevedo923251523",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "past_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data3={
    "id": 3,
    "name": "The Wild Sax Band",
    "genres": ["Jazz", "Classical"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "432-325-5432",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "past_shows": [],
    "upcoming_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 0,
    "upcoming_shows_count": 3,
  }"""
  data = list(filter(lambda d: d['id'] == artist_id, artist_list))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  """ Displays the form for the artist data entry. """
  form = ArtistForm()
  artist_query = Artist.query.filter(Artist.artist_id == artist_id).one_or_none()

  artist = {}
  artist['id'] = artist_query.artist_id   
  artist['name'] = artist_query.name 
  artist['genres'] = artist_query.genres 
  artist['city'] = artist_query.city 
  artist['state'] = artist_query.state 
  artist['phone'] = artist_query.phone 
  artist['website'] = artist_query.website_link
  artist['facebook_link'] = artist_query.facebook_link 
  artist['seeking_venue'] = artist_query.seeking_venues
  artist['seeking_description'] = artist_query.seeking_descriptions
  artist['image_link'] = artist_query.image_link 

  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  """Captures all the artist data for entry into the fyyurdb database."""
  form = ArtistForm()
  error = False

  try:
    artist_form = Artist(name=form.name.data, city=form.city.data, state=form.state.data,
                    phone=form.phone.data, genres=form.genres.data, facebook_link=form.facebook_link.data, 
                    image_link=form.image_link.data, website_link=form.website_link.data, seeking_venues=form.seeking_venue.data, 
                    seeking_descriptions=form.seeking_description.data)

    
    artist = Artist.query.get(artist_id)

    # Updates if the field is not empty
    if artist_form.name != None:
      artist.name = artist_form.name

    if artist_form.city != None:
      artist.city = artist_form.city

    if artist_form.state != None:
      artist.state = artist_form.state

    if artist_form.phone != None:
      artist.phone = artist_form.phone

    if artist_form.genres != None:
      artist.genres = artist_form.genres

    if artist_form.facebook_link != None:
      artist.facebook_link = artist_form.facebook_link

    if artist_form.image_link != None:
      artist.image_link = artist_form.image_link

    if artist_form.website_link != None:
      artist.website_link = artist_form.website_link

    if artist_form.seeking_venues != None:
      artist.seeking_venues = artist_form.seeking_venues

    if artist_form.seeking_descriptions != None:
      artist.seeking_descriptions = artist_form.seeking_descriptions

    db.session.commit()
    flash("Updated user '{}'".format(artist.name))
        
  except:
      db.session.rollback()
      error = True
      print(sys.exc_info())
  finally:
      db.session.close()
  if error:
      abort(500)

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  """ Displays the form for capturing venue data. """
  form = VenueForm()
  venue_query = Venue.query.filter(Venue.venue_id == venue_id).one_or_none()

  venue = {}
  venue['id'] = venue_query.venue_id   
  venue['name'] = venue_query.name 
  venue['genres'] = venue_query.genres
  venue['address'] = venue_query.address 
  venue['city'] = venue_query.city 
  venue['state'] = venue_query.state 
  venue['phone'] = venue_query.phone 
  venue['website'] = venue_query.website_link
  venue['facebook_link'] = venue_query.facebook_link 
  venue['seeking_talent'] = venue_query.seeking_talent
  venue['seeking_description'] = venue_query.seeking_descriptions
  venue['image_link'] = venue_query.image_link 

  """venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }"""
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  """ Captures all venue data for entry into the fyyurdb database. """
  form = VenueForm()
  error = False

  try:
    venue_form = Venue(name=form.name.data, city=form.city.data, state=form.state.data,
                  genres=form.genres.data, facebook_link=form.facebook_link.data, address=form.address.data, 
                  image_link=form.image_link.data, website_link=form.website_link.data, seeking_talent=form.seeking_talent.data,
                  seeking_descriptions=form.seeking_description.data)

    venue = Venue.query.get(venue_id)

    # Updates the value if field is empty. 
    if venue_form.name != None:
      venue.name = venue_form.name

    if venue_form.city != None:
      venue.city = venue_form.city

    if venue_form.state != None:
      venue.state = venue_form.state

    if venue_form.address != None:
      venue.address = venue_form.address

    if venue_form.genres != None:
      venue.genres = venue_form.genres
    
    if venue_form.phone != None:
      venue.phone = venue_form.phone

    if venue_form.facebook_link != None:
      venue.facebook_link = venue_form.facebook_link

    if venue_form.image_link != None:
      venue.image_link = venue_form.image_link

    if venue_form.website_link != None:
      venue.website_link = venue_form.website_link

    if venue_form.seeking_talent != None:
      venue.seeking_talent = venue_form.seeking_talent

    if venue_form.seeking_descriptions != None:
      venue.seeking_descriptions = venue_form.seeking_descriptions

    db.session.commit()
        
    flash("{} has been updated.'".format(venue.name))
        
  except:
      db.session.rollback()
      error = True
      print(sys.exc_info())
  finally:
      db.session.close()
  if error:
      abort(500)
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  """ Displays form for capturing artist data. """
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  """ Captures all artist data for new entry into the fyyurdb database. """
  form = ArtistForm()
  error = False
  body = {}

  try:
    artist = Artist(name=form.name.data, city=form.city.data, state=form.state.data,
                    phone=form.phone.data, genres=form.genres.data, facebook_link=form.facebook_link.data, 
                    image_link=form.image_link.data, website_link=form.website_link.data, seeking_venues=form.seeking_venue.data, 
                    seeking_descriptions=form.seeking_description.data)
  
    db.session.add(artist)
    db.session.commit()
    body['name'] = Artist.name
    body['city'] = Artist.city
    body['state'] = Artist.state
    body['phone'] = Artist.phone
    body['genres'] = Artist.genres
    body['image_link'] = Artist.image_link
    body['facebook_link'] = Artist.facebook_link
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    error = True
    flash('Artist ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
  if error:
    abort(500)

  # on successful db insert, flash success
  #flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  """ Displays all shows within the fyyurdb database. """
  x = datetime.now()
  shows = Show.query.join(Artist, Artist.artist_id == Show.artist_id).join(Venue, Venue.venue_id == Show.venue_id).order_by('start_time').all()
  count = 0
  data = []

  for i in shows:
    venue = Venue.query.filter(Venue.venue_id == i.venue_id).one_or_none()
    artist = Artist.query.join(Show, Show.artist_id == Artist.artist_id).join(Venue, Venue.venue_id == Show.venue_id).filter(Show.artist_id == i.artist_id).one_or_none()
    show_dict = {}
    show_dict['venue_id'] = venue.venue_id
    show_dict['venue_name'] = venue.name
    show_dict['artist_id'] = artist.artist_id
    show_dict['artist_name'] = artist.name
    show_dict['artist_image_link'] = artist.image_link

    upcoming_show_show = Show.query.where(i.venue_id == venue.venue_id).where(i.artist_id == artist.artist_id).where(i.start_time > x).order_by('start_time').all()

    if len(upcoming_show_show) != 0:
      upcoming_show_list = [j.start_time for j in upcoming_show_show]
      show_dict['start_time'] = upcoming_show_list[count].strftime("%Y-%m-%dT%H:%M:%SZ")
    
    past_show_show = Show.query.where(i.venue_id == venue.venue_id).where(i.artist_id == artist.artist_id).where(i.start_time < x).order_by('start_time').all()

    if len(past_show_show) != 0:
      past_show_list = [j.start_time for j in past_show_show]
      show_dict['start_time'] = past_show_list[count].strftime("%Y-%m-%dT%H:%M:%SZ")
      
    data.append(show_dict)
    count += 1
  
  """data=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 1,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 2,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 3,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 3,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 3,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
  }]"""
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  """ Displays form for show creation. """
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  """ Captures all show data for new entry into fyyurdb database. """
  form = ShowForm()
  count = len(Show.query.all())
  error = False
  body = {}

  try:
    show = Show(artist_id=form.artist_id.data, venue_id=form.venue_id.data,
                  start_time=form.start_time.data)

    db.session.add(show)
    db.session.commit()
    body['artist_id'] = Show.artist_id
    body['venue_id'] = Show.venue_id
    body['start_time'] = Show.start_time
  
    flash('Show ' + str(count + 1) + ' was successfully listed!')
  except:
    db.session.rollback()
    error = True
    flash('Show ' + str(count + 1) + ' could not be listed.')
  finally:
    db.session.close()
  if error:
    abort(500)
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  #flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
