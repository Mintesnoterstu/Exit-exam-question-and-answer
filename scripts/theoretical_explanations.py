"""
Generate theoretical (concept-based) explanations for exit exam MCQs.
Focus: definitions, principles, models, and theory — not step-by-step code traces.
"""
from __future__ import annotations

import re
from typing import Any

COURSE_THEORY = {
    "software-engineering": "Software Engineering",
    "web-programming": "Web Programming",
    "database-fundamentals": "Database Systems",
    "advanced-database": "Advanced Database Systems",
    "computer-programming": "Computer Programming",
    "oop": "Object-Oriented Programming",
    "design-analysis-algorithms": "Design and Analysis of Algorithms",
    "data-structures-algorithms": "Data Structures and Algorithms",
    "data-communication-networking": "Data Communication and Networking",
    "computer-security": "Computer Security",
    "network-system-admin": "Network and System Administration",
    "artificial-intelligence": "Artificial Intelligence",
    "operating-system": "Operating Systems",
    "computer-organization": "Computer Organization and Architecture",
    "automata-complexity": "Automata and Complexity Theory",
    "compiler-design": "Compiler Design",
}

# Maps phrases (in question or option) to theoretical concept explanations
CONCEPT_THEORY: list[tuple[list[str], str]] = [
    (["sdlc", "analysis phase", "requirements gathering", "gathering and analyzing user"], 
     "The Analysis phase of the Software Development Life Cycle (SDLC) is the requirements engineering stage where functional and non-functional needs are elicited, analyzed, and documented before any design or implementation."),
    (["single responsibility", "one reason to change"],
     "The Single Responsibility Principle (SRP) from SOLID design theory states that a module or class should encapsulate only one axis of change — one responsibility — so that modifications remain localized."),
    (["scrum", "agile"],
     "Scrum is an Agile software development framework based on iterative sprints, empirical process control, and adaptive planning — contrasting with predictive sequential models."),
    (["waterfall", "sequential flow"],
     "The Waterfall model is a classical predictive SDLC in which phases (requirements, design, implementation, testing, deployment) proceed sequentially with minimal iteration."),
    (["html", "hyper text markup"],
     "HTML (HyperText Markup Language) is the W3C standard markup language for structuring and semantically describing web document content."),
    (["css", "style web", "cascading style"],
     "CSS (Cascading Style Sheets) is the presentation-layer language that separates document structure from visual styling, layout, and responsive design."),
    (["select", "retrieve data from a database", "sql statement is used to retrieve"],
     "In relational algebra and SQL, the SELECT operation performs projection and selection over relations to retrieve tuples satisfying a predicate."),
    (["insert", "add new rows"],
     "The SQL INSERT statement implements the relational insertion operator, adding new tuples to a base relation while respecting integrity constraints."),
    (["update", "modify existing records"],
     "SQL UPDATE implements relational assignment, modifying attribute values of existing tuples that satisfy a WHERE predicate."),
    (["acid", "atomicity, consistency"],
     "ACID is the transaction model guaranteeing Atomicity (all-or-nothing), Consistency (valid state transitions), Isolation (concurrent serializability), and Durability (committed persistence)."),
    (["primary key", "unique identifier for each row"],
     "A primary key is a minimal superkey enforcing entity integrity — uniquely identifying each tuple in a relation with no NULL values."),
    (["foreign key", "references the primary key"],
     "A foreign key implements referential integrity by requiring attribute values to match a primary key in a referenced relation or be NULL."),
    (["normalization", "normal form", "1nf", "2nf", "3nf", "bcnf"],
     "Database normalization theory decomposes relations to eliminate insertion, update, and deletion anomalies by removing redundant functional dependencies."),
    (["inner join", "left join", "outer join"],
     "Relational join theory combines tuples from two relations based on join predicates; INNER keeps matches only, OUTER preserves non-matching tuples from one or both sides."),
    (["mongodb", "nosql"],
     "NoSQL databases trade strict relational schemas for flexible data models (document, key-value, column, graph) to support horizontal scalability and schema evolution."),
    (["stored procedure", "precompiled collection"],
     "Stored procedures encapsulate procedural database logic on the server, offering modularity, security, and reduced network traffic in client-server DBMS architecture."),
    (["trigger"],
     "Database triggers are event-driven procedural objects that execute automatically on INSERT, UPDATE, or DELETE — implementing reactive integrity and auditing."),
    (["view", "virtual table"],
     "A view is a virtual relation defined by a query expression; it provides logical data independence and controlled access without duplicating storage."),
    (["index", "speed up data retrieval", "b+ tree", "b-tree"],
     "Indexing theory uses auxiliary access paths (B-trees, B+ trees, hash indexes) to reduce I/O cost from O(n) scans toward O(log n) lookups."),
    (["deadlock", "two transactions waiting"],
     "Deadlock theory (Coffman conditions) requires mutual exclusion, hold-and-wait, no preemption, and circular wait; resolution uses prevention, avoidance, detection, or recovery."),
    (["two-phase locking", "2pl"],
     "Two-Phase Locking (2PL) is a concurrency control protocol ensuring conflict-serializable schedules by prohibiting lock acquisition after any lock release."),
    (["cap theorem"],
     "The CAP theorem (Brewer) states that a distributed data store cannot simultaneously guarantee Consistency, Availability, and Partition tolerance during network partitions."),
    (["tcp", "three-way handshake", "connection-oriented"],
     "TCP is a transport-layer protocol providing connection-oriented, reliable, ordered byte-stream delivery via sequence numbers, acknowledgments, and flow/congestion control."),
    (["udp", "connectionless"],
     "UDP is a connectionless transport protocol offering minimal overhead and no delivery guarantees — suitable for latency-sensitive or broadcast applications."),
    (["http", "port 80", "retrieve data from a server"],
     "HTTP is the application-layer request-response protocol of the Web; GET retrieves representations, POST submits entities, following REST architectural constraints."),
    (["https", "port 443", "ssl", "tls"],
     "HTTPS combines HTTP with TLS cryptographic protocols to provide confidentiality, integrity, and server authentication over port 443."),
    (["osi", "network layer", "routing"],
     "The OSI reference model partitions network communication into seven layers; Layer 3 (Network) handles logical addressing and routing via IP."),
    (["data link", "error detection"],
     "The Data Link layer (OSI Layer 2) frames bits into frames, provides MAC addressing, and performs error detection/correction on the local link."),
    (["dhcp"],
     "DHCP is an application-layer protocol that automates dynamic IP address assignment, subnet mask, default gateway, and DNS configuration."),
    (["dns", "domain names"],
     "DNS is the hierarchical distributed naming system that resolves human-readable domain names to IP addresses via recursive and iterative queries."),
    (["arp", "mac address"],
     "ARP (Address Resolution Protocol) maps known IP addresses to MAC addresses on the local network segment."),
    (["firewall"],
     "A firewall enforces network security policy by filtering packets based on rules — implementing perimeter defense in depth-in-security architecture."),
    (["aes", "symmetric encryption"],
     "Symmetric cryptography uses a shared secret key for encryption and decryption; AES is the NIST standard block cipher for confidentiality."),
    (["rsa", "asymmetric", "ecc", "diffie-hellman"],
     "Asymmetric (public-key) cryptography uses key pairs — enabling key exchange, digital signatures, and encryption without pre-shared secrets."),
    (["sha-256", "hashing", "hash algorithm"],
     "Cryptographic hash functions produce fixed-length digests with preimage resistance and collision resistance — SHA-256 is a secure standard."),
    (["sql injection", "xss", "csrf"],
     "Web application security theory classifies injection flaws (SQLi, XSS, CSRF) as failures to validate, sanitize, or authorize untrusted input."),
    (["phishing", "social engineering"],
     "Phishing is a social engineering attack exploiting human psychology to obtain credentials or sensitive data via deceptive communication."),
    (["stack", "lifo"],
     "A stack is an abstract data type with LIFO semantics — fundamental to expression evaluation, recursion, and depth-first traversal."),
    (["queue", "fifo", "breadth-first"],
     "A queue is an ADT with FIFO semantics — used in scheduling, buffering, and breadth-first graph traversal."),
    (["binary search", "sorted array"],
     "Binary search exploits the total ordering of sorted arrays to achieve O(log n) search via divide-and-conquer on index ranges."),
    (["merge sort", "divide-and-conquer"],
     "Merge sort is a stable divide-and-conquer sorting algorithm with O(n log n) worst-case time, based on merging sorted subarrays."),
    (["quick sort", "average-case"],
     "Quicksort applies partition-based divide-and-conquer; average O(n log n) but worst O(n²) when pivots are adversarial."),
    (["dijkstra", "shortest path", "non-negative"],
     "Dijkstra's algorithm is a greedy graph algorithm computing single-source shortest paths in graphs with non-negative edge weights."),
    (["bellman-ford", "negative weight"],
     "Bellman-Ford relaxes all edges repeatedly, handling negative weights and detecting negative cycles — O(VE) time."),
    (["dynamic programming", "overlapping subproblems"],
     "Dynamic programming applies optimal substructure and overlapping subproblems via memoization or tabulation to avoid exponential recomputation."),
    (["hash table", "collision", "chaining"],
     "Hash tables map keys to buckets via hash functions; collision resolution uses chaining or open addressing with load factor analysis."),
    (["polymorphism", "one interface"],
     "Polymorphism (from Greek 'many forms') allows uniform treatment of objects of different types through a common interface — compile-time or runtime binding."),
    (["encapsulation", "inheritance"],
     "Encapsulation bundles data with methods controlling access; inheritance enables IS-A relationships and code reuse in OOP type hierarchies."),
    (["virtual function", "runtime polymorphism"],
     "Virtual functions enable dynamic dispatch in C++ — the runtime vtable mechanism resolves the correct overridden method."),
    (["constructor", "initializes an object"],
     "A constructor is a special initialization method invoked at object creation to establish invariants and allocate resources."),
    (["garbage collection"],
     "Garbage collection is automatic memory reclamation based on reachability analysis — eliminating manual deallocation in managed runtimes like the JVM."),
    (["pointer", "address of another variable"],
     "A pointer is a variable holding a memory address, enabling indirect access and dynamic data structures in systems programming."),
    (["machine learning", "learn from data"],
     "Machine learning is the AI paradigm where systems improve performance on a task through experience (data) without explicit rule programming."),
    (["supervised", "labeled data"],
     "Supervised learning trains on labeled input-output pairs to learn a mapping function for prediction or classification."),
    (["unsupervised", "clustering"],
     "Unsupervised learning discovers hidden structure in unlabeled data — clustering, dimensionality reduction, and density estimation."),
    (["neural network", "activation function", "backpropagation"],
     "Artificial neural networks are universal function approximators; backpropagation applies the chain rule of calculus to update weights via gradient descent."),
    (["overfitting", "regularization"],
     "Overfitting occurs when model capacity exceeds data complexity; regularization (L1/L2, dropout) penalizes complexity to improve generalization."),
    (["precision", "recall", "f1"],
     "Classification evaluation theory uses precision (positive predictive value), recall (sensitivity), and F1 (harmonic mean) to measure performance beyond accuracy."),
    (["transformer", "attention", "bert", "gpt"],
     "Transformer architecture replaces recurrence with self-attention mechanisms, enabling parallel processing of sequences and contextual token representations."),
    (["reinforcement learning", "agent", "reward"],
     "Reinforcement learning models an agent interacting with an environment to maximize cumulative reward through policy optimization."),
    (["process", "thread", "separate memory"],
     "Process theory treats each process as an independent execution unit with its own address space; threads share memory within a process for lightweight concurrency."),
    (["deadlock", "mutual exclusion", "circular wait"],
     "Deadlock theory identifies four necessary conditions; prevention strategies break at least one condition (e.g., resource ordering breaks circular wait)."),
    (["paging", "virtual memory", "page fault"],
     "Virtual memory uses paging to map logical pages to physical frames on demand; page faults trigger OS loading from secondary storage."),
    (["tlb", "translation lookaside"],
     "The TLB is a hardware cache of page table entries that accelerates virtual-to-physical address translation."),
    (["lru", "fifo", "page replacement"],
     "Page replacement algorithms (FIFO, LRU, Optimal) govern which frame to evict when physical memory is full — balancing implementation cost and hit rate."),
    (["scheduling", "round robin", "fcfs", "preemptive"],
     "CPU scheduling theory allocates processor time among ready processes using policies (FCFS, SJF, Round Robin, Priority) optimizing turnaround, waiting time, or fairness."),
    (["semaphore", "mutex"],
     "Semaphores are Dijkstra's synchronization primitive for counting resource availability; mutexes provide binary mutual exclusion."),
    (["compiler", "lexical analysis", "token"],
     "Compiler theory divides translation into phases: lexical analysis (tokens), syntax analysis (parse tree), semantic analysis (types), optimization, and code generation."),
    (["finite automaton", "regular language", "dfa", "nfa"],
     "Finite automata recognize regular languages — the Type-3 class in Chomsky hierarchy, equivalent to regular expressions."),
    (["pushdown automaton", "context-free"],
     "Pushdown automata extend finite automata with a stack, recognizing context-free languages (Type-2) used in programming language syntax."),
    (["turing machine", "recursively enumerable"],
     "Turing machines are the theoretical model of computation; the Church-Turing thesis equates algorithmic computability with TM recognizability."),
    (["halting problem", "undecidable"],
     "The halting problem is undecidable — no algorithm can determine whether an arbitrary program halts on an arbitrary input (Turing, 1936)."),
    (["p and np", "np-complete", "polynomial time"],
     "Complexity theory classifies problems by resource bounds: P (polynomial time solvable), NP (polynomial time verifiable), NP-complete (hardest in NP)."),
    (["chomsky hierarchy"],
     "The Chomsky hierarchy orders formal grammars by generative power: regular ⊂ context-free ⊂ context-sensitive ⊂ unrestricted."),
    (["von neumann", "harvard architecture"],
     "Von Neumann architecture stores programs and data in unified memory; Harvard architecture uses separate instruction and data memories for parallel fetch."),
    (["pipeline", "hazard", "branch prediction"],
     "Instruction pipelining overlaps fetch, decode, execute, memory, and writeback stages; hazards (structural, data, control) require forwarding, stalls, or prediction."),
    (["cache", "locality", "write-through", "write-back"],
     "Cache memory exploits temporal and spatial locality; write policies (write-through vs write-back) trade consistency with memory traffic."),
    (["cisc", "risc"],
     "CISC uses complex variable-length instructions; RISC favors simple fixed-length instructions and register-heavy operations for pipelining efficiency."),
    (["mesi", "cache coherence"],
     "MESI is a cache coherence protocol maintaining consistency across multiprocessor caches via Modified, Exclusive, Shared, Invalid states."),
]

