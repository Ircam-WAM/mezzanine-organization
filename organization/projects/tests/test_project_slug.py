from django.test import TestCase
from organization.projects.models import Project


class ProjectSlugTestCase(TestCase):

    def setUp(self):
        Project.objects.create(title='Test project')

    def test_project_slug(self):
        project = Project.objects.get(title='Test project')
        self.assertEqual(project.slug, 'test-project')
