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
    # SQL and DBMS fundamentals
    (["where clause", "filter records", "used to filter"],
     "The WHERE clause implements relational selection (σ), filtering tuples that satisfy a Boolean predicate before GROUP BY aggregation or ORDER BY sorting."),
    (["order by", "sort results", "used to sort"],
     "ORDER BY specifies sort order on result columns after selection and projection — it does not filter rows (WHERE) or group them (GROUP BY)."),
    (["group by", "filter records"],
     "GROUP BY partitions rows for aggregate functions; it does not filter individual rows — that is the role of WHERE."),
    (["what does sql stand", "sql stand for", "structured query language"],
     "SQL (Structured Query Language) is the standard declarative language for defining, querying, and manipulating relational databases under the relational model."),
    (["count the number of rows", "count()", "sql function is used to count"],
     "COUNT() is the SQL aggregate function returning the number of rows (or non-NULL values) in a group — distinct from SUM(), which totals numeric columns."),
    (["sum()", "sql function"],
     "SUM() is an SQL aggregate computing the arithmetic total of numeric values in a column — not row cardinality."),
    (["transaction in dbms", "logical unit of work"],
     "A transaction is a logical unit of work satisfying ACID properties — a sequence of operations treated atomically as all-or-nothing."),
    (["dirty read", "read committed", "isolation level prevents"],
     "READ COMMITTED isolation prevents dirty reads by allowing reads only of committed data; READ UNCOMMITTED permits uncommitted writes to be visible."),
    (["read uncommitted"],
     "READ UNCOMMITTED is the weakest isolation level, allowing dirty reads — transactions may see uncommitted changes from others."),
    (["serializable"],
     "SERIALIZABLE is the strictest isolation level, equivalent to serial execution — preventing dirty reads, non-repeatable reads, and phantoms."),
    (["varchar", "char(", "fixed-length", "variable-length"],
     "CHAR(n) stores fixed-length padded strings; VARCHAR(n) stores variable-length strings up to n characters — a schema design distinction in relational storage."),
    (["checkpoint in database", "checkpoint"],
     "A checkpoint is a recovery mechanism that writes dirty pages and log records to stable storage, reducing redo work after a crash."),
    (["delete a table", "drop table", "remove a table"],
     "DROP TABLE is DDL that removes the table definition and data from the catalog; DELETE removes rows but preserves schema."),
    (["create a database", "create database"],
     "CREATE DATABASE is a DDL statement establishing a new database namespace with its own schema catalog."),
    (["rollback command", "purpose of the `rollback`", "purpose of rollback"],
     "ROLLBACK terminates a transaction and undoes all its uncommitted changes, restoring the database to the state before BEGIN."),
    (["commit command", "purpose of the `commit`", "purpose of commit"],
     "COMMIT makes all changes in the current transaction permanent and visible to other transactions — the durability boundary."),
    (["data dictionary"],
     "The data dictionary (system catalog) stores metadata — table definitions, constraints, users, and privileges — managed by the DBMS."),
    (["current date", "curdate", "now()"],
     "SQL date/time functions (CURDATE(), NOW(), CURRENT_TIMESTAMP) return the system date or timestamp for queries and defaults."),
    (["delete` and `truncate", "difference between `delete` and `truncate"],
     "DELETE is DML removing rows one-by-one with optional WHERE and trigger firing; TRUNCATE is DDL deallocating all rows quickly without row-level logging."),
    (["add a column", "alter table"],
     "ALTER TABLE ADD COLUMN modifies schema by introducing a new attribute with specified type and constraints."),
    (["remove a column"],
     "ALTER TABLE DROP COLUMN removes an attribute from a relation's schema definition."),
    (["savepoint"],
     "A savepoint is a named marker within a transaction enabling partial ROLLBACK to that point without aborting the entire transaction."),
    (["transaction log"],
     "The transaction log (redo/undo log) records every change for crash recovery and replication — the foundation of WAL protocols."),
    (["stored function"],
     "A stored function is a named procedural object in the DBMS that accepts parameters and returns a computed value, callable from SQL."),
    (["purpose of the `union`", "union operator"],
     "UNION combines result sets of compatible SELECT queries, eliminating duplicates (UNION ALL retains them) — set union in relational algebra."),
    (["distributed database", "centralized database"],
     "A distributed database spans multiple sites with data fragmentation or replication; a centralized database resides on a single server node."),
    (["two-phase commit", "2pc"],
     "Two-Phase Commit (2PC) is a distributed transaction protocol ensuring all nodes commit or abort atomically across a network."),
    (["recovery technique uses a log", "undo incomplete"],
     "Log-based recovery uses undo (rollback uncommitted) and redo (replay committed) operations guided by checkpoint and LSN ordering."),
    # Programming languages
    (["valid c++ identifier", "valid identifier"],
     "C++ identifiers must start with a letter or underscore and contain alphanumeric characters — keywords and leading digits are invalid."),
    (["cout <<", "output of `cout"],
     "C++ stream insertion (cout <<) outputs expressions; boolean expressions print 1/0 or true/false depending on compiler settings; relational operators yield bool."),
    (["define a class in java", "class in java"],
     "The `class` keyword declares a reference type encapsulating fields and methods — the fundamental unit of OOP in Java."),
    (["public static void main", "main method"],
     "The main method is the JVM entry point: `public static void main(String[] args)` — public for JVM access, static for no instance, void return."),
    (["java identifier"],
     "Java identifiers follow Unicode letter rules, cannot be keywords, and are case-sensitive — distinct from C++ naming with some differences."),
    (["pointer in c++", "nullptr"],
     "C++ pointers hold addresses; nullptr is the typed null pointer constant replacing C's NULL macro for type safety."),
    (["reference in c++", "alias"],
     "A C++ reference is an alias binding to an existing object — must be initialized and cannot be rebound, unlike pointers."),
    (["exception handling", "try catch", "throw"],
     "Exception handling separates normal flow from error paths: try blocks, catch handlers, and throw propagate exceptions up the call stack."),
    (["method overloading", "same name different parameters"],
     "Method overloading resolves calls at compile time by signature (name + parameter types) — distinct from overriding via virtual dispatch."),
    (["method overriding", "virtual", "override"],
     "Method overriding replaces a base-class virtual method in a derived class — resolved at runtime through dynamic dispatch."),
    (["interface in java", "implements"],
     "A Java interface defines abstract method contracts; implementing classes must provide concrete definitions — enabling multiple inheritance of type."),
    (["abstract class"],
     "An abstract class may contain abstract methods (no body) and concrete methods — it cannot be instantiated directly."),
    (["package in java"],
     "Packages namespace classes and control visibility — the Java module system for organizing code and managing imports."),
    (["string in java", "immutable"],
     "Java String objects are immutable — concatenation creates new objects; the String pool caches literals for memory efficiency."),
    (["arraylist", "linkedlist", "java collection"],
     "ArrayList provides O(1) indexed access on dynamic arrays; LinkedList offers O(1) insertion at known nodes — different trade-offs in the Java Collections Framework."),
    # Networking
    (["email transmission", "send email", "protocol is used for email"],
     "SMTP (Simple Mail Transfer Protocol) is the application-layer protocol for sending email between MTAs on port 25."),
    (["what does ip stand", "ip stand for", "internet protocol"],
     "IP (Internet Protocol) is the network-layer protocol providing logical addressing and best-effort datagram delivery across interconnected networks."),
    (["private ip address", "192.168", "10.0", "172.16"],
     "Private IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) are non-routable on the public Internet per RFC 1918, used behind NAT."),
    (["mac address", "physical address"],
     "A MAC address is the 48-bit hardware identifier at the Data Link layer — flat structure unlike hierarchical IP addressing."),
    (["subnet mask", "network address"],
     "A subnet mask defines the network/host boundary in IPv4 addressing — combined with IP via bitwise AND to derive network prefix."),
    (["nat", "network address translation"],
     "NAT maps private internal addresses to public external addresses, conserving IPv4 space and providing basic perimeter isolation."),
    (["ping", "icmp"],
     "Ping uses ICMP Echo Request/Reply to test reachability and measure round-trip time — a network diagnostic at Layer 3."),
    (["telnet", "remote login"],
     "Telnet provides unencrypted remote terminal access on port 23 — superseded by SSH for secure administration."),
    (["ssh", "secure shell"],
     "SSH (Secure Shell) on port 22 provides encrypted remote login, command execution, and secure file transfer (SFTP/SCP)."),
    (["ftp", "file transfer"],
     "FTP (File Transfer Protocol) on port 21 transfers files using separate control and data channels — application-layer service."),
    (["http method", "get request", "post request"],
     "HTTP methods define semantics: GET retrieves resources (safe, idempotent), POST submits data for processing (non-idempotent)."),
    (["cookie", "session management web"],
     "HTTP cookies are client-side stored tokens enabling session state, personalization, and tracking across stateless HTTP requests."),
    (["csrf", "cross-site request"],
     "CSRF exploits authenticated sessions by tricking browsers into submitting forged requests — mitigated by tokens and SameSite cookies."),
    (["man-in-the-middle", "mitm"],
     "A MITM attack intercepts communication between parties — prevented by TLS certificate validation and mutual authentication."),
    (["denial of service", "dos attack"],
     "DoS attacks exhaust resources (bandwidth, CPU, connections) to deny service — DDoS distributes the attack across many sources."),
    (["intrusion detection", "ids"],
     "An IDS monitors network or host activity for suspicious patterns — signature-based or anomaly-based detection of attacks."),
    (["vpn tunnel"],
     "VPN tunneling encapsulates packets in encrypted tunnels over public networks, providing confidentiality and authenticated remote access."),
    # AI / ML
    (["what is artificial intelligence", "artificial intelligence?"],
     "Artificial Intelligence is the field of creating systems that perform tasks requiring human-like intelligence — perception, reasoning, learning, and decision-making."),
    (["classification problem", "example of a classification"],
     "Classification is supervised learning predicting discrete class labels (spam/not spam, disease type) from labeled training features."),
    (["difference between regression and classification", "regression and classification"],
     "Regression predicts continuous numeric outputs; classification predicts discrete categorical labels — both are supervised but differ in output type."),
    (["training set", "test set", "validation set"],
     "Training data fits model parameters; validation tunes hyperparameters; test data provides unbiased generalization evaluation — the holdout principle."),
    (["feature selection", "dimensionality"],
     "Feature selection reduces input dimensionality by retaining informative attributes — combating curse of dimensionality and overfitting."),
    (["gradient descent", "learning rate"],
     "Gradient descent iteratively minimizes loss by moving opposite the gradient; learning rate controls step size — too large diverges, too small slows convergence."),
    (["confusion matrix"],
     "A confusion matrix tabulates TP, TN, FP, FN for classification — the basis for precision, recall, accuracy, and F1 metrics."),
    (["expert system", "knowledge base", "inference engine"],
     "Expert systems encode domain knowledge in rules (knowledge base) and apply inference engines for decision support — early AI paradigm."),
    (["natural language processing", "nlp"],
     "NLP applies computational techniques to human language — tokenization, parsing, semantics, and generation for translation, chatbots, and search."),
    # Computer architecture and OS
    (["purpose of the cpu", "what is the purpose of the cpu"],
     "The CPU fetches, decodes, and executes instructions — coordinating ALU operations, registers, and control signals in the fetch-decode-execute cycle."),
    (["difference between ram and rom", "ram and rom"],
     "RAM is volatile read-write primary memory for active programs; ROM is non-volatile read-only storage for firmware and boot code."),
    (["storage device", "secondary storage", "hard disk", "ssd"],
     "Secondary storage (HDD, SSD, optical) provides non-volatile mass storage with slower access than primary RAM — the persistence layer."),
    (["bus", "system bus", "address bus", "data bus"],
     "Computer buses are shared communication pathways: address bus carries memory locations, data bus transfers words, control bus carries signals."),
    (["interrupt"],
     "Interrupts are hardware or software signals that suspend current execution to service urgent events — enabling I/O and multitasking."),
    (["dma", "direct memory access"],
     "DMA allows I/O devices to transfer data directly to memory without CPU byte-by-byte involvement — reducing processor overhead."),
    (["context switch"],
     "A context switch saves the current process state (registers, PC, page table) and loads another — the OS mechanism for multiprogramming."),
    (["what is swapping", "swapping in memory"],
     "Swapping moves entire process address spaces between main memory and disk when RAM is insufficient — distinct from paging individual pages."),
    (["what is thrashing"],
     "Thrashing occurs when a system spends more time paging than executing — caused by insufficient frames and high degree of multiprogramming."),
    (["banker's algorithm"],
     "Banker's algorithm is deadlock avoidance that simulates resource allocation to ensure the system remains in a safe state."),
    (["producer consumer", "bounded buffer"],
     "The producer-consumer problem models concurrent threads sharing a bounded buffer — solved with semaphores or monitors for synchronization."),
    (["reader writer", "readers-writers"],
     "The readers-writers problem allows multiple concurrent readers or exclusive writers — balancing consistency and concurrency."),
    (["spooling"],
     "Spooling (Simultaneous Peripheral Operations On-Line) buffers I/O jobs on disk — e.g., print spooler decouples process speed from device speed."),
    # Compiler and complexity
    (["symbol table", "purpose of a symbol table"],
     "The symbol table stores identifiers (variables, functions, types) with attributes during compilation — supporting scope resolution and code generation."),
    (["type of grammar", "regular grammar", "context-free grammar", "context-sensitive"],
     "The Chomsky hierarchy classifies grammars: Type-3 regular, Type-2 context-free, Type-1 context-sensitive, Type-0 unrestricted — each with matching automaton power."),
    (["reduction in complexity", "purpose of a reduction"],
     "A reduction transforms problem A to problem B so that solving B solves A — the foundation of NP-completeness proofs."),
    (["ambiguous grammar"],
     "An ambiguous grammar generates some strings with multiple parse trees — undesirable in programming languages requiring unique syntax."),
    (["ll(1)", "lr(1)", "parser generator"],
     "LL(1) parsers are top-down with one token lookahead; LR(1) parsers are bottom-up shift-reduce — LR handles more grammars including left recursion."),
    (["syntax directed translation", "sdt"],
     "Syntax-directed translation attaches semantic actions to grammar productions — computing attributes during parse tree construction."),
    (["code optimization", "peephole optimization"],
     "Code optimization improves generated code for speed or size — local peephole rules, global data-flow analysis, and loop optimizations."),
    (["register allocation"],
     "Register allocation maps variables to finite CPU registers — graph coloring and spilling to memory when registers are exhausted."),
    (["lexeme", "token type"],
     "A lexeme is the character sequence matched by a pattern; the lexer classifies it into a token type (keyword, identifier, literal)."),
    (["follow set", "first set"],
     "FIRST and FOLLOW sets guide predictive parsing — FIRST(α) is terminals starting derivations of α; FOLLOW(A) is terminals after nonterminal A."),
    (["moore machine", "mealy machine"],
     "Moore machines output on states; Mealy machines output on transitions — both are finite-state transducers extending acceptors."),
    (["recursively enumerable", "recognizable"],
     "Recursively enumerable languages are recognized by Turing machines that may not halt on non-members — the most general computable class."),
    (["decidable", "decision problem"],
     "A decision problem is decidable if a Turing machine always halts with yes/no — unlike semi-decidable (recognizable only) problems."),
    (["space complexity", "pspace"],
     "Space complexity measures memory as a function of input size; PSPACE is the class of problems solvable in polynomial space."),
    (["big-o", "asymptotic notation", "theta notation"],
     "Asymptotic notation (O, Ω, Θ) describes growth rates ignoring constants — Big-O is upper bound, Omega is lower, Theta is tight bound."),
    # Software engineering extras
    (["coupling", "cohesion"],
     "Coupling measures inter-module dependency (lower is better); cohesion measures intra-module focus (higher is better) — modular design principles."),
    (["functional requirement", "non-functional"],
     "Functional requirements specify system behaviors; non-functional requirements specify quality attributes like performance, security, and usability."),
    (["gantt chart", "pert chart"],
     "Gantt charts show task timelines on a calendar; PERT charts show task dependencies and critical paths in project scheduling."),
    (["risk management", "risk mitigation"],
     "Risk management identifies, analyzes, and mitigates project threats — probability-impact matrices and contingency planning."),
    (["use case diagram", "uml"],
     "Use case diagrams model actor-system interactions in UML — capturing functional requirements from an external user perspective."),
    (["class diagram", "sequence diagram"],
     "Class diagrams show static structure (classes, associations); sequence diagrams show dynamic message passing over time in UML."),
    (["prototype model", "evolutionary"],
     "Prototyping builds partial systems for user feedback before full development — evolutionary when prototypes become the product."),
    (["incremental model"],
     "The incremental model delivers software in functional slices, each adding features — combining elements of waterfall and iterative development."),
    (["cmmi", "capability maturity"],
     "CMMI defines process maturity levels (Initial through Optimizing) for organizational software process improvement."),
    # Web programming extras
    (["console.log", "javascript method", "write to the console"],
     "console.log() is the JavaScript standard API for writing diagnostic messages to the browser or Node.js developer console — distinct from document.write() (DOM output) or alert() (modal dialogs)."),
    (["ajax", "asynchronous"],
     "AJAX enables asynchronous HTTP requests from JavaScript without full page reload — the foundation of dynamic web applications."),
    (["xml", "extensible markup"],
     "XML is a markup language for structured hierarchical data with custom tags — used in configuration, SOAP, and data interchange."),
    (["session in php", "php session"],
     "PHP sessions store server-side user state keyed by session ID in cookies — enabling login persistence across HTTP requests."),
    (["get vs post", "get and post"],
     "GET appends parameters to URL (visible, cacheable, length-limited); POST sends data in request body (hidden, larger payloads)."),
    (["responsive design", "media query"],
     "Responsive web design adapts layout to screen size using fluid grids, flexible images, and CSS media queries."),
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
    "where": "the SQL WHERE clause for row-level filtering via predicates",
    "having": "the SQL HAVING clause for filtering groups after aggregation",
    "count()": "COUNT(), the SQL aggregate for row cardinality",
    "sum()": "SUM(), the SQL aggregate for numeric totals",
    "avg()": "AVG(), the SQL aggregate for arithmetic mean",
    "max()": "MAX(), the SQL aggregate returning the maximum value",
    "min()": "MIN(), the SQL aggregate returning the minimum value",
    "truncate": "TRUNCATE, DDL that removes all rows without row-level DELETE logging",
    "create table": "CREATE TABLE, DDL defining a new relation schema",
    "create database": "CREATE DATABASE, DDL establishing a new database namespace",
    "read committed": "READ COMMITTED isolation preventing dirty reads",
    "read uncommitted": "READ UNCOMMITTED, the weakest isolation allowing dirty reads",
    "repeatable read": "REPEATABLE READ isolation preventing non-repeatable reads within a transaction",
    "serializable": "SERIALIZABLE, the strictest transaction isolation level",
    "structured query language": "Structured Query Language — the standard relational query language",
    "hypertext markup language": "HTML — markup for web documents, not a database query language",
    "simple mail transfer": "SMTP-related naming — not the SQL expansion",
    "hypertext preprocessor": "PHP — a server-side scripting language, not SQL",
    "logical unit of work": "a transaction — an ACID logical unit of database operations",
    "single sql statement": "a single statement — not the full transactional unit defined by ACID",
    "dirty read": "reading uncommitted data from another transaction",
    "non-repeatable read": "reading different values for the same row within one transaction",
    "phantom read": "new rows appearing in a repeated range query within a transaction",
    "hard disk": "magnetic secondary storage with rotating platters",
    "ssd": "solid-state storage using flash memory — faster than HDD",
    "optical disk": "optical media like CD/DVD for storage",
    "flash memory": "non-volatile EEPROM-based storage used in SSDs and USB drives",
    "register file": "CPU registers — fastest storage in the memory hierarchy",
    "magnetic tape": "sequential archival storage — not primary or secondary random-access memory",
    "classification": "predicting discrete class labels in supervised learning",
    "regression": "predicting continuous numeric values in supervised learning",
    "clustering": "grouping unlabeled data in unsupervised learning",
    "regular grammar": "Type-3 grammar generating regular languages",
    "context-free grammar": "Type-2 grammar generating context-free languages",
    "context-sensitive grammar": "Type-1 grammar with length-non-decreasing productions",
    "unrestricted grammar": "Type-0 grammar with full Turing-machine generative power",
    "document.write()": "document.write() — writes HTML directly to the document stream during page load, not the developer console",
    "console.log()": "console.log() — the standard API for developer console diagnostic output",
    "window.alert()": "window.alert() — displays a modal dialog box, blocking further interaction until dismissed",
    "print()": "print() — not a native JavaScript function; JavaScript uses console.log() for console output",
}

