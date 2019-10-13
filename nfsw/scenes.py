from nfsw.redis import redis
from nfsw.util import read_junk


def get_scene(name):
    scenes = {
        'sexshop': sexshop,
        'garden': garden,
        'nymphomaniac': nymphomaniac
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
        '\nI\'m going to force you to eat his dingle berries',
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
        l = len(gobbledygook)

        for i in range(0, l):
            if r.sismember('scene:coitus:gg', i):
                continue

            r.sadd('scene:coitus:gg', i)
            return gobbledygook[i]

        return '\n'.join([
            'Your concierge is busy',
            'masturbating. He his unable',
            'to respond to you at the moment'
        ])


    def intro():
        return rj('intro-{}'.format(type))


    def colloquial():
        return '\n'.join([
            'Use the colloquial term',
            'Pretty please'
        ])


    def p_done(q):
        # Mark scene done
        r.sadd('scenes:done', 'coitus')

        # Move to next scene
        r.set('scene', 'strayed')

        return '\n\n'.join([
            rj('fuck-{}'.format(type[1])),
            strayed({'intro': 1})
        ])


    def p(q):

        if 'fuck' in q:
            return p_done(q)

        if 'sex' in q or 'coitus' in q:
            return colloquial()

        return gg()


    if 'intro' in o:
        return intro()


    if 'q' in o:
        return p(o['q'])


def strayed(o):
    return 'Code Strayed'
