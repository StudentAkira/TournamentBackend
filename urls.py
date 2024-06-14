from enum import Enum


class URLs(Enum):
    #auth
    auth_prefix = "/api/auth"
    auth_tags = ["auth"]
    login = "/login"
    logout = "/logout"

    #event
    event_prefix = "/api/event"
    event_tags = ["event"]
    get_event_by_id = "/event/get_by_id"
    event = "/event"
    get_event_with_nominations = "/events_with_nominations"

    #match
    match_prefix = "/api/match"
    match_tags = ["match"]
    get_group_matches = "/get_group_matches"
    get_bracket_matches = "/get_bracket_matches"
    set_group_match_result = "/set_group_match_result"
    set_bracket_match_result = "/set_bracket_match_result"

    #nomination
    nomination_prefix = "/api/nomination"
    nomination_tags = ["nomination"]
    nomination = "/nomination"
    get_nominations_related_to_event = "/get_nominations_related_to_event"
    get_nominations_not_related_to_event = "/get_nominations_not_related_to_event"

    #nomination_event
    nomination_event_prefix = "/api/nomination_event"
    nomination_event_tags = ["nomination_event"]
    nomination_event_pdf = "/nomination_event_pdf"
    nomination_event_data = "/nomination_event_data"
    nomination_event_full_info = "/nomination_event_full_info"
    append_nomination_for_event = "/append_nomination_for_event"
    delete_nomination_from_event = "/delete_nomination_from_event"
    close_registration = "/close_registration"
    open_registration = "/open_registration"

    #nomination_event_judge
    nomination_evnet_judge = "/api/nomination_event_judge"
    nomination_event_judge_tags = ["nomination_event_judge"]
    nomination_event_judge = "/nomination_event_judge"

    #participant
    participant_prefix = "/api/participant"
    participant_tags = ["participant"]
    participant = "/participant"

    #race_round
    race_round_prefix = "/api/race_round"
    race_round_tags = ["race_round"]
    race_round = "/race_round"

    #team
    team_prefix = "/api/team"
    team_tags = ["team"]
    teams = "/teams"

    #team_participant
    team_participant_prefix = "/api/team_participant"
    team_participant_tags = ["team_participant"]
    team_participant = "/team_participant"

    #team_participant_nomination_event
    team_participant_nomination_event_prefix = "/api/team_participant_nomination_event"
    team_participant_nomination_event_tags = ["team_participant_nomination_event"]

    #tournament
    tournaments_prefix = "/api/tournaments"
    tournaments_tags = ["tournaments"]
    get_groups_of_tournament = "/get_groups_of_tournament"
    start_group_stage = "/start_group_stage"
    finish_group_stage = "/finish_group_stage"
    start_play_off_stage = "/start_play_off_stage"
    finish_play_off_stage = "/finish_play_off_stage"

    #user
    user_prefix = "/api/user"
    user_tags = ["user"]
    profile = "/profile"
    users = "/users"
    create_admin = "/create_admin"
    create_user = "/create_user"


