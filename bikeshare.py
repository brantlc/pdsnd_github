import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'none']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day_of_week - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington)
    city = input("Choose a city (Chicago, New York City, or Washington):\n").lower()

    while city not in CITY_DATA:
        city = input("Please type Chicago, New York City, or Washington.\n").lower()

    # get user input for month (all, january, february, ... , june)
    month = input("Choose a month from January to June to filter by, or choose none:\n").lower()

    while month not in months:
        month = input("Please type a month name or none.\n").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_of_week = input("Choose a day of the week to filter by, or choose none. Sunday is 0 and Saturday is 6.\n")\
        .lower()

    digit_days = ('0', '1', '2', '3', '4', '5', '6', 'none')
    while day_of_week not in digit_days:
        day_of_week = input("Please type a number between 0 (Sunday) and 6 (Saturday) or none.\n")

    print('-'*40)
    return city, month, day_of_week


def load_data(city, month, day_of_week):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "none" to apply no month filter
        (str) day_of_week - name of the day of week to filter by, or "none" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day of week'] = df['Start Time'].dt.weekday
    # filter by month if applicable
    if month != 'none':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day_of_week != 'none':
        # filter by day of week to create the new dataframe
        df = df[df['day of week'] == int(day_of_week)]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # find the mode of month and convert it to a string
    month_index = df['month'].mode()[0]
    popular_month = months[month_index - 1].title()

    # display the most common month
    print('Month: ', popular_month)

    # find the mode of day and convert it to a string
    day = df['day of week'].mode()[0]
    popular_day = days[day - 1].title()

    # display the most common day of week
    print('Day: ', popular_day)

    # extract hour from Start Time and find the mode of it
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]

    # display the most common start hour
    print('Hour: {}00'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # find and display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('Start: ', popular_start)

    # find and display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('End: ', popular_end)

    # create trip column from Start Station and End Station
    df['trip'] = df['Start Station'] + ' to ' + df['End Station']

    # find and display most frequent combination of start station and end station trip
    popular_trip = df['trip'].mode()[0]
    print('Trip: ', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # convert End Time to datetime so that Start Time can be subtracted from it to create trip time column and find the
    # sum
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['trip time'] = df['End Time'] - df['Start Time']
    total_time = df['trip time'].sum()

    # display total travel time
    print('The total travel time was: ', total_time)

    # find and display mean travel time
    mean_time = df['trip time'].mean()
    print('The average travel time was: ', mean_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # find and display counts of user types
    type_counts = df['User Type'].value_counts()
    print('The counts of each user type were:\n', type_counts)

    # find and display counts of gender
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print('\nThe counts of each gender were:\n', gender_counts)
    else:
        print('\nThere is no gender data for this city.')

    # find and display oldest, youngest, and most common age
    if 'Birth Year' in df:
        oldest = int(2020 - df['Birth Year'].min())
        youngest = int(2020 - df['Birth Year'].max())
        popular_age = int(2020 - df['Birth Year'].mode()[0])
        print('\nThe oldest user was {} years old.'.format(oldest))
        print('The youngest user was {} years old.'.format(youngest))
        print('The most common age of users was: ', popular_age)
    else:
        print('\nThere is no age data for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(city):
    """
    Loads raw data for the specified city and outputs 5 lines at a time.

    Args:
        (str) city - name of the city to analyze
    """
    # open csv file
    with open(CITY_DATA[city]) as f:

        # ask user if they'd like to see raw data
        see_data = input("Would you like to see the raw data? Y/N?\n").lower()

        # make sure we get a correct input from the user
        while see_data != 'n' and see_data != 'y':
            see_data = input("Please type Y for yes or N for no.\n").lower()

        # output 5 lines of data and ask user if they'd like to see more
        while see_data == 'y':
            print(f.readline())
            print(f.readline())
            print(f.readline())
            print(f.readline())
            print(f.readline())
            see_data = input('Would you like to see more lines? Y/N?\n').lower()
            while see_data != 'n' and see_data != 'y':
                see_data = input("Please type Y for yes or N for no.\n").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # check for empty dataframe
        if df.empty:
            print("\nThere is no data when filtering this way.")
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            raw_data(city)

        restart = input('\nWould you like to restart? Enter y or n.\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