# What common distractor options theoretically represent (for wrong-answer explanations)
OPTION_CONCEPT_HINTS: dict[str, str] = {
    "design": "the SDLC Design phase, where system architecture and specifications are created after requirements are known",
    "implementation": "the Implementation/Coding phase where designs are translated into executable code",
    "testing": "the Testing/Verification phase focused on validating behavior against requirements",
    "waterfall": "the sequential Waterfall lifecycle model with phase-gate progression",
    "insert": "the SQL INSERT operator for adding tuples to relations",
    "delete": "the SQL DELETE operator for removing tuples",
    "udp": "UDP, a connectionless transport protocol without reliability guarantees",
    "tcp": "TCP, a connection-oriented reliable transport protocol",
    "stack": "the Stack ADT with LIFO access semantics",
    "queue": "the Queue ADT with FIFO access semantics",
    "linear search": "linear (sequential) search with O(n) worst-case complexity",
    "bubble sort": "Bubble sort, a simple O(n²) comparison sort",
    "merge sort": "Merge sort, an O(n log n) divide-and-conquer sort",
    "aes": "AES symmetric encryption",
    "rsa": "RSA asymmetric public-key cryptography",
    "1nf": "First Normal Form — atomic values and no repeating groups",
    "2nf": "Second Normal Form — no partial key dependencies",
    "3nf": "Third Normal Form — no transitive dependencies",
    "bcnf": "Boyce-Codd Normal Form — every determinant is a candidate key",
}

