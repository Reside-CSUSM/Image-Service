
COUNTRY_ABBREVIATION = {
    "India":"IND",
    "United States of America":"USA",
    "Australia":"AUS",
    "China":"CN"
}


class CountryResolver():

    def ResolveToAbbr(name):
        try:
            return COUNTRY_ABBREVIATION[name]
        except Exception as error:
            return None

    def ResolveToName(abbr):
        list = COUNTRY_ABBREVIATION.items()
        for item in list:
            if(item[1] == abbr):
                return item[0]
        return None