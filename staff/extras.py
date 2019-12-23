def getquery_name(name,query,objs):
    if (query == "all"):
       return objs
    list = []
    for obj in objs:
        if obj.user_profile.name == query:
            list.append(obj)
    return list

def getquery_state(state,query,objs):
    if (query == "all"):
        return objs
    list = []
    for obj in objs:
        if obj.user_profile.state.name == query:
            list.append(obj)
    return list

def getquery_city(city,query,objs):
    if (query == "all"):
        return objs
    list = []
    for obj in objs:
        if obj.user_profile.city.name == query:
            list.append(obj)

    return list
