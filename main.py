import tkinter as tk
from tkinter import ttk


# global variables to store ranking data
individual_ranking_data = []  
team_ranking_data = []        

#store individuals and teams
individuals = []
teams = {}

#store tournament data
tournaments = []
current_tournament_events = []

# rank for teams and individuls
rank_points = {
    'R1': 10,
    'R2': 8,
    'R3': 6,
    'R4': 4,
    'R5': 2,
    'R0': 0  
}

#max amount of teams and individuals
MAX_TEAMS = 4
MAX_INDIVIDUALS = 20 

#func to setup a tournament
def open_tournament_setup():
    setup_window = tk.Toplevel(window)
    setup_window.title("Initialize New Tournament")

    tk.Label(setup_window, text="Tournament Setup", font=('Helvetica', 18, 'bold')).pack(pady=20)

    event_type = tk.StringVar()
    tk.Radiobutton(setup_window, text="Individual Events", variable=event_type, value="individual").pack()
    tk.Radiobutton(setup_window, text="Team Events", variable=event_type, value="team").pack()

    # entry fields for name and description
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
        # insert the new event into the current tournament
        current_tournament = tournaments[-1] if tournaments else None
        if current_tournament:
            current_tournament['events'].append({
            'name': event_name,
            'type': event_type_selected,
            'for': event_type.get() 
                })
            current_tournament_events.append({
                'name': event_name,
                'type': event_type_selected,
            }) 
            # insert the new event into the event list table
            event_table.insert('', 'end', values=(event_name, event_type_selected))
            name_entry.delete(0, 'end')
            description_text.delete('1.0', tk.END)

    finish_button = tk.Button(setup_window, text="Finish", command=lambda: setup_window.destroy())
    finish_button.pack(pady=20)

    tk.Label(setup_window, text="Event List", font=('Helvetica', 14)).pack()

    #the event list table
    columns = ('#1', '#2')
    event_table = ttk.Treeview(setup_window, columns=columns, show='headings')
    event_table.heading('#1', text='Event Name')
    event_table.heading('#2', text='Event Type')

    event_table.column('#1', width=120, anchor='center')
    event_table.column('#2', width=120, anchor='center')

    event_table.pack()

    tournaments.append({
        'name': '',
        'description': '',
        'events': [],
    })

    for event in current_tournament_events:
        event_table.insert('', 'end', values=(event['name'], event['type']))

#func for ranking for individuals
def open_individual_ranking():
    ranking_window = tk.Toplevel(window)
    ranking_window.title("Individual Ranking Entry")

    #main frame 
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

    # dropdown to select the event
    event_names = [event['name'] for event in current_tournament_events if event['type'] == 'individual']
    selected_event = tk.StringVar()
    event_dropdown = ttk.Combobox(second_frame, textvariable=selected_event, values=event_names, state="readonly")
    event_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
    if event_names:
        selected_event.set(event_names[0])

    ranking_entries = []
    for i, individual in enumerate(individuals, start=1):
        tk.Label(second_frame, text=individual, anchor="w").grid(row=i, column=0, padx=10, pady=5, sticky="w")

        rank_var = tk.StringVar(value='R0')
        rank_dropdown = ttk.Combobox(second_frame, textvariable=rank_var, values=list(rank_points.keys()), state="readonly")
        rank_dropdown.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
        ranking_entries.append((individual, rank_var))

    # func to save rankings and points
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
        
        
        ranking_window.destroy()

    save_button = tk.Button(second_frame, text="Save Ranking", command=save_individual_ranking)
    save_button.grid(row=len(individuals) + 1, column=1, pady=10)

    
    second_frame.update_idletasks()
    my_canvas.config(scrollregion=my_canvas.bbox("all"))

#func for ranking for teams
def open_team_ranking():
    ranking_window = tk.Toplevel(window)
    ranking_window.title("Team Ranking Entry")

    #main frame with a scrollbar
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

    # entry widgets for team rankings
    ranking_entries = []
    for i, team_name in enumerate(teams.keys(), start=1):
        tk.Label(second_frame, text=team_name, anchor="w").grid(row=i, column=0, padx=10, pady=5, sticky="w")

        rank_var = tk.StringVar(value='R0')
        rank_dropdown = ttk.Combobox(second_frame, textvariable=rank_var, values=list(rank_points.keys()), state="readonly")
        rank_dropdown.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
        ranking_entries.append((team_name, rank_var))

    # func to save rankings and points
    def save_team_ranking():
        event = selected_event.get()
        for team_name, rank_var in ranking_entries:
            rank = rank_var.get()
            points = assign_points(rank)
            team_ranking_data.append({'team': team_name, 'event': event, 'rank': rank, 'points': points})
    
        ranking_window.destroy()


    # save button
    save_button = tk.Button(second_frame, text="Save Ranking", command=save_team_ranking)
    save_button.grid(row=len(teams) + 1, column=1, pady=10)

    second_frame.update_idletasks()
    my_canvas.config(scrollregion=my_canvas.bbox("all"))

# convert rank to points func
def assign_points(rank):
    return rank_points.get(rank, 0)

#func to open results of individuals
def open_results_individual():
    individual_results_window = tk.Toplevel(window)
    individual_results_window.title("Results by Event (Individual)")


    tk.Label(individual_results_window, text="Results by Event (Individual)", font=('Helvetica', 18, 'bold')).pack(pady=10)

    #table for displaying results
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

#func to open results of teams
def open_results_teams():
    teams_results_window = tk.Toplevel(window)
    teams_results_window.title("Results by Event (Teams)")

    tk.Label(teams_results_window, text="Results by Event (Teams)", font=('Helvetica', 18, 'bold')).pack(pady=10)

    #table for displaying results
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