CODE_OUTPUT_THEORY = {
    "java": "In Java language semantics, control-flow constructs (loops, conditionals) and operator precedence govern expression evaluation. Integer arithmetic follows two's complement rules; String concatenation is defined when any operand is of type String.",
    "cpp": "In C++ semantics, operators have defined precedence and associativity. Integer division truncates toward zero. References alias existing objects; pointers hold addresses. Undefined behavior arises when the language standard imposes no requirements.",
    "c": "In C semantics, arithmetic conversions and integer division follow the C standard. Static storage duration persists across calls; automatic variables have function scope.",
}


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())


def detect_topic_theory(question: str, correct_text: str) -> str | None:
    combined = _normalize(question + " " + correct_text)
    for keywords, theory in CONCEPT_THEORY:
        if any(kw in combined for kw in keywords):
            return theory
    return None


def theory_for_option(option_text: str, course_id: str) -> str:
    low = _normalize(option_text)
    for hint_key, hint in OPTION_CONCEPT_HINTS.items():
        if hint_key in low:
            return hint
    for keywords, theory in CONCEPT_THEORY:
        if any(kw in low for kw in keywords):
            return theory
    course = COURSE_THEORY.get(course_id, "Computer Science")
    return f"a concept studied within {course} — specifically, '{option_text}' as defined in standard CS curriculum materials"


