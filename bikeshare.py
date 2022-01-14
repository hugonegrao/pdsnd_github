import datetime
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = {'jan': 1,
          'feb': 2,
          'mar': 3,
          'apr': 4,
          'may': 5,
          'jun': 6}

DAYS_OF_WEEK = {'monday': 0,
                'tuesday': 1,
                'wednesday': 2,
                'thursday': 3,
                'friday': 4,
                'saturday': 5,
                'sunday': 6}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city = ''
    dfilter = ''
    month = ''
    day = ''

    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while not (city == 'chicago' or city == 'new york city' or city == 'washington'):
        city = (input('Would you like to see data for Chicago, New York City or Washington?\n')).lower()


    while not (dfilter == 'month' or dfilter == 'day' or dfilter == 'both' or dfilter == 'none'):
        dfilter = (input('Would you like to see the data by month, day, both or not at all? Type "none" for no time filter\n')).lower()


        if(dfilter == 'month'):
            # get user input for month (all, january, february, ... , june)
            while not (month in MONTHS.keys()):
                month = (input('Would you like to see data for which month: Jan, Feb, Mar, Apr, May or Jun?\n')).lower()
                day = 'all'
            month = MONTHS.get(month)


        elif(dfilter == 'day'):
        # get user input for day of week (all, monday, tuesday, ... sunday)
            while not (day in DAYS_OF_WEEK.keys()):
                day = (input('Would you like to see data for which day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday?\n')).lower()
                month = 'all'
            day = DAYS_OF_WEEK.get(day)

        elif(dfilter == 'both'):
            while not (month in MONTHS.keys()):
                month = (input('Would you like to see data for which month: Jan, Feb, Mar, Apr, May or Jun?\n')).lower()
            month = MONTHS.get(month)

            while not (day in DAYS_OF_WEEK.keys()):
                day = (input('Would you like to see data for which day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday?\n')).lower()
            day = DAYS_OF_WEEK.get(day)

        elif(dfilter == 'none'):
            month = 'all'
            day = 'all'

    print('-'*40)
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
    df = pd.read_csv(CITY_DATA.get(city))
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    if (month == 'all'):
        month = None
    else:
        df = df[df['Start Time'].dt.month == int(month)]

    if (day == 'all'):
        day = None
    else:
        df = df[df['Start Time'].dt.weekday == int(day)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    try:
        most_common_month = df['Start Time'].dt.month.value_counts().idxmax()
        most_common_month_name = str([key  for (key, value) in MONTHS.items() if value == most_common_month])
        print("The most common month is: \n", most_common_month_name.title().strip("'[]'"))

    except:
        print("\nThere was no 'Start Time' column in the dataset\n")
        pass

    # display the most common day of week
    try:
        most_common_day_of_week = df['Start Time'].dt.weekday.value_counts().idxmax()
        most_common_day_of_week_name = str([key  for (key, value) in DAYS_OF_WEEK.items() if value == most_common_day_of_week])
        print("\nThe most common day of week is: \n", most_common_day_of_week_name.title().strip("'[]'"))

    except:
        print("\nThere was no 'Start Time' column in the dataset\n")
        pass

    # display the most common start hour
    try:
        most_common_start_hour = df['Start Time'].dt.hour.value_counts().idxmax()
        print("\nThe most common start hour is: \n", most_common_start_hour)

    except:
        print("\nThere was no 'Start Time' column in the dataset\n")
        pass

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    try:
        most_common_start_station = df['Start Station'].value_counts().idxmax()
        print('\nThe most commonly used start station is: \n', most_common_start_station)

    except:
        print("\nThere was no 'Start Station' column in the dataset\n")
        pass

    # display most commonly used end station
    try:
        most_common_end_station = df['End Station'].value_counts().idxmax()
        print('\nThe most commonly used end station is: \n', most_common_end_station)

    except:
        print("\nThere was no 'End Station' column in the dataset\n")
        pass

    # display most frequent combination of start station and end station trip
    try:
        most_frequent_combination_start_end_station = df.groupby(['Start Station','End Station']).size().idxmax()
        print('\nThe most frequent combination of start station and end station trip is: \n', most_frequent_combination_start_end_station)

    except:
        print("\nThere was no 'Start Station' and/or 'End Station' column in the dataset\n")
        pass

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    try:
        total_travel_time = df['Trip Duration'].sum()
        print('The total travel time is: \n', total_travel_time)

    except:
        print("\nThere was no 'Trip Duration' column in the dataset\n")
        pass

    # display mean travel time
    try:
        mean_travel_time = df['Trip Duration'].mean()
        print('The mean travel time is: \n', mean_travel_time)

    except:
        print("\nThere was no 'Trip Duration' column in the dataset\n")
        pass

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    try:
        user_type_count = df['User Type'].value_counts()
        print('The breakdown of users is: \n', user_type_count)

    except:
        print("\nThere was no 'User Type' column in the dataset\n")
        pass

    # Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print('\nThe breakdown of gender is: \n', gender_count)

    except:
        print("\nThere was no 'Gender' column in the dataset\n")
        pass

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year_of_birth = df['Birth Year'].min()
        most_recent_year_of_birth = df['Birth Year'].max()
        most_common_year_of_birth = df['Birth Year'].value_counts().idxmax()

        print('\nThe earliest year of birth is: ', earliest_year_of_birth)
        print('\nThe most recent year of birth is: ', most_recent_year_of_birth)
        print('\nThe most common year of birth is: ', most_common_year_of_birth)

    except:
        print("\nThere was no 'Birth Year' column in the dataset\n")
        pass

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """ Displays raw bikeshare data. """
    i = 0

    # Get the number of lines in the dataframe
    count_rows = df.shape[0]

    # Get the user input
    raw = input('\nWould you like to examine some individual trip data? Enter yes or no.\n').lower()
    pd.set_option('display.max_columns',200)

    while True:
        if (raw == 'no' or raw == 'n'):
            break
        elif (raw == 'yes' or raw == 'ye' or raw == 'y'):

            # Break the code if there is no more raw data to display
            if(i >= count_rows):
                break
            else:
                # Slice the dataframe to display next five rows
                print(df.iloc[i:i+5].to_string(index=False))
                raw = input('\nWould you like to continue examining some individual trip data? Enter yes or no.\n').lower()
                i += 5
        else:
            raw = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if not (restart.lower() == 'yes' or restart.lower() == 'ye' or restart.lower() == 'y'):
            print('Thank you for using this script')
            time.sleep(3)
            break


if __name__ == "__main__":
	main()
