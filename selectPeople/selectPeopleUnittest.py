#coding: utf8
import unittest
from selectPeople import SelectPeople

class TestSelectPeople(unittest.TestCase):
    def setUp(self):
        speechRecordsFile = "speechRecords.pkl"
        fd = open('personnelNumbers.txt')
        self.numberMapToEveryone = eval(fd.read())
        fd.close()
        
        self.amountToSelect = 2
        self.selectPeopleClass = SelectPeople(self.numberMapToEveryone, speechRecordsFile)

    def test_getNumbersSelected(self):
        for number in self.selectPeopleClass.getNumbersSelected(self.amountToSelect):
            self.assertIn(number, self.numberMapToEveryone)

    def test_getSpeechInfo(self):
        numbersSelected = self.selectPeopleClass.getNumbersSelected(self.amountToSelect)
        
        speechInfo = self.selectPeopleClass.getSpeechInfo(numbersSelected)
        for number in speechInfo:
            self.assertLessEqual( 1, speechInfo[number][0] )
            self.assertLessEqual( *speechInfo[number] )

    def test_updateOrRevokeRecords(self):
        numbersSelected = self.selectPeopleClass.getNumbersSelected(self.amountToSelect)

        import pickle
        speechRecordsFile = "speechRecords.pkl"
        with open(speechRecordsFile, 'rb') as fd:
            old_speechRecords = pickle.load( fd )

        # test if it's OK to update records    
        self.selectPeopleClass.updateOrRevokeRecords( numbersSelected )
        with open(speechRecordsFile, 'rb') as fd:
            new_speechRecords = pickle.load( fd )           
        for number in old_speechRecords:
            if number in numbersSelected:
                self.assertEqual(old_speechRecords[number], new_speechRecords[number])
            else:
                self.assertEqual(old_speechRecords[number] + 1, new_speechRecords[number])

        # test if it's OK to revoke records 
        self.selectPeopleClass.updateOrRevokeRecords( numbersSelected, True )
        with open(speechRecordsFile, 'rb') as fd:
            new_speechRecords = pickle.load( fd )
        self.assertEqual(old_speechRecords, new_speechRecords)

if __name__ == "__main__":
    unittest.main()
