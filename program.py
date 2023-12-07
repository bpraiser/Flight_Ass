import csv
from datetime import datetime, timedelta


class Flight:
    def __init__(self, flight_number, flight_origin, aircraft_number, airline_name, airline_code, current_distance, current_speed, timetabled_arrival):
        self.flight_number = flight_number
        self.flight_origin = flight_origin
        self.aircraft_number = aircraft_number
        self.airline_name = airline_name
        self.airline_code = airline_code
        self.current_distance = current_distance
        self.current_speed = current_speed
        self.timetabled_arrival = timetabled_arrival

    def calculate_eta(self):
        if self.current_speed == 0:
            return None
        return self.current_distance / self.current_speed

def read_data(file_name):
    flights = []
    with open(file_name, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            flight = Flight(row['Flight_number'], row['Flight_origin'], row['Aircraft_number'],
                            row['Airline_name'], row['Airline_code'], float(row['Current_distance']),
                            float(row['Current_flight_speed']), row['Timetabled_arrival_time'])
            flights.append(flight)
    return flights

def write_data(file_name, flights):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Flight_number', 'Flight_origin', 'Aircraft_number', 'Airline_name', 'Airline_code', 'Current_distance', 'Current_flight_speed', 'Timetabled_arrival_time'])
        for flight in flights:
            writer.writerow([flight.flight_number, flight.flight_origin, flight.aircraft_number,
                             flight.airline_name, flight.airline_code, flight.current_distance,
                             flight.current_speed, flight.timetabled_arrival])



def search_flights(flights, search_type, query):
    results = []
    current_time = datetime.now()

    for flight in flights:
        # Search by Flight Number
        if search_type == 1 and query.lower() in flight.flight_number.lower():
            results.append(flight)
        # Search by Flight Origin
        elif search_type == 2 and query.lower() in flight.flight_origin.lower():
            results.append(flight)
        # Search by Aircraft Number
        elif search_type == 3 and query.lower() in flight.aircraft_number.lower():
            results.append(flight)
        # Search by Airline Name
        elif search_type == 4 and query.lower() in flight.airline_name.lower():
            results.append(flight)
        # Search by Airline Code
        elif search_type == 5 and query.lower() in flight.airline_code.lower():
            results.append(flight)
        # Search Flight by Expected Time of Arrival
        elif search_type == 6:
            eta = flight.calculate_eta()
            if eta is not None and 0 <= eta <= 1:  # Within the next hour
                results.append(flight)
        # Search Flights by Timetabled Time
        elif search_type == 7:
            try:
                timetabled_arrival = datetime.strptime(flight.timetabled_arrival, '%H:%M')
                if current_time <= timetabled_arrival <= (current_time + timedelta(hours=1)):
                    results.append(flight)
            except ValueError:
                # Handle invalid date format
                pass

    return results


def format_cell(data, width):
    data = ''+data
    if len(data) > width:
        return data[:width - 3] + '...'
    return data + ' ' * (width - len(data))

def display_flights(flights, columnWidth):

    col_names = ["Flight#", "Origin", "Craft#", "Name", "Code", 
                  "Timetabled Arrival", "ETA"]

    # Ensure columnWidth array matches the number of columns
    if len(columnWidth) != len(col_names):
        print("Error: Column width array does not match the number of columns.")
        return

    
    # Print header
    header = "|".join(format_cell(col, columnWidth[i]) for i, col in enumerate(col_names))
    print('=' * len(header))  # Print separator
    print(header)
    print('=' * len(header))  # Print separator

    # Print each flight's details
    for flight in flights:
        eta = f"{flight.calculate_eta():.2f}h" if flight.calculate_eta() else "N/A"
        row = [
            format_cell(flight.flight_number, columnWidth[0]),
            format_cell(flight.flight_origin, columnWidth[1]),
            format_cell(flight.aircraft_number, columnWidth[2]),
            format_cell(flight.airline_name, columnWidth[3]),
            format_cell(flight.airline_code, columnWidth[4]),
            format_cell(flight.timetabled_arrival, columnWidth[5]),
            format_cell(eta, columnWidth[6])
        ]
        print("|".join(row))
        print('-' * len(header))  # Print separator after each row

 
        
def main():
    # Define column widths
    columnWidth = [9, 12, 9, 20, 7, 9, 9]  # Example widths
    
    flights = read_data("data.txt")
    while True:
        print("\nFlight Enquiry System")
        print("1. Search by Flight Number")
        print("2. Search by Flight Origin")
        print("3. Search by Aircraft Number")
        print("4. Search by Airline Name")
        print("5. Search by Airline Code")
        print("6. Search Flights by Expected Time of Arrival")
        print("7. Search Flights by Timetabled Time")
        print("8. Save Changes")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == '9':
            break
        elif choice == '8':
            write_data("data.txt", flights)
            print("Data saved successfully.")
            continue

        query = ""
        if choice in ['1', '2', '3', '4', '5', '6', '7']:
            query = input("Enter search query: ")

        results = search_flights(flights, int(choice), query)
        display_flights(results, columnWidth)  # Pass columnWidth here

    write_data("data.txt", flights)

if __name__ == "__main__":
    main()

