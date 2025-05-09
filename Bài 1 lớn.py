import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_player(player):
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    
    response_player = session.get(player)
    time.sleep(1)
    if response_player.status_code == 200:
        soup_player = bs(response_player.text, 'html.parser')
        cv_player = []
        
        # Goalkeeping
        check_goalkeeping_table = soup_player.find('div', id='all_stats_keeper')
        if check_goalkeeping_table is None:
            cv_player.extend([None, None, None, None])

        else:
            goalkeeping_table = check_goalkeeping_table.find('tbody').find_all('tr')
            res1 = goalkeeping_table[-1]
            cv_player.extend(
                [
                res1.find('td', {'data-stat': 'gk_goals_against_per90'}).text,
                res1.find('td', {'data-stat': 'gk_save_pct'}).text,
                res1.find('td', {'data-stat': 'gk_clean_sheets_pct'}).text,
                res1.find('td', {'data-stat': 'pk_save_pct'}).text
                ]
            )
        
        # Shooting
        shooting_table = soup_player.find('div', id='all_stats_shooting').find('tbody').find_all('tr')
        res2 = shooting_table[-1]
        cv_player.extend(
            [
            res2.find('td', {'data-stat': 'shots_on_target_pct'}).text,
            res2.find('td', {'data-stat': 'shots_on_target_per90'}).text,
            res2.find('td', {'data-stat': 'goals_per_shot'}).text,
            res2.find('td', {'data-stat': 'average_shot_distance'}).text
            ]
        )
        
        # Passing
        passing_table = soup_player.find('div', id='all_stats_passing').find('tbody').find_all('tr')
        res3 = passing_table[-1]
        cv_player.extend(
            [
            res3.find('td', {'data-stat': 'passes_completed'}).text,
            res3.find('td', {'data-stat': 'passes_pct'}).text,
            res3.find('td', {'data-stat': 'passes_total_distance'}).text,
            res3.find('td', {'data-stat': 'passes_pct_short'}).text,
            res3.find('td', {'data-stat': 'passes_pct_medium'}).text,
            res3.find('td', {'data-stat': 'passes_pct_long'}).text,
            res3.find('td', {'data-stat': 'assisted_shots'}).text,
            res3.find('td', {'data-stat': 'passes_into_final_third'}).text,
            res3.find('td', {'data-stat': 'passes_into_penalty_area'}).text,
            res3.find('td', {'data-stat': 'crosses_into_penalty_area'}).text,
            res3.find('td', {'data-stat': 'progressive_passes'}).text
            ]
        )
        
        # Goal and Shot Creation
        goal_and_shot_creation_table = soup_player.find('div', id='all_stats_gca').find('tbody').find_all('tr')
        res4 = goal_and_shot_creation_table[-1]
        cv_player.extend(
            [
            res4.find('td', {'data-stat': 'sca'}).text,
            res4.find('td', {'data-stat': 'sca_per90'}).text,
            res4.find('td', {'data-stat': 'gca'}).text,
            res4.find('td', {'data-stat': 'gca_per90'}).text
            ]
        )
        
        # Defensive Actions
        defensive_actions_table = soup_player.find('div', id='all_stats_defense').find('tbody').find_all('tr')
        res5 = defensive_actions_table[-1]
        cv_player.extend(
            [
            res5.find('td', {'data-stat': 'tackles'}).text,
            res5.find('td', {'data-stat': 'tackles_won'}).text,
            res5.find('td', {'data-stat': 'challenges'}).text,
            res5.find('td', {'data-stat': 'challenges_lost'}).text,
            res5.find('td', {'data-stat': 'blocks'}).text,
            res5.find('td', {'data-stat': 'blocked_shots'}).text,
            res5.find('td', {'data-stat': 'blocked_passes'}).text,
            res5.find('td', {'data-stat': 'interceptions'}).text
            ]
        )
        
        # Possession
        possession_table = soup_player.find('div', id='all_stats_possession').find('tbody').find_all('tr')
        res6 = possession_table[-1]
        cv_player.extend(
            [
            res6.find('td', {'data-stat': 'touches'}).text,
            res6.find('td', {'data-stat': 'touches_def_pen_area'}).text,
            res6.find('td', {'data-stat': 'touches_def_3rd'}).text,
            res6.find('td', {'data-stat': 'touches_mid_3rd'}).text,
            res6.find('td', {'data-stat': 'touches_att_3rd'}).text,
            res6.find('td', {'data-stat': 'touches_att_pen_area'}).text,
            res6.find('td', {'data-stat': 'take_ons'}).text,
            res6.find('td', {'data-stat': 'take_ons_won_pct'}).text,
            res6.find('td', {'data-stat': 'take_ons_tackled_pct'}).text,
            res6.find('td', {'data-stat': 'carries'}).text,
            res6.find('td', {'data-stat': 'carries_progressive_distance'}).text,
            res6.find('td', {'data-stat': 'progressive_carries'}).text,
            res6.find('td', {'data-stat': 'carries_into_final_third'}).text,
            res6.find('td', {'data-stat': 'carries_into_penalty_area'}).text,
            res6.find('td', {'data-stat': 'miscontrols'}).text,
            res6.find('td', {'data-stat': 'dispossessed'}).text,
            res6.find('td', {'data-stat': 'passes_received'}).text,
            res6.find('td', {'data-stat': 'progressive_passes_received'}).text
            ]
        )
        
        # Miscellaneous Stats
        miscellaneous_stats_table = soup_player.find('div', id='all_stats_misc').find('tbody').find_all('tr')
        res7 = miscellaneous_stats_table[-1]
        cv_player.extend(
            [
            res7.find('td', {'data-stat': 'fouls'}).text,
            res7.find('td', {'data-stat': 'fouled'}).text,
            res7.find('td', {'data-stat': 'offsides'}).text,
            res7.find('td', {'data-stat': 'crosses'}).text,
            res7.find('td', {'data-stat': 'ball_recoveries'}).text,
            res7.find('td', {'data-stat': 'aerials_won'}).text,
            res7.find('td', {'data-stat': 'aerials_lost'}).text,
            res7.find('td', {'data-stat': 'aerials_won_pct'}).text
            ]
        )
        
        return cv_player
    
    else:
        print(f'Link {player} error')
        return [None] * 57

