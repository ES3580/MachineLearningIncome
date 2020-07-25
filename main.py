from datetime import datetime
import json
import requests

def update_data(endpoints):
  #for each endpoint, query and store data in file

  #build list of x dictionaries
  #ordered_data = [ {} for i in range(len(endpoints)) ]
  ordered_data = [ [] for i in range(len(endpoints)) ]
  print (ordered_data)

  #get current year
  current_year = datetime.now().year


  #make requests and store in dictionaries between 1922 and current year in 10yr incs
  while (current_year-9 > 1922):
    '''
    headers = {'Content-type': 'application/json'}
    data = json.dumps({"seriesid": endpoints,"startyear": str(current_year-9), "endyear": str(current_year)})
    p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
    words = p.text
    filename = 'p' + str(current_year) + '.txt'
    with open(filename,'w') as fout:
      fout.write(p.text)
      '''
    with open('p2020.txt','r') as fin:
      words = fin.read()
    json_data = json.loads(words)


    with open('temp.json', 'w') as fout:
      json.dump(json_data['Results']['series'], fout, indent=4)

    trunk_data = json_data['Results']['series']

    for i in range(len(endpoints)):
      print(endpoints[i])

      ordered_data[i].extend(trunk_data[i]['data'])
    current_year = current_year - 10


  
  for i in range(len(endpoints)):
    fout = open(endpoints[i], 'w')
    fout.write(ordered_data)
    fout.close()
  
  return



def main():
  #update the database given list of enpoints
  endpoints = ['CUUR0000SA0','SUUR0000SA0']
  update_data(endpoints)

  
  
main()
