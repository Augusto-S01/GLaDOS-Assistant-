flowchart TD
    A[Início] --> B[Sound Capture Service]
    B -->|"*'audio.wav'*"| C[QUEUE-MESSAGE-CSG-INPUT]
    C --> D[Comprehension-Service-Glados]
    D -->|"*'Hello GlaDOS , how are you'*"| E[QUEUE-MESSAGE-STTS-INPUT]
    E --> F[Thinking-Service-Glados]
    F -->|"*'Hello human, i'm fine thanks'*"| G[QUEUE-MESSAGE-TSG-INPUT]
    G --> H[Speaking-Service-Glados]
    H -->|*Text-to-Audio Output*| I[QUEUE-MESSAGE-SSG-INPUT]
    I --> J["'output.wav'"]
    
    classDef service fill:#f9f,stroke:#333,stroke-width:2px;
    class B,D,F,H service;
    
    classDef queue fill:#bbf,stroke:#333,stroke-width:2px;
    class C,E,G,I queue;

    class A,B,C,D,E,F,G,H,I,J fill:#fff,stroke:#333,stroke-width:2px;
    class A,B,C,D,E,F,G,H,I,J text:#000
