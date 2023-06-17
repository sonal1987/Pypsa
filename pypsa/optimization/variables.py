#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Define optimisation variables from PyPSA networks with Linopy.
"""
import logging

from pypsa.descriptors import get_activity_mask
from pypsa.descriptors import get_switchable_as_dense as get_as_dense

logger = logging.getLogger(__name__)


def define_operational_variables(n, sns, c, attr):
    """
    Initializes variables for power dispatch for a given component and a given
    attribute.

    Parameters
    ----------
    n : pypsa.Network
    c : str
        name of the network component
    attr : str
        name of the attribute, e.g. 'p'
    """
    if n.df(c).empty:
        return

    active = get_activity_mask(n, c, sns) if n._multi_invest else None
    coords = [sns, n.df(c).index.rename(c)]
    n.model.add_variables(coords=coords, name=f"{c}-{attr}", mask=active)


def define_status_variables(n, sns, c):
    com_i = n.get_committable_i(c)

    if com_i.empty:
        return

    active = get_activity_mask(n, c, sns, com_i) if n._multi_invest else None
    coords = (sns, com_i)
    is_binary = not n._linearized_uc
    kwargs = dict(upper=1, lower=0) if not is_binary else {}
    n.model.add_variables(
        coords=coords, name=f"{c}-status", mask=active, binary=is_binary, **kwargs
    )


def define_start_up_variables(n, sns, c):
    com_i = n.get_committable_i(c)

    if com_i.empty:
        return

    active = get_activity_mask(n, c, sns, com_i) if n._multi_invest else None
    coords = (sns, com_i)
    is_binary = not n._linearized_uc
    kwargs = dict(upper=1, lower=0) if not is_binary else {}
    n.model.add_variables(
        coords=coords, name=f"{c}-start_up", mask=active, binary=is_binary, **kwargs
    )


def define_shut_down_variables(n, sns, c):
    com_i = n.get_committable_i(c)

    if com_i.empty:
        return

    active = get_activity_mask(n, c, sns, com_i) if n._multi_invest else None
    coords = (sns, com_i)
    is_binary = not n._linearized_uc
    kwargs = dict(upper=1, lower=0) if not is_binary else {}
    n.model.add_variables(
        coords=coords, name=f"{c}-shut_down", binary=is_binary, **kwargs, mask=active
    )


def define_nominal_variables(n, c, attr):
    """
    Initializes variables for nominal capacities for a given component and a
    given attribute.

    Parameters
    ----------
    n : pypsa.Network
    c : str
        network component of which the nominal capacity should be defined
    attr : str
        name of the variable, e.g. 'p_nom'
    """
    ext_i = n.get_extendable_i(c)
    if ext_i.empty:
        return

    n.model.add_variables(coords=[ext_i], name=f"{c}-{attr}")


def define_spillage_variables(n, sns):
    """
    Defines the spillage variables for storage units.
    """
    c = "StorageUnit"
    if n.df(c).empty:
        return

    upper = get_as_dense(n, c, "inflow", sns)
    if (upper.max() > 0).all():
        return

    active = get_activity_mask(n, c, sns).where(upper > 0, False)
    n.model.add_variables(0, upper, name="StorageUnit-spill", mask=active)


def define_loss_variables(n, sns, c):
    """
    Initializes variables for transmission losses.
    """
    if n.df(c).empty or c not in n.passive_branch_components:
        return

    active = get_activity_mask(n, c, sns) if n._multi_invest else None
    coords = [sns, n.df(c).index.rename(c)]
    n.model.add_variables(0, coords=coords, name=f"{c}-loss", mask=active)
