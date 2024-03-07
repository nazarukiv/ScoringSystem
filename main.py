import tkinter as tk
from tkinter import ttk
import random
from tkinter import messagebox
import pytest
#----------------------------------------------------------------------------------------------------------------|
# global variables to store ranking data
individual_ranking_data = []  
team_ranking_data = []        

#store individuals and teams
individuals = []
teams = {}
individual_event_registrations = {} 

#store tournament data
tournaments = []
current_tournament_events = []

# configuration of the style for the buttons
style = ttk.Style()
style.configure('Exit.TButton', font=('Helvetica', 12, 'bold'), foreground='red', anchor='s')

# rank for teams and individuls
rank_points = {'R1': 10, 'R2': 8, 'R3': 6, 'R4': 4, 'R5': 2, 'R0': 0}
match_outcomes = {'Win': 8, 'Draw': 4, 'Lose': 0}

names = ['Oliver', 'Harry', 'George', 'Noah', 'Jack', 'Leo', 'Arthur', 'Muhammad', 'Oscar', 'Charlie',
                 'Jacob', 'Thomas', 'Henry', 'Freddie', 'Alfie', 'Theo', 'William', 'James', 'Ethan', 'Archie',]

team_sport_points = {'Win': 0, 'Draw': 0, 'Lose': 0}
ranked_event_points = {'R1': 0, 'R2': 0, 'R3': 0, 'R4': 0, 'R5': 0}

#max amount of teams and individuals
MAX_TEAMS = 4
MAX_INDIVIDUALS = 20 
#----------------------------------------------------------------------------------------------------------------|




#funcs for buttons logic
#--------------------------------------------------------|

def close_window_and_go_back(window):
    """
    Closes the current window. This simulates going back to the main menu.
    
    window: The window to close.
    """
    window.destroy()

def create_back_button(window):
    """
    creates a styled "Back to Menu" button in the given window.
    
    window: The window where the button will be placed.
    """
    style = ttk.Style()
    style.configure('Back.TButton', font=('Helvetica', 15, 'bold'), foreground='white')
    
    back_button = ttk.Button(window, text="Back to Menu", style='Back.TButton', command=lambda: close_window_and_go_back(window))
    back_button.pack(pady=15)

def exit_application():
    """
    closes the entire application safely.
    """
    window.quit()

def update_individual_results():
    print("Individual results refreshed.")

def update_team_results():
    print("Team results refreshed.")

def close_points_window(points_window):
    points_window.destroy()

def create_refresh_button(window, update_function):
    """
    Creates a styled "Refresh" button in the given window.
    
    window: The window where the button will be placed.
    update_function: The function to call when the button is clicked.
    """
    style = ttk.Style()
    style.configure('Refresh.TButton', font=('Helvetica', 10, 'bold'), foreground='green')
    
    refresh_button = ttk.Button(window, text="Refresh", style='Refresh.TButton', command=update_function )
    refresh_button.pack(pady=10)

def generate_random_names(number_of_names):
    return random.sample(names, number_of_names)

def generate_random_scores_and_ranks(num_scores, max_score=5):
    scores = [random.randint(1, max_score) for _ in range(num_scores)]
    ranks = ['R' + str(score) for score in scores]
    return scores, ranks

def generate_random_events(num_events, max_score=10):
    return [f'Event {i+1}' for i in range(num_events)]

def generate_random_scores_and_ranks(num_scores, max_score=5):
    scores = [random.randint(1, max_score) for _ in range(num_scores)]
    ranks = ['R' + str(score) for score in scores]
    return scores, ranks

# convert rank to points func
def assign_points(event_type, rank):
    if event_type == 'team_sport':
        return team_sport_points.get(rank, 0)
    elif event_type == 'ranked_event':
        return ranked_event_points.get(rank, 0)
    else:
        return rank_points.get(rank, 0)  
#--------------------------------------------------------|



#func for buttons and screens

