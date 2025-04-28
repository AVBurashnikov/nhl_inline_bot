from datetime import datetime

from app.models.base import NHLAPIBaseModel


class Team(NHLAPIBaseModel):
    ...


class Summary(NHLAPIBaseModel):
    ...


class Clock(NHLAPIBaseModel):
    ...


class GameSummaryModel(NHLAPIBaseModel):
    id: int
    game_type: int
    start_time_u_t_c: datetime
    game_state: str
    away_team: Team
    home_team: Team
    shootout_in_use: bool
    reg_periods: int
    ot_in_use: bool
    summary: Summary
    clock: Clock | None = None