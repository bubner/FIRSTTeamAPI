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

    # Try last season first, incase the team has not registered for the current season yet
    res = urlopen(_query(team_number, datetime.now().year - 1))
    bigdata = json.loads(res.read().decode("utf-8"))

    if not bigdata.get("hits").get("hits"):
        # Try again with current season for new teams
        res = urlopen(_query(team_number, datetime.now().year))
        bigdata = json.loads(res.read().decode("utf-8"))
    
    if not bigdata.get("hits").get("hits"):
        # Stop at this point, if a team is over two years unregistered they are probably not active
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
    # These are defined by FIRST
    years = {
        2023: [323, 321, 325, 319],
        2022: [311, 309, 313, 307],
        2021: [299, 297, 301, 295],
        2020: [277, 275, 279, 273],
    }.get(year)

    # Convert mappings into the suffix for the query
    season_selector = ",{'bool':{'should':[{'match':{'fk_program_seasons':'%s'}},{'match':{'fk_program_seasons':'%s'}},{'match':{'fk_program_seasons':'%s'}},{'match':{'fk_program_seasons':'%s'}}]}}]}},'sort':'team_nickname.raw'}" % tuple(years)

    # Generate full query URL, substituting in the team number and season selector
    # This will look for JFLL, FLL, FTC, and FRC teams at once
    query = "https://es02.firstinspires.org/teams/_search?size=20&from=0&source_content_type=application/json&source={'query':{'bool':{'must':[{'match':{'team_number_yearly':'%s'}},{'bool':{'should':[{'match':{'team_type':'JFLL'}},{'match':{'team_type':'FLL'}},{'match':{'team_type':'FTC'}},{'match':{'team_type':'FRC'}}]}}" % team_number + season_selector

    # Convert all ' to %22, therefore making it a valid URL
    return query.replace("'", "%22")
