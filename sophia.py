#!/usr/bin/env python
# coding: utf-8

# In[27]:


from flask import Flask, make_response, request, jsonify
import requests

# build the flask app
app = Flask(__name__)

# definition of the results function
def results():
    req = request.get_json(force=True)
    action = req.get('queryResult').get('action')
    country = req.get('queryResult').get('parameters').get('geo-country')
    city = req.get('queryResult').get('parameters').get('geo-city')
    print(country)
    print(req)
    name = req.get('queryResult').get('intent').get('displayName')
    print(name)
    
    if name == "corona-cases":
        print('triggered')
        
        url = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/latest_stat_by_country.php"
        querystring = {"country":country}
        headers = {'x-rapidapi-host': "coronavirus-monitor.p.rapidapi.com",'x-rapidapi-key': "ed82524e9fmsh1763d34ca4333f4p186c05jsnacbb4da30812"            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        stat = response.json()
        stats = stat["latest_stat_by_country"][0]
        country = stats['country_name']
        total_cases = stats['total_cases']
        active_cases = stats['active_cases']
        total_deaths = stats['total_deaths']
        total_recovered = stats['total_recovered']
        total_tests = stats['total_tests']
        print('Corona updates In '+country+ ': '+' '+'Total no of cases: '+total_cases +' '+'Active Cases: '+active_cases+' '+'Total Deaths: '+total_deaths+' '+'Total recovered: '+total_recovered+' '+'Total tests done: '+total_tests)
        
        result = {} # an empty dictionary

        # fulfillment text is the default response that is returned to the dialogflow request
        result["fulfillmentText"] = 'Corona updates In '+ country+ ': '+' '+'Total no of cases: '+total_cases +' '+'Active Cases: '+active_cases+' '+'Total Deaths: '+total_deaths+' '+'Total recovered: '+total_recovered+' '+'Total tests done: '+total_tests

        # jsonify the result dictionary
        # this will make the response mime type to application/json
        result = jsonify(result)

        # return the result json
        return make_response(result)    
                                

    if name == "Weather":
    
        url = "https://community-open-weather-map.p.rapidapi.com/find"

        querystring = {"type":"link%2C accurate","units":"imperial%2C metric","q":city}

 
        headers = {
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
        'x-rapidapi-key': "7ed96bbd91msh12a34d07591d143p1de796jsn714ce64fe29c"
        }

 
        response = requests.request("GET", url, headers=headers, params=querystring)


        x = response.json()


        temperature = str(round(x["list"][0]["main"]["temp"] -273.15,2))
        humidity = str(x["list"][0]["main"]["humidity"])
        description = str(x["list"][0]['weather'][0]['description'])
        
        result = {} # an empty dictionary

        # fulfillment text is the default response that is returned to the dialogflow request
        result["fulfillmentText"] = 'In ' +city + ' Temperature is: ' +temperature +' degrees, '+'Humidity is: '+ humidity + ' and the weather is '+description
                            
        # jsonify the result dictionary
        # this will make the response mime type to application/json
        result = jsonify(result)

        # return the result json
        return make_response(result)
        
        
        
    
                                #"HTML": 'In ' +city + ' Temperature is: ' +temperature +' degrees, '+'Humidity is: '+ humidity + ' and the weather is '+description
                            
 
        
    if name == "OR_top_5_countries":
        url = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/cases_by_country.php"
        headers = {
        'x-rapidapi-host': "coronavirus-monitor.p.rapidapi.com",
        'x-rapidapi-key': "ed82524e9fmsh1763d34ca4333f4p186c05jsnacbb4da30812"
        }


        response = requests.request("GET", url, headers=headers)

        top = response.json()

        c0=top['countries_stat'][0]['country_name']
        t0=top['countries_stat'][0]['cases']

        c1=top['countries_stat'][1]['country_name']
        t1=top['countries_stat'][1]['cases']

        c2=top['countries_stat'][2]['country_name']
        t2=top['countries_stat'][2]['cases']

        c3=top['countries_stat'][3]['country_name']
        t3=top['countries_stat'][3]['cases']
        c4=top['countries_stat'][4]['country_name']
        t4=top['countries_stat'][4]['cases']
        
        result = {} # an empty dictionary

        # fulfillment text is the default response that is returned to the dialogflow request
        result["fulfillmentText"] = "Top 5 countries with total no of cases:"+' '+ "1. "+c0+" "+"-"+" "+t0+ " "+"2. "+c1+" "+"-"+" "+t1+" "+"3. "+c2+" "+"-"+" "+t2+" "+"4. "+c3+" "+"-"+" "+t3+" "+"5. "+c4+" "+"-"+" "+t4
               
        # jsonify the result dictionary
        # this will make the response mime type to application/json
        result = jsonify(result)

        # return the result json
        return make_response(result)        
        #"HTML":"Top 5 countries with total no of cases:"+'<br>'+ "1. "+c0+" "+"-"+" "+t0+ "<br>"+"2. "+c1+" "+"-"+" "+t1+"<br>"+"3. "+c2+" "+"-"+" "+t2+"<br>"+"4. "+c3+" "+"-"+" "+t3+"<br>"+"5. "+c4+" "+"-"+" "+t4
               
        
    
# default route for the webhook
# it accepts both the GET and POST methods
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # calling the result function for response
    return results()


# call the main function to run the flask app
if __name__ == '__main__':
    app.run(debug = False)

