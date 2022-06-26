from typing import (
    List,
    Optional,
    Tuple,
    Union
)
from loguru._logger import Logger
import pandas as pd
from imdb import Cinemagoer

ia = Cinemagoer()


def extract_actor_details(actor: Union[str, float], log: Logger) -> Tuple[Optional[pd.DataFrame], str]:
    log.debug(f'Working with actor detail: {actor}')
    if isinstance(actor, str):
        # Get first result (hopefully the best match!)
        actor = actor.replace('_', ' ')
        person_search_results = next(iter(ia.search_person(name=actor)), None)
        if person_search_results is None:
            log.info('Person not found. Returning None.')
            return None, f'Actor not found by text: {actor}'
        # Get more detailed info about the actor selected
        actor_info = ia.get_person(personID=int(person_search_results.personID))
    elif isinstance(actor, float):
        actor_info = ia.get_person(personID=actor)
    else:
        log.info('Actor was not string or float type. Returning None.')
        return None, 'Unexpected input.'

    # Get filmography of them while they were in an acting role
    filmography = actor_info.data.get('filmography', {})
    # Make a dataframe of the actor's filmography
    actor_df = pd.DataFrame()
    for role, movies in filmography.items():
        if role == 'thanks':
            continue
        extracts = []
        for movie in movies:
            extracts.append({
                'id': movie.movieID,
                'title': movie.data.get('title'),
                'year': movie.data.get('year'),
                'kind': movie.data.get('kind'),
                'actor': actor_info.data.get('name'),
                'role': role,
                'role_name': [x.data.get('name') for x
                              in movie.currentRole] if isinstance(movie.currentRole, list) else None
            })
        actor_df = pd.concat([actor_df, pd.DataFrame(extracts).explode('role_name')])
    log.debug(f'Extracted {actor_df.shape[0]} rows of details')

    # Group all roles by movie id
    actor_df['year'] = actor_df['year'].apply(lambda x: str(int(x)) if not pd.isna(x) else '???')
    actor_df = actor_df.groupby(['id', 'year', 'title', 'kind'], as_index=False).agg({
        'actor': 'first',
        'role': lambda x: ', '.join(x.dropna().unique()),
        'role_name': lambda x: ', '.join(x.dropna().unique())
    })
    log.debug(f'Grouped details into {actor_df.shape[0]} rows.')
    return actor_df, 'Success'


def inner_join_actors(actors: List[Union[str, int]], log: Logger) -> Tuple[Optional[pd.DataFrame], str]:
    actor_dfs = []
    for actor in actors:
        # Add dataframe to list we'll merge
        df, reason = extract_actor_details(actor, log=log)
        if df is None:
            return None, reason
        actor_dfs.append(df)
    merged_df = pd.merge(*actor_dfs, on=['id', 'title', 'year', 'kind'], how='inner', suffixes=('_a', '_b'))

    if merged_df.empty:
        log.info('The inner joined dataframe was empty.')
        return None, 'Empty inner join - these actors likely haven\'t worked together :('
    log.debug(f'The inner joined dataframe resulted in {merged_df.shape[0]} rows of details.')
    return merged_df.sort_values(['year', 'title'], ascending=True).reset_index(drop=True), 'Success'