CODE_OUTPUT_THEORY = {
    "java": "In Java language semantics, control-flow constructs (loops, conditionals) and operator precedence govern expression evaluation. Integer arithmetic follows two's complement rules; String concatenation is defined when any operand is of type String.",
    "cpp": "In C++ semantics, operators have defined precedence and associativity. Integer division truncates toward zero. References alias existing objects; pointers hold addresses. Undefined behavior arises when the language standard imposes no requirements.",
    "c": "In C semantics, arithmetic conversions and integer division follow the C standard. Static storage duration persists across calls; automatic variables have function scope.",
}


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())


def _keyword_matches(keyword: str, text: str) -> bool:
    """Match keywords without false positives (e.g. 'rip' inside 'print')."""
    if len(keyword) <= 4:
        pattern = rf"(?:^|[^a-z0-9]){re.escape(keyword)}(?:[^a-z0-9]|$)"
        return bool(re.search(pattern, text))
    return keyword in text


def _first_sentence(text: str) -> str:
    match = re.search(r"^.+?\.(?:\s+|$)", text)
    if match:
        return match.group(0).strip()
    idx = text.find(".")
    return text[: idx + 1] if idx != -1 else text


def detect_topic_theory(question: str, correct_text: str = "") -> str | None:
    combined = _normalize(f"{question} {correct_text}")
    question_only = _normalize(question)
    best: tuple[int, str] | None = None
    for keywords, theory in CONCEPT_THEORY:
        for kw in keywords:
            if _keyword_matches(kw, combined) or _keyword_matches(kw, question_only):
                if best is None or len(kw) > best[0]:
                    best = (len(kw), theory)
    return best[1] if best else None


