from graphene.test import Client as GraphQLClient
from django.test import TestCase
from graphene import Schema
from .schema import schema
from .models import Component

# TestCases For APIs
class GraphQLTestCase(TestCase):
    
    def setUp(self):
        self.client = GraphQLClient(schema)
        self.task = Component.objects.create(name='Task 1', status='ACTIVE')
        self.task = Component.objects.create(name='Task 2', status='ACTIVE')
        
    def test_get_query(self):
        query = '''
            query {
                tasks{
                id
                name
                status
                }
            }
        '''
        response = self.client.execute(query)
        data = response['data']['tasks']
        self.assertEqual(data[0], {'id': '1', 'name': 'Task 1', 'status': 'ACTIVE'})
        
    def test_create_query(self):
        query = '''
            mutation {
                create_task: createTask(name:"test task", status: "ACTIVE") {
                    task {
                        id,
                        name,
                        status
                    }
                }
            }
        '''
        response = self.client.execute(query)
        data = response['data']['create_task']['task']
        self.assertEqual(data['name'], 'test task')
        self.assertEqual(data['status'], 'ACTIVE')
        
    def test_update_query(self):
        query = '''
            mutation{
                updateTask(
                id: 1,
                name:"DDF",
                status: "PUBLISHED"){
                    post{
                    id,
                    name,
                    status
                    }
                }
            }
        '''
        response = self.client.execute(query)
        data = response['data']['updateTask']['post']
        self.assertEqual(data, {'id': '1', 'name': 'DDF', 'status': 'PUBLISHED'})
        
    def test_delete_query(self):
        query = '''
            mutation deleteMutation{
                deleteTask(id: 1) {
                    task {
                        id
                    } 
                }
            }
        '''
        response = self.client.execute(query)
        data = response['data']['deleteTask']
        self.assertEqual(data['task'], None)
        
    def test_bulk_delete_query(self):
        query = '''
            mutation deleteMutationbulk{
                bulkDelete(ids: [1,2]) {
                    success
                }
            }
        '''
        response = self.client.execute(query)
        data = response['data']['bulkDelete']
        self.assertEqual(data['success'], True)