def build_theoretical_explanation(
    num: int,
    course_id: str,
    question: str,
    correct: str,
    options: dict[str, str],
    code: dict[str, Any] | None = None,
) -> dict:
    correct_upper = correct.upper()
    correct_text = options.get(correct, options.get(correct_upper, ""))
    qlow = _normalize(question)
    course_name = COURSE_THEORY.get(course_id, "Computer Science")

    topic_theory = detect_topic_theory(question, correct_text)

    if topic_theory:
        correct_exp = (
            f"{topic_theory} "
            f"The answer '{correct_text}' correctly identifies this principle as defined in {course_name} theory and MoE exit exam materials."
        )
    elif code:
        lang = code.get("language", "text")
        lang_theory = CODE_OUTPUT_THEORY.get(lang, CODE_OUTPUT_THEORY.get("java", ""))
        correct_exp = (
            f"{lang_theory} "
            f"Applying these language-theoretic rules to the given construct, the output '{correct_text}' follows from the formal semantics of {lang.upper()} operators and control structures."
        )
    else:
        correct_exp = (
            f"In {course_name}, '{correct_text}' represents the established theoretical definition that satisfies the concept tested. "
            f"It aligns with the formal properties, terminology, and models taught in the Ethiopian MoE CS exit exam blueprint for this topic area."
        )

    incorrect: dict[str, str] = {}
    for letter, text in options.items():
        if letter.upper() == correct_upper:
            continue
        opt_theory = theory_for_option(text, course_id)
        incorrect[letter.upper()] = (
            f"'{text}' corresponds to {opt_theory}. "
            f"While this is a valid concept in {course_name}, it addresses a different theoretical aspect than the one the question examines."
        )

    mistake = _common_mistake(qlow, course_id)
    return {"correct": correct_exp, "incorrect": incorrect, "commonMistake": mistake}


