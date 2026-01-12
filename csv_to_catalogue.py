import csv
import html
from pathlib import Path

def csv_to_catalogue(csv_file, output_file='catalogue.html', title='Alza Product Export List'):
    """
    Convert a CSV file into an interactive HTML catalogue with filtering and search.
    
    Args:
        csv_file: Path to the CSV file
        output_file: Output HTML file name (default: catalogue.html)
        title: Title for the catalogue page
    """
    
    # Read CSV data
    items = []
    headers = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        items = list(reader)
    
    if not items:
        print("Error: CSV file is empty or invalid")
        return
    
    # Check if CPU and RAM columns exist
    cpu_column = next((h for h in headers if 'cpu' in h.lower() or 'processor' in h.lower()), None)
    ram_column = next((h for h in headers if 'ram' in h.lower() or 'memory' in h.lower() or 'paměť' in h.lower()), None)
    
    # Get unique values for filters
    cpu_values = set()
    ram_values = set()
    
    if cpu_column:
        cpu_values = sorted(set(item.get(cpu_column, '') for item in items if item.get(cpu_column, '')))
    
    if ram_column:
        ram_values = sorted(set(item.get(ram_column, '') for item in items if item.get(ram_column, '')))
    
    # Generate HTML
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #f5f7fa;
            color: #333;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1600px;
            margin: 0 auto;
        }}
        
        .header {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
            margin-bottom: 20px;
        }}
        
        h1 {{
            font-size: 2em;
            color: #1a1a1a;
            margin-bottom: 20px;
            font-weight: 600;
        }}
        
        .controls {{
            display: flex;
            gap: 15px;
            align-items: center;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }}
        
        .filter-group {{
            display: flex;
            flex-direction: column;
            gap: 5px;
        }}
        
        .filter-label {{
            font-size: 0.85em;
            font-weight: 600;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .filter-select {{
            padding: 10px 15px;
            border: 2px solid #e2e8f0;
            border-radius: 6px;
            font-size: 0.95em;
            background: white;
            cursor: pointer;
            min-width: 180px;
            transition: all 0.2s ease;
        }}
        
        .filter-select:hover {{
            border-color: #5a67d8;
        }}
        
        .filter-select:focus {{
            outline: none;
            border-color: #5a67d8;
            box-shadow: 0 0 0 3px rgba(90, 103, 216, 0.1);
        }}
        
        .search-box {{
            flex: 1;
            min-width: 300px;
        }}
        
        .search-input {{
            width: 100%;
            padding: 12px 16px;
            border: 2px solid #e2e8f0;
            border-radius: 6px;
            font-size: 0.95em;
            transition: all 0.2s ease;
        }}
        
        .search-input:focus {{
            outline: none;
            border-color: #5a67d8;
        }}
        
        .clear-filters {{
            background: #ef4444;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-size: 0.9em;
            cursor: pointer;
            transition: all 0.2s ease;
            font-weight: 500;
        }}
        
        .clear-filters:hover {{
            background: #dc2626;
        }}
        
        .filter-info {{
            background: #eff6ff;
            border: 2px solid #bfdbfe;
            padding: 12px 16px;
            border-radius: 6px;
            color: #1e40af;
            font-size: 0.9em;
        }}
        
        .table-container {{
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
            overflow: hidden;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        thead {{
            background: #f8fafc;
            border-bottom: 2px solid #e2e8f0;
        }}
        
        th {{
            padding: 16px 20px;
            text-align: left;
            font-weight: 600;
            color: #475569;
            font-size: 0.85em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        th:first-child {{
            padding-left: 24px;
            width: 60px;
        }}
        
        tbody tr {{
            border-bottom: 1px solid #f1f5f9;
            transition: background 0.15s ease;
        }}
        
        tbody tr:hover {{
            background: #f8fafc;
        }}
        
        tbody tr:nth-child(even) {{
            background: #fafbfc;
        }}
        
        tbody tr:nth-child(even):hover {{
            background: #f1f5f9;
        }}
        
        tbody tr.hidden {{
            display: none;
        }}
        
        td {{
            padding: 16px 20px;
            color: #334155;
            font-size: 0.95em;
        }}
        
        td:first-child {{
            padding-left: 24px;
            color: #64748b;
            font-weight: 500;
            width: 60px;
        }}
        
        .detail-icon {{
            color: #5a67d8;
            cursor: pointer;
            font-size: 1.2em;
            transition: color 0.2s;
        }}
        
        .detail-icon:hover {{
            color: #4c51bf;
        }}
        
        .product-name {{
            font-weight: 500;
            color: #1a202c;
        }}
        
        .product-price {{
            font-weight: 600;
            color: #2d3748;
        }}
        
        .product-link a {{
            color: #5a67d8;
            text-decoration: none;
            transition: color 0.2s;
            word-break: break-all;
        }}
        
        .product-link a:hover {{
            color: #4c51bf;
            text-decoration: underline;
        }}
        
        .no-results {{
            text-align: center;
            padding: 60px 20px;
            color: #94a3b8;
            font-size: 1.1em;
        }}
        
        .footer {{
            margin-top: 20px;
            padding: 16px 24px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
            color: #64748b;
            font-size: 0.9em;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        @media (max-width: 768px) {{
            .table-container {{
                overflow-x: auto;
            }}
            
            table {{
                min-width: 600px;
            }}
            
            h1 {{
                font-size: 1.5em;
            }}
            
            .controls {{
                flex-direction: column;
                align-items: stretch;
            }}
            
            .filter-group, .search-box {{
                width: 100%;
            }}
            
            .filter-select {{
                width: 100%;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{html.escape(title)}</h1>
            <div class="controls">
'''
    
    # Add CPU filter if column exists
    if cpu_column and cpu_values:
        html_content += f'''                <div class="filter-group">
                    <label class="filter-label">CPU</label>
                    <select class="filter-select" id="cpuFilter">
                        <option value="">All CPUs</option>
'''
        for value in cpu_values:
            html_content += f'                        <option value="{html.escape(value)}">{html.escape(value)}</option>\n'
        html_content += '''                    </select>
                </div>
'''
    
    # Add RAM filter if column exists
    if ram_column and ram_values:
        html_content += f'''                <div class="filter-group">
                    <label class="filter-label">RAM</label>
                    <select class="filter-select" id="ramFilter">
                        <option value="">All RAM</option>
'''
        for value in ram_values:
            html_content += f'                        <option value="{html.escape(value)}">{html.escape(value)}</option>\n'
        html_content += '''                    </select>
                </div>
'''
    
    html_content += '''                <div class="search-box">
                    <input type="text" class="search-input" id="searchInput" placeholder="Search items...">
                </div>
                
                <button class="clear-filters" id="clearFilters">Clear Filters</button>
            </div>
            
            <div class="filter-info" id="filterInfo" style="display: none;"></div>
        </div>
        
        <div class="table-container">
            <table id="productTable">
                <thead>
                    <tr>
                        <th>No.</th>
                        <th>Detail</th>
'''
    
    # Add table headers for each CSV column
    for header in headers:
        html_content += f'                        <th>{html.escape(header)}</th>\n'
    
    html_content += '''                    </tr>
                </thead>
                <tbody id="tableBody">
'''
    
    # Add each item as a table row
    for idx, item in enumerate(items, 1):
        # Add data attributes for filtering
        cpu_val = item.get(cpu_column, '') if cpu_column else ''
        ram_val = item.get(ram_column, '') if ram_column else ''
        data_attrs = f'data-cpu="{html.escape(cpu_val)}" data-ram="{html.escape(ram_val)}"'
        
        html_content += f'                    <tr {data_attrs}>\n'
        html_content += f'                        <td>{idx}</td>\n'
        html_content += '                        <td><span class="detail-icon">⊙</span></td>\n'
        
        for header in headers:
            value = item.get(header, '')
            css_class = ''
            
            # Apply specific styling based on column
            if header.lower() in ['name', 'product name', 'název', 'nazev']:
                css_class = 'product-name'
            elif header.lower() in ['price', 'cena', 'cost']:
                css_class = 'product-price'
            elif header.lower() in ['link', 'url', 'alza link', 'odkaz']:
                css_class = 'product-link'
            
            if value:
                # Check if value is a URL and make it clickable
                if value.startswith('http://') or value.startswith('https://'):
                    display_value = f'<a href="{html.escape(value)}" target="_blank">{html.escape(value)}</a>'
                    html_content += f'                        <td class="{css_class}">{display_value}</td>\n'
                else:
                    html_content += f'                        <td class="{css_class}">{html.escape(value)}</td>\n'
            else:
                html_content += f'                        <td class="{css_class}"></td>\n'
        
        html_content += '                    </tr>\n'
    
    html_content += '''                </tbody>
            </table>
        </div>
        
        <div class="no-results" id="noResults" style="display: none;">
            No items found matching your filters.
        </div>
        
        <div class="footer">
            <div id="recordCount">
                <strong>Total records:</strong> <span id="visibleCount">''' + str(len(items)) + '''</span> of ''' + str(len(items)) + ''' item(s)
            </div>
        </div>
    </div>

    <script>
        const cpuFilter = document.getElementById('cpuFilter');
        const ramFilter = document.getElementById('ramFilter');
        const searchInput = document.getElementById('searchInput');
        const clearFiltersBtn = document.getElementById('clearFilters');
        const tableBody = document.getElementById('tableBody');
        const tableContainer = document.querySelector('.table-container');
        const noResults = document.getElementById('noResults');
        const filterInfo = document.getElementById('filterInfo');
        const visibleCount = document.getElementById('visibleCount');
        
        // Apply all filters
        function applyFilters() {
            const cpuValue = cpuFilter ? cpuFilter.value.toLowerCase() : '';
            const ramValue = ramFilter ? ramFilter.value.toLowerCase() : '';
            const searchTerm = searchInput.value.toLowerCase();
            
            const rows = tableBody.querySelectorAll('tr');
            let visibleRowCount = 0;
            
            rows.forEach(row => {
                const rowCpu = (row.dataset.cpu || '').toLowerCase();
                const rowRam = (row.dataset.ram || '').toLowerCase();
                const rowText = row.textContent.toLowerCase();
                
                const matchesCpu = !cpuValue || rowCpu === cpuValue;
                const matchesRam = !ramValue || rowRam === ramValue;
                const matchesSearch = !searchTerm || rowText.includes(searchTerm);
                
                if (matchesCpu && matchesRam && matchesSearch) {
                    row.classList.remove('hidden');
                    visibleRowCount++;
                } else {
                    row.classList.add('hidden');
                }
            });
            
            // Update visible count
            visibleCount.textContent = visibleRowCount;
            
            // Show/hide no results message
            if (visibleRowCount === 0) {
                tableContainer.style.display = 'none';
                noResults.style.display = 'block';
            } else {
                tableContainer.style.display = 'block';
                noResults.style.display = 'none';
            }
            
            // Update filter info
            updateFilterInfo(cpuValue, ramValue, searchTerm);
        }
        
        // Update filter information display
        function updateFilterInfo(cpu, ram, search) {
            const filters = [];
            if (cpu) filters.push(`CPU: ${cpu}`);
            if (ram) filters.push(`RAM: ${ram}`);
            if (search) filters.push(`Search: "${search}"`);
            
            if (filters.length > 0) {
                filterInfo.textContent = '🔍 Active filters: ' + filters.join(' | ');
                filterInfo.style.display = 'block';
            } else {
                filterInfo.style.display = 'none';
            }
        }
        
        // Clear all filters
        function clearAllFilters() {
            if (cpuFilter) cpuFilter.value = '';
            if (ramFilter) ramFilter.value = '';
            searchInput.value = '';
            applyFilters();
        }
        
        // Event listeners
        if (cpuFilter) cpuFilter.addEventListener('change', applyFilters);
        if (ramFilter) ramFilter.addEventListener('change', applyFilters);
        searchInput.addEventListener('input', applyFilters);
        clearFiltersBtn.addEventListener('click', clearAllFilters);
    </script>
</body>
</html>'''
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ Catalogue created successfully: {output_file}")
    print(f"✓ Total items: {len(items)}")
    print(f"✓ Fields: {', '.join(headers)}")
    if cpu_column:
        print(f"✓ CPU filter added: {len(cpu_values)} unique values")
    if ram_column:
        print(f"✓ RAM filter added: {len(ram_values)} unique values")


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("CSV to HTML Catalogue Converter")
    print("=" * 60)
    print()
    
    # Get CSV file name from user
    csv_file = input("Enter the CSV file name (e.g., products.csv): ").strip()
    
    # Check if file exists
    if not Path(csv_file).exists():
        print(f"\n❌ Error: File '{csv_file}' not found!")
        print("Make sure the file exists in the current directory.")
        exit(1)
    
    # Get optional custom output name
    output_file = input("Enter output HTML file name (press Enter for 'catalogue.html'): ").strip()
    if not output_file:
        output_file = 'catalogue.html'
    elif not output_file.endswith('.html'):
        output_file += '.html'
    
    # Get optional custom title
    catalogue_title = input("Enter catalogue title (press Enter for 'Alza Product Export List'): ").strip()
    if not catalogue_title:
        catalogue_title = 'Alza Product Export List'
    
    print("\n" + "-" * 60)
    print("Converting...")
    print("-" * 60 + "\n")
    
    # Convert the CSV to HTML catalogue
    try:
        csv_to_catalogue(csv_file, output_file, catalogue_title)
        print("\n" + "=" * 60)
        print(f"✓ Success! Open '{output_file}' in your browser to view!")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        exit(1)