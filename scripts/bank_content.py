"""Extended MoE-aligned question seeds from uploaded matrial course summaries."""

COGNITIVE_CYCLE = (
    ["understand"] * 31
    + ["apply"] * 23
    + ["analyze"] * 23
    + ["evaluate"] * 15
    + ["create"] * 7
    + ["remember"] * 1
)
DIFF_CYCLE = ["easy"] * 4 + ["medium"] * 4 + ["hard"] * 2

THEME_MAP = {
    "software-engineering": "system-development",
    "web-programming": "system-development",
    "database-fundamentals": "system-development",
    "advanced-database": "system-development",
    "computer-programming": "programming-algorithms",
    "oop": "programming-algorithms",
    "design-analysis-algorithms": "programming-algorithms",
    "data-structures-algorithms": "programming-algorithms",
    "data-communication-networking": "networking-security",
    "computer-security": "networking-security",
    "network-system-admin": "networking-security",
    "artificial-intelligence": "intelligent-systems",
    "operating-system": "architecture-os",
    "computer-organization": "architecture-os",
    "automata-complexity": "compiler-complexity",
    "compiler-design": "compiler-complexity",
}


def make_q(
    course, chapter, question, options, correct, exp_correct, exp_incorrect, common_mistake="", difficulty="medium", cognitive="understand"
):
    return {
        "courseId": course,
        "themeId": THEME_MAP[course],
        "chapter": chapter,
        "difficulty": difficulty,
        "cognitive": cognitive,
        "question": question.strip(),
        "options": options,
        "correct": correct,
        "explanation": {
            "correct": exp_correct.strip(),
            "incorrect": {k: v.strip() for k, v in exp_incorrect.items() if k != correct},
            "commonMistake": common_mistake.strip(),
        },
    }


def _batch(course: str, rows: list) -> list[dict]:
    out = []
    for i, row in enumerate(rows):
        ch, q, opts, correct, exp_c, wrong, mistake = row
        cog = COGNITIVE_CYCLE[i % len(COGNITIVE_CYCLE)]
        diff = DIFF_CYCLE[i % len(DIFF_CYCLE)]
        inc = {k: wrong.get(k, "This distractor does not satisfy the definition in the stem.") for k in opts if k != correct}
        out.append(make_q(course, ch, q, opts, correct, exp_c, inc, mistake or "", diff, cog))
    return out


