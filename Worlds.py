import vrchatapi
from vrchatapi.api.worlds_api import WorldsApi

def searchWorlds(client, searchTerm):
    world_api = WorldsApi(client)
    result = world_api.search_worlds(search=searchTerm)

    print("test: " + str(result))

def getWorldInfo(client, worldID) -> dict:
    world_api = WorldsApi(client)
    result = world_api.get_world(worldID)

    #print("RESULT:\n" + str(result))

    return result.to_dict()
