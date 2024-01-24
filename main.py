import tkinter as tk
from tkinter import ttk

# Global variables to store ranking data
individual_ranking_data = []
team_ranking_data = []
individuals = []
teams = {}

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
        # insert the new event
        event_table.insert('', 'end', values=(event_name, event_type_selected))
        # clear the data
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

def open_individual_ranking():
    ranking_window = tk.Toplevel(window)
    ranking_window.title("Individual Ranking Entry")

    tk.Label(ranking_window, text="Individual Ranking", font=('Helvetica', 18, 'bold')).pack(pady=10)

    #main frame 
    main_frame = tk.Frame(ranking_window)
    main_frame.pack(fill=tk.BOTH, expand=1)

    my_canvas = tk.Canvas(main_frame)
    my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    #scrollbar
    my_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

 
    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    second_frame = tk.Frame(my_canvas)

    #new frame 
    my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

    #entry widgets for individual rankings
    entries = {} 
    for i in range(1, 21):  #20 individual players
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
    save_button.pack(pady=10)

def open_team_ranking():
    ranking_window = tk.Toplevel(window)
    ranking_window.title("Team Ranking Entry")

    tk.Label(ranking_window, text="Team Ranking", font=('Helvetica', 18, 'bold')).pack(pady=10)

    #scrolling region to hold the rankings
    canvas = tk.Canvas(ranking_window)
    scrollbar = ttk.Scrollbar(ranking_window, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Dictionary to store entry widgets for team rankings
    entries = {}
    for i in range(1, 5):  # Assuming 4 teams
        tk.Label(scrollable_frame, text=f"Team {i}", anchor="w").grid(row=i, column=0, padx=10, pady=5, sticky="w")
        entry = tk.Entry(scrollable_frame)
        entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
        entries[f"Team {i}"] = entry

    #save button
    def save_team_ranking():

        ranking = {}
        for i in range(1, 5):  #4 teams
            team = f"Team {i}"
            ranking[team] = entries[team].get()
        team_ranking_data.append(ranking)
        ranking_window.destroy()

    save_button = tk.Button(ranking_window, text="Save Team Ranking", command=save_team_ranking)
    save_button.pack(pady=10)

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

    tk.Label(input_window, text="Enter player names, one per line:").pack()
    text_area = tk.Text(input_window, height=20, width=50)
    text_area.pack()

    def process_names():
        names = text_area.get("1.0", tk.END).strip().split('\n')
        current_team = 'A'  
        team_count = 0  
        
        for name in names:
            if name:  # ONLY non-empty names
                individual_id = len(individuals) + 1  
                individuals.append({'id': individual_id, 'name': name, 'team': f'Team {current_team}'})
                
  
                team_count += 1
                if team_count > 5:
           
                    current_team = chr(ord(current_team) + 1)
                    team_count = 1

            
                teams.setdefault(f'Team {current_team}', []).append(name)

        input_window.destroy()
        display_individuals_and_teams() 

    tk.Button(input_window, text="Submit", command=process_names).pack()

def display_individuals_and_teams():
    display_window = tk.Toplevel(window)
    display_window.title("Individuals and Teams")

    #display individuals
    individuals_tree = ttk.Treeview(display_window, columns=('Individual ID', 'Individual Name', 'Team'))
    individuals_tree.heading('#1', text='Individual ID')
    individuals_tree.heading('#2', text='Individual Name')
    individuals_tree.heading('#3', text='Team')
    individuals_tree.pack()

    #display teams
    teams_tree = ttk.Treeview(display_window, columns=('Team', 'Members'))
    teams_tree.heading('#1', text='Team')
    teams_tree.heading('#2', text='Members')
    teams_tree.pack()

    for individual in individuals:
        individuals_tree.insert('', 'end', values=(individual['id'], individual['name'], individual['team']))

    for team, members in teams.items():

        first_member_id = individuals[next(i for i, x in enumerate(individuals) if x['name'] == members[0])]['id']
        teams_tree.insert('', 'end', iid=first_member_id, values=(team, ', '.join(members)))

    teams_tree.pack()
    teams_tree.view('iid', '#0', sort_by='num')


# main window setup
window = tk.Tk()
window.title("Scoring System")
window.geometry("850x650")  # Adjust the size as necessary to fit content

# menu frame
main_menu_frame = tk.Frame(window, bg="white")
main_menu_frame.pack(pady=100)

#buttons that will be displayed on the main menu
start_button = tk.Button(main_menu_frame, text="Start New Tournament", width=20, height=2,
                         command=open_tournament_setup)
start_button.pack(pady=10)

input_names_button = tk.Button(main_menu_frame, text="Input Player Names",width=20, height=2, command=input_player_names)
input_names_button.pack(pady=10)

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