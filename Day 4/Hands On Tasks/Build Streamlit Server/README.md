# Build Streamlit Server Workshop - Quick Start Guide

## Installation

1. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify installation:**
   ```bash
   streamlit --version
   ```

## Running the Workshop Tasks

### Task 1: Basic Setup
```bash
streamlit run task_1_app.py
```
Test with:
```bash
python test_task_1.py
```

### Task 2: Sidebar and Input
```bash
streamlit run task_2_app.py
```
Test with:
```bash
python test_task_2.py
```

### Task 3: Tabs and Layout
```bash
streamlit run task_3_app.py
```

### Task 4: API Integration
**Important:** Start the FastAPI server first!
```bash
# Terminal 1: Start FastAPI server
cd "../Build FastAPI Server"
python task_5_server.py

# Terminal 2: Start Streamlit app
streamlit run task_4_app.py
```
Test with:
```bash
python test_task_4.py
```

## Completed Application

The full application from the original code is in:
```
../frontend/streamlit_app.py
```

## Common Commands

- **Stop Streamlit:** Press `Ctrl+C` in terminal
- **Reload app:** Streamlit auto-reloads when you save files
- **Clear cache:** Click "Clear cache" in the browser menu (☰)

## Troubleshooting

### "Module not found" errors
```bash
pip install streamlit requests Pillow
```

### API connection errors
1. Check FastAPI server is running: `http://127.0.0.1:8000/docs`
2. Verify port 8000 is not in use
3. Check firewall settings

### Port already in use
```bash
# Kill process on port 8501 (Streamlit)
# Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Or use a different port:
streamlit run task_1_app.py --server.port 8502
```

## Workshop Flow

1. Read the `overview.md` for introduction
2. Complete tasks 1-5 in order
3. Read the corresponding `.md` file for each task
4. Implement the code in each `task_X_app.py`
5. Test your implementation
6. Move to the next task

## Tips

- Save frequently - Streamlit auto-reloads
- Use `st.write()` for debugging
- Check browser console for JavaScript errors
- Read error messages carefully - they're helpful!

## Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Cheat Sheet](https://docs.streamlit.io/library/cheatsheet)
- [Streamlit Gallery](https://streamlit.io/gallery)

Good luck with the workshop! 🚀
