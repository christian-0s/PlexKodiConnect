#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
import os
import sys
import re
import platform

import xbmc
from xbmcaddon import Addon

from . import path_ops

# Paths are in unicode, otherwise Windows will throw fits
# For any file operations with KODI function, use encoded strings!


def try_decode(string, encoding='utf-8'):
    """
    Will try to decode string (encoded) using encoding. This possibly
    fails with e.g. Android TV's Python, which does not accept arguments for
    string.encode()
    """
    if isinstance(string, unicode):
        # already decoded
        return string
    try:
        string = string.decode(encoding, "ignore")
    except TypeError:
        string = string.decode()
    return string


# Percent of playback progress for watching item as partially watched. Anything
# more and item will NOT be marked as partially, but fully watched
MARK_PLAYED_AT = 0.9
# How many seconds of playback do we ignore before marking an item as partially
# watched?
IGNORE_SECONDS_AT_START = 60

_ADDON = Addon()
ADDON_NAME = 'PlexKodiConnect'
ADDON_ID = 'plugin.video.plexkodiconnect'
ADDON_VERSION = _ADDON.getAddonInfo('version')
ADDON_PATH = try_decode(_ADDON.getAddonInfo('path'))
ADDON_FOLDER = try_decode(xbmc.translatePath('special://home'))
ADDON_PROFILE = try_decode(xbmc.translatePath(_ADDON.getAddonInfo('profile')))

KODILANGUAGE = xbmc.getLanguage(xbmc.ISO_639_1)
KODIVERSION = int(xbmc.getInfoLabel("System.BuildVersion")[:2])
KODILONGVERSION = xbmc.getInfoLabel('System.BuildVersion')
KODI_PROFILE = try_decode(xbmc.translatePath("special://profile"))

if xbmc.getCondVisibility('system.platform.osx'):
    DEVICE = "MacOSX"
elif xbmc.getCondVisibility("system.platform.uwp"):
    DEVICE = "Microsoft UWP"
elif xbmc.getCondVisibility('system.platform.atv2'):
    DEVICE = "AppleTV2"
elif xbmc.getCondVisibility('system.platform.ios'):
    DEVICE = "iOS"
elif xbmc.getCondVisibility('system.platform.windows'):
    DEVICE = "Windows"
elif xbmc.getCondVisibility('system.platform.raspberrypi'):
    DEVICE = "RaspberryPi"
elif xbmc.getCondVisibility('system.platform.linux'):
    DEVICE = "Linux"
elif xbmc.getCondVisibility('system.platform.android'):
    DEVICE = "Android"
else:
    DEVICE = "Unknown"

MODEL = platform.release() or 'Unknown'
# Plex' own platform for e.g. Plex Media Player
PLATFORM = 'Konvergo'
PLATFORM_VERSION = '2.26.0.947-1e21fa2b'

DEVICENAME = try_decode(_ADDON.getSetting('deviceName'))
if not DEVICENAME:
    DEVICENAME = try_decode(xbmc.getInfoLabel('System.FriendlyName'))
    _ADDON.setSetting('deviceName', DEVICENAME)
DEVICENAME = DEVICENAME.replace(":", "")
DEVICENAME = DEVICENAME.replace("/", "-")
DEVICENAME = DEVICENAME.replace("\\", "-")
DEVICENAME = DEVICENAME.replace("<", "")
DEVICENAME = DEVICENAME.replace(">", "")
DEVICENAME = DEVICENAME.replace("*", "")
DEVICENAME = DEVICENAME.replace("?", "")
DEVICENAME = DEVICENAME.replace('|', "")
DEVICENAME = DEVICENAME.replace('(', "")
DEVICENAME = DEVICENAME.replace(')', "")
DEVICENAME = DEVICENAME.replace(' ', "")

COMPANION_PORT = int(_ADDON.getSetting('companionPort'))

