"""Module containing convenience functions for working with the API."""
import time

from nailgun import entities
from robottelo.common.helpers import bz_bug_is_open


def enable_rhrepo_and_fetchid(basearch, org_id, product, repo,
                              reposet, releasever):
    """Enable a RedHat Repository and fetches it's Id.

    :param str org_id: The organization Id.
    :param str product: The product name in which repository exists.
    :param str reposet: The reposet name in which repository exists.
    :param str repo: The repository name who's Id is to be fetched.
    :param str basearch: The architecture of the repository.
    :param str releasever: The releasever of the repository.
    :return: Returns the repository Id.
    :rtype: str

    """
    product = entities.Product(name=product, organization=org_id).search()[0]
    r_set = entities.RepositorySet(name=reposet, product=product).search()[0]
    payload = {}
    if basearch is not None:
        payload['basearch'] = basearch
    if releasever is not None:
        payload['releasever'] = releasever
    r_set.enable(payload)
    result = entities.Repository(name=repo).search(
        query={'organization_id': org_id})
    if bz_bug_is_open(1252101):
        for _ in range(5):
            if len(result) > 0:
                break
            time.sleep(5)
            result = entities.Repository(name=repo).search(
                query={'organization_id': org_id})
    return result[0].id
