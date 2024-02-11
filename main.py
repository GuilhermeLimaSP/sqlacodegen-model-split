import os

# Change this
model_folder_name = 'models_generated'
unique_model_file = 'output-sqlacodegen.py'

# Change only if you know what you are doing
sqlalchemy_types = ['ForeignKey', 'ARRAY', 'BIGINT', 'BigInteger', 'BINARY', 'BLOB', 'BOOLEAN', 'Boolean', 'CHAR', 'CLOB', 'DATE', 'Date', 'DATETIME', 'DateTime', 'DECIMAL', 'Enum', 'FLOAT', 'Float', 'INT', 'INTEGER', 'Integer', 'Interval', 'JSON', 'LargeBinary', 'NCHAR', 'NUMERIC', 'Numeric', 'NVARCHAR', 'PickleType', 'REAL', 'SMALLINT', 'SmallInteger', 'String', 'TEXT', 'Text', 'TIME', 'Time', 'TIMESTAMP', 'TupleType', 'TypeDecorator', 'Unicode', 'UnicodeText', 'VARBINARY', 'VARCHAR']
mysql_dialects = ['BIGINT', 'BINARY', 'BIT', 'BLOB', 'BOOLEAN', 'CHAR', 'DATE', 'DATETIME', 'DECIMAL', 'DOUBLE', 'ENUM', 'FLOAT', 'INTEGER', 'JSON', 'LONGBLOB', 'LONGTEXT', 'MEDIUMBLOB', 'MEDIUMINT', 'MEDIUMTEXT', 'NCHAR', 'NUMERIC', 'NVARCHAR', 'REAL', 'SET', 'SMALLINT', 'TEXT', 'TIME', 'TIMESTAMP', 'TINYBLOB', 'TINYINT', 'TINYTEXT', 'VARBINARY', 'VARCHAR', 'YEAR']

def create_model(name, class_code):
    code = ""
    
    # Imports
    import_code = get_imports(name, class_code)
    code += f"{import_code}"
    
    # Base + class code
    code += "\n\nBase = declarative_base()"
    code += f"\n\n\n{class_code}"
    
    with open(f'./{model_folder_name}/{name}.py', 'w') as file_data:
        file_data.write(code)

def get_imports(class_name, block_code):
    sqlalchemy_imports = ['Column']
    mysql_dialect_imports = []
    
    if 'server_default=text' in block_code:
        sqlalchemy_imports.append('text')
    
    block_lines = block_code.split('\n')
    for line in block_lines:
        try:
            column_value = line.split('Column(')[1].split(')')[0]
            if '(' in column_value:
                column_value = column_value.split('(')[0]
            if ',' in column_value:
                column_value = column_value.split(',')[0]
                
            column_value = column_value.strip()
            if column_value in sqlalchemy_imports or column_value in mysql_dialect_imports:
                continue

            if column_value in sqlalchemy_types:
                sqlalchemy_imports.append(column_value)
            elif column_value in mysql_dialects:
                mysql_dialect_imports.append(column_value)
            else:
                print(f"Unknown type '{column_value}' in '{class_name}'")
        except:
            pass

    code = ""
    
    sqlalchemy_imports_string = ", ".join(sqlalchemy_imports)
    if sqlalchemy_imports_string:
        code += f"\nfrom sqlalchemy import {sqlalchemy_imports_string}"
        
    mysql_dialect_imports_string = ", ".join(mysql_dialect_imports)
    if mysql_dialect_imports_string:
        code += f"\nfrom sqlalchemy.dialects.mysql import {mysql_dialect_imports_string}"
        
    code += "\nfrom sqlalchemy.ext.declarative import declarative_base"
    if "relationship" in block_code:
        code += "\nfrom sqlalchemy.orm import relationship"
        
    return code
                
def main():
    with open('models_games.py', 'r') as file_data:
        content = file_data.read()
        blocks = content.split('\n\n\n')

    if not os.path.exists(model_folder_name):
        print("Creating folder for models...")
        os.makedirs(model_folder_name)
        
    created_count = 0
    for block in blocks:
        if 'class' in block.lower():
            class_name = block.split('class')[1].split('(Base)')[0].strip()          
            created_count = created_count + 1 
            
            create_model(class_name, block)
            print(f'Creating model {class_name}...')
            
    print(f'Done, created {created_count} models')
            
if __name__ == '__main__':
    main()
