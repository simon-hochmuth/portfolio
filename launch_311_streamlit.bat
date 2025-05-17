@echo off
echo 🔄 Navigating to project directory...
cd /d E:\Coding_Corner\portfolio

echo ✅ Activating virtual environment...
call simon_hochmuth_portfolio\Scripts\activate.bat

echo 🚀 Launching Streamlit app...
streamlit run src\scripts\NYC_311_API_Project\src\app.py

pause