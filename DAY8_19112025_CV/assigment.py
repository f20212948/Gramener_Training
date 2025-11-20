import re
import pandas as pd
# The extracted text block
ocr_text = """"""

def extract_invoice_data(text):
    """
    Uses regular expressions to extract structured fields from the OCR text.
    """
    extracted_data = {}

    # --- Header Fields ---
    
    # 1. Invoice No: Looks for "Invoice no:" followed by digits/letters
    invoice_no_match = re.search(r'Invoice no:\s*(\S+)', text, re.IGNORECASE)
    if invoice_no_match:
        extracted_data['Invoice Number'] = invoice_no_match.group(1).strip()
    
    # 2. Date of Issue: Looks for "Date of issue:" followed by a date format
    date_match = re.search(r'Date of issue:\s*(\d{2}/\d{2}/\d{4})', text)
    if date_match:
        extracted_data['Date of Issue'] = date_match.group(1).strip()

    # 3. IBAN: Looks for "IBAN:" followed by alphanumeric characters
    iban_match = re.search(r'IBAN:\s*(\S+)', text, re.IGNORECASE)
    if iban_match:
        extracted_data['IBAN'] = iban_match.group(1).strip()
        
    # --- Parties (Seller/Client) ---
    
    #----------
    total_net_match = re.search(r'Total\s*\$\s*([\d\s,]+)', text)
    if total_net_match:

        cleaned_value = total_net_match.group(1).replace(' ', '').replace(',', '.')
        extracted_data['Total Net Worth'] = float(cleaned_value)

    total_vat_match = re.search(r'Total\s*\$\s*[\d\s,]+\s*\$\s*([\d\s,]+)', text)
    if total_vat_match:
        cleaned_value = total_vat_match.group(1).replace(' ', '').replace(',', '.')
        extracted_data['Total VAT Amount'] = float(cleaned_value)


    total_gross_match = re.search(r'Total\s*\$\s*[\d\s,]+\s*\$\s*[\d\s,]+\s*\$\s*([\d\s,]+)', text)
    if total_gross_match:
        cleaned_value = total_gross_match.group(1).replace(' ', '').replace(',', '.')
        extracted_data['Total Gross Worth'] = float(cleaned_value)
        

    tax_ids = re.findall(r'Tax Id:\s*([\d\-]{6,})', text)
    if len(tax_ids) >= 2:
        extracted_data['Seller Tax ID'] = tax_ids[0].strip()
        extracted_data['Client Tax ID'] = tax_ids[1].strip()


    return extracted_data


def extract_item_dataframe(text):
    # --- Data Cleaning Helper Function ---
    def clean_financial(s):
        """Converts European number format (space thousands, comma decimal) to float."""
        if pd.isna(s) or s is None:
            return None
        s = str(s).strip()
        # 1. Remove space thousand separator (e.g., '7 800,00' -> '7800,00')
        s = s.replace(' ', '')
        # 2. Replace comma decimal separator with period (e.g., '7800,00' -> '7800.00')
        s = s.replace(',', '.')
        try:
            return float(s)
        except ValueError:
            return s
            
    # --- 1. Isolate the item block ---
    try:
        # Get text between "ITEMS" and "SUMMARY"
        item_block_text = text.split("ITEMS")[1].split("SUMMARY")[0].strip()
    except IndexError:
        print("Could not find 'ITEMS' or 'SUMMARY' markers.")
        return pd.DataFrame()

    item_block_lines = item_block_text.split('\n')
    
    # Find the start of the item data by skipping the header lines (which end with 'worth')
    start_index = -1
    for i, line in enumerate(item_block_lines):
        if 'worth' in line.lower():
            start_index = i + 1
            break
        
    if start_index == -1:
        print("Could not find the end of the item table header.")
        return pd.DataFrame()
        
    data_lines = item_block_lines[start_index:]
    
    # --- 2. Parsing Logic ---
    columns = ['No', 'Description', 'Qty', 'UM', 'Net Price', 'Net Worth', 'VAT %', 'Gross Worth']
    items_list = []
    current_item = {'Description_lines': []}

    # Regex to anchor the fixed numeric columns (Qty, UM, Net price, etc.)
    # This pattern identifies the start of the quantitative data in a line.
    numeric_pattern = re.compile(r'(\d[\s,]*\d{2})\s+(each)\s+([\d\s,]+)\s+([\d\s,]+)\s+(\d{1,2}%)\s+([\d\s,]+)')

    for line in data_lines:
        line = line.strip()
        if not line:
            continue
            
        match = numeric_pattern.search(line)
        
        if match:
            # A new item starts here: Finalize the previous item first
            if current_item.get('Description_lines'):
                current_item['Description'] = ' '.join(current_item.pop('Description_lines')).strip()
                
                # Check if the Item No. was implicitly prepended to the description
                if 'No' not in current_item or current_item['No'] is None:
                    num_match = re.match(r'(\d+)\.\s*(.*)', current_item['Description'])
                    if num_match:
                        current_item['No'] = num_match.group(1)
                        current_item['Description'] = num_match.group(2).strip()
                
                if 'Qty' in current_item:
                    items_list.append(current_item)
            
            # Start the new item dictionary
            current_item = {}

            # Extract numeric fields
            (qty_raw, um, net_price_raw, net_worth_raw, vat_perc, gross_worth_raw) = match.groups()
            
            # Store the data
            current_item['Qty'] = qty_raw
            current_item['UM'] = um
            current_item['Net Price'] = net_price_raw
            current_item['Net Worth'] = net_worth_raw
            current_item['VAT %'] = vat_perc
            current_item['Gross Worth'] = gross_worth_raw
            
            # Extract the initial description (text before the quantity)
            desc_start_text = line[:match.start()].strip()
            
            # Extract Item No.
            num_match = re.match(r'(\d+)\.\s*(.*)', desc_start_text)
            if num_match:
                current_item['No'] = num_match.group(1)
                current_item['Description_lines'] = [num_match.group(2).strip()]
            else:
                current_item['No'] = None
                current_item['Description_lines'] = [desc_start_text]

        else:
            # This line is a continuation of the current item's description
            if current_item.get('Description_lines') is not None:
                 current_item['Description_lines'].append(line)


    # 3. Finalize the very last item
    if current_item and current_item.get('Description_lines'):
        current_item['Description'] = ' '.join(current_item.pop('Description_lines')).strip()
        
        if 'No' not in current_item or current_item['No'] is None:
            num_match = re.match(r'(\d+)\.\s*(.*)', current_item['Description'])
            if num_match:
                current_item['No'] = num_match.group(1)
                current_item['Description'] = num_match.group(2).strip()
                
        if 'Qty' in current_item:
            items_list.append(current_item)


    # --- 4. Create DataFrame and Clean Data Types ---
    df = pd.DataFrame(items_list, columns=columns)
    
    # Apply cleaning and conversion to numeric columns
    for col in ['Qty', 'Net Price', 'Net Worth', 'Gross Worth']:
        df[col] = df[col].apply(clean_financial)
        
    # Clean and convert 'No' column to integer
    df['No'] = df['No'].astype(str).str.replace('.', '', regex=False).str.replace(' ', '', regex=False).replace('None', '0', regex=False).astype(int)
    
    return df

# Run the extraction function
invoice_data = extract_invoice_data(ocr_text)
# Execute the function and display the DataFrame
df_items = extract_item_dataframe(ocr_text)

# --- Display Results ---
print("--- Extracted Invoice Data ---")
for key, value in invoice_data.items():
    print(f"**{key}:** {value}")
# Print the resulting DataFrame
print(df_items)