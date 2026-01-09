


def create(filters):
    BASE_QUERY = "SELECT * FROM clothes"
    conditions = []
    parameters = []

    columns = ['brand', 'category', 'gender', 'style']

    for col in columns:
        if filters.get(col) is not None:
            conditions.append(f"{col} = %s")
            parameters.append(filters[col])

    if filters.get('price_eur') is not None:
        conditions.append("price_eur = %s")
        parameters.append(filters['price_eur'])

    if filters.get('colors') is not None:
        conditions.append("colors @> %s")
        parameters.append([filters['colors']])

    if conditions:
        full_query = BASE_QUERY + " WHERE " + " AND ".join(conditions)
    else:
        full_query = BASE_QUERY

    return full_query, parameters

