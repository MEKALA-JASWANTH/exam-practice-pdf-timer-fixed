# 📚 Exam Practice PDF Timer - Fixed Version

> **Fixed version of PDF exam practice tool with timer - Resolved missing questions issue and improved option display handling.**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## ✨ What's Fixed in This Version

### 🐞 Bug Fixes

1. **Missing Question 11 Issue - RESOLVED** ✅
   - **Problem**: Questions were being skipped during PDF extraction (particularly Q11)
   - **Root Cause**: 
     - Overly strict regex patterns that didn't match all question formats
     - Arbitrary `break` condition that stopped extraction after 5 questions per page
   - **Solution**: 
     - Enhanced regex patterns to support multiple question numbering formats
     - Removed premature break conditions
     - Added support for "Q.1", "Q1", "Question 1", "1.", "1)" formats

2. **Improved Option Parsing** ✅
   - Better detection of A, B, C, D answer choices
   - Handles various option formats (A. , A) , A: )
   - More robust text cleaning

### 🎓 Key Improvements

- **Enhanced Question Extraction**: No more missing questions!
- **Flexible Pattern Matching**: Supports various PDF formats
- **Image Support Preparation**: Added PIL/Pillow and PyMuPDF for future image handling
- **Improved UI**: Clean, intuitive interface with question navigation
- **Timer Functionality**: Track your exam time
- **Progress Tracking**: See which questions you've answered

## 🚀 Quick Start

### Prerequisites

```bash
Python 3.8 or higher
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/MEKALA-JASWANTH/exam-practice-pdf-timer-fixed.git
cd exam-practice-pdf-timer-fixed
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app.py
```

4. **Open your browser** at `http://localhost:8501`

## 📝 How to Use

1. **Upload PDF**: Click "Choose PDF file" and select your exam PDF
2. **Set Duration**: Choose exam duration (1-180 minutes)
3. **Start Exam**: Click "🚀 Start Exam"
4. **Answer Questions**: Select answers using radio buttons
5. **Navigate**: Use Previous/Next buttons or quick navigation grid
6. **Submit**: Click "✅ Submit Exam" when done

## 🛠️ Technical Details

### Fixed Code Changes

**Before (Buggy)**:
```python
patterns = [
    r'Q\.\s*(\d+)[.:\s]+(.+?)(?=Q\.\s*\d+|\*)',
    r'(\d+)\.\s+(.+?)(?=\d+\.|$)',
]
if len(matches) > 5:  # ❌ This caused questions to be skipped!
    break
```

**After (Fixed)**:
```python
patterns = [
    r'Q(?:uestion)?[.:]?\s*(\d+)[.:)\s]+(.+?)(?=Q(?:uestion)?[.:]?\s*\d+|$)',
    r'(\d+)[.:)]\s+(.+?)(?=\d+[.:)\s]|$)',
]
# Removed arbitrary break - process all questions!
```

## 📊 Project Status

- [x] Fix missing question issue (Q11)
- [x] Improve regex patterns
- [x] Add multiple question format support
- [x] Remove extraction limits
- [ ] Add image extraction from PDFs
- [ ] Display images in questions
- [ ] Add answer key validation
- [ ] Export results to PDF

## 💻 Technologies Used

- **Streamlit**: Web interface
- **PyPDF2**: PDF text extraction
- **Python**: Backend logic
- **Pillow**: Image processing (prepared)
- **PyMuPDF**: Advanced PDF handling (prepared)

## 👥 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📝 License

MIT License - feel free to use for educational purposes

## 🎉 New: Multi-PDF Support

Upload and combine multiple PDFs into a single exam session!

### Features:
- **Upload Multiple PDFs**: Select multiple PDF files at once
- **Question Bank**: Automatically merges questions from all PDFs
- **Source Tracking**: Each question shows which PDF it came from
- **Progress by PDF**: See your progress broken down by PDF source during the exam
- **Performance Analytics**: View completion rates per PDF at the end

### How to Use:
1. Click "Choose PDF file(s)" and select multiple PDFs (hold Ctrl/Cmd to select multiple)
2. All questions from selected PDFs will be combined into one exam
3. During the exam, you'll see which PDF each question came from
4. At the end, view your performance breakdown by PDF source

## 🚀 Future Enhancements

1. **Image Support**: Extract and display images/diagrams from PDFs
2. **Answer Validation**: Check answers against answer key
3. **Statistics**: Track performance over time
4. **Multiple PDFs**: Support for question banks ✅ (IMPLEMENTED - See "Multi-PDF Support" section above)
5. **Export**: Save results as PDF reports

---

**Made with ❤️ for better exam preparation**

Repository: [exam-practice-pdf-timer-fixed](https://github.com/MEKALA-JASWANTH/exam-practice-pdf-timer-fixed)

---

## 📝 Recent Updates

**Version 2.0 - November 2025**
- ✅ Fixed critical question extraction bug (Q11 issue resolved)
- ✅ Added multi-PDF support for combining multiple exam papers
- ✅ Enhanced regex patterns for better question detection
- ✅ Improved UI/UX with better navigation
- ✅ Added performance analytics by PDF source

## 🎯 Use Cases

- **Students**: Practice for competitive exams with timed sessions
- **Teachers**: Create practice tests from multiple PDF sources
- **Self-learners**: Track progress and identify weak areas
- **Exam Prep**: Simulate real exam conditions with timer

## 💡 Tips for Best Results

1. Use clear, well-formatted PDF files for best question extraction
2. Ensure questions follow standard numbering (1., Q1, Question 1, etc.)
3. Keep PDFs focused on MCQ-type questions with A/B/C/D options
4. Use the multi-PDF feature to create comprehensive practice sessions

## 🔧 Troubleshooting

**Questions not extracting properly?**
- Check if your PDF has clear question numbering
- Ensure options are labeled with A, B, C, D
- Try using a different PDF format or re-export your PDF

**Timer not working?**
- Refresh the page
- Clear browser cache
- Ensure JavaScript is enabled

## 📞 Contact & Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Email: [Your contact email]
- Pull requests are always welcome!


