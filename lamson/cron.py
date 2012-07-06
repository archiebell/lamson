from datetime import datetime, timedelta
import time
import logging

_cronTab = None
def getCronTab():
    global _cronTab
    if not _cronTab:
        _cronTab = CronTab()
        
    return _cronTab
    
# From http://stackoverflow.com/a/374207
class CronAllMatch(set):
    """Universal set - match everything"""
    def __contains__(self, item): return True

cronAllMatch = CronAllMatch()

def conv_to_set(obj):  # Allow single integer to be provided
    if isinstance(obj, (int,long)):
        return set([obj])  # Single item
    if not isinstance(obj, set):
        obj = set(obj)
    return obj

class CronEvent(object):
    def __init__(self, action, 
                       min=cronAllMatch, hour=cronAllMatch, 
                       day=cronAllMatch, month=cronAllMatch, dow=cronAllMatch, 
                       args=(), kwargs={}):
        self.mins = conv_to_set(min)
        self.hours= conv_to_set(hour)
        self.days = conv_to_set(day)
        self.months = conv_to_set(month)
        self.dow = conv_to_set(dow)
        
        self.action = action
        self.args = args
        self.kwargs = kwargs

    def matchtime(self, t):
        """Return True if this event should trigger at the specified datetime"""
        return ((t.minute     in self.mins) and
                (t.hour       in self.hours) and
                (t.day        in self.days) and
                (t.month      in self.months) and
                (t.weekday()  in self.dow))

    def check(self, t):
        if self.matchtime(t):
            logging.debug("Running action " + str(self.action) + " at " + str(time.time()))
            self.action(*self.args, **self.kwargs)
            
class CronTab(object):
    def __init__(self, *events):
        self.events = list(events)

    def add(self, e):
        logging.debug("Adding event " + str(e.action))
        self.events.append(e)
    def run(self):
        logging.debug("Entering cron loop")
        t=datetime(*datetime.now().timetuple()[:5])
        while 1:
            for e in self.events:
                e.check(t)

            t += timedelta(minutes=1)
            while datetime.now() < t:
                time.sleep(max(1, (t - datetime.now()).seconds))
                
def print_time():
    print "Printing time", time.time()
                
if __name__ == "__main__":
    c = getCronTab()
    c.add(CronEvent(print_time, range(0,59)))
    c.run()
