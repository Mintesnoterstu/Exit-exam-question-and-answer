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
    (["what is virtual memory", "virtual memory"],
     "Virtual memory is a memory-management abstraction that gives each process a large private virtual address space independent of physical RAM size. The OS maps virtual pages to physical frames using paging; pages not in RAM reside on disk (swap space or paging file). The Memory Management Unit (MMU) translates virtual addresses, and a page fault loads the required page from secondary storage into a physical frame."),
    (["paging", "page fault", "page table"],
     "Paging divides physical memory into fixed-size frames and logical memory into pages. The page table maps virtual pages to frames, enabling demand paging and reducing external fragmentation."),
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
    # --- Extended coverage for full 500-question bank ---
    (["integration testing", "interaction between different components"],
     "Integration testing theory validates interfaces and data flow between modules or subsystems after unit testing, following the testing pyramid and V-model verification stages."),
    (["unit testing", "individual components"],
     "Unit testing isolates the smallest testable units (functions, classes) to verify correctness against specifications — the foundation of bottom-up verification."),
    (["regression testing", "retesting modified"],
     "Regression testing theory ensures that changes do not reintroduce defects by re-executing test cases affected by modifications."),
    (["acceptance testing", "customer requirements"],
     "Acceptance testing validates the system against user requirements and business criteria — the final validation before deployment."),
    (["black-box testing", "without knowing internal"],
     "Black-box (specification-based) testing derives test cases from functional requirements without knowledge of internal structure."),
    (["white-box testing", "internal code structure"],
     "White-box (structural) testing uses knowledge of internal logic, paths, and branches to achieve coverage criteria."),
    (["singleton pattern", "only one instance"],
     "The Singleton creational pattern restricts instantiation to a single object, providing global access point — used for shared resources like configuration managers."),
    (["factory pattern", "abstract factory"],
     "Factory patterns (Factory Method, Abstract Factory) encapsulate object creation, decoupling client code from concrete class dependencies."),
    (["observer pattern", "one-to-many dependency"],
     "The Observer behavioral pattern defines a publish-subscribe relationship where dependents are notified of state changes in a subject."),
    (["open-closed principle", "open-closed"],
     "The Open-Closed Principle states software entities should be open for extension but closed for modification — enabling polymorphic extension."),
    (["liskov substitution", "liskov"],
     "The Liskov Substitution Principle requires subtypes to be substitutable for base types without altering program correctness."),
    (["dependency inversion", "depend on abstractions"],
     "The Dependency Inversion Principle directs high-level modules to depend on abstractions, not concrete implementations — enabling loose coupling."),
    (["srs", "software requirements specification", "characteristic of a good srs"],
     "An SRS (Software Requirements Specification) must be complete, consistent, unambiguous, verifiable, and modifiable per IEEE 830 / software requirements engineering standards."),
    (["non-functional requirement", "respond within"],
     "Non-functional requirements specify quality attributes (performance, security, usability, reliability) rather than specific system behaviors."),
    (["denormalization", "adding redundancy"],
     "Denormalization intentionally introduces controlled redundancy to optimize read performance, trading normalization purity for query efficiency."),
    (["optimistic concurrency", "conflicts detected at commit"],
     "Optimistic concurrency control assumes conflicts are rare, validating transactions at commit time rather than holding locks during execution."),
    (["phantom read", "new rows appearing"],
     "A phantom read occurs when a transaction re-executes a query and finds new rows inserted by another transaction — prevented by SERIALIZABLE isolation."),
    (["write-ahead log", "wal"],
     "Write-Ahead Logging (WAL) requires log records to reach stable storage before dirty pages — the theoretical basis for crash recovery."),
    (["materialized view", "stores the query results physically"],
     "A materialized view persists query results physically, trading storage for pre-computed retrieval speed."),
    (["window function", "across a set of rows"],
     "SQL window functions perform aggregate calculations over a defined window of rows without collapsing result groups like GROUP BY."),
    (["json", "javascript object notation"],
     "JSON (JavaScript Object Notation) is a lightweight text format for data interchange based on object and array literal syntax."),
    (["dom", "document object model"],
     "The DOM is a W3C standard tree API representing HTML/XML documents, enabling programmatic access and dynamic modification."),
    (["php", "hypertext preprocessor"],
     "PHP is a server-side scripting language designed for web development with embedded HTML and request-based execution model."),
    (["rest", "idempotency", "microservices"],
     "REST architectural constraints include statelessness, uniform interface, and idempotent GET/PUT/DELETE semantics; microservices decompose monoliths into independently deployable services."),
    (["devops", "continuous integration"],
     "DevOps integrates development and operations through CI/CD pipelines, automating build, test, and deployment for rapid delivery."),
    (["spiral model", "risk analysis"],
     "The Spiral model combines iterative development with systematic risk analysis at each cycle — a hybrid of waterfall and prototyping."),
    (["candidate key", "surrogate key", "composite key"],
     "Key theory: candidate keys are minimal unique identifiers; surrogate keys are artificial system-generated keys; composite keys combine multiple attributes."),
    (["cross join", "cartesian product"],
     "A CROSS JOIN computes the Cartesian product of two relations — every combination of rows from both tables."),
    (["self-join", "joining a table with itself"],
     "A self-join joins a relation to itself using aliases to express hierarchical or comparative relationships within one table."),
    (["group by", "having clause"],
     "GROUP BY partitions tuples into groups for aggregation; HAVING filters groups post-aggregation (unlike WHERE which filters rows pre-aggregation)."),
    (["distinct", "unique values"],
     "DISTINCT implements duplicate elimination in relational projection, returning unique tuple values."),
    (["authentication", "authorization"],
     "Authentication verifies identity; authorization determines permitted actions — distinct pillars of access control theory (AAA: Authentication, Authorization, Accounting)."),
    (["multi-factor", "mfa", "two or more verification"],
     "Multi-Factor Authentication combines categories of evidence (knowledge, possession, inherence) to strengthen identity assurance."),
    (["subnet", "cidr", "class c", "class a", "class b"],
     "IP addressing theory uses CIDR notation to define network/host boundaries; private ranges (10/8, 172.16/12, 192.168/16) enable NAT-based internal networks."),
    (["bgp", "exterior gateway"],
     "BGP (Border Gateway Protocol) is the path-vector EGP routing protocol for inter-autonomous-system routing on the Internet."),
    (["ospf", "link-state"],
     "OSPF is a link-state IGP using Dijkstra's SPF algorithm to compute shortest paths within an autonomous system."),
    (["rip", "hop count"],
     "RIP is a distance-vector IGP using hop count as metric with a maximum of 15 hops to prevent count-to-infinity."),
    (["vlan", "802.1q"],
     "VLANs logically segment broadcast domains; IEEE 802.1Q defines frame tagging for trunk links carrying multiple VLANs."),
    (["spanning tree", "rstp", "stp"],
     "Spanning Tree Protocol (STP/RSTP) prevents Layer-2 loops by creating a loop-free logical topology via bridge protocol data units."),
    (["do-while", "at least once"],
     "The do-while loop is a post-test iteration construct guaranteed to execute its body at least once before condition evaluation."),
    (["recursion", "base case", "recursive case"],
     "Recursion theory defines functions in terms of themselves with a base case terminating the recurrence and recursive cases reducing problem size."),
    (["tail recursion", "last operation"],
     "Tail recursion places the recursive call as the final operation, enabling compiler optimization to iterative form without stack growth."),
    (["avl", "red-black", "self-balancing"],
     "Self-balancing BSTs (AVL, Red-Black) maintain O(log n) height through rotation invariants, guaranteeing logarithmic search/insert/delete."),
    (["heap sort", "binary heap", "priority queue"],
     "Binary heaps are complete trees satisfying the heap property; they implement priority queues and enable O(n log n) heap sort."),
    (["kruskal", "prim", "minimum spanning tree"],
     "MST algorithms (Kruskal's greedy edge selection, Prim's vertex growth) find minimum-weight spanning trees in connected graphs."),
    (["floyd-warshall", "all pairs"],
     "Floyd-Warshall uses dynamic programming on adjacency matrices to compute all-pairs shortest paths in O(V³)."),
    (["huffman", "prefix codes"],
     "Huffman's greedy algorithm constructs optimal prefix-free binary codes minimizing expected codeword length for data compression."),
    (["knapsack", "dynamic programming"],
     "The 0/1 knapsack exhibits optimal substructure solvable by DP in O(nW) — a canonical optimization problem in algorithm theory."),
    (["ford-fulkerson", "maximum flow", "edmonds-karp"],
     "Max-flow algorithms (Ford-Fulkerson, Edmonds-Karp) compute maximum network flow subject to capacity constraints using augmenting paths."),
    (["kosaraju", "tarjan", "strongly connected"],
     "SCC algorithms (Kosaraju's two-pass DFS, Tarjan's single DFS with low-link) identify maximal strongly connected subgraphs in directed graphs."),
    (["logistic regression", "classification algorithm"],
     "Logistic regression models class probability using the sigmoid function — a linear classifier despite its name."),
    (["k-means", "clustering algorithm"],
     "K-means partitions data into k clusters by minimizing within-cluster variance — a centroid-based unsupervised method."),
    (["random forest", "ensemble", "bagging", "boosting"],
     "Ensemble learning combines multiple models: bagging (parallel, variance reduction) and boosting (sequential, bias reduction) improve generalization."),
    (["relu", "sigmoid", "activation function"],
     "Activation functions introduce non-linearity in neural networks; ReLU, Sigmoid, and Tanh define different gradient and saturation behaviors."),
    (["lstm", "gru", "vanishing gradient"],
     "LSTM/GRU architectures use gating mechanisms to preserve long-range dependencies and mitigate vanishing gradients in recurrent networks."),
    (["bert", "gpt", "bidirectional"],
     "BERT uses bidirectional transformer encoding; GPT uses unidirectional autoregressive language modeling — different pre-training objectives."),
    (["precision", "recall", "f1 score", "roc", "auc"],
     "Classification metrics theory: Precision = TP/(TP+FP), Recall = TP/(TP+FN), F1 harmonizes both; ROC plots TPR vs FPR; AUC measures ranking quality."),
    (["banker's algorithm", "deadlock avoidance"],
     "Banker's algorithm avoids deadlock by ensuring the system remains in a safe state before granting resource requests."),
    (["round robin", "time slice", "preemptive"],
     "Round Robin scheduling allocates CPU in fixed time quanta cyclically — fair preemptive scheduling for time-sharing systems."),
    (["fcfs", "first come", "non-preemptive"],
     "FCFS (First-Come First-Served) is non-preemptive scheduling serving processes in arrival order."),
    (["belady", "anomaly", "page replacement"],
     "Belady's anomaly demonstrates that increasing frame allocation can increase page faults for FIFO — not possible for stack algorithms like LRU."),
    (["harvard", "separate instruction"],
     "Harvard architecture uses separate memory buses for instructions and data, enabling simultaneous fetch — common in DSPs and microcontrollers."),
    (["mesi", "write-through", "write-back"],
     "Cache write policies: write-through updates memory immediately; write-back defers memory update until block eviction."),
    (["lexical analysis", "token", "syntax analysis", "parse tree"],
     "Compilation phases: lexical analysis tokenizes source; syntax analysis builds parse trees from context-free grammars."),
    (["semantic analysis", "type checking"],
     "Semantic analysis validates type compatibility, scope rules, and language constraints beyond syntactic correctness."),
    (["lr parser", "ll parser", "top-down", "bottom-up"],
     "LL parsers are top-down predictive; LR parsers are bottom-up shift-reduce — LR handles more grammars."),
    (["left recursion", "left factoring"],
     "Grammar transformations: eliminating left recursion and left factoring prepare context-free grammars for top-down parsing."),
    (["cook-levin", "sat", "np-complete"],
     "The Cook-Levin theorem proves Boolean SAT is NP-complete — the foundation for NP-completeness theory."),
    (["pumping lemma", "not regular", "not context-free"],
     "Pumping lemmas prove languages are not in a class by showing strings cannot be pumped while remaining in the language."),
    (["myhill-nerode", "equivalence classes"],
     "The Myhill-Nerode theorem characterizes regular languages via finitely many right-equivalence classes of strings."),
    (["interpreter", "translates line by line"],
     "An interpreter executes source code directly without prior full translation; a compiler translates the entire program to machine code beforehand."),
    (["three-address code", "intermediate code", "ssa"],
     "Intermediate representations (three-address code, SSA form) bridge source and target languages, enabling machine-independent optimization."),
    (["constant folding", "dead code elimination", "loop unrolling"],
     "Compiler optimizations: constant folding evaluates at compile time; DCE removes unreachable code; loop unrolling reduces branch overhead."),
]

