# -*- coding: utf-8 -*-
#
#   SPDX-License-Identifier: ISC
#
#   Copyright (C) 2019 rsiddharth <s@ricketyspace.net>
#
#   This file is part of nfsw.
#

import os.path
import subprocess

from flask import current_app, g, session

from nfsw.redis import redis
from nfsw.util import read_junk


def get_scene(name):
    scenes = {
        'sexshop': sexshop,
        'garden': garden,
        'nymphomaniac': nymphomaniac,
        'coitus': coitus,
        'strayed': strayed,
        'xkcd': xkcd,
        'bedroom': bedroom,
        'thanks': thanks
    }

    return scenes.get(name, None)


def current_scene():
    r = redis()

    return get_scene(
        r.get('scene').decode()
    )


def sexshop(o):
    r = redis()

    gobbledygook = [
        'I just got raped in the'
        '\narse by 9238 sentinels.'
        '\nPlease don\'t fuck with me like that'
        '\n\nIt\'s easy.'
        ]


    def rj(name):
        return read_junk('sexshop/{}'.format(name))


    def gg():
        l = len(gobbledygook)

        for i in range(0, l):
            if r.sismember('scene:sexshop:gg', i):
                continue

            r.sadd('scene:sexshop:gg', i)
            return gobbledygook[i]

        return 'I\'m outta words.'


    def intro():
        return rj('intro')


    def p_done(q):
        if r.sismember('scenes:done', 'sexshop'):
            return rj('done')

        # Set player type.
        type = '{}{}'.format(r.get('player:type:body').decode(),
                             r.get('player:type:mind').decode())
        r.set('player:type', type)

        # Mark scene done
        r.sadd('scenes:done', 'sexshop')

        # Move to next scene
        r.set('scene', 'garden')

        return garden({'intro': 1})


    def p_body(q):
        if 'female' in q:
            r.set('player:type:body', 'f')

            return '\n\n'.join([
                rj('body-f-done'),
                rj('mind-q')
            ])

        if 'male' in q:
            r.set('player:type:body', 'm')

            return '\n\n'.join([
                rj('body-m-done'),
                rj('mind-q')
            ])

        return '\n'.join([gg(), rj('body-q')])


    def p_mind(q):
        if 'women' in q:
            r.set('player:type:mind', 'w')

            return '\n\n'.join([
                rj('mind-f-done'),
                p_done(q)
            ])

        if 'men' in q:
            r.set('player:type:mind', 'm')

            return '\n\n'.join([
                rj('mind-m-done'),
                p_done(q)
            ])

        return '\n'.join([gg(), rj('mind-q')])


    def p(q):
        if r.exists('player:type'):
            return p_done(q)

        if not r.exists('player:type:body'):
            return p_body(q)

        if not r.exists('player:type:mind'):
            return p_mind(q)

        return p_done(q)


    if 'intro' in o:
        return intro()

    if 'q' in o:
        return p(o['q'])


def garden(o):
    r = redis()

    gobbledygook = [
        'You\'re such a hot mess.'
        '\nCome on, talk some sense.',
        'The tulips in the garden'
        '\nget fucked by bees everyday'
        '\nYou can too.',
        'There is nothing much you can'
        '\ndo in the garden.'
        '\nYou do see the building right?'
        '\nThe building\'s door looks open'
        '\nto me',
        'I get bit by mosquitos all the time'
        '\nin this garden at night.'
        '\nYou\'re the last thing I want here'
        '\nCan you please figure a way'
        '\nto get the fuck outta here?'
    ]


    def rj(name):
        return read_junk('garden/{}'.format(name))


    def gg():
        l = len(gobbledygook)

        for i in range(0, l):
            if r.sismember('scene:garden:gg', i):
                continue

            r.sadd('scene:garden:gg', i)
            return gobbledygook[i]

        return '\n'.join(['Your concierge is busy sucking',
                          'his dog\'s gonads.',
                          'It\'s gonna take forever.',
                          'He is unable to answer at this moment'])


    def intro():
        return rj('intro')


    def verb_in(q):
        if 'go' in q:
            return True

        if 'enter' in q:
            return True

        return False


    def object_in(q):
        if 'building' in q:
            return True

        return False


    def p_done(q):
        # Mark scene done
        r.sadd('scenes:done', 'garden')

        # Move to next scene
        r.set('scene', 'nymphomaniac')

        return  '\n\n'.join([
            rj('to-the-building'),
            nymphomaniac({'intro': 1})
        ])


    def p(q):

        if verb_in(q) and object_in(q):
            return p_done(q)

        return gg()


    if 'intro' in o:
        return rj('intro')

    if 'q' in o:
        return p(o['q'])


