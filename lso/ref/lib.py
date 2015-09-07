from lso import ctx
from sanskrit.schema import *


def get_base_root(ctx, name):
    results = ctx.session.query(Root).filter(Root.name == name).all()
    return ctx.session.query(Root).filter(Root.name == name).first()


def get_3s_verbs(ctx, root):
    if root is None:
        return []

    e_person_id = ctx.enum_id['person']
    e_number_id = ctx.enum_id['number']
    results = ctx.session.query(Verb).filter(Verb.root_id == root.id)\
                   .filter(Verb.person_id == e_person_id['3'])\
                   .filter(Verb.number_id == e_number_id['s']).all()

    return {(x.mode_id): x for x in results}


def get_participle_stems(ctx, root):
    if root is None:
        return []
    results = ctx.session.query(ParticipleStem)\
                       .filter(ParticipleStem.root_id == root.id)
    return {(x.mode_id, x.voice_id): x for x in results}


def get_root_paradigm(ctx, slp1_name):
    root = get_base_root(ctx, slp1_name)

    return {
        'query': slp1_name,
        'root': root,
        'verbs': get_3s_verbs(ctx, root),
        'participles': get_participle_stems(ctx, root),
    }
