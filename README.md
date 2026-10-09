# 🇳🇵 Nepali Vehicle Number Plate Recognition (ANPR)

A project to detect, analyze, and read Nepali vehicle number plates (both Devanagari and English Embossed formats) and lay the foundation for traffic violation reporting.

---

## 📁 Repository Structure

```
nepal-traffic-anpr/
├── data/
│   ├── raw/            # Place original vehicle images / video frames here
│   └── processed/      # Cropped plate images ready for OCR
├── models/             # Store trained model weights (.pt)
├── notebooks/          # Jupyter notebooks for experiments, learning, and testing
├── src/                # Python scripts and source code
├── .gitignore          # Prevents pushing heavy images and models to GitHub
├── requirements.txt    # Essential Python libraries
└── README.md           # Project documentation
```

---

## 🛠️ Getting Started

### 1. Set Up Virtual Environment

Open your terminal in this repository and create a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

Install the core computer vision and deep learning packages:

```bash
pip install -r requirements.txt
```

### 3. Start Learning in Jupyter Notebook

To experiment with OpenCV and view images interactively:

```bash
jupyter notebook
```
Save your experiment notebooks in the `notebooks/` folder.

---

## 🎯 Learning & Building Roadmap

- [ ] **Step 1: Data Collection & Exploration**
  - Collect sample photos of Nepali bikes, cars, and buses (Devanagari & Embossed).
  - Practice loading and displaying them using OpenCV and Matplotlib in a notebook.

- [ ] **Step 2: License Plate Detection (YOLO)**
  - Label bounding boxes for plates using Roboflow or Label Studio.
  - Train a lightweight YOLO model to crop license plates from full vehicle photos.

- [ ] **Step 3: Character Recognition (OCR)**
  - Experiment with OCR models to read Nepali numbers (०-९) and vehicle symbols (क-ह).
  - Handle English embossed plates.

- [ ] **Step 4: Traffic Rules & Mock Database**
  - Parse the recognized text into structured vehicle information.
  - Connect with a mock database of vehicle owners and traffic violations.

---

## 👤 Author

**Sushant Singh Thapa**  
*Data Science Student*  
GitHub: [@sushantt-ds](https://github.com/sushantt-ds)