#func to input players for individuals section and names of teams(to future management in "Manage Team")
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
        team_names = [name for name in team_names if name]  
        individual_names = individual_text_area.get("1.0", tk.END).strip().split('\n')
        individual_names = [name for name in individual_names if name]  

        # validation check for maximum number of teams - Modification for Test 5 (Fail)
        if len(teams) + len(team_names) > MAX_TEAMS:
            tk.messagebox.showerror("Error", f"Maximum number of teams ({MAX_TEAMS}) reached. You cannot add more teams.")
            return  

        # validation for maximum number of individuals
        if len(individuals) + len(individual_names) > MAX_INDIVIDUALS:
            tk.messagebox.showerror("Error", f"Maximum number of individuals ({MAX_INDIVIDUALS}) reached.")
            input_window.destroy()
            return

        for name in team_names:
            if name:
                teams[name] = []  # adding team names to the teams dictionary

        for name in individual_names:
            if name and len(individuals) < MAX_INDIVIDUALS:
                individuals.append(name)

        input_window.destroy()
        display_individuals_and_teams()

    tk.Button(input_window, text="Submit", command=process_names).pack()

#func to display individuals and teams(after each assignment , the pop-up screen of individuals and teams will be shown)
def display_individuals_and_teams():
    display_window = tk.Toplevel(window)
    display_window.title("Individuals and Teams")

    # display individuals
    individuals_frame = tk.LabelFrame(display_window, text="Individuals")
    individuals_frame.pack(padx=10, pady=10)

    for i, individual in enumerate(individuals, start=1):
        tk.Label(individuals_frame, text=f"Individual {i}: {individual}").pack(anchor="w")

    #display teams and their members
    teams_frame = tk.LabelFrame(display_window, text="Teams")
    teams_frame.pack(padx=10, pady=10)

    for team_name in teams.keys():
        members_str = ", ".join(teams[team_name]) if teams[team_name] else "No members"
        tk.Label(teams_frame, text=f"Team {team_name}: Members: {members_str}").pack(anchor="w")

#manage team func to add, delete and manage team members
def open_manage_teams():
    manage_teams_window = tk.Toplevel(window)
    manage_teams_window.title("Manage Teams")

    tk.Label(manage_teams_window, text="Select a Team to Manage:").pack()

    # listbox to display teams for selection
    teams_listbox = tk.Listbox(manage_teams_window)
    teams_listbox.pack()

    for team in teams.keys():
        teams_listbox.insert(tk.END, team)

    #func to handle adding players to the selected team
    def add_players_to_team():
        selected_team_index = teams_listbox.curselection()
        if selected_team_index:
            selected_team = teams_listbox.get(selected_team_index[0])
            selected_players = [player for player, var in player_checkboxes.items() if var.get()]
            
            # add selected players to the selected team, avoiding duplicates
            updated_members = list(set(teams[selected_team] + selected_players))
            teams[selected_team] = updated_members
            
            display_individuals_and_teams()

        for var in player_checkboxes.values():
            var.set(False)

    # func to handle removing players from the selected team
    def remove_players_from_team():
        selected_team_index = teams_listbox.curselection()
        if selected_team_index:
            selected_team = teams_listbox.get(selected_team_index[0])
            selected_players = [player for player, var in player_checkboxes.items() if var.get()]
            
            # remove selected players from the team
            teams[selected_team] = [member for member in teams[selected_team] if member not in selected_players]
            
            display_individuals_and_teams()

        for var in player_checkboxes.values():
            var.set(False)

    # checkboxes for selecting players to add or remove
    player_checkboxes = {}
    for player in individuals:
        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(manage_teams_window, text=player, variable=var)
        checkbox.pack()
        player_checkboxes[player] = var

    # button to add selected players to the team
    tk.Button(manage_teams_window, text="Add Players to Team", command=add_players_to_team).pack()

    # button to remove selected players from the team
    tk.Button(manage_teams_window, text="Remove Selected Players from Team", command=remove_players_from_team).pack()

# main window setup
window = tk.Tk()
window.title("Scoring System")
window.geometry("900x750")  # the size can be changed easily here

# menu frame
main_menu_frame = tk.Frame(window, bg="white")
main_menu_frame.pack(pady=100)


# "Start New Tournament" button
start_button = tk.Button(main_menu_frame, text="Start New Tournament", width=20, height=2,
                         command=open_tournament_setup)
start_button.pack(pady=10)

# "Input Player and Teams" button
input_names_button = tk.Button(main_menu_frame, text="Input Player and Teams ",width=20, height=2, command=input_player_names)
input_names_button.pack(pady=10)

# "Manage Teams" button
manage_teams_button = tk.Button(main_menu_frame, text="Manage Teams", width=20, height=2, command=open_manage_teams)
manage_teams_button.pack(pady=10)

# "Team Ranking" button
team_ranking_button = tk.Button(main_menu_frame, text="Team Ranking", width=20, height=2, command=open_team_ranking)
team_ranking_button.pack(pady=10)

# "Individual Ranking" button
individual_ranking_button = tk.Button(main_menu_frame, text="Individual Ranking", width=20, height=2,
                                      command=open_individual_ranking)
individual_ranking_button.pack(pady=10)


# "Results by Event (Individual)" button
individual_results_button = tk.Button(main_menu_frame, text="Results by Event (Individual)", width=20, height=2,
                                      command=open_results_individual)
individual_results_button.pack(pady=10)

# "Results by Event (Teams)" button
teams_results_button = tk.Button(main_menu_frame, text="Results by Event (Teams)", width=20, height=2,
                                command=open_results_teams)
teams_results_button.pack(pady=10)



# run the main loop
window.mainloop()