# DSC 510
# Week 12
# Programming Assignment Week 12
# Author Sucharitha Puppala
# 05/31/2022

# Change#:0
# Change(s) Made: Original Version
# Date of Change: 05/31/2022
# Author: Sucharitha Puppala
# Change Approved by:
# Date Moved to Production: 05/31/2022


import requests
from requests.exceptions import HTTPError


# Accepting the user choice and validating the input
def valUserChoice():
    val = True
    while val:
        try:
           userChoice = input("Would you like to lookup weather data by US City or zip code.\nEnter 1 for US City 2 for zip: ")
           val = False
        except:
            print('The input you entered was not a number. Please enter a valid Number.')
            val = True
    return userChoice


# Accepting the user choice of units and validating the input
def valUnitsChoice():
    val = True
    while val:
        try:
           userUnitsChoice = input("Would you like to view temps in Fahrenheit, Celsius, or Kelvin.\nEnter 'F' for Fahrenheit, 'C' for Celsius, 'K' for Kelvin: ")
           val = False
        except:
            print('The input you entered was not a String. Please enter a valid value.')
            val = True
    return userUnitsChoice


# Validating the input choice of City or Zip
def valInput(userChoice):
    while userChoice != '1' and userChoice != '2':
        userChoice = input("Please enter a valid value to continue. It should be either (1/2):")
    if userChoice == '1' or userChoice == '2':
        valStat = 'S'
    return valStat, userChoice


# Validating the input choice of units for temperature
def valUnitsInput(userUnitsChoice):
    while userUnitsChoice != 'F' and userUnitsChoice != 'C' and userUnitsChoice != 'K' and userUnitsChoice != 'c' and userUnitsChoice != 'k' and userUnitsChoice != 'f':
        userUnitsChoice = input("Please enter a valid value to continue. It should be either (F/K/C):")
    if userUnitsChoice == 'F' or userUnitsChoice == 'f' or userUnitsChoice == 'C' or userUnitsChoice == 'c' or userUnitsChoice == 'K' or userUnitsChoice == 'k':
        valUntStat = 'S'
    return valUntStat, userUnitsChoice


# Printing the weather data
def prettyPrintFormat(city_name, current_temp, temp_min, temp_max, pressure, humidity, mainClimate, description, errorReason):
    if errorReason == '':
        print('-'*50)
        print('Current Weather Conditions For {:11}'.format(city_name).title())
        print('-'*50)
        print('Current Temp     :{:11} degress'.format(current_temp))
        print('High Temp        :{:11} degress'.format(temp_min))
        print('Low Temp         :{:11} degress'.format(temp_max))
        print('Pressure         :{:11} hpa'.format(pressure))
        print('Humidity         :{:11} %'.format(humidity))
        print('Cloud Cover      :{:>12} '.format(mainClimate).title())
        print('Description      :{:>16} '.format(description).title())
        print('-'*50)
    else:
        print('-'*50)
        print('Error Reason     :{:>16} '.format(errorReason).title())
        print('-'*50)


# Validate the input to check whether the retry option provided is valid or not
def valContinueInput(operation):
    while operation != 'Y' and operation != 'N' and operation != 'y' and operation != 'n':
        operation = input("Please enter a valid value to continue. It should be either (Y/N):")
    if operation == 'Y' or operation == 'N' or operation == 'y' or operation == 'n':
        valContStat = 'S'
    return valContStat, operation


# Accepting the city/state/zip validating the input
def validateName(attrName):
    while attrName == '':
        attrName = input("Please enter a valid value to continue. It cannot be blank/null:")
    if attrName != '':
        valNameStat = 'S'
    return valNameStat, attrName


def getGeoCodeData(option, cityOrZip, stateName):
    city_name = ''
    state = ''
    latitude = ''
    longitude = ''
    errorReason = ''
    if option == "q":
        url = "http://api.openweathermap.org/geo/1.0/direct?q="+cityOrZip+","+stateName+",US&limit=1&appid=b601d146da5bf0572dafa84f54b5ebda"
    if option == "zip":
        url = "http://api.openweathermap.org/geo/1.0/zip?zip="+cityOrZip+",US&appid=b601d146da5bf0572dafa84f54b5ebda"
    error = "N"
    try:
        r = requests.get(url)
        r.raise_for_status()
    except HTTPError as http_err:
        error = "Y"
    except Exception as err:
        error = "O"
        errorReason = 'Connection Error Occured'
    if error == 'O':
        print(errorReason)
    else:
        events = r.json()
        if error == 'Y':
            for key, value in events.items():
                if key == 'message':
                    errorReason = value
        else:
            if option == "q":
                if not events:
                    errorReason = 'No Details found for the provided input'
                else:
                    for key, value in events[0].items():
                        if key == 'name':
                            city_name = value
                        if key == 'state':
                            state = value
                        if key == 'lat':
                            latitude = value
                        if key == 'lon':
                            longitude = value
            if option == "zip":
                city_name = events['name']
                latitude = events['lat']
                longitude = events['lon']
    return city_name, latitude, longitude, state, errorReason


