# coding:utf8

# runtime environment: python 3

import random, pickle

class SelectPeople(object):
    def __init__(self, numberMapToEveryone, speechRecordsFile):
        from copy import copy
        self.numberMapToEveryone = copy( numberMapToEveryone )
        self.speechRecordsFile = speechRecordsFile
        
        fd = open(self.speechRecordsFile, 'rb')
        self.__speechRecords = pickle.load( fd )
        fd.close()
        
    def startAndGetSelectResult(self, amountToSelect=2):
        numbersSelected = self.getNumbersSelected( amountToSelect )
        speechInfo = self.getSpeechInfo( numbersSelected )
        self.updateOrRevokeRecords( numbersSelected )
        return speechInfo
        
    def getNumbersSelected(self, amountToSelect):
        numbersSelected = []
        for count in range( amountToSelect ):
            allNumbers = list( self.numberMapToEveryone.keys() )
            number = random.choice( allNumbers )
            numbersSelected.append( number )
            del self.numberMapToEveryone[ number ]
        return numbersSelected

    def getSpeechInfo(self, numbersSelected):
        speechInfo = {}
        for number in numbersSelected:
            maxAmountToSpeak = self.__speechRecords[ number ]
            speechInfo[ number ] = ( random.randint(1, maxAmountToSpeak), maxAmountToSpeak )
        return speechInfo

    def updateOrRevokeRecords( self, numbersSelected, isRevoke=False ):
        for number in self.__speechRecords:
            if number not in numbersSelected:
                if isRevoke is False:
                    self.__speechRecords[number] += 1
                else:
                    self.__speechRecords[number] -= 1
        with open(self.speechRecordsFile, 'wb') as fd:
            pickle.dump( self.__speechRecords, fd )


##################################################################################   
def initSpeechRecordsFile( speechRecordsFile, amountOfPeople ):
    '''initialize ereryone's record to be 1 and serialize to file'''
    initRecordsInfo = {}
    for number in range(amountOfPeople):
        initRecordsInfo[ number ] = 1
    with open(speechRecordsFile, 'wb') as fd:
        pickle.dump( initRecordsInfo, fd)
        
#################################################################################
g_speechRecordsFile = "speechRecords.pkl"

with open('personnelNumbers.txt') as fd:
    g_numberMapToEveryone = eval(fd.read())

# 如果是第一次执行，就要先把所有人的记录置为1
from os.path import exists
if not exists( g_speechRecordsFile ):
    initSpeechRecordsFile(g_speechRecordsFile, len(g_numberMapToEveryone))
    
if __name__ == '__main__':
    amountToSelect = 2

    while True:    
        selectPeopleClass = SelectPeople( g_numberMapToEveryone, g_speechRecordsFile )
        selectResult = selectPeopleClass.startAndGetSelectResult( amountToSelect )

        print("\n经本程序慎重思考后，现公布中奖名单如下：\n")
        for number in selectResult:
            print("\t*{0}*同志本次应该至少讲*{1}*个脚本，因其已连续有*{2}*次躲过天命。".format( g_numberMapToEveryone[number], *selectResult[number]) )

        #import sys
        # 小于 python 3 版本就转换 input 函数为 raw_input 函数
        #if int(sys.version[0]) < 3:
        #    input = eval('raw_input')
            
        if input("\n以上几人是否都在？(y/n)") in ('Y', 'y'):
            print("\n那就有请几位上台领奖…………\n")
            break
        else:
            selectPeopleClass.updateOrRevokeRecords( selectResult.keys(), True )
            print("=" * 70)
