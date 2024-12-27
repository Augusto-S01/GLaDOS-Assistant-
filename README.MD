# Project Overview

This repository contains a microservices-based architecture leveraging Apache Kafka for asynchronous communication. Below is a detailed description of the containers, services, and queues used in the system.



[![](https://mermaid.ink/img/pako:eNqVk1Fv2yAQx78KIg-RIpii5WmuNCmxHceVum7CeZnpA7VxjGKDh6Fp1fQj9VPsi43YTtdZ2UN5QAd39_9xh-4ZZirn0INFpQ5ZybQBSUAlcGuZxvL3aybUHcD4K1ilRFmZA581xmoOCNcPIuN3ffDqFHOkcDZlNhfq04E9TGcUHoGf_tiG2xDfhIQsoxD7JMLxt-_bZEj0O_Eg9VXdaF5y2Qol8SCOo4rlqh1CgzfGhleVAs4Z3BKAQKkOgLknPSnbQ8MRlCQJ-YcadtR1mpRC7oXcXQauR8DS1kwiIKY1KITkwJRM7tseGY2QyajOqCNuUtJw9n_ipiPOEv5osFF4eeoluLWmsWZ2BPG4rBEj7hjXKYVT1eV030Dh4O73rGJtG_ACtP0DXClV5U2KLwVqjVZ77k0Wi8Vg44PITel9bh6v3mWDFQrQGm3OElcX9X9Zbs_q9_cfUPdRiCIU9wLO8963RCvkO3ro-BHaoBhdnwsoPoC4JGNc073JfD6nEiJYc10zkbvJeD4lUmhKXnMKPWfmvGC2MhRS-eJCmTWKPMkMekZbjqBWdldCr2BV6062yZnhgWA7zeq324bJn0r9PfNcGKVv-lnsRvLlD_LtH5o?type=png)](https://mermaid.live/edit#pako:eNqVk1Fv2yAQx78KIg-RIpii5WmuNCmxHceVum7CeZnpA7VxjGKDh6Fp1fQj9VPsi43YTtdZ2UN5QAd39_9xh-4ZZirn0INFpQ5ZybQBSUAlcGuZxvL3aybUHcD4K1ilRFmZA581xmoOCNcPIuN3ffDqFHOkcDZlNhfq04E9TGcUHoGf_tiG2xDfhIQsoxD7JMLxt-_bZEj0O_Eg9VXdaF5y2Qol8SCOo4rlqh1CgzfGhleVAs4Z3BKAQKkOgLknPSnbQ8MRlCQJ-YcadtR1mpRC7oXcXQauR8DS1kwiIKY1KITkwJRM7tseGY2QyajOqCNuUtJw9n_ipiPOEv5osFF4eeoluLWmsWZ2BPG4rBEj7hjXKYVT1eV030Dh4O73rGJtG_ACtP0DXClV5U2KLwVqjVZ77k0Wi8Vg44PITel9bh6v3mWDFQrQGm3OElcX9X9Zbs_q9_cfUPdRiCIU9wLO8963RCvkO3ro-BHaoBhdnwsoPoC4JGNc073JfD6nEiJYc10zkbvJeD4lUmhKXnMKPWfmvGC2MhRS-eJCmTWKPMkMekZbjqBWdldCr2BV6062yZnhgWA7zeq324bJn0r9PfNcGKVv-lnsRvLlD_LtH5o)

---

## Containers Overview

| **Container**    | **Service**                   | **Description**                                                        | **Alias**            |
|------------------|-------------------------------|------------------------------------------------------------------------|----------------------|
| `zookeeper`      | Zookeeper                     | Centralized service for maintaining configuration and state for Kafka. |                      |
| `kafka`          | Kafka                         | Message broker used for asynchronous communication between services.   |                      |
| `producer`       | Producer                      | Service responsible for producing messages to Kafka topics.            |                      |
| `consumer`       | Consumer                      | Service responsible for consuming messages from Kafka topics.          |                      |
| `sound-capture`  | Sound Capture Service         | Captures audio input for further processing.                           | SCS or Ear           |
| `speech-to-text` | Comprehension-Service-Glados  | Converts audio input into text and sends results to the pipeline.      | STT or comprehension |
| `llm-process`    | Thinking-Service-Glados       | Processes text data using a large language model.                      | LLMP or Thinking     |
| `text-to-speech` | Speaking-Service-Glados       | Converts processed text into audio output for the user.                | TTS or Speak         |

---

## Services

| **Acronym** | **Service Name**               | **Description**                                    | **Alias** |
|-------------|--------------------------------|----------------------------------------------------|-----------|
| `SCP`       | Sound Capture Service          | Captures audio input for further processing.       |           |
| `CSG`       | Comprehension-Service-Glados   | Converts audio input into text for the pipeline.   |           |
| `TSG`       | Thinking-Service-Glados        | Processes text using a large language model.       |           |
| `SSG`       | Speaking-Service-Glados        | Converts processed text into audio output.         |           |

---

## Kafka Queues

| **Queue Name**              | **Description**                                 | **Alias** |
|-----------------------------|-------------------------------------------------|-----------|
| `QUEUE-MESSAGE-CSG-INPUT	`  | Queue for audio input.                          |           |
| `QUEUE-MESSAGE-STTS-INPUT`  | Queue for text input.                           |           |
| `QUEUE-MESSAGE-TSG-INPUT`   | Queue for text input to LLM processing.         |           |
| `QUEUE-MESSAGE-SSG-INPUT`   | Queue for output from LLM to audio processing.  |           |

---

## Notes
- **Alias:** A placeholder for informal names or shortcuts for easier reference to containers, services, or queues.
- This structure can be expanded with additional services and queues as the project evolves.

---

## Getting Started

To set up the environment and run the services:
1. Install Docker and Docker Compose.
2. Build and start the environment using:
   ```bash
   docker-compose up --build

