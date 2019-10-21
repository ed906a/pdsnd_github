import time
import pandas as pd
import numpy as np
import json as json

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print()
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:        
        city = input('Choose the city you want to know the Bikeshare data: Chicago, New York City, Washington:\n').lower() 
        if city not in ('chicago', 'new york city', 'washington'):         
            print('Wrong Input,  please check your spelling then try again!\n')            
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)  
    while True:        
        month = input('Choose what month for Bikeshare data: January, February, March, April, May, June or All:\n').lower()
        if month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):         
            print('Wrong Input,  please check your spelling then try again!\n')           
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    
    while True:        
        day = input('Choose what day for Bikeshare data: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or All:\n').lower()
        if day not in ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all'):         
            print('Wrong Input,  please check your spelling then try again!\n')            
            continue
        else:
            break


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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

    df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    
    df['date']  = pd.to_datetime(df['Start Time'])
    df['month'] = df['date'].dt.month
    common_month = df['month'].mode()[0]
    print('Most common Month:', common_month)
    
    # display the most common day of week
    df['day of week'] = df['date'].dt.weekday_name
    common_day_of_week = df['day of week'].mode()[0]
    print('Most common Month:', common_day_of_week)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_start_hour = df['hour'].mode()[0]
    print('Most common Start Hour:', common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].value_counts().idxmax()
    print('Most commonly use Start Station:', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].value_counts().idxmax()
    print('Most commonly use End Station:', common_end_station)

    # display most frequent combination of start station and end station trip
    trip = df["Start Station"].astype(str) + " to " + df["End Station"].astype(str)
    trip.describe()
    frequent_trip = trip.describe()["top"]
    print('Most frequent combination of start&end station trip: ', frequent_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tot_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time: ', tot_travel_time)

    # display mean travel time
    tot_mean_time = df['Trip Duration'].mean()
    print('Mean Travel Time: ', tot_mean_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Count of User_type:\n',user_types)
    print()
    # Display counts of gender
    if 'Gender' not in df.columns:
        print('Sorry, there is no gender info for this city.')
    else:
        gender_count = df['Gender'].value_counts()
        print('Count of Gender:\n ',gender_count)
    print()
    # Display earliest, most recent, and most common year of birth
    print('Year of Birth Stats:')
    if 'Birth Year' not in df.columns:
        print('Sorry, there is no birth year info for this city.')
    else:
        min_birth = df['Birth Year'].min()
        print('Earliest year of birth:', int(min_birth))
        max_birth = df['Birth Year'].max()
        print('Most recent year of birth:', int(max_birth))
        common_birth = df['Birth Year'].mode()[0]
        print('Most common birth year', int(common_birth))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays raw bikeshare data."""
    row_length = df.shape[0]

    for i in range(0, row_length, 5):
        
        yes = input('\nDo you want to display atleast 5- raw data? Please input: \'yes\' or \'no\'\n ')
        if yes.lower() != 'yes':
            break
        row_data = df.iloc[i: i + 5].to_json(orient='records', lines=True).split('\n')
        for row in row_data:
            parsed_row = json.loads(row)
            json_row = json.dumps(parsed_row, indent=2)
            print(json_row)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print()
            print('Have a good one! Til\' next time!')
            break


if __name__ == "__main__":
	main()
