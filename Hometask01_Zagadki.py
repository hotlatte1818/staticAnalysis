# -*- coding: utf-8 -*-
import sys  # importing the standart library `sys`.
__author__ = 'kolupaev_k'

if sys.version_info[0]==2:
	input_function = raw_input
else:
	input_function=input


questionNumber=1



# Функция//////////////////////////////////////////////////////////////////////////////////////////////////////
def QuesFunc(input_function, questionNumber, question, answer_det, correct_answer ):
	print("--------------------------------------------------------------------")
	print("Вопрос %s :" %questionNumber)
	print(question)
	users_input = input_function('Твой ответ (%s):' %answer_det)

	if users_input==correct_answer:
		print("Правильно!")
	else:
		print("Не верно, правильный ответ: %s" %correct_answer)
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////


while  questionNumber<7:
	
	if questionNumber==1:
		question="Какое из из чисел 75 и 28.15 - число float? "
		answer_det="напиши число 75 или 28.15"
		correct_answer="28.15"
	
	if questionNumber==2:
		question="Какое из из чисел 100 и 0.025 - число int? "
		answer_det="напиши число 100 или 0.025"
		correct_answer="100"		
	
	if questionNumber==3:
		question="Как в Питоне обозначают Ложь?"
		answer_det="напиши заначение"
		correct_answer="False"	

	if questionNumber==4:
		question="Какое значение в Питоне у True?"
		answer_det="напиши заначение"
		correct_answer="1"	
	
	if questionNumber==5:
		question="Какое значение в Питоне у Пусто?"
		answer_det="напиши заначение"
		correct_answer="None"			
	
	if questionNumber==6:
		question="Какая кодировка - стандарт в Питоне?"
		answer_det="напиши название кодировки "
		correct_answer="Unicode"			


	QuesFunc(input_function, questionNumber, question, answer_det, correct_answer )

	questionNumber=questionNumber+1






# -----КОНЕЦ----------------------------------------------------

print("--------------------------------------------------------------------")
b=input_function("The end!")

