from django.core.management.base import BaseCommand, CommandError
from Uni_Socs.models import Events
from Users.models import RSVP_event

import datetime


# ########## HELPER METHOD ##########
def clear_all_past_events(date_today):      # The method in which all the logic of deleting past events occurs and RSVP
    all_events = Events.objects.all()       # all events
    date_today = date_today                 # get back date

    for event in all_events:           # Iteration for passing through all events
        if event.date < date_today:    # Cycle date comparison with today's date
            past_rsvp = RSVP_event.objects.filter(event=event.id)       # Sorting all RSVP_event by event.id 's

            event.delete()                      # DELETE PAST EVENT
            past_rsvp.delete()                  # DELETE RSVP PAST EVENT

    print('all past events deleted')            # Message for the user


class Command(BaseCommand):
    help = "Clear all events that have already passed"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        yes_or_no = input("Do you really want to delete all past events?(Yes/No): ")   # Warning for removal
        date_today = datetime.date.today()              # Receiving today's date

        try:
            if yes_or_no == 'Yes' or yes_or_no == 'yes':           # Validation for correct input from the user
                clear_all_past_events(date_today)                  # Launches Helper Method
            else:
                print('Operation canceled by the user')            # Message for the user
                return                                             # exit

        except Exception as e:                                     # Django requirement!!
            raise CommandError(repr(e))