def nymphomaniac(o):
    r =  redis()

    gobbledygook = [
        'I don\'t have time for your gobbledygook'
        '\nCan we just focus on your fucking task'
        '\nplease.',
        'Blood starts trickling from the corners'
        '\nof the big screen',
        'You feel your gonads spurt and blot'
        '\nyour underwear. You sample it with your'
        '\nindex finger, smell it and lick it.'
        '\nIt\'s blood.'
    ]
    gobbledygook_hunk = [
        'Can\'t do nothin\' with hunk.'
        '\nBetter luck next time',
        'Next time you try to do anything with the hunk'
        '\nI\'m going to force you to eat his dingle berries.',
        'Stop your infatuation with the hunk.'
        '\nForget his dingle berries.'
        '\nEven better.'
        '\nI might be forced to feed you the skinned'
        '\ncat for lunch today, if you persist.'
    ]

    def rj(name):
        return read_junk('nymphomaniac/{}'.format(name))


    def gg_hunk():
        l = len(gobbledygook_hunk)

        for i in range(0, l):
            if r.sismember('scene:nymphomaniac:gg-hunk', i):
                continue

            r.sadd('scene:nymphomaniac:gg-hunk', i)
            return gobbledygook_hunk[i]

        return '\n'.join([
        'An invisible hand forces your mouth open.',
        'A squishy chunk of the skinned cat\'s',
        'fried meat forces it\'s way through your',
        'mouth, to your esophagus and into your stomach.'
        ])


    def gg():
        l = len(gobbledygook)

        for i in range(0, l):
            if r.sismember('scene:nymphomaniac:gg', i):
                continue

            r.sadd('scene:nymphomaniac:gg', i)
            return gobbledygook[i]

        return '\n'.join(['For fuck sake answer the question.'])


    def hunk_in(q):
        if 'hunk' in q:
            return True

        if 'water' in q and 'fountain' in q:
            return True

        return False


    def ans_in(q):
        if 'leaked' in q:
            return True

        if 'vaginal' in q and 'fluid' in q:
            return True

        return False


    def p_done(q):
        # Mark scene done
        r.sadd('scenes:done', 'nymphomaniac')

        # Move to next scene
        r.set('scene', 'coitus')

        return '\n\n'.join([
            rj('door-opens'),
            coitus({'intro': 1})
        ])


    def p(q):
        if hunk_in(q):
            return gg_hunk()

        if ans_in(q):
            return p_done(q)

        return gg()


    if 'intro' in o:
        return rj('intro')


    if 'q' in o:
        return p(o['q'])


def coitus(o):
    r =  redis()

    type = r.get('player:type').decode()
    gobbledygook = [
        'Really?'
        '\nWhen cat Tom sees rat Jerry'
        '\nTom chases Jerry'
        '\nThat\'s basic instinct'
        '\nDon\'t you have one?',
        'Come on'
        '\nA chipmunk would know'
        '\nwhat to do when it sees'
        '\nan attractive partner'
        '\nchipping away at an acorn'
    ]


    def rj(name):
        return read_junk('coitus/{}'.format(name))


    def gg():
        gg_last =  '\n'.join([
            'Your concierge is busy',
            'masturbating. He his unable',
            'to respond to you at the moment'
        ])

        if fucked():
            return gg_last


        l = len(gobbledygook)

        for i in range(0, l):
            if r.sismember('scene:coitus:gg', i):
                continue

            r.sadd('scene:coitus:gg', i)
            return gobbledygook[i]

        return gg_last


    def intro():
        if fucked():
            return rj('mirror-intro')

        return rj('intro-{}'.format(type))


    def colloquial():
        return '\n'.join([
            'Use the colloquial term',
            'Pretty please'
        ])


    def fucked():
        if r.get('scene:coitus:fucked'):
            return True

        return False


    def fuck(q):
        r.set('scene:coitus:fucked', 1)

        return '\n\n'.join([
            rj('fuck-{}'.format(type)),
            rj('mirror-intro')
        ])


    def mirror(q):
        if not r.get('scene:coitus:fucked'):
            return False

        if 'touch' in q and 'mirror' in q:
            return True

        return False


    def p_done(q):
        # Mark scene done
        r.sadd('scenes:done', 'coitus')

        # Move to next scene
        r.set('scene', 'strayed')

        return '\n\n'.join([
            rj('mirror'),
            strayed({'intro': 1})
        ])


    def p(q):
        if mirror(q):
            return p_done(q)

        if not fucked() and 'fuck' in q:
            return fuck(q)

        if not fucked() and ('sex' in q or 'coitus' in q):
            return colloquial()

        return gg()


    if 'intro' in o:
        return intro()


    if 'q' in o:
        return p(o['q'])


