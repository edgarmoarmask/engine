from lib.objects.entities import EntityTypes


class EntityUrls:

    @staticmethod
    def get_url(entity_type: EntityTypes):
        url_switcher = {
            EntityTypes.PERSON.name : "person.png",
            EntityTypes.ORGANIZATION.name: "organization.png",
            EntityTypes.LOCATION.name: "location.png",
            EntityTypes.CITY.name: "city.png",
            EntityTypes.COUNTRY.name: "country.png",
            EntityTypes.STATE_OR_PROVINCE.name: "province.png",
            EntityTypes.CRIMINAL_CHARGE.name: "criminal-charge.png",
            EntityTypes.CAUSE_OF_DEATH.name: "cause-of-death.png",
            EntityTypes.NATIONALITY.name: "nationality.png",
            EntityTypes.TITLE.name: "title.png",
            EntityTypes.DATE.name: "date.png",
            EntityTypes.LAW.name: "law.png",
            EntityTypes.RELIGION.name: "religion.png",
        }

        result = url_switcher.get(entity_type.name, "misc.png" )

        result = "/assets/images/" + result

        return result

def test():
    print("PERSON ->", EntityUrls.get_url(EntityTypes.PERSON))
    print("ORG ->", EntityUrls.get_url(EntityTypes.ORGANIZATION))
    print("LOCATION ->", EntityUrls.get_url(EntityTypes.LOCATION))
    print("DEFAULT ->", EntityUrls.get_url(EntityTypes.TIME))