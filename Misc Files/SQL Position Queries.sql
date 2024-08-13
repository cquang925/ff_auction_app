use NFL

-- QB 
select	p.FirstName,
		p.LastName, 
		t.TeamAbb as Team, 
		q.Games_Played as GP,   
		q.Pts_Total,
		q.Comp,
		q.Pass_Att, 
		q.Pass_Yards,
		q.Pass_TDs, 
		q.Rush_Yards, 
		q.Rush_TDs
	from NFL.Y2019.People p
		right join NFL.Y2019.QB_Season q
			on p.PlayerID = q.PlayerID
		left join NFL.dbo.Teams t
			on p.TeamID = t.TeamID
				order by q.Pts_Total desc

-- RB
select	p.FirstName,
		p.LastName,
		t.TeamAbb as Team,
		r.Games_Played as GP,
		r.Pts_Total,
		r.Rush_Att,
		r.Rush_Yards,
		r.Rush_TDs,
		r.Targets,
		r.Rec_Yards,
		r.Rec_TDs
	From NFL.Y2019.RB_Season r
		left join NFL.Y2019.People p
			on r.PlayerID = p.PlayerID
				left join NFL.dbo.Teams t
					on p.TeamID = t.TeamID
						order by r.Pts_Total desc

-- WR 
Select	p.FirstName,
		p.LastName,
		t.TeamAbb as Team,
		w.Games_Played as GP,
		w.Pts_Total,
		w.Targets,
		w.Receptions,
		w.Rec_Yards,
		w.Rec_TDs
	From NFL.Y2019.WR_Season w
		left join NFL.Y2019.People p
			on w.PlayerID = p.PlayerID
				left join NFL.dbo.Teams t
					on p.TeamID = t.TeamID
						order by w.Pts_Total desc

-- TE
Select	p.FirstName,
		p.LastName,
		t.TeamAbb as Team,
		te.Games_Played as GP,
		te.Pts_Season,
		te.Targets,
		te.Receptions,
		te.Rec_Yards,
		te.Rec_TDs
	From NFL.Y2019.TE_Season te
		left join NFL.Y2019.People p
			on te.PlayerID = p.PlayerID
				left join NFL.dbo.Teams t
					on p.TeamID = t.TeamID
						order by te.Pts_Season desc

-- Kicker
Select	p.FirstName,
		p.LastName,
		t.TeamAbb as Team,
		k.Games_Played as GP,
		k.Pts_Season,
		k.FG_Made,
		k.FG_Att,
		k.FG_Percetage as FG_Percentage,
		k.XP_Made
	from NFL.Y2019.K_Season k
		left join NFL.Y2019.People p
			on k.PlayerID = p.PlayerID
				left join NFL.dbo.Teams t
					 on p.TeamID = t.TeamID
						order by k.Pts_Season desc

-- DEF
Select	d.Place,
		d.Team_Name,
		t.TeamAbb as Team,
		d.Pts_Season,
		d.Sacks,
		d.Interceptions,
		d.Fumbles_Recovered,
		d.Safeties,
		d.Def_Tds,
		d.Pts_Against
	from NFL.Y2019.DEF_Season d
		left join NFL.dbo.Teams t
			on d.TeamID = t.TeamID
				order by d.Pts_Season desc