#--------------------------------------------------------#--------------------------------------------------------|
# func to set up the dynamic point systems
def set_points_system():
    points_window = tk.Toplevel(window)
    points_window.title("Set Points System")

    guideline_text = ("Enter the points for each outcome in team sports and ranks in ranked events.\n"
                      "For example, enter how many points a Win, Draw, or Loss should be worth, and\n"
                      "how many points each rank (R1, R2, etc.) should receive.")
    guideline_label = tk.Label(points_window, text=guideline_text, justify=tk.LEFT)
    guideline_label.pack(pady=10)

    # entry fields for team sports points
    team_points_entries = {}
    for outcome in ['Win', 'Draw', 'Lose']:
        frame = tk.Frame(points_window)
        frame.pack(padx=10, pady=5, fill=tk.X)
        tk.Label(frame, text=f"Points for {outcome}: ", width=15, anchor='w').pack(side=tk.LEFT)
        points_entry = tk.Entry(frame, width=5)
        points_entry.pack(side=tk.LEFT)
        team_points_entries[outcome] = points_entry

    tk.Label(points_window, text="Set Points for Ranked Events", font=('Helvetica', 14, 'bold')).pack(pady=10)

    # entry fields for ranked events points
    ranked_points_entries = {}
    for rank in ['R1', 'R2', 'R3', 'R4', 'R5']:
        frame = tk.Frame(points_window)
        frame.pack(padx=10, pady=5, fill=tk.X)
        tk.Label(frame, text=f"Points for {rank}: ", width=15, anchor='w').pack(side=tk.LEFT)
        points_entry = tk.Entry(frame, width=5)
        points_entry.pack(side=tk.LEFT)
        ranked_points_entries[rank] = points_entry

    def save_points():
        # save points for team sports
        for outcome, entry in team_points_entries.items():
            try:
                team_sport_points[outcome] = int(entry.get())
            except ValueError:
                tk.messagebox.showerror("Error", f"Invalid entry for {outcome}. Please enter a number.")
                return
        # save points for ranked events
        for rank, entry in ranked_points_entries.items():
            try:
                ranked_event_points[rank] = int(entry.get())
            except ValueError:
                tk.messagebox.showerror("Error", f"Invalid entry for {rank}. Please enter a number.")
                return
        points_window.destroy()

    save_button = tk.Button(points_window, text="Save Points", command=save_points)
    save_button.pack(pady=15)
    save_button.config(bg='green', fg='black', font=('Helvetica', 13, 'bold'))

    # "Cancel" button
    cancel_button = tk.Button(points_window, text="Cancel", command=lambda: close_points_window(points_window))
    cancel_button.pack(pady=5)
    cancel_button.config(bg='red', fg='blue', font=('Helvetica', 13, 'bold'))

