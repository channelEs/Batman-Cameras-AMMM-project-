import os
import re

class DATAttributes(object):
    pass

class DATParser(object):
    @staticmethod
    def _tryParse(x):
        if x in ['True', 'true', 'TRUE', 'T', 't']: return True
        if x in ['False', 'false', 'FALSE', 'F', 'f']: return False
        try:
            if '.' in x:
                return float(x)
            else:
                return int(x)
        except ValueError:
            return x

    @staticmethod
    def _parse_array_content(content_str):
        clean_str = content_str.replace('[', '').replace(']', '')
        tokens = clean_str.split()
        return [DATParser._tryParse(t) for t in tokens]

    @staticmethod
    def _openFile(filePath):
        if not os.path.exists(filePath):
            raise Exception('The file (%s) does not exist' % filePath)
        return open(filePath, 'r')

    @staticmethod
    def parse(filePath):
        fileHandler = DATParser._openFile(filePath)
        fileContent = fileHandler.read()
        fileHandler.close()

        datAttr = DATAttributes()
        fileContent = re.sub(r'//.*|^#.*', '', fileContent, flags=re.MULTILINE)
        fileContent = re.sub(r',', ' ', fileContent)
        pattern = re.compile(r'^\s*([a-zA-Z]\w*)\s*=\s*(.*?)\s*;', re.DOTALL | re.MULTILINE)
        
        entries = pattern.findall(fileContent)

        for name, value_str in entries:
            value_str = value_str.strip()
            if value_str.startswith('[') and ('[' in value_str[1:]):
                row_pattern = re.compile(r'\[(.*?)\]')
                inner_content = value_str[1:-1] # Strip outer brackets
                rows_str = row_pattern.findall(inner_content)
                
                matrix_data = []
                for row_s in rows_str:
                    if row_s.strip(): 
                        matrix_data.append(DATParser._parse_array_content(row_s))
                
                setattr(datAttr, name, matrix_data)

            elif value_str.startswith('['):
                vector_data = DATParser._parse_array_content(value_str)
                setattr(datAttr, name, vector_data)

            else:
                setattr(datAttr, name, DATParser._tryParse(value_str))

        return datAttr

# class DATAttributes(object):
#     pass


# class DATParser(object):
#     @staticmethod
#     def _tryParse(x):
#         try:
#             return int(x)
#         except ValueError:
#             pass

#         try:
#             return float(x)
#         except ValueError:
#             pass

#         # try parsing x as bool
#         if x in ['True',  'true',  'TRUE', 'T', 't']: return True
#         if x in ['False', 'false', 'FALSE', 'F', 'f']: return False

#         # x cannot be parsed, leave it as is
#         return x

#     @staticmethod
#     def _openFile(filePath):
#         if not os.path.exists(filePath):
#             raise Exception('The file (%s) does not exist' % filePath)
#         return open(filePath, 'r')

#     @staticmethod
#     def parse(filePath):
#         fileHandler = DATParser._openFile(filePath)
#         fileContent = fileHandler.read()
#         fileHandler.close()

#         datAttr = DATAttributes()

#         # lines not starting with <spaces>[a-zA-Z] are ignored.
#         # comments can be added using for instance '$','//','#', ...

#         # parse scalar attributes
#         pattern = re.compile(r'^[\s]*([a-zA-Z][\w]*)[\s]*\=[\s]*([\w\/\.\-]+)[\s]*\;', re.M)
#         entries = pattern.findall(fileContent)
#         for entry in entries:
#             datAttr.__dict__[entry[0]] = DATParser._tryParse(entry[1])

#         # parse 1-dimension vector attributes
#         pattern = re.compile(r'^[\s]*([a-zA-Z][\w]*)[\s]*\=[\s]*\[[\s]*(([\w\/\.\-]+[\s]*)+)\][\s]*\;', re.M)
#         entries = pattern.findall(fileContent)
#         for entry in entries:
#             pattern2 = re.compile(r'([\w\/\.]+)[\s]*')
#             values = pattern2.findall(entry[1])
#             datAttr.__dict__[entry[0]] = map(DATParser._tryParse, values)

#         # parse 2-dimension vector attributes
#         pattern = re.compile(r'^[\s]*([a-zA-Z][\w]*)[\s]*\=[\s]*\[(([\s]*\[[\s]*(([\w\/\.\-]+[\s]*)+)\][\s]*)+)[\s]*\][\s]*\;', re.M)
#         entries = pattern.findall(fileContent)

#         for entry in entries:
#             pattern2 = re.compile(r'[\s]*\[[\s]*(([\w\/\.\-]+[\s]*)+)\][\s]*')
#             entries2 = pattern2.findall(entry[1])
#             values = []
#             for entry2 in entries2:
#                 pattern2 = re.compile(r'([\w\/\.\-]+)[\s]*')
#                 values2 = pattern2.findall(entry2[0])
#                 values.append(map(DATParser._tryParse, values2))
#             datAttr.__dict__[entry[0]] = values

#         return datAttr
