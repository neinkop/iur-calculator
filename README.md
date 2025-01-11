# IUR-Calculator
**The Small IUR Calculator**
The project was implemented as part of an additional examination assignment in the module "Programming 1" with Prof. Dr. Andreas Biesdorf at Trier University of Applied Sciences.  
The calculation of the key figures is based on the formula collection from the module "Internal Corporate and Investment Accounting" by Prof. Dr. Michael Keilus.

### Context and Problem Description ("Problem Space")  
The profitability of investment projects is determined by various financial indicators. These indicators provide a foundation for economic decision-making and can sometimes be calculated manually. However, the effort required for the calculation varies significantly: while some indicators, such as the net present value, are relatively simple to compute, determining more complex values like the internal rate of return requires considerably more effort. In some cases, it is almost impossible to calculate these values accurately without computer-assisted methods.  

**Key Requirements:**  
- **Functional Requirements:**  
  - Implementation of calculations for static and dynamic investment indicators  
  - Automatic assignment of calculated values to respective investment projects  
- **Non-functional Requirements:**  
  - High accuracy of calculations  
  - User-friendly presentation of results  

---

### Solution and Implementation Concept ("Solution Space")  
The basic solution involves implementing the calculations for the indicators as functions and organizing them using an object-oriented approach. For each investment project, an object of the corresponding class is created. These objects store both input values and the calculated indicators as attributes.  

**Core Elements of the Solution:**  
- **Classification of Investment Projects:**  
  - *Static IPs:* Calculation of static indicators (e.g., profit, imputed interest, static payback period, etc.)  
  - *Dynamic IPs:* Calculation of dynamic indicators (e.g., net present value, internal rate of return, dynamic payback period, etc.)  
- **Implementation of the Newton-Raphson Method:**  
  - This iterative method is used to efficiently determine the internal rate of return, as other search methods were found to have unacceptable runtime performance.  
- **Modular Structure:**  
  - Each class has clearly defined responsibilities and methods.  
  - Extensibility for adding new indicators or methods/functions.  

---

### Testing Concept  
To ensure the functionality and accuracy of the calculations, targeted tests are conducted:  
1. **Comparison with Known Results:**  
   - A complete investment project, whose indicators are known from lecture materials, is calculated, and the results are compared.  
2. **Tests with Edge Cases:**  
   - High discount rates (DR)  
   - Project duration = 0  
   - Initial investment (a₀) = negative  

---

### Outlook  
Future developments could include the following:  
- **Data Import:**  
  - Implementation of a function to read cash flow series from CSV files  
  - Integration of a database connection to retrieve cash flow series from databases  
- **Automatic Decision Support:**  
  - Predefined decision rules could be used to automatically recommend for or against an investment project.  
  - Implementation of risk analysis/indicators  
- **Expansion of Indicators:**  
  - Integration of additional indicators to enable a more comprehensive analysis  

This project was jointly developed by Paul Jakob and Bastian Bach. The section on static investment analysis was primarily implemented by Bastian Bach, while the dynamic investment analysis was primarily implemented by Paul Jakob. Testing and code optimizations were carried out collaboratively.  
