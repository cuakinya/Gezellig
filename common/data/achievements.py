# Club achievements (badges that moderators can give to members via godmode).
#
# The list is empty on purpose: the achievements of the original club were tied to its own events and images.
# To add your own, append items of this format (order matters, it is used as the display index):
#
#     ("unique_code", {
#         "name": "Achievement name",
#         "description": "Short description of what it is given for",
#         "image": "/static/images/achievements/unique_code.png",  # any URL or a file in frontend/static
#         "style": "color: #FFF; background-color: #65C3BA;",  # optional CSS for the badge
#     }),
#
# Then run `python manage.py update_achievements` to sync the list with the database.
# NOTE: the command deletes achievements (and their awards to users) whose code is not in this list.
ACHIEVEMENTS = []
