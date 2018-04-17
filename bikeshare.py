import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
from termcolor import colored, cprint
import os

dirname = os.path.dirname(__file__)

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

MONTH_DICT = {
    'jan': 1,
    'feb': 2,
    'mar': 3,
    'apr': 4,
    'may': 5,
    'jun': 6,
    'all': 'all'
}

MONTH_LIST = [ None, 'January', 'February', 'March', 'April', 'May', 'June']

DOW_DICT = {
    'mon': 0,
    'tue': 1,
    'wed': 2,
    'thu': 3,
    'fri': 4,
    'sat': 5,
    'sun': 6,
    'all': 'all'
}

DOW_LIST = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def readable_hour(n):
    suffix = 'pm' if n >= 12 else 'am'
    return str(n%12) + suffix

# ordinal value taken from: https://stackoverflow.com/questions/9647202/ordinal-numbers-replacement
ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    greeting = '{: ^100}'.format('Hello! Let\'s explore some US bikeshare data!')
    cprint('*'*len(greeting), 'white', 'on_cyan')
    cprint(greeting, 'white', 'on_cyan', attrs=['bold'])
    cprint('*'*len(greeting), 'white', 'on_cyan')
    cprint('\n\n')
    cprint('Note, you may need to install some 3rd party packages for this program to work.', 'white', 'on_red')
    cprint('\n\n')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cprint('Which city would you like to get info for?', 'magenta')
    while True:
        city = input('Please choose Chicago, New York City, or Washington:\n').lower()
        if city in CITY_DATA.keys():
            cprint('\nIt looks like you want information for ' + city.title() + '. We can get that for you!\n', 'yellow')
            break
        else:
            cprint('\nI\'m sorry, I dont have info for that city. Please choose a valid city.\n', 'red')

    # get user input for month (all, january, february, ... , june)
    cprint('Which month would you like to get data for?', 'magenta')
    while True:
        month = input('Please choose: Jan, Feb, Mar, Apr, May, Jun, or All\n').lower()
        if month in MONTH_DICT.keys():
            cprint('\nIt looks like you want information for ' + month.title() + '. We can get that for you!\n', 'yellow')
            month = MONTH_DICT[month]
            break
        else:
            cprint('\nI\'m sorry, I dont have info for that month. Please choose a valid month.\n', 'red')


    # get user input for day of week (all, monday, tuesday, ... sunday)
    cprint('Which day of the week would you like to get data for?', 'magenta')
    while True:
        day = input('Please choose: Mon, Tue, Wed, Thu, Fri, Sat, Sun, or All\n').lower()
        if day in DOW_DICT.keys():
            cprint('\nIt looks like you want information for ' + day.title() + '. We can get that for you!\n', 'yellow')
            day = DOW_DICT[day]
            break
        else:
            cprint('\nI\'m sorry, I dont have info for that day. Please choose a valid day.\n', 'red')

    cprint('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    file_path = os.path.join(dirname, CITY_DATA[city])
    df = pd.read_csv(file_path)

    # Format start and end time strings into usable date objects
    df['Start Time'] = pd.to_datetime(df['Start Time'], format='%Y-%m-%d %H:%M:%S')
    df['End Time'] = pd.to_datetime(df['End Time'], format='%Y-%m-%d %H:%M:%S')

    # Filter by requested criteria, if provided
    if month == 'all' and day == 'all': 
        return df
    elif month == 'all':
        return df[(df['Start Time'].dt.dayofweek == day)]
    elif day == 'all':
        return df[(df['Start Time'].dt.month == month)]
    else:
        return df[ (df['Start Time'].dt.month == month) & (df['Start Time'].dt.dayofweek == day) ]


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    month_counts = df['Start Time'].dt.month.value_counts()
    month_max = month_counts.idxmax()

    # mean_count_month = 
    counts_day_of_week = df['Start Time'].dt.dayofweek.value_counts()
    counts_hour = df['Start Time'].dt.hour.value_counts()

    # display the most common month
    cprint('The most common month that people chose to ride:', 'white')
    cprint(MONTH_LIST[month_counts.idxmax()] + '\n', 'cyan', attrs=['bold'])

    # display the most common day of week
    cprint('The most common day that people chose to ride:', 'white')
    cprint(DOW_LIST[counts_day_of_week.idxmax()] + '\n', 'cyan', attrs=['bold'])

    # display the most common start hour
    cprint('The most common hour that people chose to ride:', 'white')
    cprint(readable_hour(counts_hour.idxmax()) + '\n', 'cyan', attrs=['bold'])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    top_start_stations = df['Start Station'].value_counts().keys().tolist()[:5]
    top_start_counts = df['Start Station'].value_counts().tolist()[:5]
    top_start = zip(top_start_stations, top_start_counts)

    top_end_stations = df['End Station'].value_counts().keys().tolist()[:5]
    top_end_counts = df['End Station'].value_counts().tolist()[:5]
    top_end = zip(top_start_stations, top_start_counts)

    df['Start End'] = df['Start Station'] + ' --> ' + df['End Station']
    top_start_end_stations = df['Start End'].value_counts().keys().tolist()[:5]
    top_start_end_counts = df['Start End'].value_counts().tolist()[:5]

    # display most commonly used start station
    cprint('The most popular start stations:', 'white')
    for i, (station, count) in enumerate(top_start):
        rank = ordinal(i+1)
        text = 'The {0}-most popular start station is {1} with {2} riders.'.format(rank, station, '{:,}'.format(count))
        cprint(text + '\n', 'cyan', attrs=['bold'])

    # display most commonly used end station
    cprint('The most popular end stations:', 'white')
    for i, (station, count) in enumerate(top_end):
        rank = ordinal(i+1)
        text = 'The {0}-most popular end station is {1} with {2} riders.'.format(rank, station, '{:,}'.format(count))
        cprint(text + '\n', 'cyan', attrs=['bold'])

    # display most frequent combination of start station and end station trip
    top_route_start = top_start_end_stations[0].split(' --> ')[0]
    top_route_end = top_start_end_stations[0].split(' --> ')[1]
    top_route_count = top_start_end_counts[0]
    text = 'The the most popular route was {0} to {1} with {2} riders.'.format(top_route_start, top_route_end, '{:,}'.format(top_start_end_counts[0]))
    cprint('The most popular route:', 'white')
    cprint(text + '\n', 'cyan', attrs=['bold'])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = str(timedelta(seconds=float(df['Trip Duration'].sum())))
    total_travel_time_days = total_travel_time.split(', ')[0]
    total_travel_time_hr = total_travel_time.split(', ')[1].split(':')[0]
    total_travel_time_min = total_travel_time.split(', ')[1].split(':')[1]
    total_travel_time_sec = total_travel_time.split(', ')[1].split(':')[2]

    mean_travel_time = str(timedelta(seconds=float(df['Trip Duration'].mean())))
    mean_travel_time_hr = mean_travel_time.split(':')[0]
    mean_travel_time_min = mean_travel_time.split(':')[1]
    mean_travel_time_sec = mean_travel_time.split(':')[2]
    # display total travel time
    cprint('Total travel time for all riders:', 'white')
    text = '{0} days, {1} hours, {2} minutes, and {3} seconds.'.format(str(total_travel_time_days), str(total_travel_time_hr), str(total_travel_time_min), str(total_travel_time_sec))
    cprint(text + '\n', 'cyan', attrs=['bold'])

    # display mean travel time
    cprint('Mean travel time for all riders:', 'white')
    text = '{0} hours, {1} minutes, and {2} seconds.'.format(str(mean_travel_time_hr), str(mean_travel_time_min), str(mean_travel_time_sec))
    cprint(text + '\n', 'cyan', attrs=['bold'])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    # Display counts of user types
    user_types = df['User Type'].value_counts().keys().tolist()[:5]
    user_types_count = df['User Type'].value_counts().tolist()[:5]
    top_user_types = zip(user_types, user_types_count)
    cprint('Riders by type:\n', 'white')
    for i, (t, count) in enumerate(top_user_types):
        rank = ordinal(i+1)
        text = 'The {0}-most common user type is {1} with {2} riders.'.format(rank, t, '{:,}'.format(count))
        cprint(text + '\n', 'cyan', attrs=['bold'])

    # Display counts of gender
    if 'Gender' in df:
        gender_types = df['Gender'].value_counts().keys().tolist()[:5]
        gender_types_count = df['Gender'].value_counts().tolist()[:5]
        top_gender_types = zip(gender_types, gender_types_count)
        cprint('Riders by gender:\n', 'white')
        for i, (t, count) in enumerate(top_gender_types):
            rank = ordinal(i+1)
            text = 'The {0}-most common gender is {1} with {2} riders.'.format(rank, t, '{:,}'.format(count))
            cprint(text + '\n', 'cyan', attrs=['bold'])
    else:
        cprint('Gender data not available for this city.\n', 'white')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        cprint('Riders by age:\n', 'white')

        dob_common = int(df['Birth Year'].mode())
        text = 'Born in {0} the most common rider age is {1}'.format(str(dob_common), str(datetime.now().year - dob_common))
        cprint(text + '\n', 'cyan', attrs=['bold'])

        dob_youngest = int(df['Birth Year'].max())
        text = 'Born in {0} the youngest rider age is {1}'.format(str(dob_youngest), str(datetime.now().year - dob_youngest))
        cprint(text + '\n', 'cyan', attrs=['bold'])

        dob_oldest = int(df['Birth Year'].min())
        text = 'Born in {0} the oldest rider age is {1}'.format(str(dob_oldest), str(datetime.now().year - dob_oldest))
        cprint(text + '\n', 'cyan', attrs=['bold'])
    else:
        cprint('Age data not available for this city.\n', 'white')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