def _common_mistake(qlow: str, course_id: str) -> str:
    if any(k in qlow for k in ["normal form", "normalization", "bcnf"]):
        return "Confusing normal forms (1NF through BCNF) and their dependency rules is a frequent theoretical error on exit exams."
    if any(k in qlow for k in ["tcp", "udp", "osi", "port"]):
        return "Mixing protocol layers and transport semantics (connection-oriented vs connectionless) is a common theoretical confusion."
    if any(k in qlow for k in ["complexity", "o(", "time complexity", "space complexity"]):
        return "Confusing worst-case, average-case, and amortized complexity classes leads to incorrect algorithmic analysis."
    if any(k in qlow for k in ["p and np", "np-complete", "undecidable", "halting"]):
        return "Confusing decidable, undecidable, NP, and NP-complete complexity classes is a classic automata theory pitfall."
    if any(k in qlow for k in ["inheritance", "polymorphism", "encapsulation", "abstract"]):
        return "Confusing OOP pillars (encapsulation, inheritance, polymorphism) and SOLID principles is common in OOP theory questions."
    if any(k in qlow for k in ["supervised", "unsupervised", "classification", "regression"]):
        return "Confusing supervised, unsupervised, and reinforcement learning paradigms is a frequent AI theory mistake."
    if any(k in qlow for k in ["deadlock", "semaphore", "mutex", "scheduling"]):
        return "Confusing synchronization primitives, deadlock conditions, and scheduling policies is common in OS theory."
    return f"Students often select familiar terminology without matching the precise theoretical definition required in {COURSE_THEORY.get(course_id, 'CS')} exams."
