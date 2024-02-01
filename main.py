import tkinter as tk
from tkinter import ttk

# Global variables to store ranking data
individual_ranking_data = []  # List of dictionaries
team_ranking_data = []        # List of dictionaries

#Storing team and individuals into dict and list(Array) and tournament for future ranking and results
individuals = []
teams = {}
tournaments = []
current_tournament_events = []

# Rank for teams and individuls
rank_points = {
    'R1': 10,
    'R2': 8,
    'R3': 6,
    'R4': 4,
    'R5': 2,
    'R0': 0  
}

#Max amount of teams and individuals
MAX_TEAMS = 6
MAX_INDIVIDUALS = 20

def open_tournament_setup():
    setup_window = tk.Toplevel(window)
    setup_window.title("Initialize New Tournament")

    tk.Label(setup_window, text="Tournament Setup", font=('Helvetica', 18, 'bold')).pack(pady=20)

    event_type = tk.StringVar()
    tk.Radiobutton(setup_window, text="Individual Events", variable=event_type, value="individual").pack()
    tk.Radiobutton(setup_window, text="Team Events", variable=event_type, value="team").pack()

    # Entry fields for name and description
    tk.Label(setup_window, text="Name").pack()
    name_entry = tk.Entry(setup_window)
    name_entry.pack()

    tk.Label(setup_window, text="Description").pack()
    description_text = tk.Text(setup_window, height=5, width=40)
    description_text.pack()

    # button to add Academic events
    def add_academic_event():
        event_name = name_entry.get()
        event_type_selected = "Academic"
        add_event_to_list(event_name, event_type_selected)

    academic_event_button = tk.Button(setup_window, text="Add Academic Event", command=add_academic_event)
    academic_event_button.pack()

    # button to add Sporting events
    def add_sporting_event():
        event_name = name_entry.get()
        event_type_selected = "Sporting"
        add_event_to_list(event_name, event_type_selected)

    sporting_event_button = tk.Button(setup_window, text="Add Sporting Event", command=add_sporting_event)
    sporting_event_button.pack()

    def add_event_to_list(event_name, event_type_selected):
        # Insert the new event into the current tournament
        current_tournament = tournaments[-1] if tournaments else None
        if current_tournament:
            # Include the event_type (individual or team) in the event data
            current_tournament['events'].append({
            'name': event_name,
            'type': event_type_selected,
            'for': event_type.get()  # 'individual' or 'team'
                })
            current_tournament_events.append({
                'name': event_name,
                'type': event_type_selected,
            })  # Add to the list of current events
            # Insert the new event into the event list table
            event_table.insert('', 'end', values=(event_name, event_type_selected))
            # Clear the data
            name_entry.delete(0, 'end')
            description_text.delete('1.0', tk.END)

    finish_button = tk.Button(setup_window, text="Finish", command=lambda: setup_window.destroy())
    finish_button.pack(pady=20)

    tk.Label(setup_window, text="Event List", font=('Helvetica', 14)).pack()

    # Creating the event list table
    columns = ('#1', '#2')
    event_table = ttk.Treeview(setup_window, columns=columns, show='headings')
    event_table.heading('#1', text='Event Name')
    event_table.heading('#2', text='Event Type')

    # Define column width and alignment
    event_table.column('#1', width=120, anchor='center')
    event_table.column('#2', width=120, anchor='center')

    event_table.pack()

    # Create a new tournament and add it to the tournaments list
    tournaments.append({
        'name': '',
        'description': '',
        'events': [],
    })

    # Update the event list table with current events
    for event in current_tournament_events:
        event_table.insert('', 'end', values=(event['name'], event['type']))

def open_individual_ranking():
    ranking_window = tk.Toplevel(window)
    ranking_window.title("Individual Ranking Entry")

    # Create a main frame with a scrollbar
    main_frame = tk.Frame(ranking_window)
    main_frame.pack(fill=tk.BOTH, expand=1)
    
    my_canvas = tk.Canvas(main_frame)
    my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    
    my_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    second_frame = tk.Frame(my_canvas)
    my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

    # Dropdown to select the event
    event_names = [event['name'] for event in current_tournament_events if event['type'] == 'individual']
    selected_event = tk.StringVar()
    event_dropdown = ttk.Combobox(second_frame, textvariable=selected_event, values=event_names, state="readonly")
    event_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
    if event_names:
        selected_event.set(event_names[0])

    # Entry widgets for individual rankings
    ranking_entries = []
    for i, individual in enumerate(individuals, start=1):
        tk.Label(second_frame, text=individual, anchor="w").grid(row=i, column=0, padx=10, pady=5, sticky="w")

        rank_var = tk.StringVar(value='R0')
        rank_dropdown = ttk.Combobox(second_frame, textvariable=rank_var, values=list(rank_points.keys()), state="readonly")
        rank_dropdown.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
        ranking_entries.append((individual, rank_var))

    # Function to save rankings and points
    def save_individual_ranking():
        event = selected_event.get()
        for individual, rank_var in ranking_entries:
            rank = rank_var.get()
            points = assign_points(rank)
            individual_ranking_data.append({
            'name': individual,
            'event': event,
            'rank': rank,
            'points': points
            })
        
        # Update some GUI elements or close the window
        ranking_window.destroy()

    save_button = tk.Button(second_frame, text="Save Ranking", command=save_individual_ranking)
    save_button.grid(row=len(individuals) + 1, column=1, pady=10)

    # Update the scroll region to encompass the inner frame
    second_frame.update_idletasks()
    my_canvas.config(scrollregion=my_canvas.bbox("all"))

