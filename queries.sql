-- Regular Season
-- Moments
select AVG(WStl) AS average,
   SQRT(AVG(WStl*WStl) - AVG(WStl)*AVG(WStl)) AS stdev from RegularGames
union
select AVG(LStl) AS average,
   SQRT(AVG(LStl*LStl) - AVG(LStl)*AVG(LStl)) AS stdev from RegularGames;

-- Winners
select g.Season, t.TeamID, t.TeamName, o.TeamID as OpponentID, o.TeamName as OpponentName, (g.DayNum / 154.0) as Day, (cast(g.WScore as float) / (g.LScore + g.WScore)) as Score, (g.WStl - 7.9174695) / 3.49906495 as Steals, (g.WBlk - 3.2870235) / 2.27007 as Blocks, (g.WPF - 17.08561) / 4.55982 as Fouls, (cast(g.WFTM as float) / g.WFTA) FreeThrowAccuracy, (cast(g.WFGM as float) / g.WFGA) as GoalAccuracy, (cast(g.WFGM3 as float) / g.WFGA3) as ThreesAccuracy, cast(g.WOR as float) / (g.WOR + g.LOR) as ReboundRateO, cast(g.WDR as float) / (g.WDR + g.LDR) as ReboundRateD, (g.WLoc == 'H') as Home , (g.WTeamID == t.TeamID) as Outcome from RegularGames g left join Teams t on t.TeamID = g.WTeamID left join Teams o on o.TeamID = g.LTeamID
union
-- Losers
select g.Season, t.TeamID, t.TeamName, o.TeamID as OpponentID, o.TeamName as OpponentName, (g.DayNum / 154.0) as Day, (cast(g.LScore as float) / (g.WScore + g.LScore)) as Score, (g.LStl - 7.9174695) / 3.49906495 as Steals, (g.LBlk - 3.2870235) / 2.27007 as Blocks, (g.LPF - 17.08561) / 4.55982 as Fouls, (cast(g.LFTM as float) / g.LFTA) FreeThrowAccuracy, (cast(g.LFGM as float) / g.LFGA) as GoalAccuracy, (cast(g.LFGM3 as float) / g.LFGA3) as ThreesAccuracy, cast(g.LOR as float) / (g.LOR + g.WOR) as ReboundRateO, cast(g.LDR as float) / (g.LDR + g.WDR) as ReboundRateD, 0 as Home , (g.WTeamID == t.TeamID) as Outcome from RegularGames g left join Teams t on t.TeamID = g.LTeamID left join Teams o on o.TeamID = g.WTeamID order by Season asc ;

select * from Teams where TeamName like '%wright%' or TeamName like '%bryant%';

-- Tournament
select g.Season, t.TeamID, t.TeamName, o.TeamID as OpponentID, o.TeamName as OpponentName, (g.DayNum / 154.0) as Day, (cast(g.WScore as float) / g.LScore) as Score, (cast(g.WFGM as float) / g.WFGA) as GoalAccuracy, (cast(g.WFGM3 as float) / g.WFGA3) as ThreesAccuracy, cast(g.WOR as float) / (g.WOR + g.LOR) as ReboundRateO, cast(g.WDR as float) / (g.WDR + g.LDR) as ReboundRateD, (g.WLoc == 'H') as Home , (g.WTeamID == t.TeamID) as Outcome from TournamentGames g left join Teams t on t.TeamID = g.WTeamID left join Teams o on o.TeamID = g.LTeamID
union
-- Losers
select g.Season, t.TeamID, t.TeamName, o.TeamID as OpponentID, o.TeamName as OpponentName, (g.DayNum / 154.0) as Day, (cast(g.LScore as float) / g.WScore) as Score, (cast(g.LFGM as float) / g.LFGA) as GoalAccuracy, (cast(g.LFGM3 as float) / g.LFGA3) as ThreesAccuracy, cast(g.LOR as float) / (g.LOR + g.WOR) as ReboundRateO, cast(g.LDR as float) / (g.LDR + g.WDR) as ReboundRateD, 0 as Home , (g.WTeamID == t.TeamID) as Outcome from TournamentGames g left join Teams t on t.TeamID = g.LTeamID left join Teams o on o.TeamID = g.WTeamID order by Season asc ;

-- Create SeasonStats
drop table SeasonStats;
create table SeasonStats as
    select g.Season, t.TeamID, t.TeamName, o.TeamID as OpponentID, o.TeamName as OpponentName, (cast(g.WScore as float) / (g.LScore + 0.000001)) as Score, cast(g.WStl as float) / (g.LStl + 0.000001) as Steals, cast(g.WBlk as float) / (g.LBlk + 0.000001) as Blocks, (cast(g.WPF as float) / (g.LPF + 0.000001)) as Fouls, (cast(g.WFTM as float) / (g.WFTA + + 0.000001)) FreeThrowAccuracy, (cast(g.WFGM as float) / (g.WFGA + 0.000001)) as GoalAccuracy, (cast(g.WFGM3 as float) / (g.WFGA3 + 0.000001)) as ThreesAccuracy, cast(g.WOR as float) / (g.WOR + g.LOR + 0.000001) as ReboundRateO, cast(g.WDR as float) / (g.WDR + g.LDR + 0.000001) as ReboundRateD, (g.WLoc == 'H') as Home , (g.WTeamID == t.TeamID) as Outcome from RegularGames g left join Teams t on t.TeamID = g.WTeamID left join Teams o on o.TeamID = g.LTeamID
