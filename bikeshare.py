import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('ENTER THE CITY: ')
    while city not in ['chicago', 'new_york_city', 'washington']:
        city = input("CHOOSE BETWEEN chicago, new_york_city OR washington: ").lower()

    # get user input for month (all, january, february, ... , june)
    month = input('ENTER MONTH: ').lower()
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
        month = input('ENTER MONTH january, february, ... , june : ').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('ENTER DAY : ').lower()
    while day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        day = input('ENTER DAY monday, tuesday, ... sunday : ').lower()

    print('-' * 40)
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
    # load intended file into data frame
    df = pd.read_csv('{}.csv'.format(city))

    # convert columns od Start Time and End Time into date format yyyy-mm-dd
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month from Start Time into new column called month
    df['month'] = df['Start Time'].dt.month

    # filter by month

    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # extract day from Start Time into new column called month
    df['day_of_week'] = df['Start Time'].dt.day_name
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if df['month'].empty:
        print("No data available to determine the most common month.")
    else:
        most_common_month = df['month'].value_counts().idxmax()
        print("The most common month is: ", most_common_month)

    # display the most common day of week
    if df['day_of_week'].empty:
        print("No data available to determine the most common day of week.")
    else:
        most_common_day_of_week = df['day_of_week'].value_counts().idxmax()
        print("The most common day of week is: ", most_common_day_of_week)

    # display the most common start hour
    if df['Start Time'].empty:
        print("No data available to determine the most common start hour.")
    else:
        df['hour'] = df['Start Time'].dt.hour
        most_common_start_hour = df['hour'].value_counts().idxmax()
        print("The most common start hour is: ", most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    if df['Start Station'].empty:
        print("No data available to determine the most common start station.")
    else:
        most_common_start_station = df['Start Station'].value_counts().idxmax()
        print("The most common start station is: ", most_common_start_station)

    # display most commonly used end station
    if df['End Station'].empty:
        print("No data available to determine the most common end station.")
    else:
        most_common_end_station = df['End Station'].value_counts().idxmax()
        print("The most common end station is: ", most_common_end_station)

    # display most frequent combination of start station and end station trip
    if df.empty or 'Start Station' not in df.columns or 'End Station' not in df.columns:
        print("No data available to determine the most common trip.")
    else:
        most_common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
        print("The most common trip is from {} to {}".format(most_common_trip[0], most_common_trip[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum() / 3600.0
    print("total travel time in hours is: ", total_duration)

    # display mean travel time
    mean_duration = df['Trip Duration'].mean() / 3600.0
    print("mean travel time in hours is: ", mean_duration)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df.columns:
        user_types = df['User Type'].value_counts()
        print("Counts of user types:\n", user_types)
    else:
        print("No 'User Type' column in the data.")

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("Counts of gender:\n", gender_counts)
    else:
        print("No 'Gender' column in the data.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        birth_years = df['Birth Year'].dropna()
        if birth_years.empty:
            print("No available data for 'Birth Year'.")
        else:
            earliest_year_of_birth = int(birth_years.min())
            most_recent_year_of_birth = int(birth_years.max())
            most_common_year_of_birth = int(birth_years.mode()[0])

            print("Earliest year of birth:", earliest_year_of_birth)
            print("Most recent year of birth:", most_recent_year_of_birth)
            print("Most common year of birth:", most_common_year_of_birth)
    else:
        print("No 'Birth Year' column in the data.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def raw_data(df):
    """Displays the data due filtration.
    5 rows will add in each press"""
    print('press enter to see row data, press no to skip')
    x = 0
    while input() != 'no':
        x = x + 5
        print(df.head(x))


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
