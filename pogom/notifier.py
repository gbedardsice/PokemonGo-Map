import json
import logging
from pushbullet import Pushbullet
from datetime import datetime
from . import config
import sys

log = logging.getLogger(__name__)

# Fixes the encoding of the male/female symbol
reload(sys)
sys.setdefaultencoding('utf8')

pushbullet_client = None
wanted_pokemon = None

# Initialize object
def init_notifier():
    global pushbullet_client, wanted_pokemon
    if config['PUSHBULLET_KEY']: pushbullet_client = Pushbullet(config['PUSHBULLET_KEY'])
    if config['WANTED_POKEMONS']:
        wanted_pokemon = config['WANTED_POKEMONS'].split(",")
        wanted_pokemon = [a.lower() for a in wanted_pokemon]

# Safely parse incoming strings to unicode
def _str(s):
  return s.encode('utf-8').strip()

# Notify user for discovered Pokemon
def pokemon_found(pokemon):
    pokename = _str(pokemon["pokemon_name"]).lower()
    if not pushbullet_client or not pokename in wanted_pokemon: return
    log.info("Notifier found wanted pokemon: {}".format(pokename))

    #http://maps.google.com/maps/place/<place_lat>,<place_long>/@<map_center_lat>,<map_center_long>,<zoom_level>z
    latLon = '{},{}'.format(repr(pokemon["latitude"]), repr(pokemon["longitude"]))
    google_maps_link = 'http://maps.google.com/maps/place/{}/@{},{}z'.format(latLon, latLon, 20)

    notification_text = "Pokemon Finder found " + _str(pokemon["pokemon_name"]) + "!"
    disappear_time = str(pokemon["disappear_time"].strftime("%I:%M%p").lstrip('0'))+")"
    location_text = "Locate on Google Maps : " + google_maps_link + ". " + _str(pokemon["pokemon_name"]) + " will be available until " + disappear_time + "."

    push = pushbullet_client.push_link(notification_text, google_maps_link, body=location_text)