def open_team_ranking():
    ranking_window = tk.Toplevel(window)
    ranking_window.title("Team Ranking Entry")

    # Create a main frame with a scrollbar
    main_frame = tk.Frame(ranking_window)
    main_frame.pack(fill=tk.BOTH, expand=1)

    my_canvas = tk.Canvas(main_frame)
    my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    my_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    second_frame = tk.Frame(my_canvas)
    my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

    event_names = [event['name'] for event in current_tournament_events if event['type'] == 'team']
    selected_event = tk.StringVar()
    event_dropdown = ttk.Combobox(second_frame, textvariable=selected_event, values=event_names, state="readonly")
    event_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
    if event_names:
        selected_event.set(event_names[0])

    # Entry widgets for team rankings
    ranking_entries = []
    for i, team_name in enumerate(teams.keys(), start=1):
        tk.Label(second_frame, text=team_name, anchor="w").grid(row=i, column=0, padx=10, pady=5, sticky="w")

        rank_var = tk.StringVar(value='R0')
        rank_dropdown = ttk.Combobox(second_frame, textvariable=rank_var, values=list(rank_points.keys()), state="readonly")
        rank_dropdown.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
        ranking_entries.append((team_name, rank_var))

    # Function to save rankings and points
    def save_team_ranking():
        event = selected_event.get()
        for team_name, rank_var in ranking_entries:
            rank = rank_var.get()
            points = assign_points(rank)
            team_ranking_data.append({'team': team_name, 'event': event, 'rank': rank, 'points': points})
    
        # Update GUI or data storage if needed
        ranking_window.destroy()


    # Save button
    save_button = tk.Button(second_frame, text="Save Ranking", command=save_team_ranking)
    save_button.grid(row=len(teams) + 1, column=1, pady=10)

    # Update the scroll region to encompass the inner frame
    second_frame.update_idletasks()
    my_canvas.config(scrollregion=my_canvas.bbox("all"))

def assign_points(rank):
    return rank_points.get(rank, 0)

def open_results_individual():
    individual_results_window = tk.Toplevel(window)
    individual_results_window.title("Results by Event (Individual)")


    tk.Label(individual_results_window, text="Results by Event (Individual)", font=('Helvetica', 18, 'bold')).pack(pady=10)

    columns = ('#1', '#2', '#3') 
    individual_results_table = ttk.Treeview(individual_results_window, columns=columns, show='headings')
    individual_results_table.heading('#1', text='Player Name')
    individual_results_table.heading('#2', text='Event Name')
    individual_results_table.heading('#3', text='Score')

    individual_results_table.column('#1', width=120, anchor='center')
    individual_results_table.column('#2', width=200, anchor='center')
    individual_results_table.column('#3', width=80, anchor='center')

    for ranking in individual_ranking_data:
        individual_results_table.insert('', 'end', values=(ranking['name'], ranking['event'], ranking['points']))

    individual_results_table.pack()

def open_results_teams():
    teams_results_window = tk.Toplevel(window)
    teams_results_window.title("Results by Event (Teams)")

    tk.Label(teams_results_window, text="Results by Event (Teams)", font=('Helvetica', 18, 'bold')).pack(pady=10)

    columns = ('#1', '#2', '#3')  
    teams_results_table = ttk.Treeview(teams_results_window, columns=columns, show='headings')
    teams_results_table.heading('#1', text='Team Name')
    teams_results_table.heading('#2', text='Event Name')
    teams_results_table.heading('#3', text='Score')

    teams_results_table.column('#1', width=120, anchor='center')
    teams_results_table.column('#2', width=200, anchor='center')
    teams_results_table.column('#3', width=80, anchor='center')

    for ranking in team_ranking_data:
        teams_results_table.insert('', 'end', values=(ranking['team'], ranking['event'], ranking['points']))

    teams_results_table.pack()

