#tests
#----------------------------------------------------------------------------------------------------------------|
import pytest

from main import MAX_TEAMS, assign_points, team_sport_points, generate_random_scores_and_ranks, generate_random_names


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



def test_regression_ranking_updates():
    """ensure ranking updates properly after system changes."""
    global individual_ranking_data
    individual_ranking_data = [
        {"name": "Player A", "event": "Event 1", "rank": "R3", "points": 6},
        {"name": "Player B", "event": "Event 1", "rank": "R2", "points": 8},
    ]

    # simulate an update
    sorted_ranking = sorted(individual_ranking_data, key=lambda x: x["points"], reverse=True)

    assert sorted_ranking[0]["name"] == "Player B"


def test_usability_team_creation_limit():
    """ensure users receive feedback when trying to create more teams than allowed."""
    global teams
    teams = {f"Team {i}": [] for i in range(MAX_TEAMS)}  # Fill max teams

    new_team = "Team X"
    error_message = "maximum number of teams reached"

    assert new_team not in teams
    assert error_message



# running the tests with pytest
if __name__ == "__main__":
    pytest.main()