#func to setup a tournament
def open_tournament_setup():
    setup_window = tk.Toplevel(window)
    setup_window.title("Initialize New Tournament")

    guideline_text = ("To start a new tournament, enter the tournament name and a brief description.\n"
                      "Choose whether it's an 'Individual' or 'Team' event type.\n"
                      "Select the ranking type for the events and add them to your tournament.\n"
                      "Press 'Finish' once all events are added.")
    guideline_label = tk.Label(setup_window, text=guideline_text, justify=tk.LEFT)
    guideline_label.pack(pady=10)

    tk.Label(setup_window, text="Tournament Setup", font=('Helvetica', 18, 'bold')).pack(pady=10)

    event_type = tk.StringVar()
    tk.Radiobutton(setup_window, text="Individual Events", variable=event_type, value="Individual").pack()
    tk.Radiobutton(setup_window, text="Team Events", variable=event_type, value="Team").pack()

    tk.Label(setup_window, text="Name").pack()
    name_entry = tk.Entry(setup_window)
    name_entry.pack()

    tk.Label(setup_window, text="Description").pack()
    description_text = tk.Text(setup_window, height=5, width=40)
    description_text.pack()

    ranking_type = tk.StringVar()
    ranking_type_dropdown = ttk.Combobox(setup_window, textvariable=ranking_type, values=("Win/Lose/Draw", "Ranked"), state="readonly")
    ranking_type_dropdown.pack()
    ranking_type.set("Win/Lose/Draw")

    def add_event_to_list(event_name, event_type_selected, ranking_type_selected, event_for):
        if len(current_tournament_events) >= 5:
            tk.messagebox.showerror("Error", "Cannot add more than 5 events to the tournament.")
            return

        current_tournament = tournaments[-1] if tournaments else None
        if current_tournament:
            if not event_name.strip():
                tk.messagebox.showerror("Error", "Event name cannot be empty.")
                return
            if any(event['name'] == event_name for event in current_tournament['events']):
                tk.messagebox.showerror("Error", f"An event with the name '{event_name}' already exists in the tournament.")
                return

            current_tournament['events'].append({
                'name': event_name,
                'type': event_type_selected,
                'ranking_type': ranking_type,
                'for': event_type
            })
            current_tournament_events.append({
                'name': event_name,
                'type': event_type_selected,
                'ranking_type': ranking_type,
                'for': event_type
            })
            event_table.insert('', 'end', values=(event_name, event_type_selected, ranking_type_selected, event_for))

            name_entry.delete(0, 'end')
            description_text.delete('1.0', tk.END)

    academic_event_button = tk.Button(setup_window, text="Add Academic Event", command=lambda: add_event_to_list(name_entry.get(), "Academic", ranking_type.get(), event_type.get()))
    academic_event_button.pack()

    sporting_event_button = tk.Button(setup_window, text="Add Sporting Event", command=lambda: add_event_to_list(name_entry.get(), "Sporting", ranking_type.get(), event_type.get()))
    sporting_event_button.pack()

    finish_button = tk.Button(setup_window, text="Finish", command=lambda: setup_window.destroy())
    finish_button.pack(pady=20)

    tk.Label(setup_window, text="Event List", font=('Helvetica', 14)).pack()

    columns = ('#1', '#2')
    event_table = ttk.Treeview(setup_window, columns=columns, show='headings')
    event_table.heading('#1', text='Event Name')
    event_table.heading('#2', text='Event Type')
    event_table.column('#1', width=120, anchor='center')
    event_table.column('#2', width=120, anchor='center')
    event_table.pack()

    # append a new tournament dictionary if this is a new tournament
    if not tournaments:
        tournaments.append({
            'name': '',
            'description': '',
            'events': []
        })

    # populate the event table with existing events if there are any
    for event in current_tournament_events:
        event_table.insert('', 'end', values=(event['name'], event['type'], event.get('ranking_type', 'N/A'), event.get('for', 'N/A')))

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
    else:
        event_dropdown['state'] = 'disabled'  # disable if no events

    ranking_entries = []
    for i, individual in enumerate(individuals, start=1):
        tk.Label(second_frame, text=individual, anchor="w").grid(row=i, column=0, padx=10, pady=5, sticky="w")

        rank_var = tk.StringVar(value='R0')
        rank_dropdown = ttk.Combobox(second_frame, textvariable=rank_var, values=list(rank_points.keys()), state="readonly")
        rank_dropdown.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
        ranking_entries.append((individual, rank_var))

    # func to save rankings and points
    def save_individual_ranking():
        event_name = selected_event.get()
        event_info = next((e for e in current_tournament_events if e['name'] == event_name), None)
        if event_info:
            for individual, rank_var in ranking_entries:
                rank = rank_var.get()
                points = assign_points(event_info['type'], rank)  # Use event type to assign points
                individual_ranking_data.append({
                    'name': individual,
                    'event': event_name,
                    'rank': rank,
                    'points': points
                })
        
        
        ranking_window.destroy()

    save_button = tk.Button(second_frame, text="Save Ranking", command=save_individual_ranking)
    save_button.grid(row=len(individuals) + 1, column=1, pady=10)

    
    second_frame.update_idletasks()
    my_canvas.config(scrollregion=my_canvas.bbox("all"))

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
    else:
        event_dropdown['state'] = 'disabled'  # disable if no events

    ranking_entries = []
    for i, individual in enumerate(individuals, start=1):
        tk.Label(second_frame, text=individual, anchor="w").grid(row=i, column=0, padx=10, pady=5, sticky="w")

        rank_var = tk.StringVar(value='R0')
        rank_dropdown = ttk.Combobox(second_frame, textvariable=rank_var, values=list(rank_points.keys()), state="readonly")
        rank_dropdown.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
        ranking_entries.append((individual, rank_var))

    # func to save rankings and points
    def save_individual_ranking():
        event_name = selected_event.get()
        event_info = next((e for e in current_tournament_events if e['name'] == event_name), None)
        if event_info:
            for individual, rank_var in ranking_entries:
                rank = rank_var.get()
                points = assign_points(event_info['type'], rank)  # Use event type to assign points
                individual_ranking_data.append({
                    'name': individual,
                    'event': event_name,
                    'rank': rank,
                    'points': points
                })
        
        
        ranking_window.destroy()

    save_button = tk.Button(second_frame, text="Save Ranking", command=save_individual_ranking)
    save_button.grid(row=len(individuals) + 1, column=1, pady=10)

    
    second_frame.update_idletasks()
    my_canvas.config(scrollregion=my_canvas.bbox("all"))

    create_back_button(ranking_window)

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
    else:
        event_dropdown['state'] = 'disabled'  # disable if no events


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

    create_back_button(ranking_window)

