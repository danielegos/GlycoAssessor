# **GlycoAssessor**

GlycoAssessor is a Python application designed to calculate and visualize Distance & Connectivity Index (DCI) and Position & Composition Index (PCI) scores for N-glycan structures. The tool helps users assess the spatial and structural properties of glycan molecules by analyzing the relationships between monosaccharide nodes and their glycosidic linkages.

---

## **Features**

- **Distance & Connectivity Index (DCI)**: 
  - Computes scores for each node based on the number of second, third, and fourth-degree connections.
  - Displays results in a weighted matrix and exports data as a CSV file.

- **Position & Composition Index (PCI)**:
  - Computes layer-based scores based on node colors, layer size, and inter-layer connectivity.
  - Displays results in a detailed matrix and exports data as a CSV file.

- **Node Layering and Connectivity Visualization**:
  - Organizes nodes into layers based on x-coordinates.
  - Computes inter-layer linkages and linkage types for each layer.

- **Image Export**:
  - Allows users to export the current N-glycan structure as an image (PNG format).

---

## **Requirements**

- Python 3.x
- Libraries:
  - `tkinter` (for the graphical user interface)
  - `pandas` (for data manipulation and exporting to CSV)
  - `PrettyTable` (for tabular data display)
  - `Pillow` (for image export functionality)

---

## **Installation**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/danielegos/GlycoAssessor.git
   cd GlycoAssessor
   ```

2. **Install dependencies:**
   Ensure you have Python 3 installed, then install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

---

## **Usage**

1. **Launch the Application:**
   To run the application, use the following command:
   ```bash
   python main.py
   ```

2. **Modes:**
   - **Calculate DCI Mode**: Computes the Distance & Connectivity Index score for the structure.
   - **Calculate PCI Mode**: Computes the Position & Composition Index score for the structure.
   - **Export Image Mode**: Allows users to export the structure visualization as a PNG image.

---

## **Data Input**

The application requires the following data input:

- **Monosaccharide Nodes (Circles)**: A dictionary where each node is represented by its ID, position (x, y), and color.
- **Glycosidic Linkages (Edges)**: A dictionary where each edge connects two nodes and has an associated edge type.

Example:
```python
circles = {
    'A': (0, 0, 'red'),
    'B': (1, 0, 'blue'),
    'C': (2, 1, 'green')
}
edges = {
    1: ((0, 0), (1, 0), 'alpha'),
    2: ((1, 0), (2, 1), 'beta')
}
```

---

## **Exporting Data**

After running the calculations, you can export the results to a CSV file, which will include:

- **DCI Matrix**: Weighted matrix showing node scores based on their connectivity.
- **PCI Matrix**: Layer-wise matrix showing scores based on node composition and inter-layer linkages.

---

## **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## **Contributing**

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

---

## **Acknowledgements**

- Thanks to the Python community and the open-source libraries used in this project.
- Special thanks to contributors at the Tissue Spatial Geometrics Lab (https://www.tsg-lab.org/) and users for testing and providing feedback.

---

Feel free to edit this README based on any additional details specific to your app.