# Unique ID for this Plex client; also see clientinfo.py
PKC_MACHINE_IDENTIFIER = None

# Minimal PKC version needed for the Kodi database - otherwise need to recreate
MIN_DB_VERSION = '2.6.6'

# Supported databases
SUPPORTED_VIDEO_DB = {
    # Kodi 17 Krypton:
    17: {
        107: 107,
    },
    # Kodi 18 Leia:
    18: {
        113: 113,
        116: 116
    },
    # Kodi 19 - EXTREMLY EXPERIMENTAL!
    19: {
        113: 113,
        116: 116
    }
}
SUPPORTED_MUSIC_DB = {
    # Kodi 17 Krypton:
    17: {
        60: 60,
    },
    # Kodi 18 Leia:
    18: {
        72: 72,
    },
    # Kodi 19 - EXTREMLY EXPERIMENTAL!
    19: {
        72: 72,
    }
}
SUPPORTED_TEXTURE_DB = {
    # Kodi 17 Krypton:
    17: {
        13: 13,
    },
    # Kodi 18 Leia:
    18: {
        13: 13,
    },
    # Kodi 19 - EXTREMLY EXPERIMENTAL!
    19: {
        13: 13,
    }
}
DB_VIDEO_VERSION = None
DB_VIDEO_PATH = None
DB_MUSIC_VERSION = None
DB_MUSIC_PATH = None
DB_TEXTURE_VERSION = None
DB_TEXTURE_PATH = None
DB_PLEX_PATH = try_decode(xbmc.translatePath("special://database/plex.db"))

EXTERNAL_SUBTITLE_TEMP_PATH = try_decode(xbmc.translatePath(
    "special://profile/addon_data/%s/temp/" % ADDON_ID))


# Multiply Plex time by this factor to receive Kodi time
PLEX_TO_KODI_TIMEFACTOR = 1.0 / 1000.0

# Playlist stuff
PLAYLIST_PATH = os.path.join(KODI_PROFILE, 'playlists')
PLAYLIST_PATH_MIXED = os.path.join(PLAYLIST_PATH, 'mixed')
PLAYLIST_PATH_VIDEO = os.path.join(PLAYLIST_PATH, 'video')
PLAYLIST_PATH_MUSIC = os.path.join(PLAYLIST_PATH, 'music')

PLEX_TYPE_AUDIO_PLAYLIST = 'audio'
PLEX_TYPE_VIDEO_PLAYLIST = 'video'
PLEX_TYPE_PHOTO_PLAYLIST = 'photo'
KODI_TYPE_AUDIO_PLAYLIST = 'music'
KODI_TYPE_VIDEO_PLAYLIST = 'video'
KODI_TYPE_PHOTO_PLAYLIST = None  # Not supported yet
KODI_PLAYLIST_TYPE_FROM_PLEX = {
    PLEX_TYPE_AUDIO_PLAYLIST: KODI_TYPE_AUDIO_PLAYLIST,
    PLEX_TYPE_VIDEO_PLAYLIST: KODI_TYPE_VIDEO_PLAYLIST
}
PLEX_PLAYLIST_TYPE_FROM_KODI = {
    KODI_TYPE_AUDIO_PLAYLIST: PLEX_TYPE_AUDIO_PLAYLIST,
    KODI_TYPE_VIDEO_PLAYLIST: PLEX_TYPE_VIDEO_PLAYLIST
}


# All the Plex types as communicated in the PMS xml replies
PLEX_TYPE_VIDEO = 'video'
PLEX_TYPE_MOVIE = 'movie'
PLEX_TYPE_CLIP = 'clip'  # e.g. trailers
PLEX_TYPE_SET = 'collection'  # sets/collections
PLEX_TYPE_MIXED = 'mixed'

PLEX_TYPE_EPISODE = 'episode'
PLEX_TYPE_SEASON = 'season'
PLEX_TYPE_SHOW = 'show'