#func to open results of individuals
def open_results_individual():
    individual_results_window = tk.Toplevel(window)
    individual_results_window.title("Results by Event (Individual)")

    tk.Label(individual_results_window, text="Results by Event (Individual)", font=('Helvetica', 18, 'bold')).pack(pady=10)

    # table for displaying results 
    columns = ('#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8', '#9')
    individual_results_table = ttk.Treeview(individual_results_window, columns=columns, show='headings')
    headings = ['Individual Name'] + generate_random_events(5) + ['Sportsmanship', 'Total Points', 'Final Rank']
    for i, heading in enumerate(headings):
        individual_results_table.heading(f'#{i+1}', text=heading)
        individual_results_table.column(f'#{i+1}', width=120, anchor='center')

    individuals_data = []
    for _ in range(MAX_INDIVIDUALS):  
        name = generate_random_names(1)[0]
        scores, ranks = generate_random_scores_and_ranks(5)
        sportsmanship = random.randint(1, 5)
        total_points = sum([rank_points[rank] for rank in ranks]) + sportsmanship
        individuals_data.append((name, ranks, sportsmanship, total_points))

    # sort individuals by total points and assign ranks
    sorted_individuals = sorted(individuals_data, key=lambda x: x[3], reverse=True)
    for rank, (name, ranks, sportsmanship, total_points) in enumerate(sorted_individuals, start=1):
        individual_results_table.insert('', 'end', values=(name, *ranks, sportsmanship, total_points, f'R{rank}'))

    individual_results_table.pack()

    create_back_button(individual_results_window)
    create_refresh_button(individual_results_window, update_individual_results)

#func to open results of teams
def open_results_teams():
    teams_results_window = tk.Toplevel(window)
    teams_results_window.title("Results by Event (Teams)")

    tk.Label(teams_results_window, text="Results by Event (Teams)", font=('Helvetica', 18, 'bold')).pack(pady=10)

    # table for displaying results with updated columns
    columns = ('#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8', '#9', '#10')
    teams_results_table = ttk.Treeview(teams_results_window, columns=columns, show='headings')
    headings = ['Team', 'Members'] + [f'Event {i+1}' for i in range(5)] + ['Sportsmanship Points', 'Total Points', 'Final Rank']
    for i, heading in enumerate(headings):
        teams_results_table.heading(f'#{i+1}', text=heading)
        teams_results_table.column(f'#{i+1}', width=120, anchor='center')

    all_individuals = generate_random_names(MAX_INDIVIDUALS)
    shuffled_individuals = random.sample(all_individuals, len(all_individuals))
    teams = {f'Team {chr(65+i)}': shuffled_individuals[i*5:(i+1)*5] for i in range(MAX_TEAMS)}

    team_points_and_ranks = {}
    for team_name, members in teams.items():
        scores, ranks = generate_random_scores_and_ranks(5)
        sportsmanship = random.randint(1, 5)
        total_points = sum(rank_points[rank] for rank in ranks) + sportsmanship
        team_points_and_ranks[team_name] = (members, ranks, sportsmanship, total_points)
    
    # sort teams by total points for final ranking
    sorted_teams = sorted(team_points_and_ranks.items(), key=lambda item: item[1][3], reverse=True)
    final_rankings = {team: index+1 for index, (team, _) in enumerate(sorted_teams)}

    # insert sorted data into the table
    for team_name, (members, ranks, sportsmanship, total_points) in sorted_teams:
        final_rank = f'R{final_rankings[team_name]}'
        teams_results_table.insert('', 'end', values=(team_name, ', '.join(members), *ranks, sportsmanship, total_points, final_rank))

    teams_results_table.pack()

    create_back_button(teams_results_window)
    create_refresh_button(teams_results_window, update_team_results)

