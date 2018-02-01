from io import StringIO
import json
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['question-database']
collection = db['questions']

natural_language_understanding = NaturalLanguageUnderstandingV1(
  username='a47bcd73-acb2-4976-ad47-4865fe674507',
  password='mDkxrnvfbTQo',
  version='2017-02-27')

fname = "uploadedFile.pdf"
def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text 

def ret_questions():
    result = convert(fname)
    #print result
    response = natural_language_understanding.analyze(
      text=result,
      features=Features(
        entities=EntitiesOptions(
          emotion=False,
          sentiment=False,
          limit=20),
        keywords=KeywordsOptions(
          emotion=False,
          sentiment=False,
          limit=30)))

    keywordsList = response["keywords"]
    questionSet = set()
    for keyset in keywordsList:
        query1 = '{"$or":['
        word = keyset["text"]
        listWords = word.split()
        size = len(listWords)
        count = 0
        str2=''
        for itr in word.split():
            if count != (size-1):
                count+=1
                str2 = str2 + '{"key": {"$regex": "'+ itr +'", "$options": "i"}},'
            else:
                str2 = str2 + '{"key": {"$regex": "'+ itr +'", "$options": "i"}}'
        str4 = ']}'

        questionForTopic = db.questions.find(json.loads(query1+str2+str4))
        for ques in questionForTopic:
            valList = ques["questions"]
            for it in valList:
                questionSet.add(it)
    return questionSet
