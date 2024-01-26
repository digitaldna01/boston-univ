#
# ps8pr2.py  (Problem Set 8, Problem 2)
#
# A class to represent calendar dates       
#

class Date:
    """ A class that stores and manipulates dates that are
        represented by a day, month, and year.
    """

    # The constructor for the Date class.
    def __init__(self, init_month, init_day, init_year):
        """ constructor that initializes the three attributes  
            in every Date object (month, day, and year)
        """
        # add the necessary assignment statements below
        self.month = init_month
        self.day = init_day
        self.year = init_year


    # The function for the Date class that returns a Date
    # object in a string representation.
    def __repr__(self):
        """ This method returns a string representation for the
            object of type Date that it is called on (named self).

            ** Note that this _can_ be called explicitly, but
              it more often is used implicitly via printing or evaluating.
        """
        s = '%02d/%02d/%04d' % (self.month, self.day, self.year)
        return s

    def is_leap_year(self):
        """ Returns True if the called object is
            in a leap year. Otherwise, returns False.
        """
        if self.year % 400 == 0:
            return True
        elif self.year % 100 == 0:
            return False
        elif self.year % 4 == 0:
            return True
        return False

    def copy(self):
        """ Returns a new object with the same month, day, year
            as the called object (self).
        """
        new_date = Date(self.month, self.day, self.year)
        return new_date

#### Put your code for problem 2 below. ####
    def advance_one(self):
        """ changes the called object so that it represents one calendar day 
            after the date that it originally represented.
        """
        days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self.day += 1
        if self.is_leap_year() == True:
            days_in_month[2] = 29
            if self.day > days_in_month[(self.month)]:
                if self.month == 12:
                    self.day = 1
                    self.month = 1
                    self.year += 1
                else:
                    self.day = 1
                    self.month += 1
        else:
            if self.day > days_in_month[(self.month)]:
                if self.month == 12:
                    self.day = 1
                    self.month = 1
                    self.year += 1
                else:
                    self.day = 1
                    self.month += 1
            
                
    def advance_n(self,n):
        """ changes the calling object so that it represents n calendar days
            after the date it originally represented.
        """
        for i in range(n + 1):
            if i > 0:
                self.advance_one()
            print(self)
    
    def __eq__(self, other):
        """ compare self and other and return True if they are identical and 
            return False if they are different
        """
        if self.month == other.month:
            if self.day == other.day:
                if self.year == other.year:
                    return True
        
        return False
    
    def is_before(self, other):
        """ returns True if the called object represents a calendar date that 
            occurs before the calendar date that is represented by other. If
            self and other represent the same day, or if self occurs after 
            other, the method should return False
        """
        if self.year < other.year:
            return True
        elif self.year == other.year:
            if self.month < other.month:
                return True
            elif self.month == other.month:
                if self.day < other.day:
                    return True
        return False
    
    def is_after(self, other):
        """ returns True if the calling object represents a calendar date that 
            occurs after the calendar date that is represented by other. If 
            self and other represent the same day, or if self occurs before 
            other, the method should return False
        """
        if self.year > other.year:
            return True
        elif self.year == other.year:
            if self.month > other.month:
                return True
            elif self.month == other.month:
                if self.day > other.day:
                    return True
        return False
    
    def days_between(self, other):
        """ returns an integer that represents the number of days between self
            and other
        """
        if self == other:
            return 0 
        self1 = self.copy()
        other1 = other.copy()
        days = 0
        if self1.is_before(other1) == True :
            while self1.is_before(other1) == True:
                days += 1
                self1.advance_one()
            return -1 * days
        else:
            while other1.is_before(self1) == True:
                days += 1
                other1.advance_one()
            return days
        
    def day_name(self):
        """ returns a string that indicates the name of the day of the week of
            the Date object that calls it.
        """
        day_names = ['Monday', 'Tuesday', 'Wednesday', 
             'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        d = Date(11,11,2019)
        
        n = self.days_between(d)
        r = n % 7 
        return day_names[r]
        
        
        
        
        
        
        
        
        
        
        
        
        
        
            
            
            
                

        