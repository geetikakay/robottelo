# -*- encoding: utf-8 -*-
# vim: ts=4 sw=4 expandtab ai
"""Test class for Repository CLI"""

from ddt import ddt
from fauxfactory import gen_string
from nose.plugins.attrib import attr
from robottelo.cli.factory import (
    make_gpg_key,
    make_org,
    make_product,
    make_repository,
)
from robottelo.cli.repository import Repository
from robottelo.common.constants import (
    FAKE_0_YUM_REPO,
    FAKE_1_YUM_REPO,
    FAKE_2_YUM_REPO,
    FAKE_3_YUM_REPO,
    FAKE_4_YUM_REPO,
    FAKE_1_PUPPET_REPO,
    FAKE_2_PUPPET_REPO,
    FAKE_3_PUPPET_REPO,
    FAKE_4_PUPPET_REPO,
    FAKE_5_PUPPET_REPO,
)
from robottelo.common.decorators import (
    data,
    run_only_on,
    skip_if_bug_open,
    stubbed,
)
from robottelo.test import CLITestCase


@ddt
class TestRepository(CLITestCase):
    """Repository CLI tests."""

    org = None
    product = None

    def setUp(self):
        """Tests for Repositiry via Hammer CLI"""

        super(TestRepository, self).setUp()

        if TestRepository.org is None:
            TestRepository.org = make_org()
        if TestRepository.product is None:
            TestRepository.product = make_product(
                {u'organization-id': TestRepository.org['id']})

    def _make_repository(self, options=None):
        """Makes a new repository and asserts its success"""

        if options is None:
            options = {}

        if not options.get('product-id', None):
            options[u'product-id'] = self.product['id']

        new_repo = make_repository(options)

        # Fetch it
        result = Repository.info({u'id': new_repo['id']})

        self.assertEqual(
            result.return_code,
            0,
            "Repository was not found")
        self.assertEqual(
            len(result.stderr), 0, "No error was expected")

        # Return the repository dictionary
        return new_repo

    @run_only_on('sat')
    @skip_if_bug_open('bugzilla', 1129617)
    @data(
        gen_string('alpha', 15),
        gen_string('alphanumeric', 15),
        gen_string('numeric', 15),
        gen_string('latin1', 15),
        gen_string('utf8', 15),
        gen_string('html', 15),
    )
    @attr('cli', 'repository')
    def test_positive_create_1(self, name):
        """@Test: Check if repository can be created with random names

        @Feature: Repository

        @Assert: Repository is created and has random name

        """

        new_repo = self._make_repository({u'name': name})
        # Assert that name matches data passed
        self.assertEqual(new_repo['name'], name, "Names don't match")

    @run_only_on('sat')
    @skip_if_bug_open('bugzilla', 1129617)
    @data(
        gen_string('alpha', 15),
        gen_string('alphanumeric', 15),
        gen_string('numeric', 15),
        gen_string('latin1', 15),
        gen_string('utf8', 15),
        gen_string('html', 15),
    )
    @attr('cli', 'repository')
    def test_positive_create_2(self, name):
        """@Test: Check if repository can be created with random names and labels

        @Feature: Repository

        @Assert: Repository is created and has random name and labels

        """

        # Generate a random, 'safe' label
        label = gen_string('alpha', 20)

        new_repo = self._make_repository({u'name': name, u'label': label})
        # Assert that name matches data passed
        self.assertEqual(new_repo['name'], name, "Names don't match")
        self.assertNotEqual(
            new_repo['name'],
            new_repo['label'],
            "Label should not match the repository name"
        )

    @run_only_on('sat')
    @skip_if_bug_open('bugzilla', 1129617)
    @data(
        {u'url': FAKE_3_YUM_REPO, u'content-type': u'yum'},
        {u'url': FAKE_4_YUM_REPO, u'content-type': u'yum'},
        {u'url': FAKE_0_YUM_REPO, u'content-type': u'yum'},
        {u'url': FAKE_2_YUM_REPO, u'content-type': u'yum'},
        {u'url': FAKE_1_YUM_REPO, u'content-type': u'yum'},
    )
    @attr('cli', 'repository')
    def test_positive_create_3(self, test_data):
        """@Test: Create YUM repository

        @Feature: Repository

        @Assert: YUM repository is created

        """

        new_repo = self._make_repository(
            {u'url': test_data['url'],
             u'content-type': test_data['content-type']})
        # Assert that urls and content types matches data passed
        self.assertEqual(
            new_repo['url'], test_data['url'], "Urls don't match")
        self.assertEqual(
            new_repo['content-type'],
            test_data['content-type'],
            "Content Types don't match"
        )

    @run_only_on('sat')
    @skip_if_bug_open('bugzilla', 1129617)
    @data(
        {u'url': FAKE_1_PUPPET_REPO, u'content-type': u'puppet'},
        {u'url': FAKE_2_PUPPET_REPO, u'content-type': u'puppet'},
        {u'url': FAKE_3_PUPPET_REPO, u'content-type': u'puppet'},
        {u'url': FAKE_4_PUPPET_REPO, u'content-type': u'puppet'},
        {u'url': FAKE_5_PUPPET_REPO, u'content-type': u'puppet'},
    )
    @attr('cli', 'repository')
    def test_positive_create_4(self, test_data):
        """@Test: Create Puppet repository

        @Feature: Repository

        @Assert: Puppet repository is created

        """

        new_repo = self._make_repository(
            {u'url': test_data['url'],
             u'content-type': test_data['content-type']})
        # Assert that urls and content types matches data passed
        self.assertEqual(
            new_repo['url'], test_data['url'], "Urls don't match")
        self.assertEqual(
            new_repo['content-type'],
            test_data['content-type'],
            "Content Types don't match"
        )

    @run_only_on('sat')
    @skip_if_bug_open('bugzilla', 1083236)
    @skip_if_bug_open('bugzilla', 1129617)
    @data(
        gen_string('alpha', 15),
        gen_string('alphanumeric', 15),
        gen_string('numeric', 15),
        gen_string('latin1', 15),
        gen_string('utf8', 15),
        gen_string('html', 15),
    )
    @attr('cli', 'repository')
    def test_positive_create_5(self, name):
        """@Test: Check if repository can be created with gpg key ID

        @Feature: Repository

        @Assert: Repository is created and has gpg key

        @BZ: 1083236

        """

        # Make a new gpg key
        new_gpg_key = make_gpg_key({'organization-id': self.org['id']})

        new_repo = self._make_repository(
            {u'name': name, u'gpg-key-id': new_gpg_key['id']})

        # Fetch it again
        result = Repository.info({'id': new_repo['id']})
        self.assertEqual(
            result.return_code,
            0,
            "Repository was not found")
        self.assertEqual(
            len(result.stderr), 0, "No error was expected")
        # Assert that data matches data passed
        self.assertEqual(
            result.stdout['gpg-key']['id'],
            new_gpg_key['id'],
            "GPG Keys ID don't match"
        )
        self.assertEqual(
            result.stdout['gpg-key']['name'],
            new_gpg_key['name'],
            "GPG Keys name don't match"
        )

    @run_only_on('sat')
    @skip_if_bug_open('bugzilla', 1103944)
    @skip_if_bug_open('bugzilla', 1129617)
    @data(
        gen_string('alpha', 15),
        gen_string('alphanumeric', 15),
        gen_string('numeric', 15),
        gen_string('latin1', 15),
        gen_string('utf8', 15),
        gen_string('html', 15),
    )
    @attr('cli', 'repository')
    def test_positive_create_6(self, name):
        """@Test: Check if repository can be created with gpg key name

        @Feature: Repository

        @Assert: Repository is created and has gpg key

        @BZ: 1103944

        """

        # Make a new gpg key
        new_gpg_key = make_gpg_key({'organization-id': self.org['id']})

        new_repo = self._make_repository(
            {u'name': name, u'gpg-key': new_gpg_key['name']})

        # Fetch it again
        result = Repository.info({'id': new_repo['id']})
        self.assertEqual(
            result.return_code,
            0,
            "Repository was not found")
        self.assertEqual(
            len(result.stderr), 0, "No error was expected")
        # Assert that data matches data passed
        self.assertEqual(
            result.stdout['gpg-key']['id'],
            new_gpg_key['id'],
            "GPG Keys ID don't match"
        )
        self.assertEqual(
            result.stdout['gpg-key']['name'],
            new_gpg_key['name'],
            "GPG Keys name don't match"
        )

    @run_only_on('sat')
    @skip_if_bug_open('bugzilla', 1083256)
    @skip_if_bug_open('bugzilla', 1129617)
    @data(u'true', u'yes', u'1')
    @attr('cli', 'repository')
    def test_positive_create_7(self, test_data):
        """@Test: Create repository published via http

        @Feature: Repository

        @Assert: Repository is created and is published via http

        @BZ: 1083256

        """

        new_repo = self._make_repository({'publish-via-http': test_data})

        # Fetch it again
        result = Repository.info({'id': new_repo['id']})
        self.assertEqual(
            result.return_code,
            0,
            "Repository was not found")
        self.assertEqual(
            len(result.stderr), 0, "No error was expected")

        self.assertEqual(
            result.stdout['publish-via-http'],
            u'yes',
            "Publishing methods don't match"
        )

    @run_only_on('sat')
    @skip_if_bug_open('bugzilla', 1129617)
    @data(u'false', u'no', u'0')
    @attr('cli', 'repository')
    def test_positive_create_8(self, use_http):
        """@Test: Create repository not published via http

        @Feature: Repository

        @Assert: Repository is created and is not published via http

        """

        new_repo = self._make_repository(
            {'publish-via-http': use_http})

        # Fetch it again
        result = Repository.info({'id': new_repo['id']})
        self.assertEqual(
            result.return_code,
            0,
            "Repository was not found")
        self.assertEqual(
            len(result.stderr), 0, "No error was expected")

        self.assertEqual(
            result.stdout['publish-via-http'],
            u'no',
            "Publishing methods don't match"
        )

    @run_only_on('sat')
    @data(
        gen_string('alpha', 300),
        gen_string('alphanumeric', 300),
        gen_string('numeric', 300),
        gen_string('latin1', 300),
        gen_string('utf8', 300),
        gen_string('html', 300),
    )
    @attr('cli', 'repository')
    def test_negative_create_1(self, name):
        """@Test: Repository name cannot be 300-characters long

        @Feature: Repository

        @Assert: Repository cannot be created

        """

        with self.assertRaises(Exception):
            self._make_repository({u'name': name})

    @run_only_on('sat')
    @skip_if_bug_open('bugzilla', 1129617)
    @data(
        {u'url': FAKE_3_YUM_REPO, u'content-type': u'yum'},
        {u'url': FAKE_4_YUM_REPO, u'content-type': u'yum'},
        {u'url': FAKE_1_YUM_REPO, u'content-type': u'yum'},
    )
    @attr('cli', 'repository')
    def test_positive_synchronize_1(self, test_data):
        """@Test: Check if repository can be created and synced

        @Feature: Repository

        @Assert: Repository is created and synced

        """

        new_repo = self._make_repository(
            {u'url': test_data['url'],
             u'content-type': test_data['content-type']})
        # Assertion that repo is not yet synced
        self.assertEqual(
            new_repo['sync']['status'],
            'Not Synced',
            "The status of repository should be 'Not Synced'")

        # Synchronize it
        result = Repository.synchronize({'id': new_repo['id']})
        self.assertEqual(
            result.return_code,
            0,
            "Repository was not synchronized")
        self.assertEqual(
            len(result.stderr), 0, "No error was expected")

        # Verify it has finished
        result = Repository.info({'id': new_repo['id']})
        self.assertEqual(
            result.stdout['sync']['status'],
            'Finished',
            "The new status of repository should be 'Finished'")

    @run_only_on('sat')
    @skip_if_bug_open('bugzilla', 1129617)
    @data(
        FAKE_4_YUM_REPO,
        FAKE_1_PUPPET_REPO,
        FAKE_2_PUPPET_REPO,
        FAKE_3_PUPPET_REPO,
        FAKE_1_YUM_REPO,
    )
    @attr('cli', 'repository')
    def test_positive_update_1(self, url):
        """@Test: Update the original url for a repository

        @Feature: Repository

        @Assert: Repository url is updated

        """

        new_repo = self._make_repository()

        # Update the url
        result = Repository.update(
            {u'id': new_repo['id'],
             u'url': url})
        self.assertEqual(
            result.return_code,
            0,
            "Repository was not updated")
        self.assertEqual(
            len(result.stderr), 0, "No error was expected")

        # Fetch it again
        result = Repository.info({'id': new_repo['id']})
        self.assertEqual(
            result.return_code,
            0,
            "Repository was not found")
        self.assertEqual(
            len(result.stderr), 0, "No error was expected")
        self.assertNotEqual(
            result.stdout['url'],
            new_repo['url'],
            "Urls should not match"
        )
        self.assertEqual(
            result.stdout['url'],
            url,
            "Urls don't match"
        )

    @run_only_on('sat')
    @stubbed
    @skip_if_bug_open('bugzilla', 1083236)
    @attr('cli', 'repository')
    def test_positive_update_2(self, test_data):
        """@Test: Update the original gpg key

        @Feature: Repository

        @Assert: Repository gpg key is updated

        @BZ: 1083236

        @Status: manual

        """

    @run_only_on('sat')
    @stubbed
    @skip_if_bug_open('bugzilla', 1083256)
    @attr('cli', 'repository')
    def test_positive_update_3(self, test_data):
        """@Test: Update the original publishing method

        @Feature: Repository

        @Assert: Repository publishing method is updated

        @BZ: 1083256

        @Status: manual

        """

    @run_only_on('sat')
    @skip_if_bug_open('bugzilla', 1129617)
    @data(
        gen_string('alpha', 15),
        gen_string('alphanumeric', 15),
        gen_string('numeric', 15),
        gen_string('latin1', 15),
        gen_string('utf8', 15),
        gen_string('html', 15),
    )
    @attr('cli', 'repository')
    def test_positive_delete_1(self, name):
        """@Test: Check if repository can be created and deleted

        @Feature: Repository

        @Assert: Repository is created and then deleted

        """

        new_repo = self._make_repository({u'name': name})
        # Assert that name matches data passed
        self.assertEqual(new_repo['name'], name, "Names don't match")

        # Delete it
        result = Repository.delete(
            {u'id': new_repo['id']})
        self.assertEqual(
            result.return_code,
            0,
            "Repository was not deleted")
        self.assertEqual(
            len(result.stderr), 0, "No error was expected")

        # Fetch it
        result = Repository.info(
            {
                u'id': new_repo['id'],
            }
        )
        self.assertNotEqual(
            result.return_code,
            0,
            "Repository should not be found"
        )
        self.assertGreater(
            len(result.stderr),
            0,
            "Expected an error here"
        )
