"""
PDF Extractor - NiceGUI Frontend

A modern web interface for extracting tables and text from PDF files
and converting them to various formats.
"""

from nicegui import ui, run
from processor import tables_to_dataframe, convert_to_format, extract_text_from_pdf, convert_text_to_format

# Theme: primary #CD2C58, secondary #FFC69D, dark mode #25343F — no blue; contrast-safe
ui.add_head_html('''
<style>
  :root {
    --app-primary: #CD2C58;
    --app-secondary: #FFC69D;
    --app-dark-bg: #25343F;
    --app-text-on-primary: #ffffff;
    --app-text-on-secondary: #1a1a1a;
    --q-primary: #FFC69D;
    --q-color-primary: #FFC69D;
  }
  .q-btn.bg-primary { --q-primary: #FFC69D; background: #FFC69D !important; color: #1a1a1a !important; }
  .q-btn.bg-primary .q-btn__content, .q-btn.bg-primary .q-icon { color: #1a1a1a !important; }
  .app-header { background-color: var(--app-primary) !important; color: var(--app-text-on-primary) !important; }
  .app-header .q-btn, .app-header .q-btn .q-icon, .app-header .q-btn i { color: var(--app-text-on-primary) !important; }
  .dark .app-header { background-color: var(--app-dark-bg) !important; color: #f0f0f0 !important; }
  .dark .app-header .q-btn, .dark .app-header .q-btn .q-icon { color: #f0f0f0 !important; }
  .app-btn-primary, .app-btn-primary.q-btn, .q-btn.app-btn-primary {
    background-color: var(--app-secondary) !important;
    color: var(--app-text-on-secondary) !important;
  }
  .app-btn-primary .q-btn__content, .app-btn-primary .q-icon, .app-btn-primary i { color: var(--app-text-on-secondary) !important; }
  .app-btn-primary:hover { filter: brightness(0.92); }
  .dark .app-btn-primary, .dark .q-btn.app-btn-primary {
    background-color: #3d4f5c !important;
    color: #f0f0f0 !important;
  }
  .dark .app-btn-primary .q-btn__content, .dark .app-btn-primary .q-icon { color: #f0f0f0 !important; }
  .dark .app-btn-primary:hover { filter: brightness(1.15); }
  .q-card { background-color: #fce8ec !important; }
  .dark .q-card { background-color: #2f4150 !important; }
  .dark body, .dark .q-drawer, .dark .q-page, .dark .q-layout,
  .dark .nicegui-content, .body--dark { background-color: #25343F !important; }
  .dark .q-field, .dark .q-field__control-container, .dark .q-uploader { background-color: #2f4150 !important; }
  .dark .q-field__native, .dark .q-field__label, .dark .q-item__label,
  .dark .q-select__dropdown-icon, .dark .text-grey, .dark .q-uploader__header span { color: #e8e8e8 !important; }
  .dark .q-card .q-field__native, .dark .q-card .q-field__label,
  .dark .q-card label, .dark .q-card .q-item__label { color: #e8e8e8 !important; }
  .dark .q-card .text-grey-7, .dark .q-card .text-grey-8 { color: #c0c0c0 !important; }
  .q-spinner .path { stroke: #FFC69D !important; }
  .q-radio__inner--active, .q-radio__inner--active .q-radio__bg,
  .q-radio .q-radio__inner:not(.q-radio__inner--focused):after,
  .q-item.q-item--active .q-radio__inner,
  .q-radio.bg-primary .q-radio__inner, .q-radio .q-radio__inner.bg-primary { color: #FFC69D !important; background: #FFC69D !important; border-color: #FFC69D !important; fill: #FFC69D !important; }
  .q-radio__inner::before { border-color: #FFC69D !important; }
  .q-radio--active .q-radio__inner::after { background: #FFC69D !important; }
  .q-field--focused .q-field__control:after { border-color: #FFC69D !important; }
  .q-uploader__header {
    background: #FFC69D !important;
    color: #1a1a1a !important;
  }
  .q-uploader__header .q-icon, .q-uploader__header span { color: #1a1a1a !important; }
  body .q-btn.bg-primary, body .q-btn[class*="primary"] { background: #FFC69D !important; color: #1a1a1a !important; }
  .q-card .q-btn:not(.q-btn--flat):not(.q-btn--round),
  .q-card .q-btn.q-btn--unelevated, .q-card .q-btn.bg-primary { background: #FFC69D !important; color: #1a1a1a !important; }
  .q-card .q-btn:not(.q-btn--flat) .q-btn__content, .q-card .q-btn:not(.q-btn--flat) .q-icon { color: #1a1a1a !important; }
  .q-card .q-btn .q-btn__content, .q-card .q-btn .q-icon { color: #1a1a1a !important; }
  .dark .q-card .q-btn:not(.q-btn--flat):not(.q-btn--round) { background: #3d4f5c !important; color: #f0f0f0 !important; }
  .dark .q-card .q-btn .q-btn__content, .dark .q-card .q-btn .q-icon { color: #f0f0f0 !important; }
  html.dark, html body.body--dark { background: #25343F !important; }
  .dark .text-grey-5, .dark .text-grey-6, .dark .text-grey-7, .dark .text-grey-8 { color: #b8b8b8 !important; }
</style>
''')


