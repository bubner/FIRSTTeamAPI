"""
    Driver for FIRSTTeamAPI.
    @author: Lucas Bubner, 2023
"""
from flask import Flask, redirect
import wrapper

app = Flask(__name__)

@app.route("/get_team/<int:team_number>")
def get(team_number: int):
    """
        Get information about a team number.
    """
    data = wrapper.get(team_number)
    return {
        "team_number": team_number,
        "valid": data.get("valid"),
        "data": data.get("data") or []
    }

@app.errorhandler(404)
def not_found(e):
    """
        Redirect invalid requests to the GitHub page.
    """
    return redirect("https://github.com/hololb/FIRSTTeamAPI/"), 404, {"Refresh": "1; url=https://github.com/hololb/FIRSTTeamAPI/"}
