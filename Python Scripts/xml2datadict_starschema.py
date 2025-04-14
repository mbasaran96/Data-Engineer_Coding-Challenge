# Import libraries
from icecream import ic # debugging Tool
import re # analyses XML strings
import xml.etree.ElementTree as ET # parses XML file
import pandas as pd # creates data frame for data dictionary
from html.parser import HTMLParser # parses HTML

# Define Class to parse HTML
class HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = [] # cache for real text

    def handle_data(self, d):
        self.fed.append(d) # is called when plain text is found between tags

    def get_data(self):
        return ''.join(self.fed) # returns the collected text as a string

# Create Functions
def strip_html(html):
    """Removes HTML-Tags and returns clear text."""
    parser = HTMLTextExtractor()
    parser.feed(html)
    return parser.get_data()

def list_cells(xml_path: str):
    """Function to extract all cells into list."""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    cells = root.findall('./diagram/mxGraphModel/root/mxCell') # './mxCell'
    return cells 

def get_shape_from_cell(cell):
    """Extract shape property from style attribute"""
    style = cell.get('style')
    prop=None
    if isinstance(style, str):
        prop = re.match(r'shape=([a-zA-Z]+);', style)
    if prop is not None:
        return prop.group(1)
    else:
        return None

def create_datadf(table_collect: dict):
    """Create blueprint of data dict."""
    d_dict = pd.DataFrame(columns=['Tabellenname', 'Spaltenname', 'Spaltentyp', 'Zeichenlaenge', 'PK', 'FK', 'AI', 'NN', 'Beschreibung'])
    row = 0
    for table_name, table in table_collect.items():
        for erm_table_row in range(int(len(table)/2)):
            flag = table[2*erm_table_row]
            description = table[2*erm_table_row + 1]
            if flag.startswith('PK,FK'):
                d_dict.loc[row] = [table_name, description, '', '', 'PK', 'FK', '', 'NN', '']
            elif flag == 'PK':
                d_dict.loc[row] = [table_name, description, '', '', flag, '', 'AI', 'NN', '']
            elif flag == 'FK':
                d_dict.loc[row] = [table_name, description, '', '', '', flag, '', '', '']
            else:
                d_dict.loc[row] = [table_name, description, '', '', '', '', '', '', '']
            row += 1
           
    return d_dict

def get_table_dict(cell_list: list):
    """Extract information needed for table, with HTML cleaned."""
    table_collect = {}
    table_name = None
    for cell in cell_list:
        shape = get_shape_from_cell(cell)
        value = cell.get('value')
        if value:
            value = strip_html(value).strip()
        if shape == 'table':
            table_name = value
            table_collect[table_name] = []
        elif shape == 'partialRectangle':
            if table_name is not None:
                table_collect[table_name].append(value)
    return table_collect

# Main Function to parse, extract and export as csv file
def main():
    xml_path = 'StarSchema.xml'
    name = xml_path[:-4]
    cells = list_cells(xml_path)
    cell_dict = get_table_dict(cells)
    data_dict_df = create_datadf(cell_dict)
    data_dict_df.to_csv(f'{name}.csv', index=False)
    ic(data_dict_df)

if __name__=='__main__':
    main()