from algo.algo import api
import time

def main():
    done = None
    #Add some logging here...
    while True:
        #Get clock for all times of the day to check for the market open
        clock = api.get_clock()
        now = clock.timestamp
        #If the markets are open and done is not set, (Meaning the function hasnt
        # ran for the day), then check the clock for a time.
        if clock.is_open and not done:
            pass

            #mark as done
            done = now.strftime('%Y-%m-%d') #Should add some logging here...
        time.sleep(1)


if __name__ == '__main__':
    main()