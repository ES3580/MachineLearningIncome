from datetime import datetime
import json
import requests
import pandas as pd
import xlsxwriter

def update_data(endpoints):
  #for each endpoint, query and store data in file

  #build list of x dictionaries
  #ordered_data = [ {} for i in range(len(endpoints)) ]
  ordered_data = [ [] for i in range(len(endpoints)) ]
  print (ordered_data)

  #get current year
  current_year = datetime.now().year
  flag = 0

  #make requests and store in dictionaries between 1922 and current year in 10yr incs
  while (current_year-9 > 1979):
    
    headers = {'Content-type': 'application/XLSX'}
    data = json.dumps({"seriesid": endpoints,"startyear": str(current_year-9), "endyear": str(current_year)})
    p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
    words = p.text
    filename = 'first.text'
    with open(filename,'w') as fout:
      fout.write(p.text)

    return
    '''
    with open('p2020.txt','r') as fin:
      words = fin.read()
    json_data = json.loads(words)
    
    with open('temp.json', 'w') as fout:
      json.dump(json_data['Results']['series'], fout, indent=4)
    trunk_data = json_data['Results']['series']
    for i in range(len(endpoints)):
      print('adding endpoint: '+ endpoints[i] + ' ' + str(current_year))
      ordered_data[i].extend(trunk_data[i]['data'])
      if (flag == 1):
        print( ordered_data[0])
        
    current_year = current_year - 10
    flag = flag + 1
  
  for i in range(len(endpoints)):
    fout = open(endpoints[i], 'w')
    fout.write(str(ordered_data[i]))
    fout.close()
  '''
  return



def get_bls_data(series, start, end):
  '''
  headers = {'Content-Type': 'application/json'}
  data = json.dumps({"seriesid": series,"startyear":"%d" % (start), "endyear":"%d" % (end)})
  p = requests.post('https://api.bls.gov/publicAPI/v1/timeseries/data/', data=data, headers=headers)
  json_data = json.loads(p.text)
  '''
  with open('large_dump_json.json','r') as fin:
    json_data = json.load(fin)
  df_list = []
  try:
    
    for series in json_data['Results']['series']:
      df = pd.DataFrame()
      df_initial = pd.DataFrame(series)
      series_col = df_initial['seriesID'][0]
      for i in range(0, len(df_initial) - 1):
        df_row = pd.DataFrame(df_initial['data'][i])
        df_row['seriesID'] = series_col
        if 'code' not in str(df_row['footnotes']): 
          df_row['footnotes'] = ''
        else:
          df_row['footnotes'] = str(df_row['footnotes']).split("'code': '",1)[1][:1]
        df = df.append(df_row, ignore_index=True)
      df_list.append(df)

    return df_list
  except:
    json_data['status'] == 'REQUEST_NOT_PROCESSED'
    print('BLS API has given the following Response:', json_data['status'])
    print('Reason:', json_data['message'])



def main():
  #update the database given list of enpoints
  with open('income_endpoints.json','r') as fin:
    words = json.loads(fin.read())

  endpoints = []
  for ep in words['series']:
    endpoints.append(next(iter(ep)))

  print(endpoints)
  #update_data(endpoints)
  start = 2011
  end = 2020
  series = endpoints

  df_list = get_bls_data(series=series, start=start, end=end)
  writer = pd.ExcelWriter('bls2.xlsx', engine='xlsxwriter', options={'strings_to_numbers': True})
  for endpoint, df in zip(endpoints, df_list):

    df.to_excel(writer, sheet_name=endpoint, index=False)
    
  writer.save()
  
  
main()