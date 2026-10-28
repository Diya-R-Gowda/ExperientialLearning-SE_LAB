"""Event management system: a booking desk for small events.

Creates events with a venue and capacity, registers guests until an event is
full, reports seats left, picks a lucky-draw winner, labels events as upcoming
or completed, and saves everything to a file.
"""
import os
import pickle
import random
from datetime import date

events = {}


def create_event(event_name, venue, capacity=50, guests=None):
    """Create an event and store it. Each event gets its own guest list."""
    if guests is None:
        guests = []
    events[event_name] = {"venue": venue, "capacity": capacity,
                          "guests": guests}
    return events[event_name]


def register_guest(event_name, guest):
    """Add a guest to an event if it exists and still has seats."""
    event = events.get(event_name)
    if event is None:
        print("No such event:", event_name)
        return False
    if len(event["guests"]) >= event["capacity"]:
        print(event_name, "is full, cannot add", guest)
        return False
    event["guests"].append(guest)
    return True


def seats_left(event_name):
    """Return how many seats are still free for an event."""
    event = events[event_name]
    return event["capacity"] - len(event["guests"])


def event_status(event_date):
    """Return 'Upcoming' for today or a future date, else 'Completed'."""
    if event_date >= date.today():
        return "Upcoming"
    return "Completed"


def guest_report(event_name, sort_order="asc"):
    """Return the guest names as one string, sorted 'asc' or 'desc'."""
    descending = sort_order == "desc"
    names = sorted(events[event_name]["guests"], reverse=descending)
    return ", ".join(names)


def save_events(file_name="events.pkl"):
    """Save all events to a file."""
    with open(file_name, "wb") as file:
        pickle.dump(events, file)


def load_events(file_name="events.pkl"):
    """Load events from a file and return them."""
    with open(file_name, "rb") as file:
        return pickle.load(file)


def print_badges(event_name):
    """Send the badge file for an event to the printer."""
    # Helper kept for the lab: not called by the demo
    os.system("lp badges_" + event_name + ".txt")


def main():
    """Run a short demonstration of the booking desk."""
    create_event("Tech Meetup", "Hall A", 3)
    create_event("Alumni Dinner", "Rooftop",2)
    register_guest("Tech Meetup", "Asha")
    register_guest("Tech Meetup", "Ravi")
    register_guest("Alumni Dinner", "Meena")
    register_guest("Workshop", "Kiran")
    left=seats_left("Tech Meetup")
    print("Seats left at Tech Meetup:", left)
    print("Seats left at Alumni Dinner:", seats_left("Alumni Dinner"))
    print("Tech Meetup guests:", guest_report("Tech Meetup", "asc"))
    print("Tech Meetup is", event_status(date(2099, 1, 15)))
    print("Alumni Dinner is", event_status(date(2020, 5, 1)))
    winner = random.choice(events["Tech Meetup"]["guests"])
    print("Lucky draw winner:", winner)
    save_events()
    restored = load_events() # reload to confirm the save worked
    print("Events restored from file:", len(restored))
    print("Venues:", [e["venue"] for e in restored.values()])

main()
