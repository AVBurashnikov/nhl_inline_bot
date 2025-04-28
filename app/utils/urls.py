class UrlBuilder:
    _urls = {
        "schedule": "https://api-web.nhle.com/v1/schedule/%s",
        "score": "https://api-web.nhle.com/v1/score/now",
        "standings": "https://api-web.nhle.com/v1/standings/now",
        "stats": "https://api-web.nhle.com/v1/%s-stats-leaders/%s/%s?limit=%s",
        "player_landing": "https://api-web.nhle.com/v1/player/%s/landing",
        "game_summary": "https://api-web.nhle.com/v1/gamecenter/%s/landing",
        "games_by_date": "https://api-web.nhle.com/v1/score/%s",
        "right_rail": "https://api-web.nhle.com/v1/gamecenter/%s/right-rail",
        "roster": "https://api-web.nhle.com/v1/roster/%s/current",
        "schedule_team": "https://api-web.nhle.com/v1/scoreboard/%s/now",
        "playoff": "https://api-web.nhle.com/v1/playoff-bracket/2025",
        "playoff_series": "https://api-web.nhle.com/v1/schedule/playoff-series/20242025/%s/",
        # goalie records url
        "skaters-records": "https://records.nhl.com/site/api/skater-career-scoring-regular-plus-playoffs?"
                           "cayenneExp=%s%%20%%3E=%%20700&sort=[{\"property\":\"%s\",\"direction\":\"DESC\"}]",

        "goalies-records": "https://records.nhl.com/site/api/goalie-career-stats?"
                           "cayenneExp=gameTypeId=2 and gamesPlayed>=100 and "
                           "franchiseId=null&sort=[\"{property\":\"gamesPlayed\",\"direction\":\"DESC\"}]"
                           "{'property':'lastName','direction':'ASC_CI'}]"

    }

    @staticmethod
    def build_url(key: str, *args) -> str:
        try:
            url_template = UrlBuilder._urls.get(key)
            if url_template is None:
                raise KeyError(f"Key '{key}' not found in Urls._urls")
            url = url_template % args
            return url
        except (KeyError, TypeError, AttributeError, ValueError, IndexError) as e:
            print(f"Error occurred: {e}")
            return ""