def theory_for_option(option_text: str, course_id: str) -> str:
    low = _normalize(option_text)
    matched = detect_topic_theory(option_text, option_text)
    if matched:
        return _first_sentence(matched).rstrip(".")
    for hint_key in sorted(OPTION_CONCEPT_HINTS, key=len, reverse=True):
        if hint_key in low or low == hint_key:
            return OPTION_CONCEPT_HINTS[hint_key]
    course = COURSE_THEORY.get(course_id, "Computer Science")
    if len(low) <= 80:
        return f"'{option_text}' — a term from {course} with a distinct definition from the correct answer"
    return f"a related {course} concept that does not satisfy the question's theoretical criterion"


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
            f"within {course_name} — the formal property, mechanism, or model that textbooks and the MoE "
            f"curriculum use to describe this topic."
        )
    return (
        f"In {course_name}, '{correct_text}' expresses the formal definition, property, "
        f"or theoretical model that the question is assessing — the concept tested matches "
        f"established theory rather than a related but distinct idea."
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


def _explain_wrong_option(
    question: str,
    wrong_text: str,
    correct_text: str,
    course_id: str,
    topic_theory: str | None,
) -> str:
    qlow = _normalize(question)
    wrong_low = _normalize(wrong_text)

    for keywords, wrong_map in QUESTION_WRONG_THEORY:
        if any(kw in qlow for kw in keywords):
            for pattern, explanation in wrong_map.items():
                if pattern in wrong_low:
                    return explanation

    if topic_theory is None:
        topic_theory = detect_topic_theory(question, correct_text)

    wrong_theory = detect_topic_theory(wrong_text, wrong_text)
    wrong_desc = theory_for_option(wrong_text, course_id)
    correct_theory = detect_topic_theory(correct_text, correct_text)
    focus = _question_focus(qlow)

    if "output of" in qlow and ("code" in qlow or "following" in qlow):
        return (
            f"By the language's operator precedence, type rules, and control-flow semantics, "
            f"'{wrong_text}' is not the value produced when the given program fragment is evaluated."
        )

    if (
        "extension" in wrong_low
        and "ram" in wrong_low
        and "disk" in wrong_low
        and topic_theory
        and "virtual memory" in _normalize(topic_theory)
        and wrong_low.find("ram") < wrong_low.find("disk")
    ):
        return (
            "This reverses the memory hierarchy: virtual memory theory defines disk as backing store "
            "for RAM (primary memory), not RAM extending disk."
        )

    if topic_theory and wrong_theory and wrong_theory != topic_theory:
        return f"{_first_sentence(wrong_theory)} {_first_sentence(topic_theory)}"

    if topic_theory:
        topic_sent = _first_sentence(topic_theory)
        if wrong_desc.startswith("'"):
            return f"{wrong_desc}. {topic_sent}"
        return f"'{wrong_text}' describes {wrong_desc}. {topic_sent}"

    if correct_theory and wrong_theory and correct_theory != wrong_theory:
        return (
            f"{_first_sentence(wrong_theory)} "
            f"The correct answer follows {_first_sentence(correct_theory).lower()}"
        )

    if correct_theory:
        return (
            f"'{wrong_text}' describes {wrong_desc}, whereas the correct choice reflects "
            f"{_first_sentence(correct_theory).lower()}"
        )

    if "stand for" in qlow or "stands for" in qlow:
        return (
            f"'{wrong_text}' is not the standard acronym expansion for the term in the question — "
            f"it names a different concept in {COURSE_THEORY.get(course_id, 'Computer Science')}."
        )
    if "difference between" in qlow:
        return (
            f"'{wrong_text}' states a property that does not capture the theoretical distinction "
            f"between the compared concepts in {focus}."
        )
    if "which protocol" in qlow or "email" in qlow:
        return (
            f"'{wrong_text}' names a protocol with a different application-layer role — "
            f"not the service defined for the communication task described."
        )
    if "which sql" in qlow or "sql clause" in qlow or "sql function" in qlow or "sql statement" in qlow:
        return (
            f"'{wrong_text}' refers to a different SQL operator — relational algebra assigns "
            f"distinct roles to selection (WHERE), projection, aggregation, and sorting."
        )
    if "which phase" in qlow or "sdlc" in qlow:
        return (
            f"'{wrong_text}' names a different SDLC phase whose deliverables and activities "
            f"do not match the process step described in the question."
        )
    if "which data structure" in qlow or "which structure" in qlow:
        return (
            f"'{wrong_text}' is a different abstract data type whose access semantics "
            f"(LIFO, FIFO, indexed, etc.) do not fit the operations required."
        )
    if "which algorithm" in qlow:
        return (
            f"'{wrong_text}' is a different algorithm whose prerequisites, complexity, "
            f"or problem domain do not match the constraints stated."
        )

    return (
        f"'{wrong_text}' corresponds to {wrong_desc}. "
        f"In {focus}, this option does not satisfy the definition, mechanism, or property "
        f"the question asks you to identify."
    )


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
        incorrect[letter.upper()] = _explain_wrong_option(
            question, text, correct_text, course_id, topic_theory
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