PLEX_TYPE_AUDIO = 'music'
PLEX_TYPE_SONG = 'track'
PLEX_TYPE_ALBUM = 'album'
PLEX_TYPE_ARTIST = 'artist'
PLEX_TYPE_MUSICVIDEO = 'musicvideo'

PLEX_TYPE_PHOTO = 'photo'

# Used for /:/timeline XML messages
PLEX_PLAYLIST_TYPE_VIDEO = 'video'
PLEX_PLAYLIST_TYPE_AUDIO = 'music'
PLEX_PLAYLIST_TYPE_PHOTO = 'photo'

KODI_PLAYLIST_TYPE_VIDEO = 'video'
KODI_PLAYLIST_TYPE_AUDIO = 'audio'
KODI_PLAYLIST_TYPE_PHOTO = 'picture'

KODI_PLAYLIST_TYPE_FROM_PLEX_PLAYLIST_TYPE = {
    PLEX_PLAYLIST_TYPE_VIDEO: KODI_PLAYLIST_TYPE_VIDEO,
    PLEX_PLAYLIST_TYPE_AUDIO: KODI_PLAYLIST_TYPE_AUDIO,
    PLEX_PLAYLIST_TYPE_PHOTO: KODI_PLAYLIST_TYPE_PHOTO
}

# All the Kodi types as e.g. used in the JSON API
KODI_TYPE_VIDEO = 'video'
KODI_TYPE_MOVIE = 'movie'
KODI_TYPE_SET = 'set'  # for movie sets of several movies
KODI_TYPE_CLIP = 'clip'  # e.g. trailers

KODI_TYPE_EPISODE = 'episode'
KODI_TYPE_SEASON = 'season'
KODI_TYPE_SHOW = 'tvshow'

KODI_TYPE_AUDIO = 'audio'
KODI_TYPE_SONG = 'song'
KODI_TYPE_ALBUM = 'album'
KODI_TYPE_ARTIST = 'artist'
KODI_TYPE_MUSICVIDEO = 'musicvideo'

KODI_TYPE_PHOTO = 'photo'

KODI_VIDEOTYPES = (
    KODI_TYPE_VIDEO,
    KODI_TYPE_MOVIE,
    KODI_TYPE_SHOW,
    KODI_TYPE_SEASON,
    KODI_TYPE_EPISODE,
    KODI_TYPE_SET,
    KODI_TYPE_CLIP
)

PLEX_VIDEOTYPES = (
    PLEX_TYPE_VIDEO,
    PLEX_TYPE_MOVIE,
    PLEX_TYPE_SHOW,
    PLEX_TYPE_SEASON,
    PLEX_TYPE_EPISODE,
    PLEX_TYPE_SET,
    PLEX_TYPE_CLIP,
    PLEX_TYPE_MIXED,  # MIXED SEEMS TO ALWAYS REFER TO VIDEO!
)

KODI_AUDIOTYPES = (
    KODI_TYPE_SONG,
    KODI_TYPE_ALBUM,
    KODI_TYPE_ARTIST,
)

PLEX_AUDIOTYPES = (
    PLEX_TYPE_SONG,
    PLEX_TYPE_ALBUM,
    PLEX_TYPE_ARTIST,
)

# Translation tables

ADDON_TYPE = {
    PLEX_TYPE_MOVIE: 'plugin.video.plexkodiconnect.movies',
    PLEX_TYPE_CLIP: 'plugin.video.plexkodiconnect.movies',
    PLEX_TYPE_EPISODE: 'plugin.video.plexkodiconnect.tvshows',
    PLEX_TYPE_SONG: 'plugin.video.plexkodiconnect'
}

ITEMTYPE_FROM_PLEXTYPE = {
    PLEX_TYPE_MOVIE: 'Movies',
    PLEX_TYPE_SEASON: 'TVShows',
    KODI_TYPE_EPISODE: 'TVShows',
    PLEX_TYPE_SHOW: 'TVShows',
    PLEX_TYPE_ARTIST: 'Music',
    PLEX_TYPE_ALBUM: 'Music',
    PLEX_TYPE_SONG: 'Music',
}