def input_player_names():
    input_window = tk.Toplevel(window)
    input_window.title("Input Player Names")

    tk.Label(input_window, text="Enter team names, one per line:").pack()
    team_text_area = tk.Text(input_window, height=5, width=50)
    team_text_area.pack()

    tk.Label(input_window, text="Enter individual competitor names, one per line:").pack()
    individual_text_area = tk.Text(input_window, height=5, width=50)
    individual_text_area.pack()

    def process_names():
        team_names = team_text_area.get("1.0", tk.END).strip().split('\n')
        individual_names = individual_text_area.get("1.0", tk.END).strip().split('\n')

        if len(teams) + len(team_names) > MAX_TEAMS:
            tk.messagebox.showerror("Error", f"Maximum number of teams ({MAX_TEAMS}) reached.")
            input_window.destroy()
            return

        if len(individuals) + len(individual_names) > MAX_INDIVIDUALS:
            tk.messagebox.showerror("Error", f"Maximum number of individuals ({MAX_INDIVIDUALS}) reached.")
            input_window.destroy()
            return

        for name in team_names:
            if name:
                teams[name] = [] 

        for name in individual_names:
            if name and len(individuals) < MAX_INDIVIDUALS:
                individuals.append(name)

        input_window.destroy()
        display_individuals_and_teams()

    tk.Button(input_window, text="Submit", command=process_names).pack()

def display_individuals_and_teams():
    display_window = tk.Toplevel(window)
    display_window.title("Individuals and Teams")

    # Display individuals
    individuals_frame = tk.LabelFrame(display_window, text="Individuals")
    individuals_frame.pack(padx=10, pady=10)

    for i, individual in enumerate(individuals, start=1):
        tk.Label(individuals_frame, text=f"Individual {i}: {individual}").pack(anchor="w")

    # Display teams and their members
    teams_frame = tk.LabelFrame(display_window, text="Teams")
    teams_frame.pack(padx=10, pady=10)

    for team_name in teams.keys():
        members_str = ", ".join(teams[team_name]) if teams[team_name] else "No members"
        tk.Label(teams_frame, text=f"Team {team_name}: Members: {members_str}").pack(anchor="w")

def open_manage_teams():
    manage_teams_window = tk.Toplevel(window)
    manage_teams_window.title("Manage Teams")

    tk.Label(manage_teams_window, text="Select a Team to Add Players:").pack()

    # Create a listbox to display teams
    teams_listbox = tk.Listbox(manage_teams_window)
    teams_listbox.pack()

    # Populate the listbox with existing teams
    for team in teams:
        teams_listbox.insert(tk.END, team)

    def add_players_to_team():
        selected_team_index = teams_listbox.curselection()
        if selected_team_index:
            selected_team = teams_listbox.get(selected_team_index[0])  # Get the selected team
            selected_players = [player for player, var in player_checkboxes.items() if var.get()]

        # Check if team exists and add selected players to the selected team
            if selected_team in teams:
                teams[selected_team] = list(set(teams[selected_team] + selected_players))  # Merge and remove duplicates

        # Update the display or save the data as needed
            display_individuals_and_teams()  # Refresh the teams and individuals display

        # Clear player selection
            for var in player_checkboxes.values():
                var.set(False)


    # Create checkboxes for available players
    player_checkboxes = {}
    for player in individuals:
        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(manage_teams_window, text=player, variable=var)
        checkbox.pack()
        player_checkboxes[player] = var

    tk.Button(manage_teams_window, text="Add Players to Team", command=add_players_to_team).pack()

# main window setup
window = tk.Tk()
window.title("Scoring System")
window.geometry("900x750")  # Adjust the size as necessary to fit content

# menu frame
main_menu_frame = tk.Frame(window, bg="white")
main_menu_frame.pack(pady=100)

#buttons that will be displayed on the main menu
start_button = tk.Button(main_menu_frame, text="Start New Tournament", width=20, height=2,
                         command=open_tournament_setup)
start_button.pack(pady=10)

input_names_button = tk.Button(main_menu_frame, text="Input Player and Teams ",width=20, height=2, command=input_player_names)
input_names_button.pack(pady=10)

manage_teams_button = tk.Button(main_menu_frame, text="Manage Teams", width=20, height=2, command=open_manage_teams)
manage_teams_button.pack(pady=10)

team_ranking_button = tk.Button(main_menu_frame, text="Team Ranking", width=20, height=2, command=open_team_ranking)
team_ranking_button.pack(pady=10)

individual_ranking_button = tk.Button(main_menu_frame, text="Individual Ranking", width=20, height=2,
                                      command=open_individual_ranking)
individual_ranking_button.pack(pady=10)



individual_results_button = tk.Button(main_menu_frame, text="Results by Event (Individual)", width=20, height=2,
                                      command=open_results_individual)
individual_results_button.pack(pady=10)


teams_results_button = tk.Button(main_menu_frame, text="Results by Event (Teams)", width=20, height=2,
                                command=open_results_teams)
teams_results_button.pack(pady=10)



# Run the main loop
window.mainloop()