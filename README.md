
# 👩🏻‍💻📓✍🏻💡The Campus Puzzle
## <br /> **Advanced Algorithm M603A** 

# 📋 Introduction

University timetabling is a problem of constraint satisfaction which involves graph colouring, bin packing and combinatorial optimisation. 
It is NP-hard in general, thus the use of a pipeline of complementary algorithms in practical systems.

**The assessment brief needs to include the following:** 

<br />(1) a Greedy baseline; 
<br />(2) a Welsh–Powell colouring of a conflict graph; 
<br />(3) a room allocator for the DP which mixes recursive backtracking with best-effort; 
<br />(4) a Conflict Report; 
<br />(5) a Manual Fix Log.


# 💻 🛠 System Architecture

<img width="1140" alt="Screenshot 2026-09-18 171234" src="https://github.com/user-attachments/assets/c1eeb9d4-3b05-42dd-b690-4777e41c5ea8" />


# 📘 Repository Structure
<div>
    <pre>
        M603/
│
├── data/
│   └── constraints.json
│
├── src/
│   ├── __pycache__/
│   │   ├── __init__.cpython-314.pyc
│   │   ├── backtracker.cpython-314.pyc
│   │   ├── data_loader.cpython-314.pyc
│   │   ├── graph_engine.cpython-314.pyc
│   │   ├── greedy_solver.cpython-314.pyc
│   │   ├── optimizer.cpython-314.pyc
│   │   └── schedule.cpython-314.pyc
│   │
│   ├── __init__.py
│   ├── backtracker.py
│   ├── data_loader.py
│   ├── graph_engine.py
│   ├── greedy_solver.py
│   ├── optimizer.py
│   └── schedule.py
│
├── .gitignore
└── main.py
    </pre>
</div>

    
# 📈 Future Improvements
**Limitations:** Backtracking is exponential worst-case, and is most appropriate for small unscheduled sets. The DP allocator makes the number of slots fixed. Soft constraints, such as preferences of the lecturer or equipment in the room, are not modelled.<br />
**Future Work:** Local search or genetic algorithms for larger sets of unspecified problems; soft constraints as penalties; web interface; integration with external venues; multi-semester planning.


# 👨‍💻 Author

**Er. Manoj Kumar**

Aspiring Software Developer | AI & ML Enthusiast