ITEMTYPE_FROM_KODITYPE = {
    KODI_TYPE_MOVIE: 'Movies',
    KODI_TYPE_SEASON: 'TVShows',
    KODI_TYPE_EPISODE: 'TVShows',
    KODI_TYPE_SHOW: 'TVShows',
    KODI_TYPE_ARTIST: 'Music',
    KODI_TYPE_ALBUM: 'Music',
    KODI_TYPE_SONG: 'Music',
}

KODITYPE_FROM_PLEXTYPE = {
    PLEX_TYPE_MOVIE: KODI_TYPE_MOVIE,
    PLEX_TYPE_EPISODE: KODI_TYPE_EPISODE,
    PLEX_TYPE_SEASON: KODI_TYPE_SEASON,
    PLEX_TYPE_SHOW: KODI_TYPE_SHOW,
    PLEX_TYPE_SONG: KODI_TYPE_SONG,
    PLEX_TYPE_ARTIST: KODI_TYPE_ARTIST,
    PLEX_TYPE_ALBUM: KODI_TYPE_ALBUM,
    PLEX_TYPE_PHOTO: KODI_TYPE_PHOTO,
    'XXXXXX': 'musicvideo',
    'XXXXXXX': 'genre'
}

PLEX_TYPE_FROM_KODI_TYPE = {
    KODI_TYPE_VIDEO: PLEX_TYPE_VIDEO,
    KODI_TYPE_MOVIE: PLEX_TYPE_MOVIE,
    KODI_TYPE_SET: PLEX_TYPE_SET,
    KODI_TYPE_EPISODE: PLEX_TYPE_EPISODE,
    KODI_TYPE_SEASON: PLEX_TYPE_SEASON,
    KODI_TYPE_SHOW: PLEX_TYPE_SHOW,
    KODI_TYPE_CLIP: PLEX_TYPE_CLIP,
    KODI_TYPE_ARTIST: PLEX_TYPE_ARTIST,
    KODI_TYPE_ALBUM: PLEX_TYPE_ALBUM,
    KODI_TYPE_SONG: PLEX_TYPE_SONG,
    KODI_TYPE_AUDIO: PLEX_TYPE_AUDIO,
    KODI_TYPE_PHOTO: PLEX_TYPE_PHOTO
}

KODI_PLAYLIST_TYPE_FROM_PLEX_TYPE = {
    PLEX_TYPE_VIDEO: KODI_TYPE_VIDEO,
    PLEX_TYPE_MOVIE: KODI_TYPE_VIDEO,
    PLEX_TYPE_EPISODE: KODI_TYPE_VIDEO,
    PLEX_TYPE_SEASON: KODI_TYPE_VIDEO,
    PLEX_TYPE_SHOW: KODI_TYPE_VIDEO,
    PLEX_TYPE_CLIP: KODI_TYPE_VIDEO,
    PLEX_TYPE_ARTIST: KODI_TYPE_AUDIO,
    PLEX_TYPE_ALBUM: KODI_TYPE_AUDIO,
    PLEX_TYPE_SONG: KODI_TYPE_AUDIO,
    PLEX_TYPE_AUDIO: KODI_TYPE_AUDIO,
    PLEX_TYPE_PHOTO: KODI_TYPE_PHOTO
}