union
-- Losers
select g.Season, t.TeamID, t.TeamName, o.TeamID as OpponentID, o.TeamName as OpponentName, (cast(g.LScore as float) / (g.WScore + 0.000001)) as Score, cast(g.LStl as float) / (g.WStl + 0.000001) as Steals, cast(g.LBlk as float) / (g.WBlk + 0.000001) as Blocks, (cast(g.LPF as float) / (g.WPF + 0.000001)) as Fouls, (cast(g.LFTM as float) / (g.LFTA + 0.000001)) FreeThrowAccuracy, (cast(g.LFGM as float) / (g.LFGA + 0.000001)) as GoalAccuracy, (cast(g.LFGM3 as float) / (g.LFGA3 + 0.000001)) as ThreesAccuracy, cast(g.LOR as float) / (g.LOR + g.WOR + 0.000001) as ReboundRateO, cast(g.LDR as float) / (g.LDR + g.WDR + 0.000001) as ReboundRateD, 0 as Home , (g.WTeamID == t.TeamID) as Outcome from RegularGames g left join Teams t on t.TeamID = g.LTeamID left join Teams o on o.TeamID = g.WTeamID order by Season asc ;


-- Create TournamentStats
create table TournamentStats as
    select g.Season, t.TeamID, t.TeamName, o.TeamID as OpponentID, o.TeamName as OpponentName, (g.DayNum / 154.0) as Day, (cast(g.WScore as float) / g.LScore) as Score, (cast(g.WFGM as float) / g.WFGA) as GoalAccuracy, (cast(g.WFGM3 as float) / g.WFGA3) as ThreesAccuracy, cast(g.WOR as float) / (g.WOR + g.LOR) as ReboundRateO, cast(g.WDR as float) / (g.WDR + g.LDR) as ReboundRateD, (g.WLoc == 'H') as Home , (g.WTeamID == t.TeamID) as Outcome from TournamentGames g left join Teams t on t.TeamID = g.WTeamID left join Teams o on o.TeamID = g.LTeamID
union
-- Losers
select g.Season, t.TeamID, t.TeamName, o.TeamID as OpponentID, o.TeamName as OpponentName, (g.DayNum / 154.0) as Day, (cast(g.LScore as float) / g.WScore) as Score, (cast(g.LFGM as float) / g.LFGA) as GoalAccuracy, (cast(g.LFGM3 as float) / g.LFGA3) as ThreesAccuracy, cast(g.LOR as float) / (g.LOR + g.WOR) as ReboundRateO, cast(g.LDR as float) / (g.LDR + g.WDR) as ReboundRateD, 0 as Home , (g.WTeamID == t.TeamID) as Outcome from TournamentGames g left join Teams t on t.TeamID = g.LTeamID left join Teams o on o.TeamID = g.WTeamID order by Season asc ;

select count(TeamID) as c from SeasonStats group by TeamID, Season order by c desc limit 1;

select min(Season), max(Season) from RegularGames;
select * from SeasonStats;
select * from TournamentStats where TeamID = 1411;

select * from CondensedStats2022;;

-- Training Data
select g.Season, g.TeamID as TeamA, ca.Stats as StatsA, g.Home as HomeA, g.OpponentID as TeamB, cb.Stats as StatsB, (select Home from SeasonStats where TeamID = cb.TeamID) as HomeB, g.Outcome from SeasonStats g left join CondensedStats ca on ca.TeamID = g.TeamID and ca.Season = g.Season left join CondensedStats cb on cb.TeamID = g.OpponentID and cb.Season = g.Season where ca.Season = 2021 order by ca.Season desc limit 1;


-- 2022 Data
select g.Season, g.TeamID as TeamA, ca.Stats as StatsA, g.Home as HomeA, g.OpponentID as TeamB, cb.Stats as StatsB, (select Home from SeasonStats where TeamID = cb.TeamID) as HomeB, g.Outcome from SeasonStats g left join CondensedStats2022 ca on ca.TeamID = g.TeamID and ca.Season = g.Season left join CondensedStats2022 cb on cb.TeamID = g.OpponentID and cb.Season = g.Season where ca.Season = 2022 order by ca.Season desc;

select a.TeamID as TeamA, a.Stats as StatsA, b.TeamID as TeamB, b.Stats as StatsB from CondensedStats2022 a left join CondensedStats2022 b on b.TeamID = 1411 where a.TeamID = 1401;

select g.Season, g.TeamID as TeamA, ca.Stats as StatsA, g.Home as HomeA, cb.TeamID as TeamB, cb.Stats as StatsB, (select Home from SeasonStats where TeamID = cb.TeamID) as HomeB from SeasonStats g left join CondensedStats2022 ca on ca.TeamID = g.TeamID and ca.Season = g.Season left join CondensedStats2022 cb on cb.TeamID = g.OpponentID and cb.Season = g.Season where ca.Season = 2022 and ca.TeamID = 1401 and cb.TeamID = 1411 order by ca.Season desc