# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Widgets(Component):
    """A Widgets component.


Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- average_score (number; optional)

- top_3 (list of dicts; optional)

    `top_3` is a list of dicts with keys:

    - title (string; optional)

    - score (string; optional)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'widgets'
    _type = 'Widgets'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, average_score=Component.UNDEFINED, top_3=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'average_score', 'top_3']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'average_score', 'top_3']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Widgets, self).__init__(**args)
