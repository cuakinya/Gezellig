# FEATURE-FLAGS
# Use them to enable/disable different functions
# We recommend to create new feature-flags if you want to add new features or disable existing ones in your fork
# That way you can add them to the upstream (the original open-source club engine, see README) for better sync in the future

# Hide posts feed (main page) from unauthorized users
#   True — feed is only visible to club members, other users will be redirected to landing page
#   False — everyone can view the feed, it becomes the main page
PRIVATE_FEED = True

# Enable auth and payment via Patreon
#   See settings.py for more configs (PATREON_ - prefixed)
PATREON_AUTH_ENABLED = False

# Show the people map (Mapbox) on /people/ and the map point picker in the profile editor
#   True — map is shown, requires MAPBOX_TOKEN (see settings.py)
#   False — map is hidden, /people/ shows only the search and the list of members;
#           saved coordinates of users and map messages stay in the database untouched
PEOPLE_MAP_ENABLED = False