KODI_PLAYLIST_TYPE_FROM_KODI_TYPE = {
    KODI_TYPE_VIDEO: KODI_TYPE_VIDEO,
    KODI_TYPE_MOVIE: KODI_TYPE_VIDEO,
    KODI_TYPE_EPISODE: KODI_TYPE_VIDEO,
    KODI_TYPE_SEASON: KODI_TYPE_VIDEO,
    KODI_TYPE_SHOW: KODI_TYPE_VIDEO,
    KODI_TYPE_CLIP: KODI_TYPE_VIDEO,
    KODI_TYPE_ARTIST: KODI_TYPE_AUDIO,
    KODI_TYPE_ALBUM: KODI_TYPE_AUDIO,
    KODI_TYPE_SONG: KODI_TYPE_AUDIO,
    KODI_TYPE_AUDIO: KODI_TYPE_AUDIO,
    KODI_TYPE_PHOTO: KODI_TYPE_PHOTO
}

REMAP_TYPE_FROM_PLEXTYPE = {
    PLEX_TYPE_MOVIE: 'movie',
    PLEX_TYPE_CLIP: 'clip',
    PLEX_TYPE_SHOW: 'tv',
    PLEX_TYPE_SEASON: 'tv',
    PLEX_TYPE_EPISODE: 'tv',
    PLEX_TYPE_ARTIST: 'music',
    PLEX_TYPE_ALBUM: 'music',
    PLEX_TYPE_SONG: 'music',
    PLEX_TYPE_PHOTO: 'photo'
}


TRANSLATION_FROM_PLEXTYPE = {
    PLEX_TYPE_MOVIE: 342,
    PLEX_TYPE_EPISODE: 20360,
    PLEX_TYPE_SEASON: 20373,
    PLEX_TYPE_SHOW: 20343,
    PLEX_TYPE_SONG: 134,
    PLEX_TYPE_ARTIST: 133,
    PLEX_TYPE_ALBUM: 132,
    PLEX_TYPE_PHOTO: 1,
}

REMAP_TYPE_FROM_PLEXTYPE = {
    'movie': 'movie',
    'show': 'tv',
    'season': 'tv',
    'episode': 'tv',
    'artist': 'music',
    'album': 'music',
    'song': 'music',
    'track': 'music',
    'clip': 'clip',
    'photo': 'photo'
}


PLEX_TYPE_FROM_WEBSOCKET = {
    1: PLEX_TYPE_MOVIE,
    2: PLEX_TYPE_SHOW,
    3: PLEX_TYPE_SEASON,
    4: PLEX_TYPE_EPISODE,
    8: PLEX_TYPE_ARTIST,
    9: PLEX_TYPE_ALBUM,
    10: PLEX_TYPE_SONG,
    12: PLEX_TYPE_CLIP,
    15: 'playlist',
    18: PLEX_TYPE_SET
}

PLEX_TYPE_NUMBER_FROM_PLEX_TYPE = {
    PLEX_TYPE_MOVIE: 1,
    PLEX_TYPE_SHOW: 2,
    PLEX_TYPE_SEASON: 3,
    PLEX_TYPE_EPISODE: 4,
    PLEX_TYPE_ARTIST: 8,
    PLEX_TYPE_ALBUM: 9,
    PLEX_TYPE_SONG: 10,
    PLEX_TYPE_CLIP: 12,
    'playlist': 15,
    PLEX_TYPE_SET: 18
}


KODI_TO_PLEX_ARTWORK = {
    'poster': 'thumb',
    'banner': 'banner',
    'fanart': 'art'
}

KODI_TO_PLEX_ARTWORK_EPISODE = {
    'thumb': 'thumb',
    'poster': 'grandparentThumb',
    'banner': 'banner',
    'fanart': 'art'
}

# Might be implemented in the future: 'icon', 'landscape' (16:9)
ALL_KODI_ARTWORK = (
    'thumb',
    'poster',
    'banner',
    'clearart',
    'clearlogo',
    'fanart',
    'discart'
)

# we need to use a little mapping between fanart.tv arttypes and kodi artttypes
FANART_TV_TO_KODI_TYPE = [
    ('poster', 'poster'),
    ('logo', 'clearlogo'),
    ('musiclogo', 'clearlogo'),
    ('disc', 'discart'),
    ('clearart', 'clearart'),
    ('banner', 'banner'),
    ('clearlogo', 'clearlogo'),
    ('background', 'fanart'),
    ('showbackground', 'fanart'),
    ('characterart', 'characterart')
]
# How many different backgrounds do we want to load from fanart.tv?
MAX_BACKGROUND_COUNT = 10


