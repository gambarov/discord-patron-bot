import os
import json
import random
from datetime import datetime
random.seed(datetime.now())


def get_random_word(theme: str):
    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, 'words.json')
    with open(path, "r", encoding='utf-8') as file:
        contents = file.read()
    themes = json.loads(contents)
    if not theme in themes:
      return None
    words = [word.strip() for word in themes[theme].split(',')]
    word = random.choice(words)
    return word


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
|   O    
|        
|        
|        
=========```''', 
'''
```
+---+    
|   |    
|   O    
|   |    
|        
|        
=========```''', 
'''
```
+---+    
|   |    
|   O    
|  /|    
|        
|        
=========```''',
'''
```
+---+    
|   |    
|   O    
|  /|\   
|        
|        
=========```''', 
'''
```
+---+    
|   |    
|   O    
|  /|\   
|  /    
|        
=========```''', 
'''
```
+---+    
|   |    
|   O    
|  /|\   
|  / \   
|        
=========```''']
