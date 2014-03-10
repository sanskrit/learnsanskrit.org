from flask import Blueprint
from flask.blueprints import BlueprintSetupState

__all__ = ['LSOBlueprint']


class LSOBlueprintSetupState(BlueprintSetupState):

    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        if endpoint == 'static':
            # We create a new BlueprintSetupState to avoid duplicating
            # the internals of `add_url_rule`.
            s = BlueprintSetupState(self.blueprint, self.app, self.options,
                                    self.first_registration)
            # By setting url_prefix to `None` we can use the rule as-is.
            s.url_prefix = None
            rule = '/static/%s/<path:filename>' % self.blueprint.name
            s.add_url_rule(rule, endpoint, view_func, **options)
        else:
            sup = super(LSOBlueprintSetupState, self)
            sup.add_url_rule(rule, endpoint, view_func, **options)


class LSOBlueprint(Blueprint):

    """A special kind of :class:`~flask.Blueprint`. It mounts the static
    folder to '/static/blueprint_name' instead of '/url_prefix/static'.
    This is useful for e.g. serving static assets from a single process.
    """

    def __init__(self, name, import_name, **kw):
        kw['static_folder'] = '../static/' + name
        kw['template_folder'] = 'templates'
        Blueprint.__init__(self, name, import_name, **kw)

    def make_setup_state(self, *a, **kw):
        return LSOBlueprintSetupState(self, *a, **kw)
