import time
import pandas as pd
import numpy as np

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
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    # while_loop keeps going until we get an answer that is within the range needed:
    # chicago, new york city, or washington
    while True:
        city = input("In what city would you like to get bikeshare data (Chicago, New York City, or Washington): ")

        # To account for possible capitalized first letters, I lower-cased the answer to see if it fits what
        # we need 
        if city.lower() not in ('chicago', 'new york city', 'washington'):
            print("Please enter one of the three choices please...")
        else:
            break

    # once we get here, we have the correct city and we will move on with filtering

    # get user input for month (all, january, february, ... , june)
    
    # this list is all the possible asnwers we can except to the month filter question
    months_list = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

    while True:
        month = input("Which month of bikeshare data do you need? (ie: January, February, All): ")

        if month.lower() not in months_list:
            print("Please enter either a month or 'All'...")

        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)

    weekday_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

    while True:
        day = input("Which weekday of bikeshare data do you need? (ie: Monday, tuesday, All, etc): ")

        if day.lower() not in weekday_list:
            print("Please enter either a weekday or 'All'...")

        else:
            break


    print('-'*40)
    return city.lower(), month.lower(), day.lower()





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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA.get(city))

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = pd.to_datetime(df['Start Time']).dt.month

    # Monday is 0, Tuesday is 1...Sunday is 6
    df['day-of-week'] = df['Start Time'].dt.dayofweek

    
    # filter by month if applicable
    if month != 'all':
    
    # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)

        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month+1]

    if day != 'all':

        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day)
        #filter by day of week to create the new dataframe
        df = df.loc[df['day-of-week'] == day]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("most common month: ")
    print(df.month.mode()[0])


    # display the most common day of week
    print("most common day of week: ")
    print(df['day-of-week'].mode()[0])

    # display the most common start hour

    df['hour'] = pd.to_datetime(df['Start Time']).dt.hour
    print('most common start hour: ')
    print(df.hour.mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("most common start station: ")
    print(df['Start Station'].mode()[0])

    # display most commonly used end station
    print("most common end station: ")
    print(df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print("most frequent combination of start station and end station trip:")
    combo = df.groupby(['Start Station','End Station']).size().nlargest(1).reset_index(name='count')
    print("Start Station: ")
    print(combo['Start Station'].iloc[0])
    print("End Station: ")
    print(combo['End Station'].iloc[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('total travel time: ')
    print(df['Trip Duration'].sum())


    # display mean travel time
    print('mean travel time: ')
    print(df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    print('Counts of user types: ')
    print(df['User Type'].value_counts().to_string(header=None))

    # Display counts of gender
    if 'Gender' in df.columns:
        print('Counts of gender: ')
        print(df['Gender'].value_counts().to_string(header=None))

    else:
        print('Sorry, no data provided on gender!')


    # Display earliest, most recent, and most common year of birth
    if 'Gender' in df.columns:
        print('Earliest birth year: ')
        print(int(df['Birth Year'].min()))

        print('Most recent birth year: ')
        print(int(df['Birth Year'].max()))

        print('Most common birth year: ')
        print(int(df['Birth Year'].mode()[0]))

    else:
        print('Sorry, no data provided on birth year!')

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

        count = 0
        n = 0

        while True:
            answer = input('\nWould you like to see 5 lines of raw data? Yes or no?.\n')

            if answer.lower() != 'yes':
                break

            while True:

                n = 1 # this marked that this 2nd while loop is used. 
                print(df[count:count+5])
                count = count + 5

                answer2 = input('\nWould you like to see next 5 lines of raw data? Yes or no?.\n')
            
                if answer2.lower() != 'yes':
                    break

            if n==1:
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
