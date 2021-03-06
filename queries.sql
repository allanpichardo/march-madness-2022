-- Regular Season

-- Winners
select g.Season, t.TeamID, t.TeamName, o.TeamID as OpponentID, o.TeamName as OpponentName, (g.DayNum / 154.0) as Day, (cast(g.WScore as float) / g.LScore) as Score, (cast(g.WFGM as float) / g.WFGA) as GoalAccuracy, (cast(g.WFGM3 as float) / g.WFGA3) as ThreesAccuracy, cast(g.WOR as float) / (g.WOR + g.LOR) as ReboundRateO, cast(g.WDR as float) / (g.WDR + g.LDR) as ReboundRateD, (g.WLoc == 'H') as Home , (g.WTeamID == t.TeamID) as Outcome from RegularGames g left join Teams t on t.TeamID = g.WTeamID left join Teams o on o.TeamID = g.LTeamID
union
-- Losers
select g.Season, t.TeamID, t.TeamName, o.TeamID as OpponentID, o.TeamName as OpponentName, (g.DayNum / 154.0) as Day, (cast(g.LScore as float) / g.WScore) as Score, (cast(g.LFGM as float) / g.LFGA) as GoalAccuracy, (cast(g.LFGM3 as float) / g.LFGA3) as ThreesAccuracy, cast(g.LOR as float) / (g.LOR + g.WOR) as ReboundRateO, cast(g.LDR as float) / (g.LDR + g.WDR) as ReboundRateD, 0 as Home , (g.WTeamID == t.TeamID) as Outcome from RegularGames g left join Teams t on t.TeamID = g.LTeamID left join Teams o on o.TeamID = g.WTeamID order by Season asc ;

select * from Teams where TeamName like '%wright%' or TeamName like '%bryant%';

-- Tournament
select g.Season, t.TeamID, t.TeamName, o.TeamID as OpponentID, o.TeamName as OpponentName, (g.DayNum / 154.0) as Day, (cast(g.WScore as float) / g.LScore) as Score, (cast(g.WFGM as float) / g.WFGA) as GoalAccuracy, (cast(g.WFGM3 as float) / g.WFGA3) as ThreesAccuracy, cast(g.WOR as float) / (g.WOR + g.LOR) as ReboundRateO, cast(g.WDR as float) / (g.WDR + g.LDR) as ReboundRateD, (g.WLoc == 'H') as Home , (g.WTeamID == t.TeamID) as Outcome from TournamentGames g left join Teams t on t.TeamID = g.WTeamID left join Teams o on o.TeamID = g.LTeamID
union
-- Losers
select g.Season, t.TeamID, t.TeamName, o.TeamID as OpponentID, o.TeamName as OpponentName, (g.DayNum / 154.0) as Day, (cast(g.LScore as float) / g.WScore) as Score, (cast(g.LFGM as float) / g.LFGA) as GoalAccuracy, (cast(g.LFGM3 as float) / g.LFGA3) as ThreesAccuracy, cast(g.LOR as float) / (g.LOR + g.WOR) as ReboundRateO, cast(g.LDR as float) / (g.LDR + g.WDR) as ReboundRateD, 0 as Home , (g.WTeamID == t.TeamID) as Outcome from TournamentGames g left join Teams t on t.TeamID = g.LTeamID left join Teams o on o.TeamID = g.WTeamID order by Season asc ;

-- Create SeasonStats
create table SeasonStats as
    select g.Season, t.TeamID, t.TeamName, o.TeamID as OpponentID, o.TeamName as OpponentName, (g.DayNum / 154.0) as Day, (cast(g.WScore as float) / g.LScore) as Score, (cast(g.WFGM as float) / g.WFGA) as GoalAccuracy, (cast(g.WFGM3 as float) / g.WFGA3) as ThreesAccuracy, cast(g.WOR as float) / (g.WOR + g.LOR) as ReboundRateO, cast(g.WDR as float) / (g.WDR + g.LDR) as ReboundRateD, (g.WLoc == 'H') as Home , (g.WTeamID == t.TeamID) as Outcome from RegularGames g left join Teams t on t.TeamID = g.WTeamID left join Teams o on o.TeamID = g.LTeamID
