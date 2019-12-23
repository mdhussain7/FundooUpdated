from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Notes
# from .serializer import NoteSerializer,CreateNoteSerializer,UpdateNoteSerializer


class NoteTests(APITestCase):
    def setUp(self):
        self.note1 = Notes.objects.create(title=' He ',  description=' He and all')
        self.note2 = Notes.objects.create(title=' You ',  description=' You and all')
        self.note3 = Notes.objects.create(title=' They ',  description=' They and all')
        self.note4 = Notes.objects.create(title=' She ',  description=' She and all')

    def test_create_note(self):
        """
            - Ensure we can create a new note object.
        """
        url = reverse('note')
        data = {'title': 'notes','description':'Created a New Note'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Notes.objects.count(), 5)

    def test_get_all_note(self):
        notes = Notes.objects.all()
        print("All Notes Check",notes)
        response = self.client.get(
            reverse('note',), format="json")
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_given_note(self):
        """Test the api can get note with given id ."""
        response = self.client.get(
            reverse('details',kwargs={'pk': self.note1.pk}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_note(self):
        """
        Ensure we can update existing object.
        """
        data = {'title': 'FunDoo', 'description': 'new Note'}
        response = self.client.put( reverse('details', kwargs={'pk': self.note1.pk}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_note(self):
        """
        Ensure we can delete existing object.
        """
        response = self.client.delete( reverse('details', kwargs={'pk': self.note1.pk}),  format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)