# extensions from:
# http://kodi.wiki/view/Features_and_supported_codecs#Format_support (RAW image
# formats, BMP, JPEG, GIF, PNG, TIFF, MNG, ICO, PCX and Targa/TGA)
KODI_SUPPORTED_IMAGES = (
    '.bmp',
    '.jpg',
    '.jpeg',
    '.gif',
    '.png',
    '.tiff',
    '.mng',
    '.ico',
    '.pcx',
    '.tga'
)


# Translation table from Alexa websocket commands to Plex Companion
ALEXA_TO_COMPANION = {
    'queryKey': 'key',
    'queryOffset': 'offset',
    'queryMachineIdentifier': 'machineIdentifier',
    'queryProtocol': 'protocol',
    'queryAddress': 'address',
    'queryPort': 'port',
    'queryContainerKey': 'containerKey',
    'queryToken': 'token',
}

# Kodi sort methods for xbmcplugin.addSortMethod()
SORT_METHODS_DIRECTORY = (
    'SORT_METHOD_UNSORTED',  # sorted as returned from Plex
    'SORT_METHOD_LABEL',
)

SORT_METHODS_PHOTOS = (
    'SORT_METHOD_UNSORTED',
    'SORT_METHOD_LABEL',
    'SORT_METHOD_DATE',
    'SORT_METHOD_DATEADDED',
)

SORT_METHODS_CLIPS = (
    'SORT_METHOD_UNSORTED',
    'SORT_METHOD_TITLE',
    'SORT_METHOD_DURATION',
)

SORT_METHODS_MOVIES = (
    'SORT_METHOD_UNSORTED',
    'SORT_METHOD_TITLE',
    'SORT_METHOD_DATEADDED',
    'SORT_METHOD_GENRE',
    'SORT_METHOD_VIDEO_RATING',
    'SORT_METHOD_VIDEO_USER_RATING',
    'SORT_METHOD_MPAA_RATING',
    'SORT_METHOD_DURATION',
    'SORT_METHOD_COUNTRY',
    'SORT_METHOD_STUDIO',
)

SORT_METHOD_TVSHOWS = (
    'SORT_METHOD_UNSORTED',
    'SORT_METHOD_TITLE',
    'SORT_METHOD_DATEADDED',
    'SORT_METHOD_VIDEO_RATING',
    'SORT_METHOD_VIDEO_USER_RATING',
    'SORT_METHOD_MPAA_RATING',
    'SORT_METHOD_COUNTRY',
    'SORT_METHOD_GENRE',
)

SORT_METHODS_EPISODES = (
    'SORT_METHOD_UNSORTED',
    'SORT_METHOD_TITLE',
    'SORT_METHOD_EPISODE',
    'SORT_METHOD_DATEADDED',
    'SORT_METHOD_VIDEO_RATING',
    'SORT_METHOD_VIDEO_USER_RATING',
    'SORT_METHOD_MPAA_RATING',
    'SORT_METHOD_DURATION',
    'SORT_METHOD_FILE',
    'SORT_METHOD_FULLPATH',
)

SORT_METHODS_SONGS = (
    'SORT_METHOD_UNSORTED',
    'SORT_METHOD_TITLE',
    'SORT_METHOD_TRACKNUM',
    'SORT_METHOD_DURATION',
    'SORT_METHOD_ARTIST',
    'SORT_METHOD_ALBUM',
    'SORT_METHOD_SONG_RATING',
    'SORT_METHOD_SONG_USER_RATING'
)