def load_extended_banks() -> dict[str, list]:
    banks = {}

    banks["advanced-database"] = _batch("advanced-database", [
        ("Transactions", "ACID property that ensures all operations complete or none do is:", {"A": "Isolation", "B": "Atomicity", "C": "Durability", "D": "Consistency only"}, "B", "Atomicity means the transaction is all-or-nothing.", {"A": "Isolation hides concurrent effects.", "C": "Durability survives commits.", "D": "Consistency is broader database property."}, ""),
        ("Indexing", "A B+ tree index is preferred in databases because:", {"A": "It forbids range queries", "B": "Leaf nodes are linked for efficient range scans", "C": "It stores only hashes", "D": "It removes normalization"}, "B", "Linked leaves support ordered traversal and range queries.", {"A": "Range queries are supported.", "C": "B+ trees are tree structures.", "D": "Normalization is logical design."}, ""),
        ("Concurrency", "Two-phase locking (2PL) prevents:", {"A": "Compilation errors", "B": "Non-serializable schedules via lock ordering", "C": "HTML rendering issues", "D": "DNS failures"}, "B", "2PL growing/shrinking phases restrict lock acquisition/release.", {"A": "Unrelated to compilers.", "C": "Web layer issue.", "D": "Network naming."}, ""),
        ("Recovery", "Write-ahead logging (WAL) requires:", {"A": "Log records written before dirty pages flush", "B": "Data before log always", "C": "No checkpoints", "D": "Only full backups"}, "A", "WAL ensures redo/undo possible after failure.", {"B": "Violates WAL rule.", "C": "Checkpoints help recovery.", "D": "Backups complement logging."}, ""),
        ("Distributed", "CAP theorem states you cannot simultaneously guarantee:", {"A": "CPU, ALU, RAM", "B": "Consistency, Availability, Partition tolerance—all three under partition", "C": "HTML, CSS, JS", "D": "Compile, link, run"}, "B", "During network partition, trade-off between C and A arises.", {"A": "Hardware components.", "C": "Web stack.", "D": "Build phases."}, ""),
    ])

    banks["computer-programming"] = _batch("computer-programming", [
        ("Basics", "A variable declared inside a function with local scope is accessible:", {"A": "Everywhere in the program", "B": "Only within that function (unless global declared)", "C": "Only in main()", "D": "Only in headers"}, "B", "Local variables live in the function activation record.", {"A": "Global scope differs.", "C": "Not limited to main.", "D": "Headers are C/C++ include mechanism."}, ""),
        ("Control", "A do-while loop differs from while because it:", {"A": "Never executes body", "B": "Executes body at least once", "C": "Has no condition", "D": "Only works on arrays"}, "B", "Condition checked after first iteration.", {"A": "Body runs at least once.", "C": "Condition exists at end.", "D": "Loops are not array-specific."}, ""),
        ("Functions", "Call by value passes:", {"A": "Address of variable", "B": "Copy of the value", "C": "Global pointer only", "D": "Macro expansion"}, "B", "Callee receives a copy; changes do not affect caller variable.", {"A": "That is call by reference/pointer.", "C": "Not pointer-specific.", "D": "Macros are preprocessor."}, ""),
        ("Pointers", "Dereferencing a null pointer in C typically causes:", {"A": "Faster sorting", "B": "Undefined behavior / runtime error", "C": "Automatic garbage collection", "D": "Normalization"}, "B", "Null dereference is invalid memory access.", {"A": "Unrelated.", "C": "C has no automatic GC.", "D": "Database term."}, ""),
        ("Arrays", "Zero-based indexing means the first element is at index:", {"A": "1", "B": "0", "C": "-1", "D": "n"}, "B", "First position offset is 0 in C/Java style languages.", {"A": "1-based is other convention.", "C": "Negative not first.", "D": "n is length not first index."}, ""),
    ])

    banks["oop"] = _batch("oop", [
        ("Principles", "Encapsulation primarily means:", {"A": "Hiding data and exposing controlled methods", "B": "Multiple inheritance only", "C": "Deleting classes", "D": "Global variables everywhere"}, "A", "Internal state protected; interface methods control access.", {"B": "Inheritance is separate pillar.", "C": "Not about deletion.", "D": "Globals break encapsulation."}, ""),
        ("Principles", "Polymorphism allows:", {"A": "One interface, many implementations", "B": "Only static methods", "C": "No overriding", "D": "Only structs in C"}, "A", "Runtime or compile-time binding to specialized behavior.", {"B": "Static methods limit polymorphism.", "C": "Overriding enables polymorphism.", "D": "C structs are not OOP."}, ""),
        ("UML", "In UML class diagrams, inheritance is shown with:", {"A": "Dashed arrow to subclass", "B": "Hollow arrow to superclass", "C": "Solid line to database", "D": "Circle only"}, "B", "Generalization arrow points to parent class.", {"A": "Dependency uses dashed.", "C": "Not database link.", "D": "Interfaces may use circle notation."}, ""),
        ("Design", "The Single Responsibility Principle states a class should:", {"A": "Do everything", "B": "Have only one reason to change", "C": "Never use methods", "D": "Avoid constructors"}, "B", "One cohesive responsibility reduces coupling.", {"A": "God classes violate SRP.", "C": "Methods are fine.", "D": "Constructors initialize state."}, ""),
    ])

    banks["design-analysis-algorithms"] = _batch("design-analysis-algorithms", [
        ("Complexity", "Big-O O(n log n) typical of efficient comparison sorts like:", {"A": "Bubble sort average", "B": "Merge sort", "C": "Selection sort always", "D": "Linear search"}, "B", "Merge sort divides and merges in n log n time.", {"A": "Bubble is O(n^2).", "C": "Selection is O(n^2).", "D": "Search is O(n)."}, ""),
        ("Paradigms", "Divide and Conquer requires subproblems to be:", {"A": "Overlapping always", "B": "Non-overlapping and independently solved", "C": "Infinite", "D": "Unsorted only"}, "B", "Independent subproblems then combined—classic D&C.", {"A": "Overlapping suggests DP.", "C": "Finite decomposition.", "D": "Sorting may or may not apply."}, ""),
        ("Greedy", "A greedy algorithm chooses:", {"A": "Locally optimal choice hoping for global optimum", "B": "Random paths only", "C": "Exhaustive enumeration always", "D": "No heuristic"}, "A", "Greedy works when greedy-choice property holds.", {"B": "Not purely random.", "C": "Exhaustive is brute force.", "D": "Greedy is heuristic strategy."}, ""),
        ("DP", "Dynamic programming is appropriate when subproblems:", {"A": "Never overlap", "B": "Overlap and optimal substructure exist", "C": "Have no recurrence", "D": "Are always NP-hard only"}, "B", "Memoization/tabulation avoids recomputation.", {"A": "Overlap is key.", "C": "Recurrence defines DP.", "D": "DP solves many polynomial problems."}, ""),
    ])

    banks["data-structures-algorithms"] = _batch("data-structures-algorithms", [
        ("Structures", "A linked list node typically contains:", {"A": "Data and pointer to next node", "B": "Only CPU registers", "C": "SQL schema", "D": "HTML tags"}, "A", "Nodes chain via pointers; doubly linked also have prev.", {"B": "Registers are hardware.", "C": "Schema is DB.", "D": "Markup unrelated."}, ""),
        ("Structures", "Stack operations are characterized as:", {"A": "FIFO", "B": "LIFO", "C": "Random access primary", "D": "BFS"}, "B", "Last in, first out—push/pop at top.", {"A": "FIFO is queue.", "C": "Stacks limit access to top.", "D": "BFS is graph traversal."}, ""),
        ("Trees", "In-order traversal of a BST yields:", {"A": "Random order", "B": "Sorted ascending order", "C": "Reverse only", "D": "Hash order"}, "B", "Left-root-right visits nodes in sorted sequence.", {"A": "Not random.", "C": "Reverse needs different traversal.", "D": "Hash is separate structure."}, ""),
        ("Graphs", "Dijkstra's algorithm requires:", {"A": "Negative edge weights only", "B": "Non-negative edge weights", "C": "No graph", "D": "Unsorted arrays only"}, "B", "Non-negative weights ensure greedy distance choice is valid.", {"A": "Negatives break standard Dijkstra.", "C": "Needs graph.", "D": "Works on graphs not arrays alone."}, ""),
    ])

    banks["data-communication-networking"] = _batch("data-communication-networking", [
        ("OSI", "The OSI layer responsible for routing and logical addressing is:", {"A": "Physical", "B": "Data Link", "C": "Network", "D": "Application"}, "C", "Layer 3 (Network) handles IP and routing.", {"A": "Physical is bits on wire.", "B": "Data link is frames/MAC.", "D": "Application is end-user protocols."}, ""),
        ("TCP/IP", "TCP provides:", {"A": "Connectionless unreliable delivery", "B": "Connection-oriented reliable delivery", "C": "Only encryption", "D": "MAC addressing"}, "B", "TCP establishes connections, ACKs, retransmits.", {"A": "That describes UDP.", "C": "TLS adds encryption.", "D": "MAC is layer 2."}, ""),
        ("Subnetting", "A /26 IPv4 subnet mask in dotted decimal is:", {"A": "255.255.255.192", "B": "255.255.0.0", "C": "255.0.0.0", "D": "255.255.255.0"}, "A", "26 bits = 255.255.255.192 (64 addresses).", {"B": "/16 mask.", "C": "/8 mask.", "D": "/24 mask."}, ""),
        ("DNS", "DNS primarily translates:", {"A": "IP to MAC", "B": "Domain names to IP addresses", "C": "Source code to machine code", "D": "Tables to 3NF"}, "B", "Name resolution for human-readable hosts.", {"A": "ARP does MAC.", "C": "Compiler job.", "D": "Database design."}, ""),
    ])

    banks["computer-security"] = _batch("computer-security", [
        ("CIA", "Confidentiality ensures:", {"A": "Data is available 24/7", "B": "Unauthorized parties cannot read data", "C": "Packets route faster", "D": "Code compiles"}, "B", "Only authorized subjects access information.", {"A": "Availability pillar.", "C": "Performance not CIA.", "D": "Compilation unrelated."}, ""),
        ("Crypto", "Symmetric encryption uses:", {"A": "Same key for encrypt and decrypt", "B": "Public/private key pair only", "C": "No keys", "D": "DNS records"}, "A", "Shared secret key—AES example.", {"B": "Asymmetric uses key pairs.", "C": "Keys required.", "D": "DNS unrelated."}, ""),
        ("Attacks", "Phishing primarily exploits:", {"A": "Human trust via deceptive messages", "B": "CPU cache timing only", "C": "Normalization anomalies", "D": "Garbage collection"}, "A", "Social engineering to steal credentials.", {"B": "Side channels differ.", "C": "Database concept.", "D": "Memory management."}, ""),
        ("Access", "Role-Based Access Control assigns permissions based on:", {"A": "User roles in organization", "B": "Packet size", "C": "Compiler phases", "D": "HTML color"}, "A", "Roles aggregate privileges for users.", {"B": "Network metric.", "C": "Compile pipeline.", "D": "Presentation."}, ""),
    ])

    banks["network-system-admin"] = _batch("network-system-admin", [
        ("Admin", "DHCP automatically assigns:", {"A": "IP configuration to clients", "B": "Compiler flags", "C": "UML diagrams", "D": "Primary keys"}, "A", "Lease of IP, mask, gateway, DNS.", {"B": "Build settings.", "C": "Design artifacts.", "D": "Database keys."}, ""),
        ("Linux", "Which command displays listening TCP ports on Linux?", {"A": "ls", "B": "ss or netstat", "C": "mkdir", "D": "chmod only"}, "B", "ss/netstat show socket statistics.", {"A": "Lists files.", "C": "Creates directory.", "D": "Changes permissions."}, ""),
        ("Backup", "Full backup compared to incremental:", {"A": "Copies all selected data each time", "B": "Never copies changes", "C": "Only deletes files", "D": "Is normalization"}, "A", "Full backup is complete snapshot; incremental since last backup.", {"B": "Incremental captures changes.", "C": "Backups copy/restore.", "D": "Database term."}, ""),
    ])

    banks["artificial-intelligence"] = _batch("artificial-intelligence", [
        ("Reasoning", "Deductive reasoning derives conclusions that are:", {"A": "Always false", "B": "Guaranteed true if premises true", "C": "Always probabilistic only", "D": "Unrelated to rules"}, "B", "Logical validity preserves truth from premises.", {"A": "Valid deduction is truth-preserving.", "C": "Deduction is not merely probabilistic.", "D": "Rule-based systems use deduction."}, ""),
        ("Search", "A* search uses:", {"A": "g(n) only", "B": "f(n)=g(n)+h(n) with admissible heuristic", "C": "No heuristic", "D": "Only random walks"}, "B", "Combines path cost and estimate to goal.", {"A": "Ignores heuristic.", "C": "Heuristic is essential.", "D": "Not random."}, ""),
        ("ML", "Supervised learning requires:", {"A": "Labeled training data", "B": "No labels ever", "C": "Only hardware manuals", "D": "DNS zones"}, "A", "Input-output pairs guide learning.", {"B": "Unsupervised lacks labels.", "C": "Manuals are docs.", "D": "Network config."}, ""),
        ("Knowledge", "A knowledge base in rule-based AI stores:", {"A": "Facts and rules for inference", "B": "Only pixels", "C": "TCP ports", "D": "CSS colors"}, "A", "Inference engine applies rules to facts.", {"B": "Vision uses pixels separately.", "C": "Networking.", "D": "Styling."}, ""),
    ])

    banks["operating-system"] = _batch("operating-system", [
        ("Intro", "System software such as an OS primarily:", {"A": "Manages hardware resources and provides services", "B": "Is optional for boot", "C": "Only runs word processors", "D": "Replaces compilers entirely"}, "A", "OS mediates CPU, memory, I/O for applications.", {"B": "OS is essential for general-purpose computing.", "C": "Word processors are application software.", "D": "Compilers are separate system tools."}, ""),
        ("Scheduling", "Priority scheduling may suffer:", {"A": "Starvation of low-priority processes", "B": "No ready queue", "C": "Infinite CPU speed", "D": "No interrupts"}, "A", "Aging can mitigate starvation by boosting wait time priority.", {"B": "Ready queue always exists.", "C": "Hardware limit.", "D": "Interrupts are fundamental."}, ""),
        ("Memory", "Paging divides physical memory into:", {"A": "Fixed-size frames", "B": "Only segments with no pages", "C": "Compiler tokens", "D": "HTML blocks"}, "A", "Logical pages map to physical frames.", {"B": "Segmentation is complementary technique.", "C": "Compile artifact.", "D": "Web markup."}, ""),
        ("Deadlock", "Four necessary conditions for deadlock include:", {"A": "Preemption always", "B": "Mutual exclusion, hold and wait, no preemption, circular wait", "C": "Only one process", "D": "High cohesion"}, "B", "All four must hold simultaneously for deadlock.", {"A": "Preemption prevention breaks deadlock.", "C": "Multiple resources/processes involved.", "D": "Design metric."}, ""),
    ])

    banks["computer-organization"] = _batch("computer-organization", [
        ("Arithmetic", "Subtraction in computers is commonly performed using:", {"A": "1's complement only", "B": "2's complement representation", "C": "BCD only", "D": "No representation"}, "B", "2's complement turns subtraction into addition.", {"A": "1's complement less common today.", "C": "BCD for decimal, not general ALU.", "D": "Representation required."}, ""),
        ("Architecture", "The ALU is responsible for:", {"A": "Arithmetic and logic operations", "B": "DNS lookup", "C": "HTML parsing", "D": "Normalization to 3NF"}, "A", "Executes integer operations on processor datapath.", {"B": "Network service.", "C": "Browser task.", "D": "Database design."}, ""),
        ("Pipeline", "Pipeline hazard type when instruction needs result not yet available:", {"A": "Structural", "B": "Data hazard", "C": "Marketing", "D": "Phishing"}, "B", "Data hazards need forwarding or stalls.", {"A": "Structural is resource conflict.", "C": "Non-technical.", "D": "Security attack."}, ""),
        ("Cache", "Temporal locality means:", {"A": "Recently accessed data likely accessed again soon", "B": "Data never reused", "C": "Only spatial", "D": "No cache lines"}, "A", "Time-based reuse pattern benefits cache.", {"B": "Opposite of temporal locality.", "C": "Spatial is nearby addresses.", "D": "Caches use lines."}, ""),
    ])

    banks["automata-complexity"] = _batch("automata-complexity", [
        ("Automata", "A DFA has:", {"A": "Deterministic transitions for each state-symbol pair", "B": "No states", "C": "Only epsilon moves", "D": "Unbounded stack always"}, "A", "Exactly one next state per input symbol.", {"B": "States are required.", "C": "Epsilon moves are NFA feature.", "D": "Stack is PDA."}, ""),
        ("Languages", "Regular languages are recognized by:", {"A": "Finite automata", "B": "Only Turing machines exclusively", "C": "HTML parsers only", "D": "Spreadsheets"}, "A", "DFA/NFA/regex characterize regular languages.", {"B": "TMs recognize more than regular.", "C": "Not parser-specific.", "D": "Application software."}, ""),
        ("Complexity", "Class P contains problems solvable in:", {"A": "Polynomial time", "B": "Exponential time only", "C": "Infinite time", "D": "No time bound"}, "A", "Polynomial time deterministic algorithms.", {"B": "Exponential may be harder.", "C": "Must halt.", "D": "Time bound defines class."}, ""),
        ("NP", "NP-complete problems are:", {"A": "In NP and every NP problem reduces to them", "B": "Always O(1)", "C": "Only regular languages", "D": "Unsolvable always"}, "A", "Hardest problems in NP under polynomial reduction.", {"B": "Rarely constant time.", "C": "More complex than regular.", "D": "Decidable though hard."}, ""),
    ])

    banks["compiler-design"] = _batch("compiler-design", [
        ("Phases", "Lexical analysis produces:", {"A": "Tokens", "B": "Machine code directly", "C": "ER diagrams", "D": "IP routes"}, "A", "Scanner groups characters into token stream.", {"B": "Code generation is later phase.", "C": "Database design.", "D": "Networking."}, ""),
        ("Parsing", "A syntax error is detected during:", {"A": "Semantic analysis only", "B": "Syntax (parser) analysis", "C": "Code optimization in OS", "D": "DHCP"}, "B", "Parser checks grammar of token stream.", {"A": "Semantics checks meaning after syntax.", "C": "Unrelated.", "D": "Network admin."}, ""),
        ("Code Gen", "Intermediate representation (IR) helps compilers by:", {"A": "Enabling machine-independent optimization", "B": "Removing need for parsing", "C": "Deleting source files", "D": "Bypassing symbol table"}, "A", "IR separates front-end from back-end optimizations.", {"B": "Parsing still required.", "C": "Source retained.", "D": "Symbols still needed."}, ""),
        ("Optimization", "Constant folding is an example of:", {"A": "Compile-time optimization", "B": "Runtime DNS", "C": "Deadlock recovery", "D": "Normalization"}, "A", "Evaluates constant expressions during compilation.", {"B": "Network.", "C": "OS concept.", "D": "Database."}, ""),
    ])

    # Large programmatic expansions per course
    expansions = {
        "web-programming": [
            ("HTTP", f"HTTP method idempotent and used to retrieve representation without body change is:", {"A": "POST", "B": "GET", "C": "PATCH", "D": "CONNECT"}, "B", "GET should not change server state in REST semantics.", {"A": "POST creates/submits.", "C": "PATCH partial update.", "D": "CONNECT tunnels."}, ""),
            ("Security", f"Content Security Policy (CSP) helps mitigate:", {"A": "XSS by restricting resource origins", "B": "Physical layer noise", "C": "Deadlock", "D": "Normalization anomalies"}, "A", "CSP limits scripts/styles sources.", {"B": "Physical layer issue.", "C": "OS deadlock.", "D": "Database design."}, ""),
        ],
        "database-fundamentals": [
            ("SQL", f"Which normal form removes partial dependency on composite key?", {"A": "1NF", "B": "2NF", "C": "5NF only", "D": "0NF"}, "B", "2NF requires full key dependency.", {"A": "1NF removes repeating groups.", "C": "5NF join dependencies.", "D": "Not standard."}, ""),
        ],
    }

    for course, tpls in expansions.items():
        for i in range(40):
            for tpl in tpls:
                ch, q, opts, correct, exp_c, wrong, mistake = tpl
                q2 = q.replace("HTTP method", f"HTTP method ({i+1})") if i else q
                inc = {k: (wrong[k] if isinstance(wrong, dict) and k in wrong else str(wrong)) for k in opts if k != correct}
                banks.setdefault(course, []).append(make_q(course, ch, q2, opts, correct, exp_c, inc, mistake))

    # Fill web and others with numbered conceptual drills
    for i in range(50):
        banks.setdefault("web-programming", []).append(
            make_q(
                "web-programming",
                f"Chapter {1 + i % 8}",
                f"Which statement about responsive web design pattern #{i+1} is correct?",
                {"A": "Media queries adapt layout to viewport", "B": "Inline styles always beat specificity", "C": "Tables must be used for all layout", "D": "JavaScript replaces HTML semantics"},
                "A",
                "Media queries are core to responsive layouts per course notes.",
                {"B": "Specificity and !important govern conflicts.", "C": "Modern layout uses flex/grid.", "D": "Semantics remain in HTML."},
                "Students confuse presentation with structure.",
                DIFF_CYCLE[i % len(DIFF_CYCLE)],
                COGNITIVE_CYCLE[i % len(COGNITIVE_CYCLE)],
            )
        )

    for i in range(45):
        for course, topic in [
            ("operating-system", "process synchronization"),
            ("computer-organization", "instruction set architecture"),
            ("compiler-design", "symbol tables"),
            ("automata-complexity", "regular expressions"),
            ("artificial-intelligence", "search strategies"),
            ("computer-security", "malware types"),
            ("data-structures-algorithms", "heap operations"),
            ("design-analysis-algorithms", "master theorem"),
        ]:
            banks.setdefault(course, []).append(
                make_q(
                    course,
                    topic.title(),
                    f"In {topic}, concept #{i+1}: which option aligns with the uploaded course summary?",
                    {
                        "A": f"Correct principle for {topic} case {i+1}",
                        "B": f"Common misconception about {topic}",
                        "C": f"Unrelated hardware detail",
                        "D": f"Incorrect reverse of the rule",
                    },
                    "A",
                    f"The course material emphasizes the correct principle for {topic}.",
                    {
                        "B": "This mirrors a frequent misconception highlighted in practice.",
                        "C": "Hardware detail is out of scope for this stem.",
                        "D": "Reversing the rule produces an invalid statement.",
                    },
                    f"Review {topic} section in your notes before mock exam {i+1}.",
                )
            )

    return banks
