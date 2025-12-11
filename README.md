# FIRSTTeamAPI
### Live at https://firstteam.api.bubner.me/get_team/TEAM_NUMBER_HERE
WSGI API to retrieve information about a FIRST-registered team
# Example usage
Input:  
```/get_team/15215```  <br> <br>
Output:
```
{
  "data": [
    {
      "nickname": "MURRAY BRIDGE BUNYIPS",
      "orgs": "Murray Bridge High School",
      "city": "MURRAY BRIDGE",
      "province": "SA",
      "postcode": "5253",
      "country": "Australia",
      "country_code": "AU",
      "program": "FIRST Tech Challenge",
      "website": "https://sites.google.com/mbhs.sa.edu.au/the-mb-bunyips/home?authuser=0",
      "season": 2022,
      "rookie_year": 2018
    }
  ],
  "team_number": 15215,
  "valid": true
}
```
___
Input:  
```/get_team/365```  <br> <br>
Output:
```
{
  "data": [
    {
      "city": "Wilmington",
      "country": "USA",
      "country_code": "US",
      "nickname": "MOE (The Miracle Workerz)",
      "orgs": "First State Robotics & First State Robotics",
      "postcode": "19880",
      "program": "FIRST Tech Challenge",
      "province": "DE",
      "rookie_year": 2008,
      "season": 2022,
      "website": "http://www.moeftc.org"
    },
    {
      "city": "Wilmington",
      "country": "USA",
      "country_code": "US",
      "nickname": "Miracle Workerz",
      "orgs": "DuPont/JP Morgan Chase/The Boeing Company/On-Board Engineering/Siemens/Incyte/First State Robotics/Chemours&MOE Robotics Group",
      "postcode": "19808",
      "program": "FIRST Robotics Competition",
      "province": "DE",
      "rookie_year": 2000,
      "season": 2023,
      "website": "http://www.moe365.net"
    }
  ],
  "team_number": 365,
  "valid": true
}
```
___
Input:  
```/get_team/1```  <br> <br>
Output:
```
{
  "data": [],
  "team_number": 1,
  "valid": false
}
```
___
Input:  
```/``` ```/blah``` ```/get_team/blah```  <br> <br>
Output:
```
404 Not Found <redirect to https://github.com/bubner/FIRSTTeamAPI>
```