#func to assigned individuals to specific event
def assign_individuals_to_events():
    assignment_window = tk.Toplevel(window)
    assignment_window.title("Assign Individuals to Events")

    tk.Label(assignment_window, text="Select Individual:").pack()
    individual_var = tk.StringVar()
    individual_dropdown = ttk.Combobox(assignment_window, textvariable=individual_var, values=individuals, state="readonly")
    individual_dropdown.pack()

    tk.Label(assignment_window, text="Select Event(s):").pack()
    event_vars = {}
    for event in current_tournament_events:
        var = tk.BooleanVar()
        tk.Checkbutton(assignment_window, text=event['name'], variable=var).pack()
        event_vars[event['name']] = var

    def save_assignments():
        selected_individual = individual_var.get()
        selected_events = [event for event, var in event_vars.items() if var.get()]

        # check if the individual is already registered for 5 events
        if selected_individual in individual_event_registrations:
            if len(individual_event_registrations[selected_individual]) + len(selected_events) > 5:
                tk.messagebox.showerror("Error", f"Cannot assign {selected_individual} to more than 5 events.")
                return
            else:
                # add to existing registrations if under 5
                individual_event_registrations[selected_individual].extend(selected_events)
        else:
            if len(selected_events) > 5:
                tk.messagebox.showerror("Error", f"Cannot assign {selected_individual} to more than 5 events.")
                return
            else:
                # create new registration if under 5
                individual_event_registrations[selected_individual] = selected_events

        tk.messagebox.showinfo("Success", f"{selected_individual} has been assigned to selected events.")
        assignment_window.destroy()

    tk.Button(assignment_window, text="Save Assignments", command=save_assignments).pack()

    create_back_button(assignment_window)

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
    
    create_back_button(display_window)

#manage team func to add, delete and manage team members
def open_manage_teams():
    manage_teams_window = tk.Toplevel(window)
    manage_teams_window.title("Manage Teams")

    guideline_text = ("Select a team from the list and use the checkboxes to manage team members.\n"
                      "'Add Players to Team' will add the selected players to the team, up to 5 members.\n"
                      "'Remove Selected Players from Team' will remove them.")
    guideline_label = tk.Label(manage_teams_window, text=guideline_text, justify=tk.LEFT)
    guideline_label.pack(pady=10)

    # listbox to display teams for selection
    teams_listbox = tk.Listbox(manage_teams_window)
    teams_listbox.pack()

    for team in teams.keys():
        teams_listbox.insert(tk.END, team)

    # func to handle adding players to the selected team
    def add_players_to_team():
        selected_team_index = teams_listbox.curselection()
        if selected_team_index:
            selected_team = teams_listbox.get(selected_team_index[0])
            selected_players = [player for player, var in player_checkboxes.items() if var.get()]
            
            # check if adding the selected players exceeds the limit of 5 members per team
            if len(teams[selected_team]) + len(selected_players) > 5:
                tk.messagebox.showerror("Error", "Cannot add more players. Each team can have only 5 members.") #error shown in the command line interface.
                return
            
            # add selected players to the selected team, avoiding duplicates
            updated_members = list(set(teams[selected_team] + selected_players))
            teams[selected_team] = updated_members[:5]  # Ensure the team does not exceed 5 members
            
            display_individuals_and_teams()

        for var in player_checkboxes.values():
            var.set(False)

    # func to handle removing players from the selected team
    def remove_players_from_team():
        selected_team_index = teams_listbox.curselection()
        if selected_team_index:
            selected_team = teams_listbox.get(selected_team_index[0])
            selected_players = [player for player, var in player_checkboxes.items() if var.get()]
            
            # Remove selected players from the team
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

