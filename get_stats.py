import requests
import sys
import json

info = { 'summoner_id'  : '',
         'summoner_name': '',
         'champion'     : '',
         'region'       : '',
         'api_key'      : '',
}

def join_url(url):
   base_url = 'https://{region}.api.pvp.net/api/lol/'
   return base_url + url

def api_request(api_type):
   summoner_id = info['summoner_id']
   summoner_name = info['summoner_name']
   region = info['region']
   api_key = info['api_key']
   if api_type == "static":
      url = join_url('static-data/oce/v1.2/champion?api_key={api_key}')
      query = requests.get(url.format(region=region, api_key=api_key))
   if api_type == "stats":
      url = join_url('{region}/v1.3/stats/by-summoner/{summoner_id}/ranked?season=SEASON4&api_key={api_key}')
      query = requests.get(url.format(summoner_id=summoner_id, region=region, api_key=api_key))
   if api_type == "match_history":
      url = join_url('{region}/v2.2/matchhistory/{summoner_id}?rankedQueues=RANKED_SOLO_5x5&api_key={api_key}')
      query = requests.get(url.format(summoner_id=summoner_id, region=region, api_key=api_key))
   if api_type == "summoner":
      url = join_url('{region}/v1.4/summoner/by-name/{summoner_name}?api_key={api_key}')
      query = requests.get(url.format(region=region, summoner_name=summoner_name, api_key=api_key))
   if api_type == "division":
      url = join_url('{region}/v2.5/league/by-summoner/{summoner_id}/entry?api_key={api_key}')
      query = requests.get(url.format(region=region, summoner_id=summoner_id, api_key=api_key))
   return query

def get_summoner_id(name):
   try:
      summoner_id = api_request('summoner')
      summoner_id = summoner_id.json()[str(info['summoner_name'])]['id']
   except:
      sys.exit('summoner does not exist')
   return summoner_id

def get_champ_id(champ_name):
   try:
      champ_query = api_request('static')
   except:
      sys.exit('Champion does not exist')
   champ_query = champ_query.json()['data']
   for champion, id in champ_query.iteritems():
      if champ_name in str(champion).lower():
         return id['id']

def ranked_stats(champ_name):
   ranked_query = api_request('stats')
   ranked_query = ranked_query.json()
   champion = get_champ_id(champ_name)
   total_wins = 0
   for cur_champ in ranked_query['champions']:
      if int(cur_champ['id']) == int(champion):
         played = int(cur_champ['stats']['totalSessionsPlayed'])
         won = int(cur_champ['stats']['totalSessionsWon'])
         percent = float(won) / float(played) * 100
   for cur_champ in ranked_query['champions']:
      if int(cur_champ['id']) == 0:
         total_won = cur_champ['stats']['totalSessionsWon']
   return (str(total_won), str(int(round(percent))))

def win_count():
   match_history = api_request('match_history')
   match_history = match_history.json()
   counter = 0
   for i in match_history['matches']:
      did_win = i['participants'][0]['stats']['winner']
      if did_win is True:
         counter += 1
   return str(counter)

def get_division():
   division = api_request('division')
   division = division.json()
   tier = division[str(info['summoner_id'])][0]['tier']
   league = division[str(info['summoner_id'])][0]['entries'][0]['division']
   return (tier, league)

def pass_data(summon_name, champ_name):
   info['summoner_name'] = summon_name
   info['champion'] = champ_name
   info['summoner_id'] = get_summoner_id(info['summoner_name'])
   summoner = info['summoner_name']
   champion = str(champ_name)
   win_rate = ranked_stats(info['champion'])
   division = get_division()
   print '\t'.join([summoner, champion, win_rate[1] + "%", win_rate[0], str(win_count()), division[0], division[1]]).expandtabs(15)

def summoner_info():
   print '\t'.join(['Summoner', 'Champion', 'Win Rate', 'Total (All)',  'Last 10', 'Division', 'League']).expandtabs(15)
   with open('summoners.txt', 'r') as summoners:
      for summoner in summoners:
         summoner = summoner.split(' ')
         pass_data(summoner[0], summoner[1].strip('\n'))

summoner_info()
                                               
