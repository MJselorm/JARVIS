🛠️ J.A.R.V.I.S. | Project Brief
Just A Rather Very Intelligent System Integrated AI Neural Link & Hardware Controller

1. Overview
This project establishes a sophisticated link between a high-level LLM (Llama 3.2 via Ollama) and physical hardware. It allows the J.A.R.V.I.S. persona to not only engage in witty banter but also execute physical commands—such as toggling LEDs, servos, or relays—via an Arduino microcontroller.

2. System Architecture
The system operates on a "Brain-to-Body" loop:

Voice/Text Input: User provides a query via the Python terminal.

Cognitive Processing: The JarvisEngine processes the intent using Ollama.

Command Extraction: Python parses the AI's response for hardware triggers (e.g., LIGHT_ON).

Hardware Execution: Python sends a serial signal to the Arduino to actuate components.
