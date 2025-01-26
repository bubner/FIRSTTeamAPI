"""
    Wrapper for the FIRST team/event search.
    @author: Lucas Bubner, 2023
"""
from urllib.request import urlopen
from datetime import datetime
import json

def get(team_number: int) -> dict:
    """
        Get information about a team number.
    """
    tdata = {}

    # Teams must be 2-5 digits
    if not 1 < len(str(team_number)) < 6:
        return {
            "valid": False
        }

    # Try backwards to get some data
    year = datetime.now().year
    bigdata = {}
    while not bigdata or not bigdata.get("hits").get("hits") and year >= 2021:
        res = urlopen(_query(team_number, year))
        bigdata = json.loads(res.read().decode("utf-8"))
        year -= 1
    
    if not bigdata or not bigdata.get("hits").get("hits"):
        # Stop at this point, if a team is over four years unregistered they are probably not active
        return {
            "valid": False
        }
    
    # Team is real
    tdata.update({
        "valid": True,
    })

    # Extract all team data from the response
    all_team_data = bigdata.get("hits").get("hits")
    extracted_data = []

    # Iterate through all team data
    for team in all_team_data:
        teamdata = {}
        data = team.get("_source")
        teamdata.update({"nickname": data.get("team_nickname")})
        teamdata.update({"orgs": data.get("team_name_calc")})
        teamdata.update({"city": data.get("team_city")})
        teamdata.update({"province": data.get("team_stateprov")})
        teamdata.update({"postcode": data.get("team_postalcode")})
        teamdata.update({"country": data.get("team_country")})
        teamdata.update({"country_code": data.get("countryCode")})
        teamdata.update({"program": data.get("program_name")})
        teamdata.update({"website": data.get("team_web_url")})
        teamdata.update({"season": int(data.get("profile_year"))})
        teamdata.update({"rookie_year": int(data.get("team_rookieyear"))})
        extracted_data.append(teamdata)
    
    tdata.update({"data": extracted_data})
        
    return tdata

def _query(team_number: int, year: int) -> str:
    # Mappings for the season selector
    # These are defined by FIRST, so they need to be updated per season
    # They can be found by analysing the HTML `<input type="hidden" name="seasonsFilter" value="335|333|337|331" id="inpSeasonsFilter" tabindex="9">` on the search page
    yrs = {
        2024: [335, 333, 337, 331],
        2023: [323, 321, 325, 319],
        2022: [311, 309, 313, 307],
        2021: [299, 297, 301, 295],
    }
    years = yrs.get(year, yrs.get(2024)) # wrap to 2024

    # Convert mappings into the suffix for the query
    season_selector = ",{'bool':{'should':[{'match':{'fk_program_seasons':'%s'}},{'match':{'fk_program_seasons':'%s'}},{'match':{'fk_program_seasons':'%s'}},{'match':{'fk_program_seasons':'%s'}}]}}]}},'sort':'team_nickname.raw'}" % tuple(years)

    # Generate full query URL, substituting in the team number and season selector
    # This will look for JFLL, FLL, FTC, and FRC teams at once
    query = "https://es02.firstinspires.org/teams/_search?size=20&from=0&source_content_type=application/json&source={'query':{'bool':{'must':[{'match':{'team_number_yearly':'%s'}},{'bool':{'should':[{'match':{'team_type':'JFLL'}},{'match':{'team_type':'FLL'}},{'match':{'team_type':'FTC'}},{'match':{'team_type':'FRC'}}]}}" % team_number + season_selector

    # Convert all ' to %22, therefore making it a valid URL
    return query.replace("'", "%22")
