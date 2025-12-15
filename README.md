# **GlycoAssessor**

GlycoAssessor is a Python application designed to calculate and visualize Distance & Connectivity Index (DCI) and Position & Composition Index (PCI) scores for N-glycan structures. The tool helps users assess the spatial and structural properties of glycan molecules by analyzing the relationships between monosaccharide nodes and their glycosidic linkages.

---
## **Tutorial**
[![GlycoAssessor-Beta-Tutorial](https://github.com/user-attachments/assets/2e34a430-2cce-42d5-998a-148710bea42d)](https://www.youtube.com/watch?v=C6A-OxZNR2g)
The image above links to a YouTube tutorial ([https://www.youtube.com/watch?v=4d3WOO03Q34](https://www.youtube.com/watch?v=C6A-OxZNR2g)).


---
## **Features**

- **Distance & Connectivity Matrix / Index (DCI)**: 
  - Computes scores for each node based on the number of second, third, and fourth-degree connections.
  - Displays results in a weighted matrix and exports data as a CSV file.

- **Position & Composition Matrix / Index (PCI)**:
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
   python GlycoAssessor.py
   ```

2. **Modes:**
   - **Calculate DCI Mode**: Computes the Distance & Connectivity Index score for the structure.
   - **Calculate PCI Mode**: Computes the Position & Composition Index score for the structure.
   - **Export Image Mode**: Allows users to export the structure visualization as a PNG image.

---

## **Data Input**

The application requires the following data input:

- **Monosaccharide Nodes (Circles)**: A dictionary where each node is represented by its ID, position (x, y), and unique sugar code (e.g., Glu for Glucose).
- **Glycosidic Linkages (Edges)**: A dictionary where each edge connects two nodes and has an associated edge type.

Example:
```python
circles = {
    'A': (0, 0, 'Glu'),
    'B': (1, 0, 'Gal'),
    'C': (2, 1, 'Fuc')
}
edges = {
    1: ((0, 0), (1, 0), 'α1,3'),
    2: ((1, 0), (2, 1), 'ß1,6')
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