#func that will give user guidlines and contanc info 
def open_help():
    help_window = tk.Toplevel(window)
    help_window.title("Help and Contact Information")

    info_text = ("Scoring System Help\n\n"
                 "This Scoring System application allows you to manage tournaments, teams, and individual rankings.\n"
                 "You can set up new tournaments, input player and team details, manage teams, and input ranking results.\n"
                 "For detailed instructions on how to use each feature, please navigate to the corresponding section and check the notes.\n\n"
                 "For feedback and repairs, please contact:\n"
                 "Email: nazaruk7649@ukr.net\n"
                 "Number: 07523703451")
    info_label = tk.Label(help_window, text=info_text, justify=tk.LEFT)
    info_label.pack(pady=10)
#----------------------------------------------------------------------------------------------------------------|


#--------------------------------------------------------|
# main window setup
window = tk.Tk()
window.title("Scoring System")
window.geometry("1100x900")  # the size can be changed easily here

# menu frame
main_menu_frame = tk.Frame(window, bg="white")
main_menu_frame.pack(pady=100)
#--------------------------------------------------------|





#----------------------------------------------------------------------------------------------------------------|
# "Help" button
help_button = tk.Button(main_menu_frame, text="Help", width=20, height=2,
                         command=open_help)
help_button.pack(pady=10)

# "Start New Tournament" button
set_button = tk.Button(main_menu_frame, text="Set Points System", width=20, height=2,
                         command=set_points_system)
set_button.pack(pady=10)

# "Start New Tournament" button
start_button = tk.Button(main_menu_frame, text="Start New Tournament", width=20, height=2,
                         command=open_tournament_setup)
start_button.pack(pady=10)

# "Input Player and Teams" button
input_names_button = tk.Button(main_menu_frame, text="Input Player and Teams ",width=20, height=2, command=input_player_names)
input_names_button.pack(pady=10)

assign_events_button = tk.Button(main_menu_frame, text="Assign Individuals to Events",width=20, height=2, command=assign_individuals_to_events)
assign_events_button.pack(pady=10)

show_button = tk.Button(main_menu_frame, text="Display Individuals And Teams", width=20, height=2,
                         command=display_individuals_and_teams)
show_button.pack(pady=10)

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

# the Exit button with an icon and style
exit_button = ttk.Button(window, text="Exit", style='Exit.TButton', command=exit_application)
#exit_button = ttk.Button(window, text="Exit", style='Exit.TButton', image=exit_icon, compound=tk.LEFT, command=exit_application)  # can be used if photo uploaded
exit_button.pack(side='bottom', anchor='w', padx=10, pady=10)


# run the main loop
window.mainloop()
#----------------------------------------------------------------------------------------------------------------|



#tests for NON_GUI functions
#----------------------------------------------------------------------------------------------------------------|
def test_generate_random_names():
    number_of_names = 5
    result = generate_random_names(number_of_names)
    assert len(result) == number_of_names  # check if the correct number of names are generated
    assert len(set(result)) == number_of_names  # check if all names are unique

def test_generate_random_scores_and_ranks():
    num_scores = 5
    max_score = 5
    scores, ranks = generate_random_scores_and_ranks(num_scores, max_score)
    assert len(scores) == num_scores
    assert all(1 <= score <= max_score for score in scores)  # check if scores are within the correct range

def test_assign_points_individual_sport():
    assert assign_points('individual_sport', 'R1') == 10
    assert assign_points('individual_sport', 'R2') == 8

def test_assign_points_team_sport():
    team_sport_points['Win'] = 3  
    team_sport_points['Draw'] = 1  
    assert assign_points('team_sport', 'Win') == 3
    assert assign_points('team_sport', 'Draw') == 1


# running the tests with pytest
if __name__ == "__main__":
    pytest.main()

#----------------------------------------------------------------------------------------------------------------|