# What common distractor options theoretically represent (for wrong-answer explanations)
OPTION_CONCEPT_HINTS: dict[str, str] = {
    "design": "the SDLC Design phase, where system architecture and specifications are created after requirements are known",
    "implementation": "the Implementation/Coding phase where designs are translated into executable code",
    "testing": "the Testing/Verification phase focused on validating behavior against requirements",
    "maintenance": "the Maintenance phase addressing post-deployment changes and enhancements",
    "waterfall": "the sequential Waterfall lifecycle model with phase-gate progression",
    "v-model": "the V-Model that pairs each development phase with a corresponding testing phase",
    "insert": "the SQL INSERT operator for adding tuples to relations",
    "delete": "the SQL DELETE operator for removing tuples",
    "alter": "the SQL ALTER statement for modifying schema structure",
    "drop": "the SQL DROP statement for removing schema objects",
    "udp": "UDP, a connectionless transport protocol without reliability guarantees",
    "tcp": "TCP, a connection-oriented reliable transport protocol",
    "ftp": "FTP (File Transfer Protocol) for file transfer at the application layer",
    "smtp": "SMTP (Simple Mail Transfer Protocol) for email transmission",
    "pop3": "POP3 for retrieving email from a mail server",
    "icmp": "ICMP for network diagnostic and error messages at the network layer",
    "arp": "ARP for resolving IP addresses to MAC addresses on local networks",
    "stack": "the Stack ADT with LIFO access semantics",
    "queue": "the Queue ADT with FIFO access semantics",
    "deque": "the Double-Ended Queue allowing insertion/removal at both ends",
    "array": "the Array structure providing O(1) indexed random access",
    "linked list": "the Linked List structure with dynamic node-based storage",
    "linear search": "linear (sequential) search with O(n) worst-case complexity",
    "binary search": "binary search requiring sorted input with O(log n) complexity",
    "bubble sort": "Bubble sort, a simple O(n²) comparison sort",
    "merge sort": "Merge sort, an O(n log n) divide-and-conquer sort",
    "quick sort": "Quick sort, a partition-based sort with O(n log n) average case",
    "selection sort": "Selection sort, an O(n²) comparison sort selecting minimum elements",
    "heap sort": "Heap sort using binary heap structure with O(n log n) complexity",
    "aes": "AES symmetric block cipher encryption",
    "rsa": "RSA asymmetric public-key cryptography",
    "des": "DES, a legacy symmetric block cipher",
    "sha-256": "SHA-256 cryptographic hash function",
    "md5": "MD5, a deprecated hash function with known collision weaknesses",
    "1nf": "First Normal Form — atomic values and no repeating groups",
    "2nf": "Second Normal Form — no partial key dependencies",
    "3nf": "Third Normal Form — no transitive dependencies",
    "bcnf": "Boyce-Codd Normal Form — every determinant is a candidate key",
    "unit testing": "Unit testing verifying individual modules in isolation",
    "system testing": "System testing validating the complete integrated system",
    "integration testing": "Integration testing verifying inter-module interfaces",
    "acceptance testing": "Acceptance testing validating against user/business requirements",
    "hub": "a network hub operating at Layer 1, broadcasting to all ports",
    "switch": "a network switch operating at Layer 2, forwarding based on MAC addresses",
    "router": "a router operating at Layer 3, forwarding based on IP addresses",
    "bridge": "a bridge connecting network segments at the data link layer",
    "gateway": "a gateway connecting networks with different protocols",
    "for loop": "the for loop, a definite iteration control structure",
    "while loop": "the while loop, a pre-test indefinite iteration construct",
    "do-while": "the do-while loop, a post-test iteration construct",
    "constructor": "a constructor method for object initialization",
    "destructor": "a destructor method for resource cleanup in C++",
    "abstract class": "an abstract class that cannot be instantiated directly",
    "interface": "an interface defining a contract of abstract methods",
    "inheritance": "inheritance enabling IS-A relationships between classes",
    "compilation": "the compilation process — not an OOP pillar",
    "remember": "the Remember level in Bloom's taxonomy — not applicable here",
    "malware": "malicious software including viruses, worms, and trojans",
    "firewall": "a network security device filtering traffic by policy rules",
    "phishing": "a social engineering attack via deceptive messages",
    "trojan": "a Trojan horse malware disguised as legitimate software",
    "worm": "a self-replicating malware spreading across networks",
    "vpn": "Virtual Private Network providing encrypted tunneling",
    "lan": "Local Area Network covering a limited geographic area",
    "wan": "Wide Area Network spanning large geographic distances",
    "ram": "Random Access Memory — volatile primary storage",
    "rom": "Read-Only Memory — non-volatile storage",
    "cpu": "Central Processing Unit executing instructions",
    "alu": "Arithmetic Logic Unit performing computations",
    "cache": "cache memory exploiting locality for faster access",
    "virtual memory": "virtual memory extending address space via paging",
    "page fault": "a page fault when a referenced page is not in physical memory",
    "mutex": "a mutex providing binary mutual exclusion",
    "semaphore": "a semaphore for counting-based synchronization",
    "round robin": "Round Robin CPU scheduling with time quanta",
    "fcfs": "First-Come First-Served non-preemptive scheduling",
    "dfa": "Deterministic Finite Automaton with unique transitions",
    "nfa": "Non-deterministic Finite Automaton allowing multiple transitions",
    "pda": "Pushdown Automaton with stack for context-free languages",
    "turing machine": "Turing Machine — the universal model of computation",
    "halting problem": "the Halting Problem — proven undecidable",
    "sat": "Boolean Satisfiability — the first proven NP-complete problem",
    "linear regression": "Linear regression for continuous value prediction",
    "logistic regression": "Logistic regression for binary classification",
    "k-means": "K-means clustering algorithm",
    "knn": "K-Nearest Neighbors instance-based learning",
    "svm": "Support Vector Machine with maximum-margin classification",
    "decision tree": "Decision tree model using hierarchical splits",
    "random forest": "Random Forest ensemble of decision trees",
    "relu": "ReLU activation function f(x)=max(0,x)",
    "sigmoid": "Sigmoid activation squashing output to (0,1)",
    "backpropagation": "Backpropagation for gradient computation in neural networks",
    "supervised learning": "Supervised learning with labeled training data",
    "unsupervised learning": "Unsupervised learning without labels",
    "reinforcement learning": "Reinforcement learning via reward signals",
    "overfitting": "Overfitting — poor generalization to unseen data",
    "underfitting": "Underfitting — model too simple to capture patterns",
    "precision": "Precision — positive predictive value in classification",
    "recall": "Recall — sensitivity / true positive rate",
    "compiler": "a compiler translating source to machine code",
    "interpreter": "an interpreter executing source line-by-line",
    "lexical analysis": "lexical analysis producing token streams",
    "syntax analysis": "syntax analysis building parse trees",
    "semantic analysis": "semantic analysis for type and scope checking",
    "token": "a token — the output unit of lexical analysis",
    "parse tree": "a parse tree representing syntactic structure",
    "21": "port 21, assigned to FTP (File Transfer Protocol)",
    "22": "port 22, assigned to SSH (Secure Shell)",
    "23": "port 23, assigned to Telnet",
    "25": "port 25, assigned to SMTP",
    "53": "port 53, assigned to DNS",
    "80": "port 80, the well-known port for HTTP",
    "443": "port 443, the well-known port for HTTPS",
    "3306": "port 3306, the default port for MySQL",
    "8080": "port 8080, commonly used as an alternate HTTP port",
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
    best: tuple[int, str] | None = None
    for keywords, theory in CONCEPT_THEORY:
        for kw in keywords:
            if kw in combined:
                if best is None or len(kw) > best[0]:
                    best = (len(kw), theory)
    return best[1] if best else None


def theory_for_option(option_text: str, course_id: str) -> str:
    low = _normalize(option_text)
    for hint_key in sorted(OPTION_CONCEPT_HINTS, key=len, reverse=True):
        if hint_key in low or low == hint_key:
            return OPTION_CONCEPT_HINTS[hint_key]
    for keywords, theory in CONCEPT_THEORY:
        if any(kw in low for kw in keywords):
            return theory
    course = COURSE_THEORY.get(course_id, "Computer Science")
    if len(low) <= 80:
        return f"the CS concept or term '{option_text}' as defined in {course} literature"
    return "a different theoretical interpretation than the one required by the question"


def _infer_correct_theory(question: str, correct_text: str, course_name: str, qlow: str) -> str:
    """Theoretical fallback when no keyword rule matches — still concept-based, not procedural."""
    if "stand for" in qlow or "stands for" in qlow:
        return (
            f"In {course_name}, '{correct_text}' is the standard acronym or formal expansion of the term "
            f"referenced in the question, as defined in textbook and MoE curriculum terminology."
        )
    if "purpose of" in qlow or "what is the purpose" in qlow:
        return (
            f"The theoretical purpose described by '{correct_text}' reflects the intended role of the mechanism "
            f"within {course_name} — how it contributes to system correctness, performance, or maintainability."
        )
    if "difference between" in qlow or "what is the difference" in qlow:
        return (
            f"'{correct_text}' correctly states the distinguishing theoretical property between the compared concepts "
            f"in {course_name} — the definition that separates one model, protocol, or structure from another."
        )
    if "time complexity" in qlow or "space complexity" in qlow or "o(" in qlow:
        return (
            f"'{correct_text}' expresses the asymptotic complexity class (Big-O notation) derived from algorithm analysis "
            f"theory — describing how resource usage grows with input size n."
        )
    if "which phase" in qlow or "sdlc" in qlow:
        return (
            f"'{correct_text}' identifies the SDLC phase whose theoretical activities and deliverables match "
            f"the process described in software engineering lifecycle models."
        )
    if "design pattern" in qlow:
        return (
            f"'{correct_text}' is the Gang-of-Four design pattern whose theoretical intent solves "
            f"the creational, structural, or behavioral problem described in the question."
        )
    if "which of the following is true" in qlow or "which of the following is a" in qlow:
        return (
            f"'{correct_text}' is the statement that holds under the formal definitions, properties, and theorems "
            f"of {course_name} — consistent with established CS theory rather than common misconceptions."
        )
    if "which protocol" in qlow or "which port" in qlow:
        return (
            f"'{correct_text}' is the protocol or port assignment defined by IANA standards and network architecture "
            f"theory for the service or layer described in the question."
        )
    if "which algorithm" in qlow:
        return (
            f"'{correct_text}' is the algorithm whose theoretical properties (correctness, complexity, prerequisites) "
            f"match the problem constraints stated in the question."
        )
    if "which data structure" in qlow or "which structure" in qlow:
        return (
            f"'{correct_text}' is the abstract data type whose access patterns (LIFO, FIFO, O(1) index, etc.) "
            f"theoretically fit the operations and constraints described."
        )
    if "which automaton" in qlow or "which grammar" in qlow:
        return (
            f"'{correct_text}' is the automaton or grammar class from the Chomsky hierarchy with the generative "
            f"power required to recognize or generate the language family in question."
        )
    if "what is a" in qlow or "what is an" in qlow or "what is the" in qlow:
        return (
            f"'{correct_text}' is the canonical theoretical definition of the concept named in the question "
            f"within {course_name}."
        )
    return (
        f"In {course_name}, '{correct_text}' expresses the formal definition, property, "
        f"or theoretical model that the question is assessing."
    )


# Question-specific theoretical explanations for common wrong answers
QUESTION_WRONG_THEORY: list[tuple[list[str], dict[str, str]]] = [
    (["virtual memory"], {
        "using ram as an extension of disk": "This reverses the memory hierarchy: virtual memory theory defines disk as backing store for RAM (primary memory), not RAM extending disk.",
        "using cache as ram": "Cache is a small, fast memory level in the hierarchy (between CPU and RAM) for locality — not a substitute for extending virtual address space beyond physical RAM.",
        "using rom as ram": "ROM is non-volatile, read-only firmware storage and cannot serve as an extension of volatile RAM in virtual memory systems.",
    }),
    (["swapping in memory", "what is swapping"], {
        "moving data between cache and memory": "Cache-memory transfers are part of the memory hierarchy for speed, not process-level swapping between main memory and disk.",
        "moving data between registers and cache": "Register-cache movement is CPU microarchitecture — unrelated to swapping entire process address spaces.",
        "moving data between disks": "Swapping moves process images between RAM and disk, not between disk drives.",
    }),
    (["thrashing"], {
        "excessive process creation": "Process creation is a scheduling/resource issue, not the paging phenomenon where constant page faults dominate CPU time.",
        "excessive i/o operations": "Thrashing is specifically caused by excessive paging due to insufficient frames, not general I/O load.",
        "excessive context switching": "Context switching is related but thrashing is defined by page fault rate exceeding useful computation.",
    }),
    (["deadlock"], {
        "a process waiting indefinitely for a resource": "Indefinite waiting describes starvation or blocking — deadlock requires a circular wait among multiple processes holding resources.",
        "a process that crashes": "A crash is abnormal termination, not the circular resource dependency that defines deadlock.",
        "a process that consumes too much cpu": "High CPU usage is not deadlock; deadlock is a state where processes are blocked waiting on each other.",
    }),
]


def _explain_wrong_option(question: str, wrong_text: str, course_id: str) -> str:
    qlow = _normalize(question)
    wrong_low = _normalize(wrong_text)
    for keywords, wrong_map in QUESTION_WRONG_THEORY:
        if any(kw in qlow for kw in keywords):
            for pattern, explanation in wrong_map.items():
                if pattern in wrong_low:
                    return explanation
    opt_theory = theory_for_option(wrong_text, course_id)
    return f"Theoretically, this describes {opt_theory}, which is a different concept from the one the question defines."


def _question_focus(qlow: str) -> str:
    if "testing" in qlow:
        return "software testing and verification theory"
    if "join" in qlow or "sql" in qlow or "database" in qlow or "normal" in qlow:
        return "relational database theory"
    if "protocol" in qlow or "network" in qlow or "tcp" in qlow or "osi" in qlow:
        return "network protocol and architecture theory"
    if "security" in qlow or "encrypt" in qlow or "attack" in qlow:
        return "information security theory"
    if "algorithm" in qlow or "complexity" in qlow or "sort" in qlow:
        return "algorithm analysis theory"
    if "process" in qlow or "thread" in qlow or "memory" in qlow or "scheduling" in qlow:
        return "operating systems theory"
    if "compiler" in qlow or "grammar" in qlow or "automaton" in qlow:
        return "formal languages and compiler theory"
    if "machine learning" in qlow or "neural" in qlow or "classification" in qlow:
        return "machine learning and AI theory"
    return "the concept domain of this question"


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
    focus = _question_focus(qlow)

    topic_theory = detect_topic_theory(question, correct_text)

    if topic_theory:
        correct_exp = topic_theory
    elif code:
        lang = code.get("language", "text")
        lang_theory = CODE_OUTPUT_THEORY.get(lang, CODE_OUTPUT_THEORY.get("java", ""))
        correct_exp = (
            f"{lang_theory} "
            f"By the formal semantics of {lang.upper()}, the evaluated result is '{correct_text}'."
        )
    else:
        correct_exp = _infer_correct_theory(question, correct_text, course_name, qlow)

    incorrect: dict[str, str] = {}
    for letter, text in options.items():
        if letter.upper() == correct_upper:
            continue
        incorrect[letter.upper()] = _explain_wrong_option(question, text, course_id)

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
