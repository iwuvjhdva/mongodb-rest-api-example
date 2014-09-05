import colander


class Item(colander.MappingSchema):
    type = colander.SchemaNode(colander.String())
    item = colander.SchemaNode(colander.String())
    qty = colander.SchemaNode(colander.Int(),
                              validator=colander.Range(0))