def strayed(o):
    r = redis()

    gobbledygook = [
        'You know one of Sugar\'s books was'
        '\nselected for Oprah\'s Book Club 2.0.',
        'Also the book was adapted into a'
        '\nbiographical drama film.',
        'Ok, this is the last one.'
        '\nChuck Palahniuk mentions about Sugar'
        '\nin Joe Rogan\'s podcast.'
    ]

    def rj(name):
        return read_junk('strayed/{}'.format(name))


    def gg():
        l = len(gobbledygook)

        for i in range(0, l):
            if r.sismember('scene:strayed:gg', i):
                continue

            r.sadd('scene:strayed:gg', i)
            return gobbledygook[i]

        return rj('passed-out')


    def p_done():
        # Mark scene done
        r.sadd('scenes:done', 'strayed')

        # Move to next scene
        r.set('scene', 'xkcd')

        return '\n\n'.join([
            rj('into-white'),
            xkcd({'intro': 1})
        ])


    def p(q):
        if 'fuck' in q:
            return rj('fuck')

        if 'masturbate' in q:
            return rj('masturbate')

        if 'cheryl strayed' in q:
            return p_done()

        return gg()


    if 'intro' in o:
        return rj('intro')


    if 'q' in o:
        return p(o['q'])


def xkcd(o):
    r = redis()

    gobbledygook = [
        'A flock of warblers cruise through'
        '\nthe wondrous blue white atmosphere'
        '\nand dwindle out of view to their'
        '\nwinter recluse',
        'You know.'
        '\nRandall Munroe likes oglaf!',
        'It\'s dusk now.'
        '\nThe space around you is'
        '\nin a welter of crimson.'
    ]

    def rj(name):
        return read_junk('xkcd/{}'.format(name))


    def gg():
        l = len(gobbledygook)

        for i in range(0, l):
            if r.sismember('scene:xkcd:gg', i):
                continue

            r.sadd('scene:xkcd:gg', i)
            return gobbledygook[i]

        return 'The space\'s outta words.'


    def p_done():
        # Mark scene done
        r.sadd('scenes:done', 'xkcd')

        # Move to next scene
        r.set('scene', 'bedroom')

        return '\n\n'.join([
            rj('pass-out'),
            bedroom({'intro': 1})
        ])


    def p(q):

        if 'people are complicated' in q:
            return p_done()

        return gg()


    if 'intro' in o:
        return rj('intro')

    if 'q' in o:
        return p(o['q'])


def bedroom(o):
    r = redis()

    def rj(name):
        return read_junk('bedroom/{}'.format(name))


    def cow():
        return os.path.join(
            current_app.root_path,
            'cow/sodomized.cow'
        )


    def wish():
        u = g.user['username']
        return 'merry fucking christmas {}.'.format(u)


    def sodomize():
        r = subprocess.run(
            'cowsay -s -f {} "{}"'.format(cow(), wish()),
            stdout=subprocess.PIPE,
            shell=True,
            universal_newlines=True
        )

        return r.stdout


    # Mark scene done
    r.sadd('scenes:done', 'bedroom')

    # Move to next scene
    r.set('scene', 'thanks')

    return '\n\n'.join([
        rj('merry-christmas'),
        sodomize(),
        thanks({})
    ])


def thanks(o):
    r = redis()

    def stats():
        k = 'players:finished'
        id = session['user_id']

        if r.r.sismember(k, id):
            return ''

        r.r.sadd(k, id)

        place = r.r.scard(k)

        # Record place
        r.set('player:place', place)

        unit = place % 10
        hund = place % 100

        th = 'th'
        if place == 1 or (unit == 1 and hund != 1):
            th = 'st'
        elif unit == 2 and hund != 1:
            th = 'nd'
        elif unit == 3 and hund != 1:
            th = 'rd'

        return '   You\'re the {}{} person to finish this game!'.format(
            place, th
        )

    if r.sismember('scenes:done', 'thanks'):
        return 'You\'ve finished the game!'

    # Mark scene done
    r.sadd('scenes:done', 'thanks')

    return '\n'.join([
        stats(),
        '\n   - Santa'
    ])
