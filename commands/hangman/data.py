import os
import json


def themes():
	dirname = os.path.dirname(__file__)
	path = os.path.join(dirname, 'words.json')
	with open(path, "r", encoding='utf-8') as file:
		contents = file.read()
	themes = json.loads(contents)
	for theme, words in themes.items():
		themes[theme] = [word.strip() for word in words.split(',')]
	return themes

happy_hangman = '''
```
+---+    
|   |    
| \🥳/    
|   |   
|  / \   
|        
=========```'''

hangmans = [
'''
```
+---     
|        
|        
|        
|        
|        
=========```''',
'''
```
+---+    
|        
|        
|        
|        
|        
=========```''',
'''
```
+---+    
|   |    
|        
|        
|        
|        
=========```''',
'''
```
+---+    
|   |    
|  🙁    
|        
|        
|        
=========```''',
'''
```
+---+    
|   |    
|  ☹️    
|   |    
|        
|        
=========```''',
'''
```
+---+    
|   |    
|  😣    
|  /|    
|        
|        
=========```''',
'''
```
+---+    
|   |    
|  😖    
|  /|\   
|        
|        
=========```''',
'''
```
+---+    
|   |    
|  😭    
|  /|\   
|  /    
|        
=========```''',
'''
```
+---+    
|   |    
|  💀    
|  /|\   
|  / \   
|        
=========```''']