union
-- Losers
select g.Season, t.TeamID, t.TeamName, o.TeamID as OpponentID, o.TeamName as OpponentName, (g.DayNum / 154.0) as Day, (cast(g.LScore as float) / g.WScore) as Score, (cast(g.LFGM as float) / g.LFGA) as GoalAccuracy, (cast(g.LFGM3 as float) / g.LFGA3) as ThreesAccuracy, cast(g.LOR as float) / (g.LOR + g.WOR) as ReboundRateO, cast(g.LDR as float) / (g.LDR + g.WDR) as ReboundRateD, 0 as Home , (g.WTeamID == t.TeamID) as Outcome from RegularGames g left join Teams t on t.TeamID = g.LTeamID left join Teams o on o.TeamID = g.WTeamID order by Season asc;

-- Create TournamentStats
create table TournamentStats as
    select g.Season, t.TeamID, t.TeamName, o.TeamID as OpponentID, o.TeamName as OpponentName, (g.DayNum / 154.0) as Day, (cast(g.WScore as float) / g.LScore) as Score, (cast(g.WFGM as float) / g.WFGA) as GoalAccuracy, (cast(g.WFGM3 as float) / g.WFGA3) as ThreesAccuracy, cast(g.WOR as float) / (g.WOR + g.LOR) as ReboundRateO, cast(g.WDR as float) / (g.WDR + g.LDR) as ReboundRateD, (g.WLoc == 'H') as Home , (g.WTeamID == t.TeamID) as Outcome from TournamentGames g left join Teams t on t.TeamID = g.WTeamID left join Teams o on o.TeamID = g.LTeamID
union
-- Losers
select g.Season, t.TeamID, t.TeamName, o.TeamID as OpponentID, o.TeamName as OpponentName, (g.DayNum / 154.0) as Day, (cast(g.LScore as float) / g.WScore) as Score, (cast(g.LFGM as float) / g.LFGA) as GoalAccuracy, (cast(g.LFGM3 as float) / g.LFGA3) as ThreesAccuracy, cast(g.LOR as float) / (g.LOR + g.WOR) as ReboundRateO, cast(g.LDR as float) / (g.LDR + g.WDR) as ReboundRateD, 0 as Home , (g.WTeamID == t.TeamID) as Outcome from TournamentGames g left join Teams t on t.TeamID = g.LTeamID left join Teams o on o.TeamID = g.WTeamID order by Season asc ;

select count(TeamID) as c from SeasonStats group by TeamID, Season order by c desc limit 1;

select * from SeasonStats where TeamID = 1123 and Season = 2003;
select * from TournamentStats where TeamID = 1411;

select * from CondensedStats2022;;

-- Training Data
select g.Season, g.TeamID as TeamA, ca.Stats as StatsA, g.Home as HomeA, g.OpponentID as TeamB, cb.Stats as StatsB, (select Home from SeasonStats where TeamID = cb.TeamID) as HomeB, g.Outcome from SeasonStats g left join CondensedStats ca on ca.TeamID = g.TeamID and ca.Season = g.Season left join CondensedStats cb on cb.TeamID = g.OpponentID and cb.Season = g.Season where ca.Season = 2021 order by ca.Season desc limit 1;


-- 2022 Data
select g.Season, g.TeamID as TeamA, ca.Stats as StatsA, g.Home as HomeA, g.OpponentID as TeamB, cb.Stats as StatsB, (select Home from SeasonStats where TeamID = cb.TeamID) as HomeB, g.Outcome from SeasonStats g left join CondensedStats2022 ca on ca.TeamID = g.TeamID and ca.Season = g.Season left join CondensedStats2022 cb on cb.TeamID = g.OpponentID and cb.Season = g.Season where ca.Season = 2022 order by ca.Season desc;

select a.TeamID as TeamA, a.Stats as StatsA, b.TeamID as TeamB, b.Stats as StatsB from CondensedStats2022 a left join CondensedStats2022 b on b.TeamID = 1411 where a.TeamID = 1401;

select g.Season, g.TeamID as TeamA, ca.Stats as StatsA, g.Home as HomeA, cb.TeamID as TeamB, cb.Stats as StatsB, (select Home from SeasonStats where TeamID = cb.TeamID) as HomeB from SeasonStats g left join CondensedStats2022 ca on ca.TeamID = g.TeamID and ca.Season = g.Season left join CondensedStats2022 cb on cb.TeamID = g.OpponentID and cb.Season = g.Season where ca.Season = 2022 and ca.TeamID = 1401 and cb.TeamID = 1411 order by ca.Season desc