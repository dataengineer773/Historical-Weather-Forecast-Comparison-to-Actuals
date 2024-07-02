# Historical Weather Forecast Comparison to Actuals
#  Initialize your weather report log file
# 1.1 Create a text file called rx_poc.log.
touch rx_poc.log

# 1.2 Add a header to your weather report.
# header=$(echo -e "year\tmonth\tday\thour\tobs_tmp\tfc_temp")
echo $header>rx_poc.log
# OR, more directly, using echo and redirection:
echo -e "year\tmonth\tday\thour\tobs_tmp\tfc_temp">rx_poc.log


#  Write a bash script that downloads the raw weather data, and extracts and loads the required data
# 2.1. Create a text file called rx_poc.sh and make it a bash script.
#! /bin/bash
# Make your script executable:
chmod u+x rx_poc.sh


# 2.2 Download today’s weather report from wttr.in:
today=$(date +%Y%m%d)
weather_report=raw_data_$today
# OR, more directly:
weather_report=raw_data_$(date +%Y%m%d)

# 2.2.2 Download the wttr.in weather report for Casablanca and save it with the filename you created:
city=Casablanca
curl wttr.in/$city --output $weather_report

# 2.3. Extract the required data from the raw data file and assign them to variables obs_tmp and fc_temp.
echo "There are    too    many spaces in this    sentence." | tr -s " "

# 2 _ xargs - can be used to trim leading and trailing spaces from a string.
# For example, to remove the spaces from the begining and the end of text:
echo " Never start or end a sentence with a space. " | xargs 

# 3_ rev - reverse the order of characters on a line of text:
echo ".sdrawkcab saw ecnetnes sihT" | rev
# You will find rev to be a useful operation to apply in combination with the cut command:
# print the last field of the string
echo "three two one" | rev | cut -d " " -f 1 | rev
# You will also find xargs to be a useful operation to apply in combination with the cut command:
# Unfortunately, this prints the last field of the string, which is empty:
echo "three two one " | rev | cut -d " " -f 1 | rev
# But if you trim the trailing space first, you get the expected result:
echo "three two one " | xargs | rev | cut -d " " -f 1 | rev


# Let’s now return to extracting the temperature data of interest:
grep °C $weather_report > temperatures.txt

# 2.3.1. Extract the current temperature, and store it in a shell variable called:
obs_tmp=$(head -1 temperatures.txt | tr -s " " | xargs | rev | cut -d " " -f2 | rev)

# 2.3.2. Extract tomorrow’s temperature forecast for noon, and store it in a shell variable called fc_tmp:
fc_temp=$(head -3 temperatures.txt | tail -1 | tr -s " " | xargs | cut -d "C" -f2 | rev | cut -d " " -f2 | rev)

# 2.4. Store the current hour, day, month, and year in corresponding shell variables:
hour=$(TZ='Morocco/Casablanca' date -u +%H) 
day=$(TZ='Morocco/Casablanca' date -u +%d) 
month=$(TZ='Morocco/Casablanca' date +%m)
year=$(TZ='Morocco/Casablanca' date +%Y)

# 2.5. Merge the fields into a tab-delimited record, corresponding to a single row in Table 1:
record=$(echo -e "$year\t$month\t$day\t$hour\t$obs_tmp\t$fc_temp")
echo $record>>rx_poc.log

### Schedule your bash script rx_poc.sh to run every day at noon local time:

#! /bin/bash
# create a datestamped filename for the raw wttr data:
today=$(date +%Y%m%d)
weather_report=raw_data_$today
# download today's weather report from wttr.in:
city=Casablanca
curl wttr.in/$city --output $weather_report
# use command substitution to store the current day, month, and year in corresponding shell variables:
hour=$(TZ='Morocco/Casablanca' date -u +%H) 
day=$(TZ='Morocco/Casablanca' date -u +%d) 
month=$(TZ='Morocco/Casablanca' date +%m)
year=$(TZ='Morocco/Casablanca' date +%Y)
# extract all lines containing temperatures from the weather report and write to file
grep °C $weather_report > temperatures.txt
# extract the current temperature 
obs_tmp=$(head -1 temperatures.txt | tr -s " " | xargs | rev | cut -d " " -f2 | rev)
# extract the forecast for noon tomorrow
fc_temp=$(head -3 temperatures.txt | tail -1 | tr -s " " | xargs | cut -d "C" -f2 | rev | cut -d " " -f2 |rev)
# create a tab-delimited record
# recall the header was created as follows:
# header=$(echo -e "year\tmonth\tday\thour_UTC\tobs_tmp\tfc_temp")
# echo $header>rx_poc.log
record=$(echo -e "$year\t$month\t$day\t$obs_tmp\t$fc_temp")
# append the record to rx_poc.log
echo $record>>rx_poc.log