# Global state to track uploaded file and processed data
uploaded_file_bytes = None
uploaded_filename = None
processed_dataframe = None
processed_text = None


async def handle_upload(e):
    """Handle file upload event."""
    global uploaded_file_bytes, uploaded_filename, processed_dataframe
    
    try:
        # In NiceGUI 3.0+, use e.file.name and await e.file.read()
        uploaded_filename = e.file.name
        uploaded_file_bytes = await e.file.read()
        
        # Reset processed data when new file is uploaded
        processed_dataframe = None
        processed_text = None
        preview_table.set_visibility(False)
        preview_label.set_visibility(False)
        preview_text.set_visibility(False)
        preview_text_label.set_visibility(False)
        download_button.set_visibility(False)
        
        # Validate it's a PDF
        if not uploaded_filename.lower().endswith('.pdf'):
            upload_status.set_text("Please upload a PDF file.")
            upload_status.classes('text-red-600')
            process_button.set_enabled(False)
            uploaded_file_bytes = None
            uploaded_filename = None
            ui.notify("Invalid file type. Please upload a PDF file.", type='negative')
            return
        
        upload_status.set_text(f"✓ File uploaded: {uploaded_filename}")
        upload_status.classes('text-gray-800 dark:text-gray-200')
        process_button.set_enabled(True)
        ui.notify(f"File '{uploaded_filename}' uploaded successfully!", type='positive', timeout=2000)
        
    except Exception as ex:
        uploaded_file_bytes = None
        uploaded_filename = None
        processed_dataframe = None
        upload_status.set_text(f"Upload error: {str(ex)}")
        upload_status.classes('text-red-600 dark:text-red-400')
        process_button.set_enabled(False)
        ui.notify(f"Upload failed: {str(ex)}", type='negative')


