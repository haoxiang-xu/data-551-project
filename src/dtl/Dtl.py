# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Dtl(Component):
    """A Dtl component.


Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- countX (list; optional)

- countY (list; optional)

- scoreX (list; optional)

- scoreY (list; optional)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dtl'
    _type = 'Dtl'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, countX=Component.UNDEFINED, countY=Component.UNDEFINED, scoreX=Component.UNDEFINED, scoreY=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'countX', 'countY', 'scoreX', 'scoreY']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'countX', 'countY', 'scoreX', 'scoreY']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Dtl, self).__init__(**args)
