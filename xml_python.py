import xml.etree.ElementTree as ET

# Пример XML строки
xml_data = '''
<user>
    <id>1</id>
    <first_name>John</first_name>
    <last_name>Doe</last_name>
    <email>john.doe@example.com</email>
</user>
'''

# Парсинг XML
root = ET.fromstring(xml_data)

# Доступ к данным
print("User ID:", root.find('id').text)
print("User Name:", root.find('first_name').text, root.find('last_name').text)
print("User Email:", root.find('email').text)