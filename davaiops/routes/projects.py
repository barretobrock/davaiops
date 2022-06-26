from pathlib import Path
import tempfile
from typing import (
    Union
)

import pandas as pd
from flask import (
    Blueprint,
    current_app,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    url_for
)
from davaiops.forms.actor_innerjoin import ActorInnerJoinForm
from davaiops.actor_inner_join import (
    inner_join_actors
)

projects = Blueprint('projects', __name__, url_prefix='/projects')


@projects.route('/aij/begin', methods=['GET', 'POST'])
def begin_actor_innerjoin():
    if request.method == 'POST':
        form = request.form
        a1, a2 = form.get('actor1'), form.get('actor2')
        endpoint = f'/projects/aij/{a1.replace(" ", "_")}/{a2.replace(" ", "_")}'
        return render_template('loading.html', endpoint=endpoint)
    form = ActorInnerJoinForm()
    return render_template('projects/actor_ij_entry.html', title='Actor InnerJoin', form=form)


@projects.route('/aij/<actor1>/<actor2>', methods=['GET'])
def do_innerjoin(actor1: Union[str, int], actor2: Union[str, int]):
    log = current_app.extensions['loguru']
    tmp_dir = Path(tempfile.gettempdir()).joinpath('innerjoin')
    tmp_dir.mkdir(parents=True, exist_ok=True)
    save_path = tmp_dir.joinpath(f'{actor1}|{actor2}.csv')
    if save_path.exists():
        log.debug('Current request was a duplicate - retrieving past results.')
        df = pd.read_csv(save_path)
    else:
        log.debug('New request - fetching results to perform inner join.')
        df, reason = inner_join_actors([actor1, actor2], log=log)
        if df is None:
            log.debug(f'df was None - reason: {reason}')
            flash(reason, 'warning')
            return redirect('/projects/aij/begin', code=302)
            # form = ActorInnerJoinForm()
            # return render_template('projects/actor_ij_entry.html', title='Actor InnerJoin', form=form)
        else:
            log.debug(f'Saving {df.shape[0]} rows to csv...')
            df.to_csv(save_path)
    results_list = df.to_dict(orient='records')
    # Get the proper name of the actors
    actor_a_name = results_list[0].get('actor_a')
    actor_b_name = results_list[0].get('actor_b')
    return render_template(
        'render_datatable.html',
        tbl_id_name='aij-results',
        order_list=[1, 'desc'],
        names=[actor_a_name, actor_b_name],
        header_maps={
            'ID': {
                'col': 'id',
                'path': 'https://www.imdb.com/title/tt%s/'
            },
            'Year': {
                'col': 'year'
            },
            'Title': {
                'col': 'title'
            },
            'Type': {
                'col': 'kind'
            },
            actor_a_name: {
                'col': 'role_name_a',
                'class': 'actor-1'
            },
            actor_b_name: {
                'col': 'role_name_b',
                'class': 'actor-2'
            },
        },
        results_list=results_list
    )
