'''
Booking automation
'''

from dataclasses import dataclass
from enum import Enum, auto
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

"""Imports for getting links from a webpage"""
from bs4 import BeautifulSoup, SoupStrainer
import requests


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

        page = requests.get(self.web_page)    
        data = page.text
        soup = BeautifulSoup(data)

        for link in soup.find_all('a'):
            print(link.get('href'))

        print(
            f"Booking course {self.name} on {self.course_time} for {Person.first_name}."
        )


def main() -> None:
    """Main function"""

    huepfen_thomas = HuepfenThomas()
    person = Person("m", "Max", "Mustermann", "Königsallee 1", "Düsseldorf", "40215", Role.EXTERNER, "max.mustermann@somemail.com", "xxxxxxxxxxxx", "xxxxxxxxxxxxxxxxxxxxxxx")

    huepfen_thomas.book(person)


if __name__ == "__main__":
    main()