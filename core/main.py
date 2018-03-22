from tabulate import tabulate
from collections import defaultdict

import json
import requests
import enum

class Role(enum.Enum):
	OFFENSE = 0
	DEFENSE = 1
	SUPPORT = 2
	TANK = 3

team_names = [
	"Boston Uprising",
	"Dallas Fuel",
	"Houston Outlaws",
	"London Spitfire",
	"Los Angeles Gladiators",
	"Los Angeles Valiant",
	"Florida Mayhem",
	"New York Excelsior",
	"Philadelphia Fusion",
	"San Francisco Shock",
	"Seoul Dynasty",
	"Shanghai Dragons",
 ]

class Team(enum.Enum):
	BOSTON_UPRISING = 0
	DALLAS_FUEL = 1
	HOUSTON_OUTLAWS = 2
	LONDON_SPITFIRE = 3
	LOS_ANGELES_GLADIATORS = 4
	LOS_ANGELES_VALIANT = 5
	FLORIDA_MAYHEM = 6
	NEW_YORK_EXCELSIOR = 7
	PHILADELPHIA_FUSION = 8
	SAN_FRANCISCO_SHOCK = 9
	SEOUL_DYNASTY = 10
	SHANGHAI_DRAGONS = 11

class Hero:
	def __init__(self, name, role):
		self.name = name
		self.role = role

HERO_NAME_TO_ROLE = {
	"Doomfist": Role.OFFENSE,
	"Genji": Role.OFFENSE,
	"McCree": Role.OFFENSE,
	"Pharah": Role.OFFENSE,
	"Reaper": Role.OFFENSE,
	"Soldier76": Role.OFFENSE,
	"Sombra": Role.OFFENSE,
	"Tracer": Role.OFFENSE,
	# Defense
	"Bastion": Role.DEFENSE,
	"Hanzo": Role.DEFENSE,
	"Junkrat": Role.DEFENSE,
	"Mei": Role.DEFENSE,
	"Torbjorn": Role.DEFENSE,
	"Widowmaker": Role.DEFENSE,
	# Tank
	"DVa": Role.TANK,
	"Orisa": Role.TANK,
	"Reinhardt": Role.TANK,
	"Roadhog": Role.TANK,
	"Winston": Role.TANK,
	"Zarya": Role.TANK,
	# Support
	"Brigitte": Role.SUPPORT,
	"Lucio": Role.SUPPORT,
	"Mercy": Role.SUPPORT,
	"Moira": Role.SUPPORT,
	"Symmetra": Role.SUPPORT,
	"Zenyatta": Role.SUPPORT,
}

ROSTER = {
	"HarryHook-3986": { "team": Team.DALLAS_FUEL, "role": Role.SUPPORT },
	"sinatraa-11809": { "team": Team.SAN_FRANCISCO_SHOCK, "role": Role.OFFENSE },
	"zappis-21285": { "team": Team.FLORIDA_MAYHEM, "role": Role.DEFENSE },
	"Muma-11444": { "team": Team.HOUSTON_OUTLAWS, "role": Role.TANK },
	"Fleta-31226": { "team": Team.SEOUL_DYNASTY, "role": Role.OFFENSE },
}
"""
Args:
  stat_names_list: List of tuples of stat_type and stat_name e.g. [("assists", "defensiveAssistsAvgPer10Min")]
  hero_names_list: List of hero names to print stats for
  all_heroes_career_stas: Dictionary of player name to a stats struct

  Ex.
	"ana": {
		"assists": {
		  "defensiveAssists": 49,
		  "defensiveAssistsAvgPer10Min": 0,
		  "defensiveAssistsMostInGame": 14,
		  "healingDone": 14016,
		  "healingDoneAvgPer10Min": 3,
		  "healingDoneMostInGame": 7415,
		  "offensiveAssists": 55,
		  "offensiveAssistsAvgPer10Min": 0,
		  "offensiveAssistsMostInGame": 16,
		  "turretsDestroyed": 3
		},
		"average": {
		  "allDamageDoneAvgPer10Min": 7.39,
		  "deathsAvgPer10Min": 0,
		  "eliminationsAvgPer10Min": 0,
		  "eliminationsPerLife": 1.86,
		  "finalBlowsAvgPer10Min": 0,
		  "meleeFinalBlowsAvgPer10Min": 0,
		  "objectiveKillsAvgPer10Min": 0,
		  "objectiveTimeAvgPer10Min": 0,
		  "soloKillsAvgPer10Min": 0,
		  "timeSpentOnFireAvgPer10Min": 0
		},
		"best": {
		  "weaponAccuracyBestInGame": "22%"
		},
		"combat": {
		  "weaponAccuracy": "17%"
		},
		"heroSpecific": {
		  "enemiesSleptAvgPer10Min": 0,
		  "nanoBoostAssistsAvgPer10Min": 0,
		  "nanoBoostsAppliedAvgPer10Min": 0,
		  "scopedAccuracy": "69%",
		},
		"game": {
		  "gamesWon": 3,
		  "timePlayed": "1 hour"
		},
		"matchAwards": {
		  "cards": 4,
		  "medals": 15,
		  "medalsBronze": 4,
		  "medalsGold": 4,
		  "medalsSilver": 7
		}
	  },
	}
"""
def pp_stats_for_heroes(stat_names_list, hero_names_list, all_heroes_career_stats):
	hero_stats = defaultdict(list)
	for hero_name in hero_names_list:
		# TODO (mich) better way
		if hero_name == "dva":
			hero_name = "dVa" # accounts for weird json response formatting for dva
		hero_stats["name"].append(hero_name or "n/a")
		for subsection, stat in stat_names_list:
			full_stat_name = ".".join([subsection, stat])
			try:
				hero_stats[stat].append(all_heroes_career_stats[hero_name][subsection][stat] or "n/a")
			except KeyError as e:
				print("key missing: " + full_stat_name)
			except TypeError as e:
				print("type error on " + full_stat_name)
	print(tabulate(hero_stats, headers="keys"))

def get_top_heroes_descending_order(player_stats):
	top_heroes = [(k, v) for k, v in player_stats["quickPlayStats"]["topHeroes"].items()]
	# sort descending order by timePlayedInSeconds
	return sorted(top_heroes, key=lambda hero: hero[1]["timePlayedInSeconds"])

# init heroes
heroes_by_name = {}
for name, role in HERO_NAME_TO_ROLE.items():
	standard_name = name.lower()
	heroes_by_name[standard_name] = Hero(standard_name, role)

stats_by_player_name = {}

REQUEST_URL = "https://ovrstat.com/stats/pc/us/"
for player_name, player_details in ROSTER.items():
	response = requests.get(REQUEST_URL + player_name)
	if response.status_code == 200:
		stats_dict = json.loads(response.content.decode('utf8'))
		stats_by_player_name[player_name] = stats_dict

player_name = "sinatraa-11809"
stat_names_list = [
	("average", "allDamageDoneAvgPer10Min"),
	("average", "criticalHitsAvgPer10Min"),
	("average", "deathsAvgPer10Min"),
	("average", "eliminationsAvgPer10Min"),
	("average", "objectiveKillsAvgPer10Min"),
	("average", "soloKillsAvgPer10Min"),
]

for player in ROSTER.keys():
	hero_names = ["allHeroes"] + [k for k, v in get_top_heroes_descending_order(stats_dict)[:5]]
	print("\nSTATS FOR " + player)
	pp_stats_for_heroes(stat_names_list, hero_names, stats_by_player_name[player]["quickPlayStats"]["careerStats"])

