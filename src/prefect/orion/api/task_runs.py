from typing import List

import sqlalchemy as sa
from fastapi import Depends, HTTPException

from prefect.orion import models, schemas
from prefect.orion.api import dependencies
from prefect.orion.utilities.server import OrionRouter

router = OrionRouter(prefix="/task_runs", tags=["task_runs"])


@router.post("/")
async def create_task_run(
    task_run: schemas.actions.TaskRunCreate,
    session: sa.orm.Session = Depends(dependencies.get_session),
) -> schemas.core.TaskRun:
    """
    Create a task run
    """
    return await models.task_runs.create_task_run(session=session, task_run=task_run)


@router.get("/{task_run_id}")
async def read_task_run(
    task_run_id: str, session: sa.orm.Session = Depends(dependencies.get_session)
) -> schemas.core.TaskRun:
    """
    Get a task run by id
    """
    task_run = await models.task_runs.read_task_run(session=session, id=task_run_id)
    if not task_run:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_run


# TODO - whats the access pattern here?
# @router.get("/")
# async def read_task_runs(
#     offset: int = 0,
#     limit: int = 10,
#     session: sa.orm.Session = Depends(dependencies.get_session),
# ) -> List[schemas.core.TaskRun]:
#     """
#     Query for task runs
#     """
#     return await models.task_runs.read_task_runs(
#         session=session, offset=offset, limit=limit
#     )


@router.delete("/{task_run_id}", status_code=204)
async def delete_task_run(
    task_run_id: str, session: sa.orm.Session = Depends(dependencies.get_session)
):
    """
    Delete a task run by id
    """
    result = await models.task_runs.delete_task_run(session=session, id=task_run_id)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return result
