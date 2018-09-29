def check_correct_user_prediction(match_state, goals_home, goals_away):
    error_state = {'state': False, 'error': 'N/A'}
    if match_state == 'home' and goals_home <= goals_away:
        error_state['state'] = True
        error_state['error'] = 'Predicted win for home team, but home team goals are less than away team goals'
    if match_state == 'away' and goals_home >= goals_away:
        error_state['state'] = True
        error_state['error'] = 'Predicted win for away team, but away team goals are less than home team goals'
    if match_state == 'tie' and goals_home != goals_away:
        error_state['state'] = True
        error_state['error'] = 'Predicted tie, but away team goals and home team goals are not equal'
    return error_state
