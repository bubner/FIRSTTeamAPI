"""
    Driver for FIRSTTeamAPI.
    @author: Lucas Bubner, 2023
"""
from flask import Flask
import scraper

app = Flask(__name__)

@app.get("/get_team/{team_number}")
def get(team_number: int):
    """
        Get information about a team number.
    """
    data = scraper.get(team_number)
    return {
        "team_number": team_number,
        "valid": data.get("valid"),
        "season": data.get("season"),
        "data": data.get("data") or []
    }
