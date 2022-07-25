class Tour:
  def __init__(self, tour_tuple):
    self.id = tour_tuple[0]
    self.label = tour_tuple[1]
    self.st_date = tour_tuple[2]
    self.end_date = tour_tuple[3]
    self.total_seats = tour_tuple[4]
    self.avail_seats = tour_tuple[5]
    self.dest = tour_tuple[6]
    self.fare = tour_tuple[7]
    self.desc = tour_tuple[8]


class Booking:
  def __init__(self, booking_tuple):
    self.id = booking_tuple[0]
    self.tour_id = booking_tuple[1]
    self.user_id = booking_tuple[2]
    self.number_of_people = booking_tuple[3]
    self.total_price = booking_tuple[4]

