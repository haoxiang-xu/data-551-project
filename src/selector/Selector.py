# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Selector(Component):
    """A Selector component.


Keyword arguments:

- id (string; optional)

- genreOptions (list; optional)

- studioOptions (list; optional)

- typeOptions (list; optional)

- values (list; optional)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'selector'
    _type = 'Selector'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, values=Component.UNDEFINED, typeOptions=Component.UNDEFINED, genreOptions=Component.UNDEFINED, studioOptions=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'genreOptions', 'studioOptions', 'typeOptions', 'values']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'genreOptions', 'studioOptions', 'typeOptions', 'values']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Selector, self).__init__(**args)