async def process_pdf():
    """Process the uploaded PDF asynchronously."""
    global uploaded_file_bytes, uploaded_filename, processed_dataframe, processed_text
    
    if not uploaded_file_bytes:
        ui.notify("Please upload a PDF file first.", type='negative')
        return
    
    # Get extraction mode
    extraction_mode = mode_selector.value.lower()
    
    # Show loading spinner
    spinner.set_visibility(True)
    process_button.set_enabled(False)
    status_label.set_text("Processing PDF...")
    status_label.classes('text-gray-800 dark:text-gray-200')
    preview_table.set_visibility(False)
    preview_label.set_visibility(False)
    preview_text.set_visibility(False)
    preview_text_label.set_visibility(False)
    download_button.set_visibility(False)
    
    try:
        if extraction_mode == 'tables':
            # Extract tables
            df = await run.cpu_bound(tables_to_dataframe, uploaded_file_bytes)
            
            if df.empty:
                spinner.set_visibility(False)
                process_button.set_enabled(True)
                status_label.set_text("No tables found in the PDF.")
                status_label.classes('text-yellow-600 dark:text-yellow-400')
                ui.notify("No tables detected in the PDF file.", type='warning', timeout=3000)
                processed_dataframe = None
                return
            
            # Store the processed dataframe
            processed_dataframe = df
            processed_text = None
            
            # Show preview table with first 5 rows
            preview_rows = df.head(5)
            preview_table.rows = preview_rows.to_dict('records')
            preview_table.columns = [{'name': col, 'label': col, 'field': col} for col in df.columns]
            preview_table.set_visibility(True)
            preview_label.set_visibility(True)
            
            # Update format selector for tables
            format_selector.options = ['CSV', 'Excel']
            if format_selector.value not in ['CSV', 'Excel']:
                format_selector.set_value('CSV')
            
            # Update status
            status_label.set_text(f"✓ Successfully extracted {len(df)} rows from {len(df.columns)} columns")
            status_label.classes('text-gray-800 dark:text-gray-200')
            ui.notify(
                f"Successfully extracted {len(df)} rows! Preview shown below.",
                type='positive',
                timeout=3000
            )
            
        else:  # text extraction
            # Extract text
            text = await run.cpu_bound(extract_text_from_pdf, uploaded_file_bytes)
            
            if not text or not text.strip():
                spinner.set_visibility(False)
                process_button.set_enabled(True)
                status_label.set_text("No text found in the PDF.")
                status_label.classes('text-yellow-600 dark:text-yellow-400')
                ui.notify("No text detected in the PDF file.", type='warning', timeout=3000)
                processed_text = None
                return
            
            # Store the processed text
            processed_text = text
            processed_dataframe = None
            
            # Show preview text (first 1000 characters)
            preview_content = text[:1000] + ('...' if len(text) > 1000 else '')
            preview_text.set_value(preview_content)
            preview_text.set_visibility(True)
            preview_text_label.set_visibility(True)
            
            # Update format selector for text
            format_selector.options = ['TXT', 'DOCX']
            if format_selector.value not in ['TXT', 'DOCX']:
                format_selector.set_value('TXT')
            
            # Update status
            char_count = len(text)
            word_count = len(text.split())
            status_label.set_text(f"✓ Successfully extracted {word_count:,} words ({char_count:,} characters)")
            status_label.classes('text-gray-800 dark:text-gray-200')
            ui.notify(
                f"Successfully extracted text! Preview shown below.",
                type='positive',
                timeout=3000
            )
        
        # Show download button
        download_button.set_visibility(True)
        spinner.set_visibility(False)
        process_button.set_enabled(True)
        
    except Exception as e:
        spinner.set_visibility(False)
        process_button.set_enabled(True)
        status_label.set_text(f"Error: {str(e)}")
        status_label.classes('text-red-600 dark:text-red-400')
        preview_table.set_visibility(False)
        preview_label.set_visibility(False)
        preview_text.set_visibility(False)
        preview_text_label.set_visibility(False)
        download_button.set_visibility(False)
        processed_dataframe = None
        processed_text = None
        ui.notify(f"Error processing PDF: {str(e)}", type='negative', timeout=5000)


def download_file():
    """Download the processed file in the selected format."""
    global processed_dataframe, processed_text, uploaded_filename
    
    # Get selected format
    selected_format = format_selector.value.lower()
    
    try:
        if processed_dataframe is not None and not processed_dataframe.empty:
            # Download table data
            output_stream = convert_to_format(processed_dataframe, selected_format)
            file_extension = '.csv' if selected_format == 'csv' else '.xlsx'
            output_filename = uploaded_filename.rsplit('.', 1)[0] + file_extension
            
        elif processed_text is not None and processed_text.strip():
            # Download text data
            output_stream = convert_text_to_format(processed_text, selected_format)
            file_extension = '.txt' if selected_format == 'txt' else '.docx'
            output_filename = uploaded_filename.rsplit('.', 1)[0] + file_extension
            
        else:
            ui.notify("No data to download. Please process the PDF first.", type='warning')
            return
        
        # Get the bytes from the stream
        output_bytes = output_stream.getvalue()
        
        # Trigger download
        ui.download(output_bytes, filename=output_filename)
        
        ui.notify(
            f"Download started: {output_filename}",
            type='positive',
            timeout=2000
        )
        
    except Exception as e:
        ui.notify(f"Error creating download file: {str(e)}", type='negative', timeout=5000)


