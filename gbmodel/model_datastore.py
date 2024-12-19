from google.cloud import datastore

def from_datastore(entity):
    if not entity:
        return None
    if isinstance(entity, list):
        entity = entity.pop()
    return [
        entity.get('player_tag'), 
        entity.get('player_name'), 
        entity.get('town_hall_level'), 
        entity.get('troops'), 
        entity.get('heroes'), 
        entity.get('pets'), 
        ]

class model:
    def __init__(self):
        self.client = datastore.Client('cloud-esmail-kesmail-441007')

    def save_village(self,player_tag, player_name, town_hall_level, troops, heroes, pets):
        """
        Saving the players info in the database
        """
        key = self.client.key("Village", player_tag)
        entity = datastore.Entity(key=key)
        entity.update({
            "player_tag": player_tag,
            "player_name": player_data.get("name"),
            "town_hall_level": player_data.get("townHallLevel"),
            "troops": troops,
            "heroes": heroes,
            "pets": pets,
        })
        self.client.put(entity)

    def get_village(self, player_tag):
        """
        get village data from Datastore.
        """
        key = self.client.key("Village", player_tag)
        return self.client.get(key)

    def select_all_villages(self):
        query = self.client.query(kind="Village")
        return list(query.fetch())
         
    
    
   
