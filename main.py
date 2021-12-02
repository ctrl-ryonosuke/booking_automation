'''
Booking automation
'''

from dataclasses import dataclass
from enum import Enum, auto
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import time

"""Imports for getting links from a webpage"""
from splinter import Browser


class Role(Enum):
    """Explicit definition of person roles for booking"""

    STUDIERENDER = auto()
    BESCHAEFTIGTER = auto()
    EXTERNER = auto()
    ALUMNI = auto()

@dataclass
class Person():
    """Basic representation of a person who can book a course"""

    gender: str
    first_name: str
    last_name: str
    street_address: str
    city: str
    postal_code: int
    role: Role 
    mail: str
    phone_number: str
    iban: str
    immatriculation_number: int = 0 

@dataclass
class Course(ABC):
    """Basic representation of a course to book"""

    name: str

    @abstractmethod
    def book(self, Person) -> None:
        """Let a person book the course"""
    
@dataclass
class HuepfenThomas(Course):
    """Fitness mit Musik Kurs von Thomas, sonntag um 19:45"""

    name: str = "Fitness mit Musik Kurs von Thomas, sonntag um 19:45"

    web_page = "https://buchung.hsz.rwth-aachen.de/angebote/Wintersemeseter_2021_22/_Fitness_mit_Musik.html"
    # TODO: automate datetime for next course
    course_time = datetime(2021, 10, 14, 19, 45, 00)
    booking_time = course_time + timedelta(days=-1)

    def book(self, Person) -> None:

        pass


def main() -> None:
    """Main function"""

    huepfen_thomas = HuepfenThomas()
    person = Person("m", "Max", "Mustermann", "Königsallee 1", "Düsseldorf", "40215", Role.EXTERNER, "max.mustermann@somemail.com", "xxxxxxxxxxxx", "xxxxxxxxxxxxxxxxxxxxxxx")

    huepfen_thomas.book(person)

    browser = Browser() # defaults to firefox
    browser.visit('https://buchung.hsz.rwth-aachen.de/angebote/Wintersemeseter_2021_22/_Fitness_mit_Musik.html')

    # Get all the inputs elements on the page
    inputs = browser.driver.find_elements_by_tag_name('input')
    print('Verfügbare Sessions:')
    for input in inputs:
        # if the input element is a "buchen" button
        if 'bs_btn_buchen' in input.get_attribute('class').split():
            # get its second degree parent (grand-parent I guess)
            parent = input.find_element_by_xpath('../..')
            all_children_by_css = parent.find_elements_by_xpath(".//*")
            for child in all_children_by_css:
                # find the element that contain the Leiter's name
                if 'bs_skl' in child.get_attribute('class').split():
                    leiter = child.find_element_by_xpath(".//*").get_attribute('innerHTML')
                    print('* '+leiter)
                    
                    # da muss man sich irgendein Mechanism überlegen für die Session Selection
                    # Bei mir gerade war eine Session von Janina zu verfügung, ich habe's dann
                    # hardcoded damit ich weitergehen kann.
                    if leiter == 'Janina Frey':
                        input.click()

    # We close the first window
    browser.windows[0].close()

    # Get all the inputs on that second page
    inputs = browser.driver.find_elements_by_tag_name('input')
    print('Verfügbare Slots')
    for input in inputs:
        # For every input that has the "buchen" class (meaning it can be booked)
        if 'buchen' in input.get_attribute('class').split():
            parent = input.find_element_by_xpath('../..')
            all_children_by_css = parent.find_elements_by_css_selector("*")
            day = all_children_by_css[1].get_attribute('innerHTML')
            date = all_children_by_css[2].get_attribute('innerHTML')
            time = all_children_by_css[3].get_attribute('innerHTML')
            print(f'* {day} {date} {time}')

            # Then you gotta input.click() on the slot you wanna book...etc.

    # browser.quit()


if __name__ == "__main__":
    main()