# Create the UI
dark_mode = ui.dark_mode()
with ui.header().classes('app-header p-4'):
    with ui.row().classes('w-full items-center justify-between'):
        ui.label('PDF Extractor').classes('text-2xl font-bold')
        
        def toggle_dark_mode():
            dark_mode.toggle()
            ui.notify(
                f"Switched to {'light' if dark_mode.value else 'dark'} mode",
                type='info',
                timeout=1500
            )
        
        ui.button(icon='dark_mode', on_click=toggle_dark_mode).props('flat round')

with ui.card().classes('w-full max-w-4xl mx-auto mt-6 p-8 shadow-lg'):
    # Title
    ui.label('PDF Extractor').classes('text-3xl font-bold text-center mb-2')
    
    # Description
    ui.label('Upload a PDF file to extract tables or text and convert them to various formats.').classes(
        'text-gray-600 dark:text-gray-300 text-center mb-6'
    )
    
    # Extraction mode selector
    ui.label('Extraction Mode').classes('text-lg font-semibold mb-2')
    
    mode_selector = ui.radio(
        ['Tables', 'Text'],
        value='Tables'
    ).props('inline').classes('mb-4')
    
    # File upload area
    ui.label('Upload PDF File').classes('text-lg font-semibold mb-2')
    
    upload = ui.upload(
        on_upload=handle_upload,
        auto_upload=True,
        max_file_size=50 * 1024 * 1024  # 50MB limit
    ).props('accept=".pdf"').classes('w-full')
    
    upload_status = ui.label('No file uploaded').classes('text-gray-500 dark:text-gray-400 text-sm mt-2')
    
    # Format selector
    ui.label('Output Format').classes('text-lg font-semibold mb-2 mt-6')
    
    format_selector = ui.select(
        ['CSV', 'Excel'],
        value='CSV',
        label='Select format'
    ).classes('mb-4')
    
    # Process button
    process_button = ui.button(
        'Process PDF',
        on_click=process_pdf
    ).classes('w-full mt-4 app-btn-primary font-semibold py-3 rounded-lg').style(
        'background-color: #FFC69D !important; color: #1a1a1a !important;'
    )
    process_button.set_enabled(False)
    
    # Status area with spinner
    with ui.row().classes('w-full mt-4 items-center justify-center'):
        spinner = ui.spinner(size='lg', color='primary')
        spinner.set_visibility(False)
        status_label = ui.label('').classes('ml-3')
    
    # Preview table (initially hidden)
    preview_table = ui.table(
        rows=[],
        columns=[],
        row_key='id'
    ).classes('w-full mt-2').style('max-height: 300px;')
    preview_table.set_visibility(False)
    
    preview_label = ui.label('Preview (First 5 rows)').classes('text-lg font-semibold mb-2 mt-6')
    preview_label.set_visibility(False)
    
    # Preview text (initially hidden)
    preview_text_label = ui.label('Preview (First 1000 characters)').classes('text-lg font-semibold mb-2 mt-6')
    preview_text_label.set_visibility(False)
    
    preview_text = ui.textarea('').classes('w-full mt-2').style('min-height: 200px; max-height: 300px;')
    preview_text.set_visibility(False)
    preview_text.props('readonly')
    
    # Download button (initially hidden)
    download_button = ui.button(
        'Download',
        on_click=download_file,
        icon='download'
    ).classes('w-full mt-4 app-btn-primary font-semibold py-3 rounded-lg').style(
        'background-color: #FFC69D !important; color: #1a1a1a !important;'
    )
    download_button.set_visibility(False)
    
    # Footer note
    ui.label('All processing is done in-memory. No files are stored on the server.').classes(
        'text-xs text-gray-400 dark:text-gray-500 text-center mt-6'
    )

# Expose ASGI app for Vercel; use NiceGUI default server when run locally
if __name__ in {"__main__", "__mp_main__"}:
    # Local: ui.run() serves at http://localhost:8080/
    ui.run(title="PDF Extractor", port=8080, dark=None)
else:
    # Vercel: mount at /api; Railway/Render: mount at / so uvicorn main:app works
    import os
    from fastapi import FastAPI
    app = FastAPI()
    mount_path = "/api" if os.environ.get("VERCEL") else "/"
    ui.run_with(app, mount_path=mount_path)
