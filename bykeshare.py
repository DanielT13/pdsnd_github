import pandas as pd
import time
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ('january', 'february', 'march', 'april', 'may', 'june')

weekdays = ('sunday', 'monday', 'tuesday', 'wednesday',
 'thursday', 'friday','saturday=')


def choice(prompt, choices=('y', 'n')):
    """Return a valid input from the user given an array of possible answers.
    """

    while True:
        choice = input(prompt).lower()
        # terminate the program if the input is end
        if choice == 'exit':
            raise SystemExit

        elif ',' not in choice:
            if choice in choices:
                break

        prompt = ("\nSomething is not right.Be sure to enter a valid option:\n>")

    return choice



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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['Start Hour'] = df['Start Time'].dt.hour
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def get_filters():
    """Ask user to specify city(ies) and filters, month(s) and weekday(s).

    Returns:
        (str) city - name of the city(ies) to analyze
        (str) month - name of the month(s) to filter
        (str) day - name of the day(s) of week to filter
    """
    print("\n--Enter exit to terminate the program if the input is end--\n")
    print("\n\nLet's explore some US bikeshare data!\n")

    while True:
        city = choice("\nWould you like to see data for "
                      "New York City, Chicago or Washington?\n",CITY_DATA)

        month = choice("\nFor which month you want to filter the data? Select"
        " from january to june\n>",months)

        day = choice("\nFor which weekday(s) do you want to filterdata? select"
        " from sunday to saturday\n>",weekdays)

        # confirm the user input
        confirmation = choice("\nPlease confirm your selection"
                              "\n\n City(ies): {}\n Month(s): {}\n Weekday(s)"
                              ": {}\n\n [y] Yes\n [n] No\n\n>"
                              .format(city, month, day))
        if confirmation == 'y':
            break
        else:
            print("\nLet's try this again!")

    print('-'*40)
    return city, month, day


def time_stats(df):
    """Display statistics on the most frequent times of travel."""

    print('\nDisplaying the statistics on the most frequent times of '
          'travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print('The month with the most travels is: ' +
          str(months[most_common_month-1]).title() + '.')

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('The most common day of the week is: ' +
          str(most_common_day) + '.')

    # display the most common start hour
    most_common_hour = df['Start Hour'].mode()[0]
    print('The most common start hour is: ' +
          str(most_common_hour) + '.')

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)


def station_stats(df):
    """Display statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = str(df['Start Station'].mode()[0])
    print("The most common start station is: " +
          most_common_start_station)

    # display most commonly used end station
    most_common_end_station = str(df['End Station'].mode()[0])
    print("The most common start end is: " +
          most_common_end_station)

    # display most frequent combination of start station and
    # end station trip
    df['Start-End Combination'] = (df['Start Station'] + ' - ' +
                                   df['End Station'])
    most_common_start_end_combination = str(df['Start-End Combination']
                                            .mode()[0])
    print("The most common start-end combination "
          "of stations is: " + most_common_start_end_combination)

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)


def trip_duration_stats(df):
    """Display statistics on the total and average trip duration."""


    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time = (str(int(total_travel_time//86400)) +
                         'd ' +
                         str(int((total_travel_time % 86400)//3600)) +
                         'h ' +
                         str(int(((total_travel_time % 86400) % 3600)//60)) +
                         'm ' +
                         str(int(((total_travel_time % 86400) % 3600) % 60)) +
                         's')
    print('The total travel time is : ' +
          total_travel_time + '.')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time = (str(int(mean_travel_time//60)) + 'm ' +
                        str(int(mean_travel_time % 60)) + 's')
    print("The mean travel time is : " +
          mean_travel_time + ".")

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)


def user_stats(df, city):
    """Display statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts().to_string()
    print("counts for user types:")
    print(user_types)

    # Display counts of gender
    try:
        gender_distribution = df['Gender'].value_counts().to_string()
        print("\nCounts for each gender:")
        print(gender_distribution)
    except KeyError:
        print("There is no data of user genders for {}."
              .format(city.title()))

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = str(int(df['Birth Year'].min()))
        print("\nThe earliest common year of birth is: " + earliest_birth_year)
        most_recent_birth_year = str(int(df['Birth Year'].max()))
        print("The most recent common year of birth is: " + most_recent_birth_year)
        most_common_birth_year = str(int(df['Birth Year'].mode()[0]))
        print("The most common  year of birth is: " + most_common_birth_year)
    except:
        print("There is no data of birth year for {}."
              .format(city.title()))

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)



def raw_data(df, mark_place):
    """Display 5 line of sorted raw data each time."""

    print("\nYou opted to view raw data.")

    # this variable holds where the user last stopped
    if mark_place > 0:
        last_place = choice("\nWould you like to continue from where you "
                            "stopped last time? \n [y] Yes\n [n] No\n\n>")
        if last_place == 'n':
            mark_place = 0

            # sort data by column
    if mark_place == 0:
        sort_df = choice("\nDisplay  5 rows of the dataframe. Sort data "
                        "by column. "
                         "Press Enter to view unsorted data."
                         "\n \n [1] Start Time\n [2] End Time\n "
                         "[3] Trip Duration\n [4] Start Station\n "
                         "[5] End Station\n\n>",
                         ('1', '2', '3', '4', '5', ''))


        if sort_df == '1':
            df = df.sort_values(['Start Time'])
        elif sort_df == '2':
            df = df.sort_values(['End Time'])
        elif sort_df == '3':
            df = df.sort_values(['Trip Duration'])
        elif sort_df == '4':
            df = df.sort_values(['Start Station'])
        elif sort_df == '5':
            df = df.sort_values(['End Station'])
        elif sort_df == '':
            pass

    # each loop displays 5 lines of raw data
    while True:
        for i in (mark_place,(df.index)):
            print("\n")
            print(df.iloc[mark_place:mark_place+5].to_string())
            print("\n")
            mark_place += 5

            if choice("Do you want to see more data data?"
                      "\n\n[y]Yes\n[n]No\n\n>") == 'y':
                continue
            else:
                break
        break

    return mark_place


def main():

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        mark_place = 0
        while True:
            select_data = choice("\nSelect the information you would "
                                 "like to obtain.\n\n [1] Time Stats\n [2] "
                                 "Station Stats\n [3] Trip Duration Stats\n "
                                 "[4] User Stats\n [5] Display Raw Data\n "
                                 "[6] Restart\n\n>",('1', '2', '3', '4', '5', '6'))

            if select_data == '1':
                time_stats(df)
            elif select_data == '2':
                station_stats(df)
            elif select_data == '3':
                trip_duration_stats(df)
            elif select_data == '4':
                user_stats(df, city)
            elif select_data == '5':
                mark_place = raw_data(df, mark_place)
            elif select_data == '6':
                break

        restart = choice("\nWould you like to restart?\n\n[y]Yes\n[n]No\n\n>")
        if restart.lower() != 'y':
            break

if __name__ == "__main__":
    main()
