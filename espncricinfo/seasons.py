import requests
from datetime import datetime
from espncricinfo.exceptions import NoSeriesError
from espncricinfo.series import Series

class Season:
    def __init__(self, season_id, season_type_id):
        self.id = season_id
        self.type_id = season_type_id
        self.json_url = f"http://core.espnuk.org/v2/sports/cricket/leagues/{season_type_id}/seasons/{season_id}"        
        self.headers = {'user-agent': 'Mozilla/5.0'}
        self.json = self.get_json(self.season_url)
        
        if self.json:
            self.year = self.json.get('year')
            self.start_date = self.parse_date(self.json.get('startDate'))
            self.end_date = self.parse_date(self.json.get('endDate'))
            self.name = self.json.get('name')
            self.short_name = self.json.get('shortName')
            self.slug = self.json.get('slug')
            self.teams_url = self.json.get('teams', {}).get('$ref')
            self.series = self._get_series()
            self.rankings_url = self.json.get('rankings', {}).get('$ref')
        else:
            raise NoSeriesError("Invalid season or no data found.")
    
    def get_json(self, url):
        response = requests.get(url, headers=self.headers)
        if response.status_code == 404:
            raise NoSeriesError("Season not found.")
        return response.json()
    
    def parse_date(self, date_str):
        if date_str:
            return datetime.strptime(date_str, "%Y-%m-%dT%H:%MZ")
        return None
    
    def _get_series(self):
        links = self.json.get('links', [])
        if links and len(links)>5:
            series_url = links[5]["href"]
            series_id = int(series_url.split("/series/")[-1].split(".html")[0])
            series = Series(series_id)
            return series
        return None
    
    def __str__(self):
        return self.name if self.name else "Unknown Season"
    
    def __repr__(self):
        return f"Season(id={self.id}, year={self.year}, name={self.name}, start_date={self.start_date}, end_date={self.end_date})"
