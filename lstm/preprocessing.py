import sys
import json
import math
import codecs
import glob
def main():
	path = '/ShuaiZhou/USC/CSCI544/Project/DataSet/*.json'   
	files = glob.glob(path)
	
	vocabulary = {}
	preprocessed = []
	preprocessed_mixed = []
	for name in files:
		data_file = open(name, encoding='utf-8')
		data = json.loads(data_file.read())
		washing(preprocessed, data, preprocessed_mixed, vocabulary)
	processedData = open("/ShuaiZhou/USC/CSCI544/Project/ancient-Chinese-poetry-generator/datasets/data_five_character_quatrains繁体.txt", 'w', encoding='utf-8')
	processedData_mix = open("/ShuaiZhou/USC/CSCI544/Project/ancient-Chinese-poetry-generator/datasets/data_mixed繁体.txt", 'w', encoding='utf-8')
	vocabulary_f = open("/ShuaiZhou/USC/CSCI544/Project/ancient-Chinese-poetry-generator/datasets/vocabulary_frequency繁体.txt", 'w', encoding='utf-8')
	
	json.dump(vocabulary, vocabulary_f,  ensure_ascii=False)
	json.dump(preprocessed, processedData,  ensure_ascii=False)
	json.dump(preprocessed_mixed, processedData_mix,  ensure_ascii=False)
	processedData.close()
	processedData_mix.close()
	data_file.close()
	print(len(preprocessed))
	print(len(preprocessed_mixed))
	print(len(vocabulary ))
		
	# s = ["明月出天山，蒼茫雲海間○。", "明月出天山，蒼茫雲海間。"]
	# print("○" in s[0])
def washing(preprocessed, data, preprocessed_mixed, vocabulary):
	symbol = "·！（）[]「」{}《》？-1234567890=+|/。●〖〗"
	for shi in data:
		if "○" in (shi["title"] or shi["author"]):
			continue
		skip = None
		for pz in shi["strains"]:
			for ppz in pz:
				if "○" in ppz:
					skip = True
		for juzi in shi["paragraphs"]:
			for jjuzi in juzi:
				if "○" in jjuzi:
					skip = True
		if skip == True:
			continue
		dic = {}
		dic["title"] = ""
		for char in shi["title"]:
			if char not in symbol:
				# char = HanziConv.toSimplified(char)
				dic["title"] += char
		dic["strains"] = ""
		dic["paragraphs"] = ""
		# pz = "平平平仄仄，平平平仄仄。"
		for pz in shi["strains"]:
			pz = pz.split("，");
			# ppz= "平平平仄仄" 
			for pzz in pz:
				for i, x in enumerate(pzz):
					if x == '平':
						dic["strains"] += "p"
					if x == '仄':
						dic["strains"] += "z"
				dic["strains"] += "$"
		shouldKeep = True
		for juzi in shi["paragraphs"]:
			juzi = juzi.split("，");
			
			for jjuzi in juzi:
				temp = ""
				for i, x in enumerate(jjuzi):
					if x not in symbol:
						# char = HanziConv.toSimplified(char)
						dic["paragraphs"] += x
						temp += x
						if x not in vocabulary:
							vocabulary[x] = 1
						else:
							vocabulary[x] +=1
				dic["paragraphs"] += "$"
				if len(temp) != 5:
					shouldKeep = False
		if shouldKeep == True:
			preprocessed.append(dic)
		else:
			preprocessed_mixed.append(dic)

	



if __name__ == "__main__":
    main()