import csv

# Read the original CSV file
with open('data/joueurs_ATP_WTA.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    players = [row[0] for row in reader if row]  # Ensure row is not empty

# List of common particles in names
particles = {'de', 'van', 'von', 'da', 'del', 'la', 'le'}

# Reformat player names
formatted_players = []
for player in players:
    parts = player.split()
    if len(parts) > 1:
        # Take the last part as first name and the rest as last name
        first_name = parts[-1]
        last_name = ' '.join(parts[:-1])
        # Get the first letter of the first name
        first_initial = first_name[0]
        # Format as "Lastname F."
        formatted_name = f"{last_name} {first_initial}."
        formatted_players.append(formatted_name)

# Write the new list to a CSV file
with open('data/new_list_players.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    for player in formatted_players:
        writer.writerow([player])

print("New player list has been created and saved to 'data/new_list_players.csv'.") 