SORT_METHODS_ARTISTS = (
    'SORT_METHOD_UNSORTED',
    'SORT_METHOD_TITLE',
    'SORT_METHOD_TRACKNUM',
    'SORT_METHOD_DURATION',
    'SORT_METHOD_ARTIST',
    'SORT_METHOD_ALBUM',
)

SORT_METHODS_ALBUMS = (
    'SORT_METHOD_UNSORTED',
    'SORT_METHOD_TITLE',
    'SORT_METHOD_TRACKNUM',
    'SORT_METHOD_DURATION',
    'SORT_METHOD_ARTIST',
    'SORT_METHOD_ALBUM',
)


XML_HEADER = '<?xml version="1.0" encoding="UTF-8"?>\n'

COMPANION_OK_MESSAGE = XML_HEADER + '<Response code="200" status="OK" />'

PLEX_REPEAT_FROM_KODI_REPEAT = {
    'off': '0',
    'one': '1',
    'all': '2'   # does this work?!?
}

# Stream in PMS xml contains a streamType to distinguish the kind of stream
PLEX_STREAM_TYPE_FROM_STREAM_TYPE = {
    'video': '1',
    'audio': '2',
    'subtitle': '3'
}


def database_paths():
    '''
    Set the Kodi database paths. Will raise a RuntimeError if the DBs are
    not found or of a wrong, unsupported version
    '''
    global DB_VIDEO_VERSION, DB_VIDEO_PATH
    global DB_MUSIC_VERSION, DB_MUSIC_PATH
    global DB_TEXTURE_VERSION, DB_TEXTURE_PATH
    database_path = try_decode(xbmc.translatePath('special://database'))
    video_versions = []
    music_versions = []
    texture_versions = []
    types = (
        (re.compile(r'''MyVideos(\d+).db'''), video_versions),
        (re.compile(r'''MyMusic(\d+).db'''), music_versions),
        (re.compile(r'''Textures(\d+).db'''), texture_versions)
    )
    for root, _, files in path_ops.walk(database_path):
        for file in files:
            for typus in types:
                match = typus[0].search(path_ops.path.join(root, file))
                if not match:
                    continue
                typus[1].append(int(match.group(1)))
    try:
        DB_VIDEO_VERSION = max(video_versions)
        SUPPORTED_VIDEO_DB[KODIVERSION][DB_VIDEO_VERSION]
        DB_VIDEO_PATH = path_ops.path.join(database_path,
                                           'MyVideos%s.db' % DB_VIDEO_VERSION)
    except (ValueError, KeyError):
        raise RuntimeError('Video DB %s not supported'
                           % DB_VIDEO_VERSION)
    try:
        DB_MUSIC_VERSION = max(music_versions)
        SUPPORTED_MUSIC_DB[KODIVERSION][DB_MUSIC_VERSION]
        DB_MUSIC_PATH = path_ops.path.join(database_path,
                                           'MyMusic%s.db' % DB_MUSIC_VERSION)
    except (ValueError, KeyError):
        raise RuntimeError('Music DB %s not supported'
                           % DB_MUSIC_VERSION)
    try:
        DB_TEXTURE_VERSION = max(texture_versions)
        SUPPORTED_TEXTURE_DB[KODIVERSION][DB_TEXTURE_VERSION]
        DB_TEXTURE_PATH = path_ops.path.join(database_path,
                                             'Textures%s.db' % DB_TEXTURE_VERSION)
    except (ValueError, KeyError):
        raise RuntimeError('Texture DB %s not supported'
                           % DB_TEXTURE_VERSION)


# Encoding to be used for our m3u playlist files
# m3u files do not have encoding specified by definition, unfortunately.
if DEVICE == 'Windows':
    M3U_ENCODING = 'mbcs'
else:
    M3U_ENCODING = sys.getfilesystemencoding()
    if (not M3U_ENCODING or
            M3U_ENCODING == 'ascii' or
            M3U_ENCODING == 'ANSI_X3.4-1968'):
        M3U_ENCODING = 'utf-8'
