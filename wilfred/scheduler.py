#################################################################
#                                                               #
# Wilfred                                                       #
# Copyright (C) 2020, Vilhelm Prytz, <vilhelm@prytznet.se>      #
#                                                               #
# Licensed under the terms of the MIT license, see LICENSE.     #
# https://github.com/wilfred-dev/wilfred                        #
#                                                               #
#################################################################

import click

from tabulate import tabulate

from wilfred.database import session, ScheduledTask


class TaskScheduler(object):
    def __init__(self, server):
        self._server = server

    def pretty(self):
        data = [u.__dict__ for u in self._server.scheduled_tasks]

        headers = {
            "minute": click.style("Minute", bold=True),
            "hour": click.style("Hour", bold=True),
            "day_of_the_month": click.style("Day of the Month", bold=True),
            "month": click.style("Month", bold=True),
            "day_of_the_week": click.style("Hour", bold=True),
            "task_type": click.style("Task Type", bold=True),
            "value": click.style("Value", bold=True),
        }

        return tabulate(data, headers=headers, tablefmt="fancy_grid",)

    def create(
        self, minute, hour, day_of_the_month, month, day_of_the_week, task_type, value
    ):
        # create
        new_task = ScheduledTask(
            server_id=self._server.id,
            minute=minute,
            hour=hour,
            day_of_the_month=day_of_the_month,
            month=month,
            day_of_the_week=day_of_the_week,
            task_type=task_type,
            value=value,
        )
        session.add(new_task)

        try:
            session.commit()
        except Exception as e:
            raise Exception(f"could not create task, {str(e)}")