url = "https://fbref.com/en/"
table = [
    'Name', 'Nation', 'Team', 'Position', 'Age',
    'MP', 'Starts', 'Minutes',
    'Goals', 'Assists', 'CrdY', 'CrdR',
    'xG', 'xAG',
    'PrgC', 'PrgP', 'PrgR',
    'Gls_per90', 'Ast_per90', 'xG_per90', 'xGA_per90',
    'GA90', 'Save%', 'CS%', 'PK_Save%',
    'SoT%', 'SoT/90', 'G/sh', 'Dist',
    'Cmp', 'Cmp%', 'TotDist', 'Cmp%_S', 'Cmp%_M', 'Cmp%_L', 'KP', 'Pass_1/3', 'PPA', 'CrsPA', 'Pass_PrgP',
    'SCA', 'SCA90', 'GCA', 'GCA90',
    'Tkl', 'TklW', 'Chal_Att', 'Chal_Lost', 'Blocks', 'Block_Sh', 'Block_Pass', 'Int',
    'Touches', 'Def_Pen', 'Def_3rd', 'Mid_3rd', 'Att_3rd', 'Att_Pen', 'TO_Att', 'Succ%', 'Tkld%', 'Carries', 'Carry_ProDist', 'Carry_PrgC', 'Carry_1/3', 'CPA', 'Mis', 'Dis', 'Rec', 'Rec_PrgR',
    'Fls', 'Fld', 'Off', 'Crs', 'Recov', 'Aerial_Won', 'Aerial_Lost', 'Aerial_Won%'
]

data_rows = []

session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))

response = session.get(url)
time.sleep(1)

if response.status_code == 200:
    soup = bs(response.text, 'html.parser')
    link_premier_league = soup.find('a', href=True, string='Premier League')
    url_premier_league = 'https://fbref.com' + link_premier_league.get('href')
    
    response_premier_league = session.get(url_premier_league)
    time.sleep(1)
    
    if response_premier_league.status_code == 200:
        soup_premier_league = bs(response_premier_league.text, 'html.parser')
        url_clubs = []
        team_premier_league = soup_premier_league.find('table').find_all('td', {'data-stat': 'team'})
        for team in team_premier_league:
            link_team = team.find('a', href=True)
            url_team = 'https://fbref.com' + link_team.get('href')
            url_clubs.append([url_team, link_team.text])
        
        for url_club in url_clubs:
            response_club = session.get(url_club[0])
            time.sleep(1)
            
            if response_club.status_code == 200:
                soup_club = bs(response_club.text, 'html.parser')
                link_players = soup_club.find('tbody').find_all('tr')
                for player in link_players:
                    minutes = str(player.find('td', {'data-stat': 'minutes'}).text)
                    if not minutes:
                        continue
                    m = int(minutes.replace(',', ''))
                    if m < 90:
                        continue
                    
                    name = player.find('th').find('a').text
                    nation = player.find('td', {'data-stat': 'nationality'}).find('a').find('span', style=True).text
                    pos = player.find('td', {'data-stat': 'position'}).text
                    age = player.find('td', {'data-stat': 'age'}).text
                    playing_time = [
                        player.find('td', {'data-stat': 'games'}).text,
                        player.find('td', {'data-stat': 'games_starts'}).text,
                        minutes
                    ]

                    performance = [
                        player.find('td', {'data-stat': 'goals'}).text,
                        player.find('td', {'data-stat': 'assists'}).text,
                        player.find('td', {'data-stat': 'cards_yellow'}).text,
                        player.find('td', {'data-stat': 'cards_red'}).text
                    ]

                    expected = [
                        player.find('td', {'data-stat': 'xg'}).text,
                        player.find('td', {'data-stat': 'xg_assist'}).text
                    ]

                    progression = [
                        player.find('td', {'data-stat': 'progressive_carries'}).text,
                        player.find('td', {'data-stat': 'progressive_passes'}).text,
                        player.find('td', {'data-stat': 'progressive_passes_received'}).text
                    ]

                    per_90_minutes = [
                        player.find('td', {'data-stat': 'goals_per90'}).text,
                        player.find('td', {'data-stat': 'assists_per90'}).text,
                        player.find('td', {'data-stat': 'xg_per90'}).text,
                        player.find('td', {'data-stat': 'xg_assist_per90'}).text
                    ]
                    
                    link_player = player.find('th').find('a', href=True)
                    url_player = 'https://fbref.com' + link_player.get('href')
                    
                    data_rows.append(
                        [
                        name,
                        nation,
                        url_club[1],
                        pos,
                        age,
                        *playing_time,
                        *performance,
                        *expected,
                        *progression,
                        *per_90_minutes,
                        *get_player(url_player)
                        ]
                    )

            else:
                print(f'Link {url_club[0]} error')

    else:
        print(f'Link {url_premier_league} error')

else:
    print(f'Link {url} error')

df = pd.DataFrame(data_rows, columns=table)
df.fillna('N/a', inplace=True)
df = df.sort_values('Name')
df.to_csv('deadline-1/result.csv', index=True)