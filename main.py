import tkinter as tk
from tkinter import ttk

# Global variables to store ranking data
individual_ranking_data = []
team_ranking_data = []

#Storing team and individuals into dict and list(Array) and tournament for future ranking and results
individuals = []
teams = {}
tournaments = []
current_tournament_events = []
team_ranking_data = {}

#Max amount of teams and individuals
MAX_TEAMS = 5
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
            current_tournament['events'].append({
                'name': event_name,
                'type': event_type_selected,
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

    tk.Label(ranking_window, text="Individual Ranking", font=('Helvetica', 18, 'bold')).pack(pady=10)

    # main frame
    main_frame = tk.Frame(ranking_window)
    main_frame.pack(fill=tk.BOTH, expand=1)

    my_canvas = tk.Canvas(main_frame)
    my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    # scrollbar
    my_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    second_frame = tk.Frame(my_canvas)

    # new frame
    my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

    # entry widgets for individual rankings
    entries = {}
    for i in range(1, 21):  # 20 individual players
        player_label = tk.Label(second_frame, text=f"Player {i}", anchor="w")
        player_label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

        entry = tk.Entry(second_frame)
        entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
        entries[f"Player {i}"] = entry

    # function to save
    def save_individual_ranking():
        ranking = {}
        for i in range(1, 21):  # Assuming 20 individual players
            player = f"Player {i}"
            ranking[player] = entries[player].get()
        individual_ranking_data.append(ranking)
        ranking_window.destroy()

    # Save button
    save_button = tk.Button(ranking_window, text="Save Ranking", command=save_individual_ranking)
    save_button.pack()

def open_team_ranking():
    ranking_window = tk.Toplevel(window)
    ranking_window.title("Team Ranking Entry")

    tk.Label(ranking_window, text="Select Event:").pack()

    # Make sure current_tournament_events is available and populated with the events
    event_names = [event['name'] for event in current_tournament_events]
    selected_event = tk.StringVar(ranking_window)
    if event_names:
        selected_event.set(event_names[0])  # Set the first event as default
        event_menu = tk.OptionMenu(ranking_window, selected_event, *event_names)
        event_menu.pack()
    else:
        tk.Label(ranking_window, text="No events available.").pack()
        return  # Exit the function if there are no events

    # Entry for team rankings
    entries = {}
    for team_name in teams:
        tk.Label(ranking_window, text=team_name).pack()
        entry = tk.Entry(ranking_window)
        entry.pack()
        entries[team_name] = entry

    def save_rankings():
        event = selected_event.get()
        rankings = {team: entry.get() for team, entry in entries.items()}
        team_ranking_data[event] = rankings
        # After saving, you might want to update some GUI elements or close the window
        ranking_window.destroy()

    save_button = tk.Button(ranking_window, text="Save Rankings", command=save_rankings)
    save_button.pack()

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
        for player, score in ranking.items():
            event_name = "Event X" 
            individual_results_table.insert('', 'end', values=(player, event_name, score))

    individual_results_table.pack()

def open_results_teams():
    teams_results_window = tk.Toplevel(window)
    teams_results_window.title("Results by Event (Teams)")

    #a title label
    tk.Label(teams_results_window, text="Results by Event (Teams)", font=('Helvetica', 18, 'bold')).pack(pady=10)

    #list/table for team results
    columns = ('#1', '#2', '#3')  
    teams_results_table = ttk.Treeview(teams_results_window, columns=columns, show='headings')
    teams_results_table.heading('#1', text='Team Name')
    teams_results_table.heading('#2', text='Event Name')
    teams_results_table.heading('#3', text='Score')

    teams_results_table.column('#1', width=120, anchor='center')
    teams_results_table.column('#2', width=200, anchor='center')
    teams_results_table.column('#3', width=80, anchor='center')

    for ranking in team_ranking_data:
        for team, score in ranking.items():
            event_name = "Event X"  
            teams_results_table.insert('', 'end', values=(team, event_name, score))

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
    individuals_tree = tk.LabelFrame(display_window, text="Individuals")
    individuals_tree.pack(padx=10, pady=10)

    for i, individual in enumerate(individuals, start=1):
        tk.Label(individuals_tree, text=f"Individual {i}: {individual}").pack(anchor="w")

    # Display teams
    teams_frame = tk.LabelFrame(display_window, text="Teams")
    teams_frame.pack(padx=10, pady=10)

    for team, members in teams.items():
        members_str = ", ".join(members) if members else "No members"
        tk.Label(teams_frame, text=f"Team: {team} - Members: {members_str}").pack(anchor="w")

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

            # Add selected players to the selected team
            teams[selected_team].extend(selected_players)

            # Update the display or save the data as needed

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