#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import sys #
from datetime import datetime
import json
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
        return f'<Todo ID: {self.venue_id}, name: {self.name}, city: {self.city}>'

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
        return f'ID: {self.artist_id}, name: {self.name}, city: {self.city}, state: {self.state}, phone: {self.phone}, genres: {self.genres}, image_link: {self.image_link}>, facebook_link: {self.facebook_link}'

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
  return render_template('pages/home.html')

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  x = datetime.now()

  venues = Venue.query.all()
  #upcoming_shows = Venue.query.group_by('city').count()
  #venue_shows = Show.query.join(Venue)
  #(venues, file=sys.stderr)
  #print(upcoming_shows, file=sys.stderr)
  #print(venue_shows, file=sys.stderr)
  
  #active_list = Artist.query.get(venue_id)
  #print(artists[2].name, file=sys.stderr)
  #print(active_list, file=sys.stderr)
  #data1 = []
  shows_data = Show.query.join(Venue).all()
  #print(shows_data, file=sys.stderr)
  #data = [{"city": i.city, "state": i.state} for i in venues]
  data = []
  final_data = []
  for i in venues:
    new_dict = {}
    new_dict['city'] = i.city
    new_dict['state'] = i.state
    if new_dict not in data: 
      data.append(new_dict)

  #print(data, file=sys.stderr)
  
  for i in data:
    new_dict = {}
    new_dict['city'] = i['city']
    new_dict['state'] = i['state']
    
    print(i['city'], file=sys.stderr)
    shows_data = Show.query.join(Venue, Venue.venue_id == Show.venue_id).filter(Venue.city == i['city']).filter(Show.start_time > x).all()
    #venues_data = Venue.query.join(Show, Venue.venue_id == Show.venue_id).filter(Show.venue_id == i['city']).filter(Show.start_time > x).all()
    print("Show data {}".format(shows_data), file=sys.stderr)
    num_of_shows = len(shows_data)
    #print(venues_data, file=sys.stderr)
    print(num_of_shows, file=sys.stderr)
    venues = []
    
    for j in shows_data:
      print("J {}".format(j), file=sys.stderr)
      show = Venue.query.join(Show, Venue.venue_id == Show.venue_id).filter(Venue.venue_id == j.venue_id).filter(Show.start_time > x).one_or_none()
      
      num_of_shows = len(Show.query.join(Venue, Venue.venue_id == Show.venue_id).filter(Venue.venue_id == j.venue_id).filter(Show.start_time > x).all())
      print("num_shows {}".format(num_of_shows), file=sys.stderr)
        #venues_data = Venue.query.join(Show, Venue.venue_id == Show.venue_id).filter(Venue.venue_id == j.venue_id).filter(Show.start_time > x).one_or_none()
        #print(venues_data, file=sys.stderr)
      # print(j, file=sys.stderr)
      # name = Venue.query.join(Show, Venue.venue_id == Show.venue_id).filter(Venue.name == i['name']).one_or_none()
      sec_dict = {}
      sec_dict['id'] = j.venue_id
      sec_dict['name'] = show.name #venues_data['Venue']
      sec_dict['num_upcoming_shows'] = num_of_shows
      venues.append(sec_dict)
      new_dict['venues'] = venues

      if new_dict not in final_data:
        final_data.append(new_dict)

    

  print(final_data, file=sys.stderr)

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
  #return "Hello"
  return render_template('pages/venues.html', areas=final_data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  x = datetime.now()

  search_term=request.form.get('search_term', '').lower()
  print(search_term, file=sys.stderr)
  venues = Venue.query.distinct().all()
  print(venues[0], file=sys.stderr)
  count = 0
  data = []
  for i in venues:
    if search_term in (i.name).lower():
      new_dict = {}
      print(i.name, file=sys.stderr)
      print(i.venue_id, file=sys.stderr)
      new_dict['id'] = i.venue_id
      new_dict['name'] = i.name
      new_dict['num_upcoming_shows'] = Artist.query.join(Show).where(Show.venue_id == i.venue_id).where(Show.start_time > x).count()
      data.append(new_dict)
      #upcoming_shows = Artist.query.join(Show).where(Show.artist_id == i.artist_id).where(Show.start_time > x).all()
      count += 1 
  #print(upcoming_shows, file=sys.stderr)
  #print(data, file=sys.stderr)
  response={
    "count": count,
    "data": data
  }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  #venues = Venue.query.distinct().all()
  x = datetime.now()

  past_shows_count = Show.query.where(Show.artist_id == venue_id).where(Show.start_time < x).count()
  print(past_shows_count, file=sys.stderr)
  upcoming_shows_count = Show.query.where(Show.artist_id == venue_id).where(Show.start_time > x).count()
  print(upcoming_shows_count, file=sys.stderr)
  upcoming_shows = Artist.query.join(Show).where(Show.artist_id == venue_id).where(Show.start_time > x).all()
  print(upcoming_shows, file=sys.stderr)
  
  #active_list = Artist.query.get(venue_id)
  #print(artists[2].name, file=sys.stderr)
  #print(active_list, file=sys.stderr)
  #data1 = []
  #data = [{"city": venues[i].city, "state": venues[i].state} for i in range(len(venues))]
  
  data1={
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
  }
  data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  form = VenueForm()
  print(form.data, file=sys.stderr)
  error = False
  body = {}

  try:
    venue = Venue(name=form.name.data, city=form.city.data, state=form.state.data,
                  genres=form.genres.data, facebook_link=form.facebook_link.data, address=form.address.data, 
                  image_link=form.image_link.data, website_link=form.website_link.data, seeking_talent=form.seeking_talent.data,
                  seeking_descriptions=form.seeking_description.data)
    print('Venue form created.', file=sys.stderr)
    print(venue, file=sys.stderr)
    db.session.add(venue)
    db.session.commit()
    #body['venue_id'] = Venue.venue_id
    body['name'] = Venue.name
    body['city'] = Venue.city
    body['state'] = Venue.state
    body['address'] = Venue.address
    body['phone'] = Venue.phone
    body['image_link'] = Venue.image_link
    body['facebook_link'] = Venue.facebook_link
    print(body, file=sys.stderr)

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
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error = False
  try:
      #Todo.query.filter_by(id=todo_id).delete()
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

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artists = Artist.query.distinct().all()
  print(artists, file=sys.stderr)
  
  #active_list = Artist.query.get(venue_id)
  #print(artists[2].name, file=sys.stderr)
  #print(active_list, file=sys.stderr)
  #data1 = []
  #data = [{"id": artists[i].artist_id, "name": artists[i].name} for i in range(len(artists))]
  #for i in range(len(artists)):
    #print(artists[i].venue_id, file=sys.stderr)
    #print(artists[i].name, file=sys.stderr)
   # data1.append({"id": artists[i].venue_id, "name": artists[i].name})
    #data1['id'] = artists[i].venue_id
    #data1['name'] = artists[i].name

  #print(data, file=sys.stderr)
  data=[{
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
  ]
  #data = data1
  #print(len(data), file=sys.stderr)
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  x = datetime.now()

  search_term=request.form.get('search_term', '').lower()
  print(search_term, file=sys.stderr)
  artists = Artist.query.distinct().all()
  print(artists[0], file=sys.stderr)
  count = 0
  data = []
  for i in artists:
    if search_term in (i.name).lower():
      new_dict = {}
      print(i.name, file=sys.stderr)
      print(i.artist_id, file=sys.stderr)
      new_dict['id'] = i.artist_id
      new_dict['name'] = i.name
      new_dict['num_upcoming_shows'] = Artist.query.join(Show).where(Show.artist_id == i.artist_id).where(Show.start_time > x).count()
      data.append(new_dict)
      #upcoming_shows = Artist.query.join(Show).where(Show.artist_id == i.artist_id).where(Show.start_time > x).all()
      count += 1 
  #print(upcoming_shows, file=sys.stderr)
  print(data, file=sys.stderr)
  response={
    "count": count,
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  #artists = Artist.query.all()
  #active_list = Artist.query.get(artist_id)
  
  data1={
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
  }
  data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  #error = False
  #print(form, file=sys.stderr)
  #try:
    
    #artist = Artist(name=form.name.data, city=form.city.data,
     #             state=form.state.data, phone=form.phone.data, genres=form.genres.data, 
      #            image_link=form.image_link.data, facebook_link=form.facebook_link.data)
    #print('Artist form created.', file=sys.stderr)
    
    #db.session.add(venue)
    #db.session.commit()
      #complete = request.get_json()['complete']
   # artist = Artist.query.get(artist_id)
    #print('artist: ', artist)
      #todo.complete = complete
      #db.session.commit()
  #except():
   #   db.session.rollback()
    #  error = True
     # print(sys.exc_info())
  #finally:
   #   db.session.close()
  #if error:
   #   abort(500)
  #else:
   # return redirect(url_for('index'))
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm()
  error = False
  print(form.data, file=sys.stderr)
  try:
    
    artist_form = Artist(name=form.name.data, city=form.city.data, state=form.state.data,
                    phone=form.phone.data, genres=form.genres.data, facebook_link=form.facebook_link.data, 
                    image_link=form.image_link.data, website_link=form.website_link.data, seeking_venues=form.seeking_venue.data, 
                    seeking_descriptions=form.seeking_description.data)
    print('Artist form created.', file=sys.stderr)
    print(artist_form, file=sys.stderr)
    #print(type(artist_form), file=sys.stderr)
    
    #db.session.add(venue)
    #db.session.commit()
      #complete = request.get_json()['complete']
    artist = Artist.query.get(1)
    print(artist, file=sys.stderr)
    for i in form.data:
      if form.data[i] == '' or None:
        #print(i, file=sys.stderr)
        pass
        #i = artist_form.i
      else:
        print(i, file=sys.stderr)
        print(form.data[i], file=sys.stderr)
        artist.i = form.data[i]
        print('-----------', file=sys.stderr)
        print(artist.i, file=sys.stderr)
        print('-----------', file=sys.stderr)
        db.session.commit()
  except():
      db.session.rollback()
      error = True
      print(sys.exc_info())
  finally:
      db.session.close()
  if error:
      abort(500)
  #else:
   # return redirect(url_for('index'))
  
  return 'Done'
  #return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  print(form, file=sys.stderr)
  venue={
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
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  form = VenueForm()
  error = False
  print(form.data, file=sys.stderr)
  try:
    
    venue_form = Venue(name=form.name.data, city=form.city.data, state=form.state.data,
                  genres=form.genres.data, facebook_link=form.facebook_link.data, address=form.address.data, 
                  image_link=form.image_link.data, website_link=form.website_link.data, seeking_talent=form.seeking_talent.data,
                  seeking_descriptions=form.seeking_description.data)
    print('Venue form created.', file=sys.stderr)
    print(venue_form, file=sys.stderr)
    #print(type(artist_form), file=sys.stderr)
    
    #db.session.add(venue)
    #db.session.commit()
      #complete = request.get_json()['complete']
    venue = Venue.query.get(1)
    print(venue, file=sys.stderr)
    for i in form.data:
      if form.data[i] == '' or None:
        #print(i, file=sys.stderr)
        pass
        #i = artist_form.i
      else:
        print(i, file=sys.stderr)
        print(form.data[i], file=sys.stderr)
        venue.i = form.data[i]
        print('-----------', file=sys.stderr)
        print(venue.i, file=sys.stderr)
        print('-----------', file=sys.stderr)
        db.session.commit()
  except:
    db.session.rollback()
    error = True
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort(500)
  #return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  form = ArtistForm()
  print(form.data, file=sys.stderr)
  error = False
  body = {}
  try:
    artist = Artist(name=form.name.data, city=form.city.data, state=form.state.data,
                    phone=form.phone.data, genres=form.genres.data, facebook_link=form.facebook_link.data, 
                    image_link=form.image_link.data, website_link=form.website_link.data, seeking_venues=form.seeking_venue.data, 
                    seeking_descriptions=form.seeking_description.data)
  
    print('Artist form created.', file=sys.stderr)
    print(artist, file=sys.stderr)
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

  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  #flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  shows = Show.query.where(Show.artist_id == 3).count()
  count = 0
  #for i in shows:
   # print(i, file=sys.stderr)
    #count += 1 
  #print(count, file=sys.stderr)
  print(shows, file=sys.stderr)
  
  #active_list = Artist.query.get(venue_id)
  #print(artists[2].name, file=sys.stderr)
  #print(active_list, file=sys.stderr)
  #data1 = []
  #data = [{"id": shows[i].show_id, "start_time": str(shows[i].start_time)} for i in range(len(shows))]
  data=[{
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
  }]
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  form = ShowForm()
  count = len(Show.query.all())
  print(count, file=sys.stderr)
  error = False
  body = {}
  try:
    show = Show(artist_id=form.artist_id.data, venue_id=form.venue_id.data,
                  start_time=form.start_time.data)
    print('Show form created.', file=sys.stderr)
    print(show, file=sys.stderr)
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