# populating weather conditions into variables
def getWeatherCondwithUnits(latitude, longitude, userUnitsChoice):
    errorReason = ''
    city_name = ''
    current_temp = ''
    temp_min = ''
    temp_max = ''
    pressure = ''
    humidity = ''
    description = ''
    mainClimate = ''
    if userUnitsChoice == 'C' or userUnitsChoice == 'c':
        userUnitsChoice = "&units=metric"
    elif userUnitsChoice == 'F' or userUnitsChoice == 'f':
        userUnitsChoice = "&units=imperial"
    else:
        userUnitsChoice = ''
    latitude = str(latitude)
    longitude = str(longitude)
    url = "http://api.openweathermap.org/data/2.5/weather?lat="+latitude+"&lon="+longitude+"&appid=b601d146da5bf0572dafa84f54b5ebda"+userUnitsChoice
    error = "N"
    try:
        r = requests.get(url)
        r.raise_for_status()
    except HTTPError as http_err:
        error = "Y"
    except Exception as err:
        error = "O"
        errorReason = 'Connection Error Occured'
    if error == 'O':
        print(errorReason)
    else:
        events = r.json()
        if error == 'Y':
            for key, value in events.items():
                if key == 'message':
                    errorReason = value
        else:
            city_name = events['name']
            for weathercond in events['main']:
                if weathercond == 'temp':
                    current_temp = events['main'][weathercond]
                if weathercond == 'temp_min':
                    temp_min = events['main'][weathercond]
                if weathercond == 'temp_max':
                    temp_max = events['main'][weathercond]
                if weathercond == 'pressure':
                    pressure = events['main'][weathercond]
                if weathercond == 'humidity':
                    humidity = events['main'][weathercond]
            for weathercond in events['weather']:
                for details in weathercond:
                    if details == 'description':
                        description = weathercond[details]
                    if details == 'main':
                        mainClimate = weathercond[details]
    return city_name, current_temp, temp_min, temp_max, pressure, humidity, mainClimate, description, errorReason


# Main function which will call the weather function with the values provided by user
def processinglogic(valStat, userChoice):
    if valStat == "S":
        if userChoice == '1':
            option = "q"
            cityName = input("Please enter the City Name: ")
            valNameStat, cityName = validateName(cityName)
            stateName = input("Please enter the state abbreviation: ")
            valNameStat, stateName = validateName(stateName)
            if valNameStat == "S":
                userUnitsChoice = valUnitsChoice()
                valUntStat, userUnitsChoice = valUnitsInput(userUnitsChoice)
                if valUntStat == "S":
                    city_name, latitude, longitude, stateName, errorReason = getGeoCodeData(option, cityName, stateName)
                    city_name, current_temp, temp_min, temp_max, pressure, humidity, mainClimate, description, errorReason = getWeatherCondwithUnits(latitude, longitude, userUnitsChoice)
        elif userChoice == '2':
            option = "zip"
            stateName = ''
            zipCode = input("Please enter the Zip Code: ")
            valNameStat, zipCode = validateName(zipCode)
            if valNameStat == "S":
                userUnitsChoice = valUnitsChoice()
                valUntStat, userUnitsChoice = valUnitsInput(userUnitsChoice)
                if valUntStat == "S":
                    cityName,  latitude, longitude, stateName, errorReason = getGeoCodeData(option, zipCode, stateName)
                    city_name, current_temp, temp_min, temp_max, pressure, humidity, mainClimate, description, errorReason = getWeatherCondwithUnits(latitude, longitude, userUnitsChoice)
    return city_name, current_temp, temp_min, temp_max, pressure, humidity, mainClimate, description, errorReason


def main():
    # Initialising Welcome Message to Customer
    welcomeMsg = 'Welcome to the Weather App!'
    # Displaying Welcome Message to Customer
    print(welcomeMsg)
    userChoice = valUserChoice()
    valStat, userChoice = valInput(userChoice)
    city_name, current_temp, temp_min, temp_max, pressure, humidity, mainClimate, description, errorReason = processinglogic(valStat, userChoice)
    prettyPrintFormat(city_name, current_temp, temp_min, temp_max, pressure, humidity, mainClimate, description, errorReason)
    # Asking the Customer to provide whether to continue or not
    operation = input("Would you like to perform another weather lookup? (Y/N):")
    valContStat, operation = valContinueInput(operation)
    if valContStat == 'S':
        itr = 1
        # Checking for Sentinel value to break the while loop
        while operation != 'N' and operation != 'n':
            if valContStat == 'S' and (operation == 'Y' or operation == 'y'):
                if itr == 1:
                    userChoice = valUserChoice()
                    valStat, userChoice = valInput(userChoice)
                    city_name, current_temp, temp_min, temp_max, pressure, humidity, mainClimate, description, errorReason = processinglogic(valStat,userChoice)
                    prettyPrintFormat(city_name, current_temp, temp_min, temp_max, pressure, humidity, mainClimate, description, errorReason)
                operation = 'N'
                # Asking the Customer to provide whether to continue or not
                operation = input("Would you like to perform another weather lookup? (Y/N):")
                valContStat, operation = valContinueInput(operation)
                if valContStat == 'S' and (operation == 'Y' or operation == 'y'):
                    userChoice = valUserChoice()
                    valStat, userChoice = valInput(userChoice)
                    city_name, current_temp, temp_min, temp_max, pressure, humidity, mainClimate, description, errorReason= processinglogic(valStat,userChoice)
                    prettyPrintFormat(city_name, current_temp, temp_min, temp_max, pressure, humidity, mainClimate, description, errorReason)
                    itr = 2


if __name__ == "__main__":
     main()
