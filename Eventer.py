import random
import calendar
import datetime

class Interval:
    '''Holds groups of dates over a defined period'''
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.dates_taken = []
        self.events = []

    def __repr__(self):
        return f'{self.start} - {self.end}\n{self.events}\n'


class EventSeries:
    def __init__(self):
       pass 

    def interval_maker(self, interval_type):
        '''makes a series of intervals to fill the year'''
        intervals = []
        #
        #@TODO: This should be a config
        #
        interval_deets={
            'week': {
                'length':lambda: 7,
                'number_in_year':lambda: 52,
                'first_date':lambda: datetime.date.today() - datetime.timedelta(days=datetime.date.today().isoweekday() % 7)
                'last_date':lambda:datetime.date.today() - datetime.timedelta(days=datetime.date.today().isoweekday() % 7) + datetime.timedelta(days=6) 
            },
            'dbl_week': {
                'length':lambda: 14,
                'number_in_year':lambda: 26,
                'first_date':lambda: datetime.date.today() - datetime.timedelta(days=datetime.date.today().isoweekday()-7 % 7)
                'last_day':datetime.date.today() - datetime.timedelta(days=datetime.date.today().isoweekday()-7 % 7) + datetime.tmedelta(days=13)
             },
             'month': {
                 'length': 0
             },
             'year': {}
        }
        #
        # End Config
        #
        if interval_type not in interval_deets.keys():
            raise KeyError("The supplied interval type wasn't found")

        start= interval_deets[interval_type]['first_date']()
        end = interval_deets[interval_type]['last_date']()
        intervals.append( Interval(start, end) )

        for i in range(interval_deets[interval_type]['number_in_year']()-1):
            start = start + datetime.timedelta(days= interval_deets[interval_type]['length']())
            end = start + datetime.timedelta(days= interval_deets[interval_type]['length']()-1)
            intervals.append( Interval(start, end))

        return intervals

    def series_maker(self, frequency=0, interval_type='week', exclude=[], include=[]):
        # Create a year starting at the beginning of the prior interval
        year = self.interval_maker(interval_type)
        # Foreach interval in that year
        for i in year:
            #  Remove Exclude events
            if len(exclude):
                while exclude[0] <= i.end:
                    i.dates_taken.append(exclude.pop(0))
            #  Add Include events
            if len(include):
                while include[0] > i.end:
                    event = include.pop(0)
                    # Don't check against exclude, assume include is higher priority
                    i.dates_taken.append(event)
                    i.events.append(event)
                    # Block out skip days
                    for x in range(skip):
                        if event + datetime.timedelta(days=x) > i.end:
                           exclude.append(event + datetime.timedelta(days=x)) 
                        else:
                            i.dates_taken.append(event + datetime.timedelta(days=x))

                        i.dates_taken.append(event - datetime.timedelta(days=x))

            #Add remaining random events 
            event_candidate = i.start
            potential_events= []
            #populate a list with possible events
            while event_candidate <= i.end:
                if event_candidate not in i.dates_taken:
                    potential_events.append(event_candidate)
                    event_candidate= event_candidate + datetime.timedelta(days=1)

            #get random events from possible events and make it official
            while len(i.events) < frequency:
                e = random.choice(potential_events)
                potential_events.pop(potential_events.index(e))
                i.dates_taken.append(e)
                i.events.append(e)


        #The bad part is over
        return year


if __name__ == '__main__':

    e = EventSeries()

    #print([x for x in e.interval_maker('week')] )
    #print([x for x in e.interval_maker('dbl_week')] )
    print( [x for x in e.series_maker(2)] )


