import pytest
import random

# ----------------------------------------------------------------------------------------------------------------|
# Global variables for testing
MAX_TEAMS = 4
MAX_INDIVIDUALS = 20

individuals = []
teams = {}
individual_event_registrations = {}

rank_points = {'R1': 10, 'R2': 8, 'R3': 6, 'R4': 4, 'R5': 2, 'R0': 0}
team_sport_points = {'Win': 3, 'Draw': 1, 'Lose': 0}

names = ['Oliver', 'Harry', 'George', 'Noah', 'Jack', 'Leo', 'Arthur', 'Muhammad', 'Oscar', 'Charlie',
         'Jacob', 'Thomas', 'Henry', 'Freddie', 'Alfie', 'Theo', 'William', 'James', 'Ethan', 'Archie']


# ----------------------------------------------------------------------------------------------------------------|
# tests based on feedback from Kostya
# ----------------------------------------------------------------------------------------------------------------|

def generate_random_names(number_of_names):
    return random.sample(names, number_of_names)


def generate_random_scores_and_ranks(num_scores, max_score=5):
    scores = [random.randint(1, max_score) for _ in range(num_scores)]
    ranks = ['R' + str(score) for score in scores]
    return scores, ranks


# generate random names
def test_generate_random_names():
    number_of_names = 5
    result = generate_random_names(number_of_names)
    assert len(result) == number_of_names
    assert len(set(result)) == number_of_names


# generate random scores and ranks
def test_generate_random_scores_and_ranks():
    num_scores = 5
    max_score = 5
    scores, ranks = generate_random_scores_and_ranks(num_scores, max_score)
    assert len(scores) == num_scores
    assert all(1 <= score <= max_score for score in scores)


# prevent exceeding individual registration limit
def test_register_individual():
    global individuals
    individuals = ["Player " + str(i) for i in range(MAX_INDIVIDUALS)]  # Fill up to max
    with pytest.raises(ValueError, match="Cannot register more individuals!"):
        if len(individuals) >= MAX_INDIVIDUALS:
            raise ValueError("Cannot register more individuals!")


# assign points based on event type
def test_assign_points():
    def assign_points(event_type, rank):
        if event_type == 'team_sport':
            return team_sport_points.get(rank, 0)
        else:
            return rank_points.get(rank, 0)

    assert assign_points('team_sport', 'Win') == 3
    assert assign_points('individual_sport', 'R1') == 10
    assert assign_points('individual_sport', 'R2') == 8


# resolve tie-breaker by points
def test_resolve_tie_breaker():
    ranking_data = [
        {"name": "Player A", "points": 10},
        {"name": "Player B", "points": 10},
        {"name": "Player C", "points": 8}
    ]
    sorted_data = sorted(ranking_data, key=lambda x: (-x['points'], x['name']))
    assert sorted_data[0]["name"] == "Player A"  # Ensures alphabetical tie-breaking


# performance
def test_stress_test_registration():
    global individual_event_registrations
    individual_event_registrations.clear()
    for i in range(500):
        individual_event_registrations[f"Player {i + 1}"] = ["Event 1"]
    assert len(individual_event_registrations) == 500


# ----------------------------------------------------------------------------------------------------------------|
# run all tests
if __name__ == "__main__":
    pytest.main()