# FIRSTTeamAPI
WSGI web scraper API to retrieve information about a FIRST-registered team

Usage:  
```/get_team/15215```  <br> <br>
Output:
```
{
  "data": [
    {
      "location": "MURRAY BRIDGE, SA 5253 Australia",
      "nickname": "MURRAY BRIDGE BUNYIPS",
      "orgs": "Murray Bridge High School",
      "program": "FIRST Tech Challenge",
      "rookie_year": 2018
    }
  ],
  "season": "2022-2023",
  "team_number": 15215,
  "valid": true
}
```

Usage:
```/get_team/1```  <br> <br>
Output:
```
{
  "data": [],
  "season": null,
  "team_number": 1,
  "valid": false
}
```