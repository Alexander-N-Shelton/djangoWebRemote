# accounts/predefined_buttons_script.py

from accounts.models import FavoriteButton

predefined_buttons = [
    ('ABC', 'abc.svg', 'CHANNEL', 'A4xi3EdB5pw'),
    ('ACC Network', 'acc.svg', 'CHANNEL', 'UJMlY7gDLGA'),
    ('Apple TV', 'apple-tv.svg', 'APP', 'com.apple.atve.androidtv.appletv/.MainActivity'),
    ('Big Ten Network', 'big-ten.svg', 'CHANNEL', 'D96Obj3W9Lg'),
    ('Disney+', 'disney+.svg', 'APP', 'com.disney.disneyplus'),
    ('ESPN U', 'espn-u.svg', 'CHANNEL', 'EOCZ_C-3EpI'),
    ('ESPN 2', 'espn2.svg', 'CHANNEL', 'u7mmqFmqCOo'),
    ('ESPN News', 'espn-news.svg', 'CHANNEL', '-h1zpPgT3_k'),
    ('Fox News', 'fox-news.svg', 'CHANNEL', 'GchZl-5n8II'),
    ('FOX', 'fox.svg', 'CHANNEL', '_1sCaUoJ4wg'),
    ('Hulu', 'hulu.svg', 'APP', 'com.hulu.livingroomplus'),
    ('NBC', 'nbc.svg', 'CHANNEL', 'A4xi3EdB5pw'),
    ('Netflix', 'netflix.svg', 'APP', 'com.netflix.ninja'),
    ('Prime Video', 'prime.svg', 'APP', 'com.amazon.amazonvideo.livingroom/com.amazon.ignition.IgnitionActivity'),
    ('SEC Network', 'secn.svg', 'CHANNEL', 'OY9o9DWacKQ'),
    ('Starz', 'starz.svg', 'APP', 'com.bydeluxe.d3.android.program.starz'),
    ('TNT', 'tnt.svg', 'CHANNEL', 'COBkkcQP4Io'),
    ('The Weather Channel', 'weather.svg', 'CHANNEL', 'u-jeeHl3yg0'),
    ('YouTube TV', 'youtube-tv.svg', 'APP', 'com.google.android.youtube.tvunplugged'),
    ('CBS', 'cbs.svg', 'CHANNEL', 'n3wTA841J-Y'),
    ('Max', 'hbo.svg', 'APP', 'com.wbd.stream/com.wbd.beam.BeamActivity'),
    ('ESPN', 'espn-e.svg', 'CHANNEL', 'Vml3PzeYi6U'),
    ('Paramount +', 'paramount+.svg', 'APP', 'com.cbs.ott'),
    ('Youtube', 'youTube.svg', 'APP', 'com.google.android.youtube.tv'),
    ('Sling TV', 'sling.svg', 'APP', 'com.sling'),
    ('TBS', 'tbs.svg', 'CHANNEL', 'iv5orcizA28'),
    ('FS1', 'fs1.svg', 'CHANNEL', 'XOeJNpLiVJI'),
    ('truTV', 'truTV.svg', 'CHANNEL', 'UKWfqRHFsqo'),
    ('Golf Channel', 'golf-channel.svg', 'CHANNEL', 'zM1V1rtG_mE'),
    ('CW', 'cw.svg', 'CHANNEL', 'None'),
    ('Peacock', 'peacock.svg', 'APP', 'com.peacocktv.peacockandroid'),
    ('Plex', 'plex.svg', 'APP', 'com.plexapp.android'),
    ('tubi', 'tubi.svg', 'APP', 'com.tubitv'),
    ('Pluto TV', 'pluto-tv.svg', 'APP', 'tv.pluto.android'),
    ('Crunchyroll', 'crunchyroll.svg', 'APP', 'com.crunchyroll.crunchyroid/.main.ui.MainActivity'),
    ('philo TV', 'philo.svg', 'APP', 'com.philo.philo.google'),
    ('fubo TV', 'fubo.svg', 'APP', 'com.fubo.firetv.screen'),
    ('DirecTV Stream', 'direcTV.svg', 'APP', 'com.att.tv/com.clientapp.MainActivity'),
    ('Spotify', 'spotify.svg', 'APP', 'com.spotify.tv.android'),
    ('Youtube Music', 'youtube-music.svg', 'APP', 'com.google.android.youtube.tvmusic')
]

for name, svg_path, target, target_type in predefined_buttons:
    FavoriteButton.objects.get_or_create(
        name=name, 
        defaults={
            "svg_path": svg_path, 
            "target": target, 
            "target_type": target_type
        }
    )