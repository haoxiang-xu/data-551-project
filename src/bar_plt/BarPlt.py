# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class BarPlt(Component):
    """A BarPlt component.


Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- data (list of dicts; optional)

    `data` is a list of dicts with keys:

    - genre (string; optional)

    - score (number; optional)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'bar_plt'
    _type = 'BarPlt'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, data=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'data']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'data']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(BarPlt, self).__init__(**args)
